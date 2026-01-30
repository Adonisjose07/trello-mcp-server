"""
This module contains tools for managing Trello boards, lists, and cards.
"""

from server.tools import board, card, checklist, list, search, attachment, custom_field


def register_tools(mcp):
    """Register tools with the MCP server."""
    # Board Tools
    mcp.add_tool(board.get_board)
    mcp.add_tool(board.get_boards)
    mcp.add_tool(board.get_board_labels)
    mcp.add_tool(board.create_board_label)
    mcp.add_tool(board.get_board_members)
    mcp.add_tool(board.get_workspaces)
    mcp.add_tool(board.get_workspace_boards)

    # List Tools
    mcp.add_tool(list.get_list)
    mcp.add_tool(list.get_lists)
    mcp.add_tool(list.create_list)
    mcp.add_tool(list.update_list)
    mcp.add_tool(list.delete_list)

    # Card Tools
    mcp.add_tool(card.get_card)
    mcp.add_tool(card.get_cards)
    mcp.add_tool(card.create_card)
    mcp.add_tool(card.update_card)
    mcp.add_tool(card.delete_card)
    # New Comment Tools
    mcp.add_tool(card.get_card_comments)
    mcp.add_tool(card.add_comment_to_card)
    # New Member Tools
    mcp.add_tool(card.add_member_to_card)
    mcp.add_tool(card.remove_member_from_card)

    # Attachment Tools
    mcp.add_tool(attachment.get_card_attachments)
    mcp.add_tool(attachment.add_attachment_to_card)
    mcp.add_tool(attachment.delete_attachment_from_card)

    # Custom Field Tools
    mcp.add_tool(custom_field.get_board_custom_field_definitions)
    mcp.add_tool(custom_field.get_card_custom_field_items)
    mcp.add_tool(custom_field.update_card_custom_field_value)

    # Checklist Tools
    mcp.add_tool(checklist.get_checklist)
    mcp.add_tool(checklist.get_card_checklists)
    mcp.add_tool(checklist.create_checklist)
    mcp.add_tool(checklist.update_checklist)
    mcp.add_tool(checklist.delete_checklist)
    mcp.add_tool(checklist.add_checkitem)
    mcp.add_tool(checklist.update_checkitem)
    mcp.add_tool(checklist.delete_checkitem)

    # Search Tool
    mcp.add_tool(search.search_trello)
