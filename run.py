
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os

def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Đã cài đặt thành công các thư viện")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi cài đặt thư viện: {e}")
        return False
    return True

def main():
    print("🔧 Đang chuẩn bị môi trường...")
    
    # Cài đặt thư viện nếu cần
    if install_requirements():
        print("🚀 Đang khởi động bot...")
        try:
            # Import và chạy bot
            from main import ZyahBot
            from config import BOT_TOKEN
            
            bot = ZyahBot(BOT_TOKEN)
            bot.run()
        except Exception as e:
            print(f"💥 Lỗi khi chạy bot: {str(e)}")
    else:
        print("❌ Không thể cài đặt thư viện cần thiết")

if __name__ == "__main__":
    main()
