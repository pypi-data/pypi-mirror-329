# -*- coding: utf-8 -*-
# Copyright (c) 2025 SRON-org. All rights reserved.
# Licensed under the MIT License. See LICENSE file for details.

"""
A tool for converting between USEFS and iCalendar files.

Author: SRInternet <srinternet@qq.com>
Version: 1

Dependencies:
    - USEFS >= 0.2.0
    - icalendar
    - pytz

Usage (command line):
    usefs_ics 2ICS <usefs_file> <output_file.ics> <file_type: yaml, toml, or json> [--timezone <timezone>]
    usefs_ics 2USEFS <ics_file> <output_file> [output_type: json, yaml, toml]
"""

import os
import sys
from typing import List, Dict, Any, Union  # 引入类型提示
import re
from datetime import datetime, timedelta, timezone
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

try:
    from icalendar import Calendar, Event, vCalAddress, vText
except ImportError:
    print("Error: icalendar library not found. Please install it using 'pip install icalendar'.")
    sys.exit(1)

try:
    import pytz
except ImportError:
    print("Error: pytz library not found. Please install it using 'pip install pytz'.")
    sys.exit(1)

try:
    from USEFS import USEFS_YamlParser, USEFS_TomlParser, USEFS_JsonParser
except ImportError:
    print("Error: USEFS library not found. Please install it using 'pip install USEFS_Python>=0.2.0'.")
    sys.exit(1)


def usefs_to_ics(usefs_file: str, file_type: str, output_file: str = "output.ics", timezone_str: str = 'Asia/Shanghai') -> None:
    """Converts a USEFS file to an ICS file."""
    try:
        tz = pytz.timezone(timezone_str)  # 获取时区对象
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"Error: Invalid timezone '{timezone_str}'. Using UTC instead.")
        tz = timezone.utc

    try:
        if file_type == "yaml":
            parser = USEFS_YamlParser(usefs_file)
        elif file_type == "toml":
            parser = USEFS_TomlParser(usefs_file)
        elif file_type == "json":
            parser = USEFS_JsonParser(usefs_file)
        else:
            raise ValueError("Invalid file type. Must be yaml, toml, or json.")

        calendar = Calendar()
        calendar.add('prodid', '-//SRON-org//USEFS to iCalendar//EN')
        calendar.add('version', '2.0')

        items = parser.get_items()
        collections = parser.get_collections()

        # Process standalone items
        for item in items:
            event = Event()
            event['summary'] = item['name']
            event['description'] = item.get('note', '')
            event['location'] = item.get('properties', {}).get('location', '')
            if not event['location']:
                event['location'] = item.get('properties', {}).get('room', '') 

            # 确保 from_date 是字符串
            from_date_str = str(item['from_date'])  # 将日期对象转换为字符串
            dtstart = tz.localize(datetime.fromisoformat(from_date_str + " " + item['from_time']))
            event.add('dtstart', dtstart)

            if 'duration' in item:
                duration = _parse_duration(item['duration'])
                dtend = dtstart + duration
                event.add('dtend', dtend)
            else:
                event.add('dtend', dtstart) # 如果没有持续时间，结束时间和开始时间相同

            # 确保 from_date 也是字符串
            event['uid'] = str(hash(item['name'] + str(item['from_date']) + item['from_time']))  # 生成唯一ID

            calendar.add_component(event)

        # Process items within collections
        for collection in collections:
            for item in collection['content']:
                event = Event()
                event['summary'] = item['name']
                event['description'] = item.get('note', '')
                event['location'] = item.get('properties', {}).get('location', '')
                if not event['location']:
                    event['location'] = item.get('properties', {}).get('room', '') 

                # 可以覆盖集合的日期
                if 'from_date' in item:
                    # 确保 from_date 是字符串
                    from_date_str = str(item['from_date'])  # 将日期对象转换为字符串
                    try:
                        dtstart = datetime.fromisoformat(from_date_str + " " + item['from_time'])
                        dtstart = tz.localize(dtstart)
                    except ValueError as e:
                        print(f"Invalid from_date or from_time format in collection item: {e}. Skipping item.")
                        continue # 忽略该日程
                else:
                     # 如果没有 from_date，获取 enable
                     enable = collection['enable'] # 例如 Monday
                     if enable not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                        print("Collection does not specify a day of the week or Date. Skipping this collection")
                        continue
                     today = datetime.today()
                     day_of_week = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}[enable]
                     days_ahead = (day_of_week - today.weekday() + 7) % 7
                     next_occurrence = today + timedelta(days=days_ahead)
                     # 添加了str()转换
                     dtstart_str = str(next_occurrence.date()) + " " + item['from_time']
                     try:
                         dtstart = datetime.fromisoformat(dtstart_str)
                         dtstart = tz.localize(dtstart)
                     except ValueError as e:
                        print(f"Invalid from_time format in collection item: {e}. Skipping item.")
                        continue

                event.add('dtstart', dtstart)

                if 'duration' in item:
                    duration = _parse_duration(item['duration'])
                    dtend = dtstart + duration
                    event.add('dtend', dtend)
                else:
                    event.add('dtend', dtstart) # 如果没有持续时间，结束时间和开始时间相同

                 # 确保 from_date 也是字符串
                event['uid'] = str(hash(collection['collection_name'] + item['name'] + str(dtstart)))  # 生成唯一ID
                calendar.add_component(event)

        with open(output_file, 'wb') as f:
            f.write(calendar.to_ical())

        print(f"Successfully converted {usefs_file} to {output_file}")


    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found at {usefs_file}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def ics_to_usefs(ics_file: str, output_file: str = "output.json", output_type: str = "json") -> None:
    """Converts an ICS file to a USEFS file (JSON, YAML, or TOML format)."""
    try:
        with open(ics_file, 'r', encoding='utf-8') as f:
            calendar = Calendar.from_ical(f.read())

        usefs_data = {
            'version': 1,
            'items': [],
            'collections': []
        }

        default_collection = { # 创建默认的集合
            'collection_name': '从ICS导入',
            'enable': 'every_day',  # 根据需要修改
            'cycle': 'every',
            'importance': 1,
            'content': []
        }


        for component in calendar.walk():
            if component.name == "VEVENT":
                item = {
                    'name': str(component.get('summary')),
                    'from_date': str(component.get('dtstart').dt.date()),
                    'from_time': component.get('dtstart').dt.time().strftime("%H:%M"),
                    'enable': 'every_day',  # 默认每天启用
                    'cycle': 'every',  # 默认每周循环
                    'importance': 1,  # 默认优先级
                    'note': str(component.get('description', '')), # 添加描述
                    'properties': {} # 添加 properties
                }

                # 尝试获取结束时间，如果没有则不设置 duration
                if component.get('dtend'):
                    dtstart = component.get('dtstart').dt
                    dtend = component.get('dtend').dt
                    duration = dtend - dtstart  # 获取时间差
                    total_seconds = duration.total_seconds()

                    if total_seconds < 60:
                        item['duration'] = f"{total_seconds}s"
                    elif total_seconds < 3600:
                        item['duration'] = f"{total_seconds / 60}m"
                    else:
                        item['duration'] = f"{total_seconds / 3600}h"

                # 获取地点信息
                location = str(component.get('location', ''))
                if location:
                    item['properties']['location'] = location # 放到properties中

                default_collection['content'].append(item) # 添加到默认集合中

        usefs_data['collections'].append(default_collection) # 添加默认集合
        # 保存为不同的格式
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                if output_type == "json":
                    json.dump(usefs_data, f, indent=2, ensure_ascii=False)
                elif output_type == "yaml":
                    yaml.dump(usefs_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, indent=2)
                elif output_type == "toml":
                    toml.dump(usefs_data, f)
                else:
                    raise ValueError("Invalid output type. Must be json, yaml, or toml.")

        except Exception as e:
            raise ValueError(f"Failed to write to output file: {e}")


        print(f"Successfully converted {ics_file} to {output_file}")

    except FileNotFoundError:
        print(f"Error: File not found at {ics_file}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) >= 4:
        conversion_type = sys.argv[1].lower()
        from_file = sys.argv[2]
        to_file = sys.argv[3]

        if conversion_type == "2ics":
            file_type = sys.argv[4].lower()
            timezone_str = sys.argv[5] if len(sys.argv) > 5 else 'Asia/Shanghai'
            usefs_to_ics(from_file, file_type, to_file, timezone_str)
        elif conversion_type == "2usefs":
            output_type = sys.argv[4].lower() if len(sys.argv) > 4 else 'json'
            ics_to_usefs(from_file, to_file, output_type)
        else:
            print("Invalid conversion type. Use '2ICS' or '2USEFS'.")
            sys.exit(1)
    else:
        print("""A tool for converting between USEFS and iCalendar files.
Usage: usefs_ics 2ICS <usefs_file> <output_file.ics> <file_type: yaml, toml, or json> [--timezone <timezone>]
       usefs_ics 2USEFS <ics_file> <output_file> [output_type: json, yaml, toml]""")
        input("按下任意键继续...")
        sys.exit(1)

# Helper function to parse duration strings

def _parse_duration(duration_str: str) -> timedelta:
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

if __name__ == "__main__":
   main()