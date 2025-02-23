import sys
from USEFS.__init__ import USEFS_YamlParser, USEFS_TomlParser, USEFS_JsonParser  
from typing import Union, Dict, Any

def load_usefs_file(file_path: str, file_type: str) -> Union["USEFSParser", None]:
    """Loads a USEFS file and returns the parser object."""
    try:
        if file_type == "yaml":
            parser = USEFS_YamlParser(file_path)
        elif file_type == "toml":
            parser = USEFS_TomlParser(file_path)
        elif file_type == "json":
            parser = USEFS_JsonParser(file_path)
        else:
            raise ValueError("Invalid file type. Must be yaml, toml, or json.")
               
        return parser
    except ValueError as e:
        print(f"Error loading file: {e}")
        return None
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def add_new_item(parser: "USEFSParser", item: Dict[str, Any]) -> None:
    """Adds a new item to the USEFS data."""
    try:
        parser.add_item(item)
        print("Added a new item.")
    except ValueError as e:
        print(f"Error adding item: {e}")


def add_new_collection(parser: "USEFSParser", collection: Dict[str, Any]) -> None:
    """Adds a new collection to the USEFS data."""
    try:
        parser.add_collection(collection)
        print("Added a new collection.")
    except ValueError as e:
        print(f"Error adding collection: {e}")


def remove_existing_item(parser: "USEFSParser", item_name: str) -> None:
    """Removes an existing item from the USEFS data."""
    try:
        parser.remove_item(item_name)
        print(f"Removed item: {item_name}")
    except Exception as e:
        print(f"Error removing item: {e}")


def remove_existing_collection(parser: "USEFSParser", collection_name: str) -> None:
    """Removes an existing collection from the USEFS data."""
    try:
        parser.remove_collection(collection_name)
        print(f"Removed collection: {collection_name}")
    except Exception as e:
        print(f"Error removing collection: {e}")


def add_item_to_existing_collection(parser: "USEFSParser", collection_name: str, item: Dict[str, Any]) -> None:
    """Adds a new item to an existing collection."""
    try:
        parser.add_item_to_collection(collection_name, item)
        print(f"Added a new item to collection '{collection_name}'.")
    except ValueError as e:
        print(f"Error adding item to collection: {e}")


def update_existing_item_in_collection(parser: "USEFSParser", collection_name: str, item_name: str, updated_item: Dict[str, Any]) -> None:
    """Updates an existing item in a specific collection."""
    try:
        parser.update_item_in_collection(collection_name, item_name, updated_item)
        print(f"Updated item '{item_name}' in collection '{collection_name}'.")
    except ValueError as e:
        print(f"Error updating item in collection: {e}")


def remove_item_from_existing_collection(parser: "USEFSParser", collection_name: str, item_name: str) -> None:
    """Removes an item from a specific collection."""
    try:
        parser.remove_item_from_collection(collection_name, item_name)
        print(f"Removed item '{item_name}' from collection '{collection_name}'.")
    except ValueError as e:
        print(f"Error removing item from collection: {e}")


def find_existing_schedule(parser: "USEFSParser", item_name: str) -> Union[Dict[str, Any], None]:
    """Finds a schedule (item) by its name, searching both items and collection contents."""
    try:
        schedule_info = parser.find_schedule(item_name)
        if schedule_info:
            print(f"Found schedule: {schedule_info}")
            return schedule_info
        else:
            print(f"Schedule '{item_name}' not found.")
            return None
    except Exception as e:
        print(f"Error finding schedule: {e}")
        return None


def get_schedule_status(parser: "USEFSParser", item_name: str, current_date_str: str) -> Union[str, None]:
    """Gets the status of a schedule, searching both items and collection contents."""
    try:
        status = parser.get_item_status(item_name, current_date_str)
        if status:
            print(f"Schedule '{item_name}' status on {current_date_str}: {status}")
            return status
        else:
            print(f"Schedule '{item_name}' not found.")
            return None
    except ValueError as e:
        print(f"Error getting schedule status: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def save_usefs_data(parser: "USEFSParser", file_path: str) -> None:
    """Saves the changes to the USEFS file."""
    try:
        parser.save_to_file(file_path)
        print(f"Successfully saved changes to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

# Example Usage:
if __name__ == "__main__":
    file_path = '../../USEFS/example.yaml' 
    file_type = "yaml"

    # 1. Load the USEFS file
    parser = load_usefs_file(file_path, file_type)
    if not parser:
        sys.exit(1)

    # 2. Add a new item to the main list
    new_item = {
        "name": "Gym Workout",
        "short_name": "Gym",
        "from_date": "2025-03-20",
        "from_time": "18:00",
        "duration": "1.5h",
        "enable": "every_day",
        "cycle": "every",
        "importance": 2,
        "note": "Leg day"
    }
    add_new_item(parser, new_item)

    # 3. Add a new collection
    new_collection = {
        "collection_name": "Weekend Activities",
        "enable": "Saturday, Sunday",
        "cycle": "every",
        "importance": 3,
        "content": []
    }
    add_new_collection(parser, new_collection)

    # 4. Remove an item
    remove_existing_item(parser, "Meeting")

    # 5. Remove a collection
    remove_existing_collection(parser, "旧课程表")

    # 6. Add an item to an existing collection
    collection_name = "课表-周一"
    new_collection_item = {
        "name": "物理实验",
        "short_name": "物",
        "from_time": "14:00",
        "duration": "2h",
        "note": "授课老师: 诺兰",
        "tags": ["学习", "物理", "实验"]
    }
    add_item_to_existing_collection(parser, collection_name, new_collection_item)

    # 7. Update an item in a collection
    item_name_to_update = "化学"
    updated_item = {
        "name": "化学",
        "short_name": "化",
        "from_time": "07:00",
        "duration": "50m",
        "note": "授课老师: 王利威（已更换）",
        "tags": ["学习", "化学", "课程"]
    }
    update_existing_item_in_collection(parser, collection_name, item_name_to_update, updated_item)

    # 8. Remove an item from a collection
    remove_item_from_existing_collection(parser, collection_name, "数学")

    # 9. Find an existing schedule (either item or in a collection)
    schedule_name = "Gym Workout"  # Replace with the schedule name to find
    schedule_info = find_existing_schedule(parser, schedule_name)

    if schedule_info:
        print(f"Schedule '{schedule_name}' found. Information:")
        for key, value in schedule_info.items():
            print(f"  {key}: {value}")

    # 10. Get Schedule Status
    item_name_to_check = "返还图书"
    check_date = "2025-01-11"
    schedule_status = get_schedule_status(parser, item_name_to_check, check_date)

    if schedule_status:
        print(f"Schedule '{item_name_to_check}' status on {check_date}: {schedule_status}")
    else:
        print(f"Schedule '{item_name_to_check}' not found.")

    # 11. Finally, save all the changes
    save_usefs_data(parser, file_path)