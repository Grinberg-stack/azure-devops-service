from azure_api import get_recent_work_items, update_work_item_title, create_child_work_item
from datetime import datetime


# Process work items retrieved from Azure DevOps
def process_work_items():

    # Step 1: Fetch recent work items from Azure DevOps
    work_items = get_recent_work_items()

    # Step 2: Check if there was an error in fetching work items
    if 'error' in work_items:
        print(f"Error fetching work items: {work_items['message']}")
        return

    # Step 3: Print the total number of fetched work items
    print(f"Found {len(work_items)} work items.")

    # Step 4: Iterate through each work item to process it
    for item in work_items:
        work_item_id = item['id']  # Extract the Work Item ID
        current_title = item['fields'].get('System.Title', 'Unknown Title')  # Get the title of the Work Item
        work_item_type = item['fields'].get('System.WorkItemType', 'Unknown Type')  # Get the type of the Work Item

        # Check if the Work Item type is one that requires a title update
        if work_item_type in ['Bug', 'Feature', 'PBI']:
            # Create a new title by appending the current date
            new_title = f"{current_title} - Updated on {datetime.now().strftime('%Y-%m-%d')}"

            # Attempt to update the Work Item title
            update_result = update_work_item_title(work_item_id, new_title)

            # Check and log the result of the update operation
            if 'error' in update_result:
                print(f"Failed to update Work Item {work_item_id}: {update_result['message']}")
            else:
                print(f"Successfully updated Work Item {work_item_id} to: {new_title}")

        # Check if the Work Item is a PBI and create a child task if necessary
        if work_item_type == 'PBI':
            # Generate a title for the new child task
            child_title = f"Task for {current_title}"

            # Attempt to create the child Work Item and link it to the parent
            create_result = create_child_work_item(work_item_id, child_title)

            # Check and log the result of the child creation operation
            if 'error' in create_result:
                print(f"Failed to create child task for Work Item {work_item_id}: {create_result['message']}")
            else:
                print(f"Successfully created child task for Work Item {work_item_id} with title: {child_title}")


# Entry point to execute the function
if __name__ == '__main__':
    process_work_items()
