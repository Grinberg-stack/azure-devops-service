import requests
from datetime import datetime, timedelta
from config import AZURE_DEVOPS_API, HEADERS


# Returns the date three days ago in ISO 8601 format
def get_start_date():
    start_date = datetime.now() - timedelta(days=3)
    return start_date.isoformat() + 'Z'  # Example: 2024-12-01T15:30:00.000000Z


# Fetch work items created in the last three days
def get_recent_work_items():
    # URL for WIQL API
    url = f"{AZURE_DEVOPS_API}/wit/wiql?api-version=7.0"

    # WIQL query to fetch specific fields for work items
    recent_items_query = {
        "query": "SELECT [System.Id], [System.Title], [System.WorkItemType] FROM WorkItems"
    }

    try:
        # Send the WIQL query to Azure DevOps
        response = requests.post(url, json=recent_items_query, headers=HEADERS)
        response.raise_for_status()  # Raises an error if the status code isn't 200

        # Parse the response to get work items
        work_items = response.json().get('workItems', [])
        print(f"Found {len(work_items)} work items.")

        detailed_work_items = []
        for item in work_items:
            # Fetch additional details for each work item
            details = get_work_item_details(item["id"])
            if details:
                detailed_work_items.append(details)

        return detailed_work_items
    except requests.RequestException as e:
        print(f"Error during WIQL request: {str(e)}")
        return {"error": "Request failed", "message": str(e)}


# Fetch detailed information for a specific work item by ID
def get_work_item_details(work_item_id):
    url = f"{AZURE_DEVOPS_API}/wit/workitems/{work_item_id}?api-version=7.0"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching details for work item {work_item_id}: {str(e)}")
        return None


# Update the title of a specific work item
def update_work_item_title(work_item_id, new_title):
    url = f"{AZURE_DEVOPS_API}/wit/workitems/{work_item_id}?api-version=7.0"

    # JSON-patch operation to replace the title field
    data = [
        {
            'op': 'replace',
            'path': '/fields/System.Title',
            'value': new_title
        }
    ]

    # Add specific content-type for PATCH request
    patch_headers = {**HEADERS, "Content-Type": "application/json-patch+json"}

    try:
        response = requests.patch(url, json=data, headers=patch_headers)
        response.raise_for_status()
        return {'id': work_item_id, 'new_title': new_title}
    except requests.RequestException as e:
        print(f"Error updating title for work item {work_item_id}: {str(e)}")
        return {"error": "Update failed", "message": str(e)}


# Create a child work item and link it to a parent
def create_child_work_item(parent_id, child_title):
    url = f"{AZURE_DEVOPS_API}/wit/workitems/$Task?api-version=7.0"

    # JSON-patch operations to create the child work item and link it
    data = [
        {
            'op': 'add',
            'path': '/fields/System.Title',
            'value': child_title
        },
        {
            'op': 'add',
            'path': '/fields/System.WorkItemType',
            'value': 'Task'
        },
        {
            'op': 'add',
            'path': '/relations/-',
            'value': {
                'rel': 'System.LinkTypes.Hierarchy-Reverse',
                'url': f"{AZURE_DEVOPS_API}/wit/workitems/{parent_id}"
            }
        }
    ]

    # Add specific content-type for POST request
    post_headers = {**HEADERS, "Content-Type": "application/json-patch+json"}

    try:
        response = requests.post(url, json=data, headers=post_headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error creating child work item for parent {parent_id}: {str(e)}")
        return {"error": "Creation failed", "message": str(e)}
