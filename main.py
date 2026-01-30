import logging
import os

import uvicorn
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.requests import Request
from starlette.responses import StreamingResponse, JSONResponse
import httpx
import time

from server.tools.tools import register_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


from mcp.server.fastmcp.server import TransportSecuritySettings

# Initialize MCP server with security settings to allow VPS hosts
mcp = FastMCP(
    "Trello MCP Server",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False)
)

# Register tools
register_tools(mcp)


def start_claude_server():
    """Start the MCP server in Claude app mode"""
    try:
        # Verify environment variables
        if not os.getenv("TRELLO_API_KEY") or not os.getenv("TRELLO_TOKEN"):
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
            )

        logger.info("Starting Trello MCP Server in Claude app mode...")
        mcp.run()
        logger.info("Trello MCP Server started successfully")
    except Exception as e:
        logger.error(f"Error starting Claude server: {str(e)}")
        raise


def start_mcp_server():
    """Start the MCP server in Streamable HTTP mode using uvicorn"""
    try:
        # Verify environment variables
        if not os.getenv("TRELLO_API_KEY") or not os.getenv("TRELLO_TOKEN"):
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
            )

        host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_SERVER_PORT", "8000"))

        # Initialize session manager via side-effect (creates mcp._session_manager)
        _ = mcp.streamable_http_app()
        
        # Import the ASGI app class
        from mcp.server.fastmcp.server import StreamableHTTPASGIApp

        from starlette.routing import Mount, Route
        from starlette.middleware import Middleware
        from starlette.middleware.cors import CORSMiddleware
        from starlette.middleware.base import BaseHTTPMiddleware
        from contextlib import asynccontextmanager
        from starlette.responses import PlainTextResponse

        class NoBufferingMiddleware:
            def __init__(self, app):
                self.app = app

            async def __call__(self, scope, receive, send):
                if scope["type"] != "http":
                    await self.app(scope, receive, send)
                    return

                async def send_wrapper(message):
                    if message["type"] == "http.response.start":
                        headers = getattr(message, "get", lambda x: [])("headers") or []
                        if isinstance(headers, tuple):
                           headers = list(headers)
                        
                        # Check definition of headers
                        is_sse = False
                        for name, value in headers:
                            if name.lower() == b"content-type" and b"text/event-stream" in value:
                                is_sse = True
                                break
                        
                        if is_sse:
                            headers.append((b"x-accel-buffering", b"no"))
                            headers.append((b"cache-control", b"no-cache"))
                            headers.append((b"connection", b"keep-alive"))
                            headers.append((b"content-encoding", b"identity"))
                            headers.append((b"x-content-type-options", b"nosniff"))
                            message["headers"] = headers
                            
                    await send(message)

                await self.app(scope, receive, send_wrapper)

        from server.utils.auth import api_key_role, Role

        class APIKeyMiddleware:
            def __init__(self, app):
                self.app = app
                # Support multiple API keys for different roles
                ro_keys_str = os.getenv("MCP_API_KEY_READ_ONLY", "")
                rw_keys_str = os.getenv("MCP_API_KEY_READ_WRITE", "")
                
                # Falling back to MCP_API_KEY as READ_WRITE for backward compatibility if configured
                legacy_keys_str = os.getenv("MCP_API_KEY", "") if not (ro_keys_str or rw_keys_str) else ""
                
                self.ro_keys = [k.strip() for k in ro_keys_str.split(",") if k.strip()]
                self.rw_keys = [k.strip() for k in rw_keys_str.split(",") if k.strip()]
                
                if legacy_keys_str:
                    logger.info("Using legacy MCP_API_KEY as READ_WRITE")
                    self.rw_keys.extend([k.strip() for k in legacy_keys_str.split(",") if k.strip()])

                logger.info(f"DEBUG: RBAC Configured - RO keys: {len(self.ro_keys)}, RW keys: {len(self.rw_keys)}")

            async def __call__(self, scope, receive, send):
                if scope["type"] != "http":
                    await self.app(scope, receive, send)
                    return

                # Skip auth for health check and OPTIONS (CORS preflight)
                if scope["path"] == "/health" or scope["method"] == "OPTIONS":
                    await self.app(scope, receive, send)
                    return

                if not self.ro_keys and not self.rw_keys:
                    logger.info("DEBUG: No API Keys configured, allowing as READ_WRITE by default")
                    api_key_role.set(Role.READ_WRITE)
                    await self.app(scope, receive, send)
                    return

                headers = dict(scope["headers"])
                auth_header = headers.get(b"authorization", b"").decode("latin-1")
                token = auth_header[7:] if auth_header.startswith("Bearer ") else ""
                
                role = None
                if token:
                    if token in self.rw_keys:
                        role = Role.READ_WRITE
                    elif token in self.ro_keys:
                        role = Role.READ_ONLY

                if role is None:
                    logger.warning(f"DEBUG: Auth Failed for token prefix: {token[:4]}... Returning 401.")
                    response = JSONResponse(
                        {"error": "Unauthorized", "message": "Invalid or missing API Key"}, 
                        status_code=401
                    )
                    await response(scope, receive, send)
                    return
                
                logger.info(f"DEBUG: Auth Success. Role: {role.value}")
                api_key_role.set(role)
                await self.app(scope, receive, send)

        middleware = [
             Middleware(
                 CORSMiddleware,
                 allow_origins=["*"],
                 allow_credentials=True,
                 allow_methods=["*"],
                 allow_headers=["*"],
             ),
             Middleware(NoBufferingMiddleware),
             Middleware(APIKeyMiddleware)
        ]

        async def health_check(request):
            return PlainTextResponse(f"OK. Path: {request.url.path}")

        @asynccontextmanager
        async def lifespan(app):
            # Verify if session manager is initialized and run it
            if hasattr(mcp, "_session_manager") and mcp._session_manager:
                 async with mcp._session_manager.run():
                     yield
            else:
                 yield
        
        # Manually create the ASGI app using the initialized session manager
        # This gives us control over the route methods
        stream_handler = StreamableHTTPASGIApp(mcp._session_manager)

        app = Starlette(routes=[
            Route("/health", endpoint=health_check),
            # Handle /mcp without trailing slash explicitly to avoid redirects
            # that cause some clients to lose the Authorization header.
            Route("/mcp", endpoint=stream_handler, methods=["GET", "POST", "DELETE"]),
            # Mount handles subpaths and /mcp/
            Mount("/mcp", app=stream_handler),
        ], middleware=middleware, lifespan=lifespan)

        logger.info(
            f"Starting Trello MCP Server in Streamable HTTP mode on http://{host}:{port}..."
        )
        uvicorn.run(app, host=host, port=port)
    except Exception as e:
        logger.error(f"Error starting MCP server: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        # Check which mode to run in (default to true for Claude app mode)
        use_claude = os.getenv("USE_CLAUDE_APP", "true").lower() == "true"

        if use_claude:
            # Run in Claude app mode
            start_claude_server()
        else:
            # Run in Streamable HTTP mode (formerly SSE)
            start_mcp_server()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise
