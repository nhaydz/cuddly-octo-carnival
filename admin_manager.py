
import json
import os
from config import DATA_FILE, ADMIN_ID
from colors import Colors

class AdminManager:
    def __init__(self):
        self.authorized_users = self._load_users()

    def _load_users(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            return {"users": [], "admin": ADMIN_ID}
        except Exception as e:
            print(f"{Colors.ERROR}[!] Lỗi khi tải dữ liệu người dùng: {e}{Colors.RESET}")
            return {"users": [], "admin": ADMIN_ID}

    def _save_users(self):
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.authorized_users, f, indent=4)
        except Exception as e:
            print(f"{Colors.ERROR}[!] Lỗi khi lưu dữ liệu người dùng: {e}{Colors.RESET}")

    def is_authorized(self, user_id):
        return user_id in self.authorized_users["users"] or user_id == self.authorized_users["admin"]

    def is_admin(self, user_id):
        return user_id == self.authorized_users["admin"]

    def add_user(self, user_id):
        if user_id in self.authorized_users["users"]:
            return f"Người dùng {user_id} đã được cấp quyền!"
        self.authorized_users["users"].append(user_id)
        self._save_users()
        return f"Đã cấp quyền cho người dùng {user_id}."

    def remove_user(self, user_id):
        if user_id not in self.authorized_users["users"]:
            return f"Người dùng {user_id} chưa được cấp quyền!"
        self.authorized_users["users"].remove(user_id)
        self._save_users()
        return f"Đã xóa quyền của người dùng {user_id}."

    def get_all_users(self):
        return self.authorized_users["users"] + [self.authorized_users["admin"]]

    def get_user_count(self):
        return len(self.authorized_users["users"])
