## rgb转hex

### 完整代码

```python
from typing import Tuple

def rgb_to_hex(color: Tuple[int, int, int], prefix: str = "") -> str:
    # 检查输入是否为三元组，并且长度是否为3
    if not isinstance(color, tuple) or len(color) != 3:
        raise ValueError("输入的颜色格式不正确。应为三元组 (r, g, b)")

    r, g, b = color

    # 如果 r, g, b 不是整数，尝试将它们转换为整数
    try:
        r, g, b = int(r), int(g), int(b)
    except ValueError:
        raise ValueError("无法将 r, g, b 转换为整数")

    # 将 r, g, b 限制在 0-255 的范围内
    r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))

    return f"{prefix}{r:02X}{g:02X}{b:02X}"
```

### 测试代码

```python

# 测试代码
rgb_colors = [
    (210, 152, 133),
    (128, 33, 59),
    (-5, 300, "a")  # 不正确的输入
]

for color in rgb_colors:
    try:
        print(rgb_to_hex(color))
    except ValueError as e:
        print(e)
```

### 简化版本

```python
def rgb_to_hex(color, prefix=""):
    r, g, b = color
    return f"{prefix}{r:02X}{g:02X}{b:02X}"
```



## hex转rgb

### 完整代码

```python
def hex_to_rgb(hex_color: str, prefix: str = "#") -> Tuple[int, int, int]:
    # 去除前缀
    if hex_color.startswith(prefix):
        hex_color = hex_color[len(prefix):]

    # 检查长度是否为6
    if len(hex_color) != 6:
        raise ValueError("输入的十六进制颜色格式不正确。应为6位字符")

    # 尝试将十六进制颜色转换为整数
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        raise ValueError("无法将输入的十六进制颜色转换为整数")

    return (r, g, b)

```

### 测试代码

```python
from typing import Tuple

# 测试代码
hex_colors = [
    "#D29885",
    "801C3B",
    "#ZZZZZZ"  # 不正确的输入
]

for hex_color in hex_colors:
    try:
        print(hex_to_rgb(hex_color))
    except ValueError as e:
        print(e)

```

```
(210, 152, 133)
(128, 28, 59)
无法将输入的十六进制颜色转换为整数
```

### 简化版本

```python
def hex_to_color(color, prefix=""):
    if color.startswith(prefix):
        color = color[len(prefix):]
        
    r = int(color[:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    return r, g, b
```

