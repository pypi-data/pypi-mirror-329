# -*- coding: utf-8 -*-
# Copyright (c) 2025 SRON-org. All rights reserved.
# Licensed under the MIT License. See LICENSE file for details.

"""
USEFS access framework for Python

Author: SRInternet <srinternet@qq.com>
Version: 1

Dependencies:
    - pyyaml
    - toml
    - json

Usage (command line):
    usefs <file_type> <usefs_file>
       <file_type>: yaml, toml, or json
       (Performs a check and prints basic file information)
"""

import os
import sys
from typing import List, Dict, Any, Union  # 引入类型提示
import re
from datetime import datetime, timedelta
import json 

try:
    import yaml
except ImportError:
    print("Error: yaml library not found. Please install it using 'pip install pyyaml'.")
    sys.exit(1)

try:
    import toml
except ImportError:
    print("Error: toml library not found. Please install it using 'pip install toml'.")
    sys.exit(1)



class USEFSParser:
    """
    Base class for parsing USEFS files in different formats.
    """
    __slots__ = ['file_path', 'version', 'items', 'collections', 'data']

    def __init__(self, file_path: str):
        """
        Initializes the parser.

        Args:
            file_path (str): Path to the USEFS file.
        """
        self.file_path = file_path
        self.version = None
        self.items = []
        self.collections = []
        self.data = {}  # Store the loaded data
        self.load_data(file_path)


    def load_data(self, file_path: str) -> None:
      """
      Loads data from the file. This method should be overridden by subclasses.
      """
      raise NotImplementedError("load_data method must be implemented by subclasses.")

    def _validate_data(self):
        """
        Validates the data format and content.
        """
        if self.version != 1:
            raise ValueError("Invalid version. Version must be 1.")

        for item in self.items:
            self._validate_item(item)

        for collection in self.collections:
            self._validate_collection(collection)

    def _validate_item(self, item: Dict[str, Any]):
        """
        Validates the format of a single item.
        """
        required_keys = ['name', 'from_date', 'from_time', 'enable', 'cycle', 'importance']
        for key in required_keys:
            if key not in item:
                raise ValueError(f"Item missing required key: {key}")

        try:
            from_date_str = str(item['from_date'])
            datetime.fromisoformat(from_date_str.replace('Z', '+00:00')) # 验证日期格式
        except ValueError as e:
            raise ValueError(f"Invalid from_date format: {item['from_date']}. Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:mm:ssZ).  Error: {e}")

        if not re.match(r"^\d{2}:\d{2}$", item['from_time']):
            raise ValueError(f"Invalid from_time format: {item['from_time']}. Use HH:mm (24-hour format).")

        enable = item['enable']
        if isinstance(enable, str):
             allowed_enable_values = ["once", "every_day", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
             days = enable.split(", ")
             for day in days:
                if day not in allowed_enable_values and not re.match(r"\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}", day):
                   raise ValueError(f"Invalid enable value: {enable}. It should be 'once', 'every_day', a day of the week, or a date range (YYYY-MM-DD/YYYY-MM-DD).")
        elif isinstance(enable, list):
            for date_str in enable:
                try:
                    datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError(f"Invalid date format in enable list: {date_str}. Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:mm:ssZ).")
        else:
            raise ValueError(f"Invalid enable type: {type(enable)}. It should be a string or a list of dates.")


        if item['cycle'] not in ['every', 'odd', 'even'] and not item['cycle'].startswith("RRULE:"):
            raise ValueError(f"Invalid cycle value: {item['cycle']}. It should be 'every', 'odd', 'even', or an RRULE expression.")

        if not isinstance(item['importance'], int) or item['importance'] < 0:
            raise ValueError(f"Invalid importance value: {item['importance']}. It should be a non-negative integer.")

        if 'duration' in item:
            duration_str = item['duration']
            if not re.match(r"^\d+(\.\d+)?[smhd]$", duration_str):
                 raise ValueError(f"Invalid duration format: {duration_str}.  Use 's' (seconds), 'm' (minutes), 'h' (hours), or 'd' (days) as units (e.g., 7200s, 120m, 2h, 0.5d).")

    def _validate_collection(self, collection: Dict[str, Any]):
        """
        Validates the format of a single collection.
        """
        required_keys = ['collection_name', 'enable', 'cycle', 'importance', 'content']
        for key in required_keys:
            if key not in collection:
                raise ValueError(f"Collection missing required key: {key}")

        if not isinstance(collection['content'], list):
            raise ValueError("Collection 'content' must be a list.")

        for item in collection['content']:
            # 验证集合中日程项
            self._validate_collection_item(item, collection)

        # 验证其他集合属性
        enable = collection['enable']
        if isinstance(enable, str):
             allowed_enable_values = ["once", "every_day", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
             days = enable.split(", ")
             for day in days:
                if day not in allowed_enable_values and not re.match(r"\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}", day):
                   raise ValueError(f"Invalid enable value: {enable}. It should be 'once', 'every_day', a day of the week, or a date range (YYYY-MM-DD/YYYY-MM-DD).")
        else:
            raise ValueError(f"Invalid enable type: {type(enable)}. It should be a string.")


        if collection['cycle'] not in ['every', 'odd', 'even'] and not collection['cycle'].startswith("RRULE:"):
            raise ValueError(f"Invalid cycle value: {collection['cycle']}. It should be 'every', 'odd', 'even', or an RRULE expression.")

        if not isinstance(collection['importance'], int) or collection['importance'] < 0:
            raise ValueError(f"Invalid importance value: {collection['importance']}. It should be a non-negative integer.")



    def _validate_collection_item(self, item: Dict[str, Any], collection:Dict[str, Any]):
        """
        Validates each item within a collection.
        """
        required_keys = ['name', 'from_time', 'duration']
        for key in required_keys:
            if key not in item:
                raise ValueError(f"Collection item missing required key: {key}")

        if not re.match(r"^\d{2}:\d{2}$", item['from_time']):
            raise ValueError(f"Invalid from_time format: {item['from_time']}. Use HH:mm (24-hour format).")

        if not re.match(r"^\d+(\.\d+)?[smhd]$", item['duration']):
             raise ValueError(f"Invalid duration format: {item['duration']}.  Use 's' (seconds), 'm' (minutes), 'h' (hours), or 'd' (days) as units (e.g., 7200s, 120m, 2h, 0.5d).")

        # # 验证item的enable是否覆盖collection的enable设置
        # if 'enable' in item:
        #     enable = item['enable']
        #     if enable != "once":
        #         raise ValueError("Collection Item can only override 'enable' with 'once'")


    def get_version(self) -> Union[int, None]:
        """
        Gets the version of the USEFS data.

        Returns:
            int: The version number.
        """
        return self.version

    def get_items(self) -> List[Dict[str, Any]]:
        """
        Gets all item information.

        Returns:
            list: List of items.
        """
        return self.items

    def get_collections(self) -> List[Dict[str, Any]]:
        """
        Gets all collection information.
        Returns:
            list: List of collections.
        """
        return self.collections

    @staticmethod
    def is_usefs_file(file_path: str) -> bool:
        """
        Checks if the given file path is a valid USEFS file.  This method should be overridden by subclasses.
        """
        raise NotImplementedError("is_usefs_file method must be implemented by subclasses.")

    def save_to_file(self, file_path: str) -> None:
        """
        Saves the USEFS data to a file. This method should be overridden by subclasses.
        """
        raise NotImplementedError("save_to_file method must be implemented by subclasses.")

    def add_item(self, item: Dict[str, Any]) -> None:
        """Adds a new item to the list of items."""
        self._validate_item(item)
        self.items.append(item)
        self.data['items'] = self.items # Update data


    def add_collection(self, collection: Dict[str, Any]) -> None:
        """Adds a new collection to the list of collections."""
        self._validate_collection(collection)
        self.collections.append(collection)
        self.data['collections'] = self.collections  # Update data

    def remove_item(self, item_name: str) -> None:
        """Removes an item by its name."""
        self.items = [item for item in self.items if item['name'] != item_name]
        self.data['items'] = self.items

    def remove_collection(self, collection_name: str) -> None:
        """Removes a collection by its name."""
        self.collections = [collection for collection in self.collections if collection['collection_name'] != collection_name]
        self.data['collections'] = self.collections

    def find_schedule(self, item_name: str) -> Union[Dict[str, Any], None]:
       """
       Finds a schedule (item) by its name.  Searches both items and collection contents.

       Args:
           item_name (str): The name of the schedule to find.

       Returns:
           Union[Dict[str, Any], None]: The schedule information if found, otherwise None.
       """
       # 搜索 items
       for item in self.items:
           if item['name'] == item_name:
               return item

       # 搜索 collections
       for collection in self.collections:
           for item in collection['content']:
               if item['name'] == item_name:
                   item['collection_name'] = collection['collection_name']
                   return item

       return None # 未找到日程

    def get_item_status(self, item_name: str, current_date_str: str) -> Union[str, None]:
        """
        Checks the status of an item based on the current date.  Searches both items and collection contents.

        Args:
            item_name (str): The name of the item to check.
            current_date_str (str): The current date in ISO 8601 format (YYYY-MM-DD).

        Returns:
            Union[str, None]: "not_started", "ongoing", "ended", or None if the item is not found.
        """
        item = self.find_schedule(item_name)  # 使用 find_schedule 方法来查找日程
        if item is None:
            return None

        try:
            current_date = datetime.fromisoformat(current_date_str).date()
        except ValueError:
            raise ValueError("Invalid current_date format. Use ISO 8601 date format (YYYY-MM-DD).")

        # 确保 from_date 存在且为字符串
        if 'from_date' in item and isinstance(item['from_date'], str):
            try:
                from_date = datetime.fromisoformat(item['from_date']).date()
            except ValueError as e:
                raise ValueError(f"Invalid from_date format in item '{item_name}': {e}")
        else:
            from_date = current_date  # 如果没有 from_date，则使用 current_date

        from_time_str = item['from_time']

        # Combine date and time
        from_time = datetime.strptime(from_time_str, '%H:%M').time()
        start_datetime = datetime.combine(from_date, from_time)
        start_date = start_datetime.date() # 定义 start_date

        # Calculate duration, if duration is available
        duration_str = item.get('duration')
        if duration_str:
            try:
                duration = self._parse_duration(duration_str)
                end_datetime = start_datetime + duration
                end_date = end_datetime.date() # 转换为 datetime.date 对象用于比较
                if current_date < start_date:
                    return "not_started"
                elif current_date >= start_date and current_date <= end_date:
                    return "ongoing"
                else:
                    return "waiting"  # 对于有 duration 的事件，状态为 waiting
            except ValueError as e:
                print(f"Invalid duration format: {e}")
                return None  # 如果 duration 格式无效，则返回 None
        else:  # If duration is not specified
            enable = item.get('enable')
            if enable == "once":  # If enable is "once" and no duration, it's ended
                if current_date >= from_date: # 只有当current_date晚于或等于from_date才返回ended，否则未开始
                    return "ended"
                else:
                    return "not_started"
            else: # 如果没有duration也不是once，按照以往逻辑
                if current_date < start_date:
                    return "not_started"
                elif current_date >= start_date:
                    return "waiting"
                else:
                    return None #其他情况返回None



    def _parse_duration(self, duration_str: str) -> timedelta:
        """Parses a duration string (e.g., "2h", "30m") into a timedelta object."""
        match = re.match(r"(\d+(?:\.\d+)?)([smhd])", duration_str)
        if not match:
            raise ValueError(f"Invalid duration format: {duration_str}")

        value, unit = match.groups()
        value = float(value)

        if unit == "s":
            return timedelta(seconds=value)
        elif unit == "m":
            return timedelta(minutes=value)
        elif unit == "h":
            return timedelta(hours=value)
        elif unit == "d":
            return timedelta(days=value)
        else:
            raise ValueError(f"Invalid duration unit: {unit}")


    def add_item_to_collection(self, collection_name: str, item: Dict[str, Any]) -> None:
        """Adds a new item to a specific collection."""
        collection = next((c for c in self.collections if c['collection_name'] == collection_name), None)
        if not collection:
            raise ValueError(f"Collection with name '{collection_name}' not found.")

        self._validate_collection_item(item, collection)  # Validate against collection rules
        collection['content'].append(item)
        self.data['collections'] = self.collections # Update data


    def update_item_in_collection(self, collection_name: str, item_name: str, new_item: Dict[str, Any]) -> None:
        """Updates an existing item in a specific collection."""
        collection = next((c for c in self.collections if c['collection_name'] == collection_name), None)
        if not collection:
            raise ValueError(f"Collection with name '{collection_name}' not found.")

        for i, item in enumerate(collection['content']):
            if item['name'] == item_name:
                self._validate_collection_item(new_item, collection)  # Validate the new item
                collection['content'][i] = new_item
                self.data['collections'] = self.collections # Update data
                return
        raise ValueError(f"Item with name '{item_name}' not found in collection '{collection_name}'.")


    def remove_item_from_collection(self, collection_name: str, item_name: str) -> None:
        """Removes an item from a specific collection."""
        collection = next((c for c in self.collections if c['collection_name'] == collection_name), None)
        if not collection:
            raise ValueError(f"Collection with name '{collection_name}' not found.")

        collection['content'] = [item for item in collection['content'] if item['name'] != item_name]
        self.data['collections'] = self.collections # Update data



class USEFS_YamlParser(USEFSParser):  # Previously USEFSParser
    """
    Parses USEFS files in YAML format.
    """
    __slots__ = [] # Inherit slots from parent

    def load_data(self, file_path: str) -> None:
        """Loads data from a YAML file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f)

            if not isinstance(self.data, dict):
                raise ValueError("Invalid USEFS file format: Root element must be a dictionary.")

            if 'version' not in self.data or ('items' not in self.data and 'collections' not in self.data):
                raise ValueError("Invalid USEFS file format: Missing 'version' or both 'items' and 'collections' keys.")

            self.version = self.data.get('version') # 使用get防止key不存在报错
            self.items = self.data.get('items', [])  # 设置默认值为空列表
            self.collections = self.data.get('collections', []) # 设置默认值为空列表
            self._validate_data()

        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML file: {e}") from e
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Invalid USEFS file format: {e}") from e


    @staticmethod
    def is_usefs_file(file_path: str) -> bool:
        """Checks if the given file is a valid YAML USEFS file."""
        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            return isinstance(data, dict) and \
                   'version' in data and \
                   ('items' in data or 'collections' in data)
        except:
            return False

    def save_to_file(self, file_path: str) -> None:
        """Saves the data to a YAML file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        except IOError as e:
            raise IOError(f"Failed to write {file_path}: {e}") from e



class USEFS_TomlParser(USEFSParser):
    """
    Parses USEFS files in TOML format.
    """

    __slots__ = [] # Inherit slots from parent

    def load_data(self, file_path: str) -> None:
        """Loads data from a TOML file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = toml.load(f)

            if not isinstance(self.data, dict):
                raise ValueError("Invalid USEFS file format: Root element must be a dictionary.")

            if 'version' not in self.data or ('items' not in self.data and 'collections' not in self.data):
                raise ValueError("Invalid USEFS file format: Missing 'version' or both 'items' and 'collections' keys.")

            self.version = self.data.get('version')
            self.items = self.data.get('items', [])
            self.collections = self.data.get('collections', [])
            self._validate_data()

        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except toml.TomlDecodeError as e:
            raise ValueError(f"Failed to parse TOML file: {e}") from e
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Invalid USEFS file format: {e}") from e


    @staticmethod
    def is_usefs_file(file_path: str) -> bool:
        """Checks if the given file is a valid TOML USEFS file."""
        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = toml.load(f)

            return isinstance(data, dict) and \
                   'version' in data and \
                   ('items' in data or 'collections' in data)
        except:
            return False

    def save_to_file(self, file_path: str) -> None:
        """Saves the data to a TOML file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                toml.dump(self.data, f)  # TOML doesn't have sort_keys, etc.
        except IOError as e:
            raise IOError(f"Failed to write {file_path}: {e}") from e


class USEFS_JsonParser(USEFSParser):
    """
    Parses USEFS files in JSON format.
    """

    __slots__ = [] # Inherit slots from parent

    def load_data(self, file_path: str) -> None:
        """Loads data from a JSON file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

            if not isinstance(self.data, dict):
                raise ValueError("Invalid USEFS file format: Root element must be a dictionary.")

            if 'version' not in self.data or ('items' not in self.data and 'collections' not in self.data):
                raise ValueError(f"Invalid USEFS file format: Missing 'version' or both 'items' and 'collections' keys. Data:{self.data}")

            self.version = self.data.get('version')
            self.items = self.data.get('items', [])
            self.collections = self.data.get('collections', [])
            self._validate_data()

        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON file: {e}") from e
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Invalid USEFS file format: {e}") from e

    @staticmethod
    def is_usefs_file(file_path: str) -> bool:
        """Checks if the given file is a valid JSON USEFS file."""
        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return isinstance(data, dict) and \
                   'version' in data and \
                   ('items' in data or 'collections' in data)
        except:
            return False

    def save_to_file(self, file_path: str) -> None:
        """Saves the data to a JSON file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)  # Added indent for readability
        except IOError as e:
            raise IOError(f"Failed to write {file_path}: {e}") from e


def main():
    if len(sys.argv) != 3:
        print("""Check USEFS File
Usage: usefs <file_type> <usefs_file>
       <file_type>: yaml, toml, or json
       (Performs a check and prints basic file information)
        """)
        sys.exit(1)

    file_type = sys.argv[1].lower()
    file_path = sys.argv[2]
    file_path = os.path.abspath(file_path)

    try:
        if file_type == "yaml":
            parser = USEFS_YamlParser(file_path)
        elif file_type == "toml":
            parser = USEFS_TomlParser(file_path)
        elif file_type == "json":
            parser = USEFS_JsonParser(file_path)
        else:
            raise ValueError("Invalid file type. Must be yaml, toml, or json.")

        if not parser.is_usefs_file(file_path):
            raise ValueError("Not a valid USEFS file")

        print(f"USEFS Version: {parser.get_version()}")

        print("\
Items:")
        for item in parser.get_items():
            print(f"  - Name: {item['name']}, Date: {item['from_date']}, Time: {item['from_time']}")

        print("\
Collections:")
        for collection in parser.get_collections():
            print(f"  - Collection Name: {collection['collection_name']}, Enable: {collection['enable']}, Cycle: {collection['cycle']}")
            for content_item in collection['content']:
                print(f"    - Name: {content_item['name']}, Time: {content_item['from_time']}, Duration: {content_item['duration']}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()