
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File dự phòng để khởi động bot
import os
import sys

# Thêm thư mục hiện tại vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ZyahBot
from config import BOT_TOKEN

def main():
    try:
        print("🌌 Đang khởi động Zyah King Bot...")
        bot = ZyahBot(BOT_TOKEN)
        bot.run()
    except Exception as e:
        print(f"💥 Lỗi: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
