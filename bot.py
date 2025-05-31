
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import main bot class
from main import ZyahBot
from config import BOT_TOKEN

if __name__ == "__main__":
    try:
        # Khởi động bot
        bot = ZyahBot(BOT_TOKEN)
        bot.run()
    except Exception as e:
        print(f"[💥] Lỗi nghiêm trọng: {str(e)}")
