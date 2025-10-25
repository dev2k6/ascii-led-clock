#!/usr/bin/env python3
import time
import datetime
import sys
import os

# ====== LED ASCII 7-SEG (3 dòng mỗi ký tự) ======
SEG = {
    "0": [" _ ",
          "| |",
          "|_|"],
    "1": ["   ",
          "  |",
          "  |"],
    "2": [" _ ",
          " _|",
          "|_ "],
    "3": [" _ ",
          " _|",
          " _|"],
    "4": ["   ",
          "|_|",
          "  |"],
    "5": [" _ ",
          "|_ ",
          " _|"],
    "6": [" _ ",
          "|_ ",
          "|_|"],
    "7": [" _ ",
          "  |",
          "  |"],
    "8": [" _ ",
          "|_|",
          "|_|"],
    "9": [" _ ",
          "|_|",
          " _|"],
    ":": ["   ",
          " . ",
          " . "],
}

# Bảng màu 256-color ANSI (đổi dần như RGB)
PALETTE = [196,202,208,214,220,226,190,154,118,82,46,47,51,39,33,27,21,57,93,129,165,201]

# Bật ANSI màu trên Windows (nếu có colorama thì dùng, không bắt buộc)
try:
    import colorama
    colorama.just_fix_windows_console()
except Exception:
    pass

def colorize(text, color_code):
    return f"\033[38;5;{color_code}m{text}\033[0m"

def clear():
    # Xoá màn và đưa con trỏ về góc trái trên
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def render_big(text, start_color_index=0, space=1, blink_colon=False):
    """
    text: chuỗi cần hiển thị (vd: '18:27:45')
    start_color_index: vị trí bắt đầu trong PALETTE
    space: số khoảng trống giữa ký tự
    blink_colon: nếu True, ký tự ':' sẽ chớp theo giây chẵn/lẻ
    """
    rows = ["", "", ""]
    ci = start_color_index
    for ch in text:
        # Chớp dấu ":" nếu cần
        if ch == ":" and blink_colon:
            # tạo hiệu ứng tắt/bật bằng việc thay "." thành "   " theo tick ngoài
            glyph = ["   ","   ","   "] if int(time.time()) % 2 == 0 else SEG[":"]
        else:
            glyph = SEG.get(ch, ["   ","   ","   "])  # fallback nếu ký tự lạ

        col = PALETTE[ci % len(PALETTE)]
        for i in range(3):
            rows[i] += colorize(glyph[i], col) + " " * space
        ci += 1

    return "\n".join(rows)

def run_clock(mode_24h=True, show_seconds=True):
    color_shift = 0
    try:
        while True:
            now = datetime.datetime.now()
            if mode_24h:
                fmt = "%H:%M:%S" if show_seconds else "%H:%M"
            else:
                fmt = "%I:%M:%S" if show_seconds else "%I:%M"
            s = now.strftime(fmt)

            clear()
            print(render_big(s, start_color_index=color_shift,
                             space=2, blink_colon=True))
            # Thanh trạng thái nhỏ bên dưới
            print()
            print("ASCII LED Clock - Press Ctrl+C to quit")
            # Dịch bảng màu mỗi khung hình
            color_shift = (color_shift + 1) % len(PALETTE)
            time.sleep(0.25)  # tốc độ làm tươi
    except KeyboardInterrupt:
        print("\nBye.")

if __name__ == "__main__":
    # Tuỳ chọn nhanh qua biến môi trường (không bắt buộc)
    # CLOCK_12H=1 để dùng 12h, CLOCK_SEC=0 để ẩn giây
    mode_24h = os.getenv("CLOCK_12H", "0") != "1"
    show_seconds = os.getenv("CLOCK_SEC", "1") == "1"
    run_clock(mode_24h=mode_24h, show_seconds=show_seconds)
