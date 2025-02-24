from typing import Literal

FIG_SIZE_REF = {
    "aps": [3.4, 7.0],
    "aip": [3.37, 6.69],
    "nature": [88 / 25.4, 180 / 25.4],
}


def get_figsize(
    col: Literal["single", "double"] = "single",
    width_scale: float = 1.0,
    style: Literal["aps", "aip", "nature"] = "aps",
    height_scale: float = 1.0,  # 0.6180339887498948,
) -> tuple[float, float]:
    if col == "single":
        col_num = 0
    elif col == "double":
        col_num = 1
    else:
        raise ValueError("col should be 'single' or 'double'")
    width = FIG_SIZE_REF[style][col_num] * width_scale
    height = width * height_scale

    return width, height
