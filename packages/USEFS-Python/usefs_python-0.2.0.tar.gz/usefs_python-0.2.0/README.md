<div align="center">

<image src="https://github.com/user-attachments/assets/9e91bfd4-4448-4668-bede-6eafb0b42888" height="86"/>

# USEFS_Python

USEFS access framework for Python

#### [Main Repo](https://github.com/SRON-org/USEFS)

</div>

## 介绍

USEFS_Python 是一个Python库，提供对使用 USEF 架构 格式的文件的进行访问、修改、增添、删除等高级管理功能。它简单、快速、便捷，能大幅提高 USEFS 在 Python 上的开发效率。

## 特性

*   读取 USEFS 文件（YAML, TOML, JSON 格式）
*   添加、删除和修改顶级日程项 (items)
*   添加、删除和修改日程集合 (collections)
*   在日程集合中添加、删除和修改日程项
*   查找现有的日程
*   确定日程的当前状态（未开始、进行中、等待下一次循环、已结束）
*   将更改保存到 USEFS 文件

## 先决条件

请使用以下代码从 **PyPI** 安装最新版本的 ```USEFS_Python``` ：
```bash
pip install USEFS_Python
```

本工具也支持使用命令行验证 USEFS 文件有效性，参见 _命令行用法_

## 使用说明

### 1. 导入模块

首先，你需要导入必要的模块和函数：

```python
import sys
from USEFS import USEFS_YamlParser, USEFS_TomlParser, USEFS_JsonParser
from typing import Union, Dict, Any
```

**注意**：```USEFS_YamlParser```, ```USEFS_TomlParser``` 和 ```USEFS_JsonParser``` 分别用于解析 ```.yaml``` 格式、```.toml``` 格式和 ```.json``` 格式的 USEFS 文件。本文以 ```.yaml``` 格式举例，不同文件格式解析的差别仅仅是使用不同的 Parser 来构建相应的解析器对象，以进一步获取 USEFS 文件的内容。

### 2. 加载文件 -> 构建解析器

```python
file_path = "my_data.yaml"
parser = USEFS_YamlParser(file_path) 
```

**注意：** 后续的*所有*操作都必须使用这个 `parser` 对象。 如果 `parser` 为 `None`，说明加载 USEFS 文件失败，你需要检查文件路径、文件类型和文件内容是否正确

### 3. 进行操作

现在，你可以使用 `parser` 对象进行各种操作。

#### 获取和打印基本信息

```python
    print(f"Version: {parser.get_version()}")

    items = parser.get_items()
    for item in items:
        print(f"  Item Name: {item['name']}, Date: {item['from_date']}")

    collections = parser.get_collections()
    for collection in collections:
        print(f"  Collection Name: {collection['collection_name']}")
        for content in collection['content']:
            print(f"    Content Item Name: {content['name']}, Time: {content['from_time']}")
```

#### 添加新的日程项

```python
new_item = {
    "name": "健身",
    "short_name": "健",
    "from_date": "2025-03-20",
    "from_time": "18:00",
    "duration": "1.5h",
    "enable": "every_day",
    "cycle": "every",
    "importance": 2,
    "note": "腿部锻炼",
    "tags": ["健身", "健康"]
}
parser.add_item(new_item)
```

#### 添加新的日程集合

```python
new_collection = {
    "collection_name": "周末活动",
    "enable": "Saturday, Sunday",
    "cycle": "every",
    "importance": 3,
    "content": [],
    "tags": ["活动", "周末"]
}
parser.add_collection(new_collection)
```

#### 移除日程项

```python
parser.remove_item("返还图书")  # 替换为要移除的日程项名称
```

#### 移除日程集合

```python
parser.remove_collection("旧课程表")  # 替换为要移除的日程集合名称
```

#### 向现有的日程集合添加日程项

```python
collection_name = "课表-周一"  # 替换为现有的集合名称
new_collection_item = {
    "name": "物理实验",
    "short_name": "物实",
    "from_time": "14:00",
    "duration": "2h",
    "note": "授课老师: 杨松霖",
    "tags": ["学习", "物理", "实验"]
}
parser.add_item_to_collection(collection_name, new_collection_item)
```

#### 更新现有日程集合中的日程项

```python
collection_name = "课表-周一"
item_name_to_update = "化学"
updated_item = {
    "name": "化学",
    "short_name": "化",
    "from_time": "07:00",
    "duration": "50m",
    "note": "授课老师: 王利威（已更换）",
    "tags": ["学习", "化学", "课程"]
}
parser.update_item_in_collection(collection_name, item_name_to_update, updated_item)
```

#### 从日程集合中移除日程项

```python
collection_name = "课表-周一"
parser.remove_item_from_collection(collection_name, "数学")
```

#### 查找日程

```python
schedule_name = "健身"  # 替换为要查找的日程名称
schedule_info = parser.find_schedule(schedule_name)
if schedule_info:
    print(f"找到日程 '{schedule_name}'。信息：")
    for key, value in schedule_info.items():
        print(f"  {key}: {value}")
```

#### 获取日程状态

```python
item_name_to_check = "健身"
check_date = "2025-03-21"
schedule_status = parser.get_schedule_status(item_name_to_check, check_date)
if schedule_status:
    print(f"日程 '{item_name_to_check}' 在 {check_date} 的状态：{schedule_status}")
```

更多详细的功能模板，请参见 [usefs_functions_example.py](./examples/usefs_functions_example.py)

### 4. 保存更改

最后，使用 `save` 方法保存所有更改：

```python
parser.save()
```

### 命令行用法

安装后，你可以使用以下命令检查 USEFS 文件：

```bash
usefs <file_type> <usefs_file>
```

`<file_type>` 可以是 `yaml`、`toml` 或 `json`。 该命令将检查 USEFS 文件的基本信息。

## 注意事项

*   确保在执行写入操作之前，你具有对文件的写入权限。
*   务必小心处理用户输入和文件写入操作，以防止安全问题。
*   此代码提供了一个基本的框架，你可以根据你的实际需求进行扩展和修改。

## 开放

USEFS_Python 时刻欢迎各位开发者完善和更新新的功能。

## 协议

[MIT](./LICENSE)
