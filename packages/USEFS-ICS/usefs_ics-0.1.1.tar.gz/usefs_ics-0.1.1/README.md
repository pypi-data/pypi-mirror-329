<div align="center">

<image src="https://github.com/user-attachments/assets/9e91bfd4-4448-4668-bede-6eafb0b42888" height="86"/>

# USEFS_ICS

A tool for converting between USEFS and iCalendar files

#### [Main Repo](https://github.com/SRON-org/USEFS)

</div>

## 介绍

USEFS_ICS 是一个简单的 Python 程序，旨在将使用 USEFS（通用日程计划表交换格式架构） 的 YAML、TOML 或 JSON 格式文件转换为标准 iCalendar ```.ics``` 格式的日历文件，允许使用者将日程计划表导入至日历软件或带有日历/提醒同步功能的手环/手表等。

> [!Important]
> 尽管此工具力求最大兼容性，但在转换过程中仍可能无法做到完全兼容。请仔细阅读以下关于转换的说明。

## 特性

*   **双向转换**: 支持 USEFS (YAML, TOML, JSON) 到 ICS 以及 ICS 到 USEFS (JSON) 格式的转换。
*   **时区支持**: 在将 USEFS 转换为 ICS 时，允许指定时区，确保日期和时间信息正确。 默认使用 `Asia/Shanghai` 时区。
*   **灵活的输入格式**: 支持 YAML、TOML 和 JSON 格式的 USEFS 文件作为输入。
*   **可读性强的输出**: 生成格式化的 JSON 格式 USEFS 文件，方便阅读和编辑。 生成的ICS文件遵循iCalendar协议，兼容主流日历软件
*   **简单易用**: 通过命令行界面进行操作，简单直接。
*   **可靠性**: 在格式转换过程中，会对关键数据进行校验，最大限度的保证了数据的准确性

## 安装

请使用以下代码从 **PyPI** 安装最新版本的 ```USEFS_ICS``` ：
```bash
pip install USEFS_ICS
```

## 用法

```bash
usefs_ics <conversion_type> <from_file> <to_file> [file_type] [timezone]
```

*   `<conversion_type>`: 指定转换类型，可以是 `2ICS` (USEFS to ICS) 或 `2USEFS` (ICS to USEFS)。
*   `<from_file>`: 输入文件路径。
*   `<to_file>`: 输出文件路径。
*   `[file_type]`: （仅在 2ICS 转换时需要）指定 USEFS 文件的类型，可以是 `yaml`、`toml` 或 `json`。
*   `[timezone]`: （可选，仅在 2ICS 转换时使用）时区，默认为 `Asia/Shanghai`。 如果未提供，则使用 `Asia/Shanghai` 作为默认时区。 如果提供了无效的时区，则将使用 UTC。

**示例**

*   将 USEFS 文件 (YAML 格式) 转换为 ICS 文件:

    ```bash
    usefs_ics 2ICS my_data.yaml output.ics yaml
    ```

*   将 ICS 文件转换为 USEFS 文件 (JSON 格式):

    ```bash
    usefs_ics 2USEFS my_calendar.ics output.json
    ```
*   将 USEFS 文件转换为 ICS 文件，并指定时区：

    ```bash
    usefs_ics 2ICS my_data.json output.ics json Asia/Tokyo
    ```

## 目前不兼容的转换

由于 USEFS 和 ICS 格式在结构和支持的特性方面存在差异，因此在转换过程中仍可能无法做到完全兼容。请注意以下事项：

### 从 ICS 转换为 USEFS (2USEFS)

*   **不兼容的集合信息**: ICS 格式不直接支持日程集合的概念。 因此，所有 ICS 日程都将转换为 USEFS 文件中一个名为 `从ICS导入` 的默认集合中的 `items`。 原有的组织结构会丢失。
*   **周期性规则**: 复杂的重复规则 (RRULE) 可能无法完全转换。 基本的重复规则（例如每天、每周）将被保留，但更复杂的规则可能会丢失或转换为近似的 USEFS 表示形式。
*   **时区信息**: 虽然日期和时间会被正确转换，但来自 ICS 文件的时区信息在转换到 USEFS 时可能会简化。
*   **参与者和组织者信息**: 参与者 (ATTENDEE) 和组织者 (ORGANIZER) 信息不会被转换到 USEFS 格式。
*   **USEFS 不支持的属性** USEFS具有 short\_name, enable, cycle, importance 这些属性，在从ICS转换为USEFS时，无法进行设置

### 从 USEFS 转换为 ICS (2ICS)

*   **USEFS 的 RRULE** USEFS具有字符串形式的RRULE规则，在转换到ICS的时候会被忽略，
*   **USEFS 中的集合信息**  转换到ICS文件中时，不会保留原有集合的信息，而是会被平铺到同一个日历中。
*   **自定义属性**: USEFS 中使用 properties 的键值对结构会被忽略，目前只会读取 location 和 room
*   **ENABLE 与 Cycle 字段的转换**: 启用规则 (ENABLE) 和循环周期 (CYCLE) 字段目前不会被完全转换为相应的 ICS RRULE 规则。

建议在执行转换后仔细检查结果文件，以确保数据尽可能准确。 对于关键数据，请考虑手动调整转换后的文件。
