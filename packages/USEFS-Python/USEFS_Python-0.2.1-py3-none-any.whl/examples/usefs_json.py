from USEFS import USEFS_JsonParser

file_path = '../../USEFS/example.json' 

try:
    parser = USEFS_JsonParser(file_path)

    print(f"Version: {parser.get_version()}")

    items = parser.get_items()
    for item in items:
        print(f"  Item Name: {item['name']}, Date: {item['from_date']}")

    collections = parser.get_collections()
    for collection in collections:
        print(f"  Collection Name: {collection['collection_name']}")
        for content in collection['content']:
            print(f"    Content Item Name: {content['name']}, Time: {content['from_time']}")

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
except ValueError as e:
    print(f"Error: Invalid file format or content: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")