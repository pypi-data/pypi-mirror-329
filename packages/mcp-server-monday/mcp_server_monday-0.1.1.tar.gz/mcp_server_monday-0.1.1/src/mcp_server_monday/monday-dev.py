import os
from typing import Optional

from monday import MondayClient

MONDAY_API_BASE_URL = "https://api.monday.com/v2"
MONDAY_API_VERSION = os.getenv("MONDAY_API_VERSION", "2025-01")
MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
MONDAY_WORKSPACE_NAME = os.getenv("MONDAY_WORKSPACE_NAME", "tasmananalytics")
MONDAY_WORKSPACE_URL = f"https://{MONDAY_WORKSPACE_NAME}.monday.com"

client = MondayClient(MONDAY_API_KEY)

# Sub Items - IT Ops Board ID: 6939188775
# IT Ops Board ID: 6938769920
# BOARD_ID = 6939188775  # Sub-items
BOARD_ID = 6938769920  # Items
# res = client.items.fetch_items_by_column_value(
#     board_id=BOARD_ID, column_id="status", value=["Queued"]
# )

group_ids = ["topics", "new_group__1"]


def handle_monday_list_items_in_groups(
    boardId: str, groupIds: list[str], limit: int = 100, cursor: Optional[str] = None
):
    """List all items in the specified groups of a Monday.com board"""

    if groupIds and not cursor:
        formatted_group_ids = ", ".join([f'"{group_id}"' for group_id in groupIds])
        items_page_params = f"""
            query_params: {{
                rules: [
                    {{column_id: "group", compare_value: [{formatted_group_ids}], operator: any_of}}
                ]
            }}
        """
    else:
        items_page_params = f'cursor: "{cursor}"'

    items_page_params += f" limit: {limit}"
    query = f"""
    query {{
        boards (ids: {boardId}) {{
            items_page ({items_page_params}) {{
                cursor
                items {{
                    id 
                    name 
                    column_values {{
                        id
                        text
                        value
                    }}
                }}
            }}
        }}
    }}
    """

    response = client.custom._query(query)
    return response


print(
    handle_monday_list_items_in_groups(
        BOARD_ID,
        group_ids,
        limit=2,
        cursor="MSw2OTM4NzY5OTIwLDN3LThiMU1TdFdtakIzdFpOSjJaaywxMiwyLHw0NzEyMzEx",
    )
)
