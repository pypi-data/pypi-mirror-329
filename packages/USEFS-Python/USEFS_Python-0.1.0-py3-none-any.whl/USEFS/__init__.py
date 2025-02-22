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

Usage:
    usefs <file_type> <usefs_file>
       <file_type>: yaml, toml, or json
"""

import os
import sys
from typing import List, Dict, Any, Union  # 引入类型提示
import re
from datetime import datetime

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

try:
    import json
except ImportError:
    print("Error: json library not found. It should be included in the default python environment.")
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

        # 验证item的enable是否覆盖collection的enable设置
        if 'enable' in item:
            enable = item['enable']
            if enable != "once":
                raise ValueError("Collection Item can only override 'enable' with 'once'")


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

            if 'version' not in self.data or 'items' not in self.data and 'collections' not in self.data:
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
            raise e # 重新抛出校验异常
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

            if 'version' not in self.data or 'items' not in self.data and 'collections' not in self.data:
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
            raise e # 重新抛出校验异常
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

            if 'version' not in self.data or 'items' not in self.data and 'collections' not in self.data:
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
            raise e # 重新抛出校验异常
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
       <file_type>: yaml, toml, or json""")
        sys.exit(1)

    file_type = sys.argv[1].lower()
    file_path = sys.argv[2]
    file_path = os.path.abspath(file_path) # 获取绝对路径

    if file_type == "yaml":
        parser = USEFS_YamlParser(file_path)
    elif file_type == "toml":
        parser = USEFS_TomlParser(file_path)
    elif file_type == "json":
        parser = USEFS_JsonParser(file_path)
    else:
        print("Invalid file type. Must be yaml, toml, or json.")
        sys.exit(1)

    if not parser.is_usefs_file(file_path):
        print("Not a valid USEFS file")
        sys.exit(1)



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
            
if __name__ == "__main__":
    main()