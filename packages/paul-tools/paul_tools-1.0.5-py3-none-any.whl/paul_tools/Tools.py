__all__ = [
    "color",
    "typeToColor",
]


def color(*value: str, color: str = "") -> list[str]:
    """
    Adds ANSI color codes to the given strings using the colorama library.
    Args:
        *value (str): One or more strings to which the color will be applied.
        color (str, optional): The name of the color to apply. Defaults to an empty string, which means no color will be applied.
    Returns:
        list[str]: A list of strings with the specified color applied. If no color is specified, returns the original strings.
    Raises:
        ValueError: If the specified color is not defined in colorama.
    Example:
        >>> color("Hello", "World", color="red")
        ['\x1b[31m', 'Hello', 'World', '\x1b[39m']
    """
    import colorama

    colorama.init()

    # 將顏色轉換為大寫
    color = color.upper()

    if color == "":
        return list(value)

    # 檢查顏色是否在 colorama 中定義
    if not hasattr(colorama.Fore, color):
        raise ValueError(f"顏色 {repr(color)} 不存在於 colorama 中。")

    # 建立新的值列表
    new_value = list(value)
    # 插入顏色碼
    new_value.insert(0, getattr(colorama.Fore, color))
    # 添加重置顏色碼
    new_value.append(colorama.Fore.RESET)

    colorama.deinit()
    return new_value


def typeToColor(type: str) -> str:
    """
    Converts a given type string to a corresponding color string.

    Args:
        type (str): The type string to convert. Expected values are "ERROR", "ERR", "WARN", "WARNING", or any other string.

    Returns:
        str: The corresponding color string. Returns "RED" for "ERROR" or "ERR", "YELLOW" for "WARN" or "WARNING", and the uppercase version of the input type for any other string.
    """
    match type.upper():
        case "ERROR" | "ERR":
            return "RED"
        case "WARN" | "WARNING":
            return "YELLOW"
        case _:
            return type.upper()
