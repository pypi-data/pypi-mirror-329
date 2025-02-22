import json
import random
import threading
from pathlib import Path


class QGInviteMgr:
    def __init__(self, file_path, code_field="ref_code", count_field="count", max_count=50):
        """
        初始化邀请码管理器。
        :param file_path: JSON 文件路径
        :param code_field: 邀请码字段名，默认为 "ref_code"
        :param count_field: 使用次数字段名，默认为 "count"
        :param max_count: 邀请码的最大使用次数，默认为 50
        """
        self.file_path = file_path
        self.code_field = code_field
        self.count_field = count_field
        self.max_count = max_count
        self.lock = threading.Lock()

    def load_invite_codes(self):
        """加载邀请码数据"""
        if not Path(self.file_path).exists():
            return []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_invite_codes(self, invite_codes):
        """保存邀请码数据"""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(invite_codes, file, indent=4)

    def get_available_code(self):
        """获取一个可用的邀请码"""
        with self.lock:  # 加锁，确保线程安全
            invite_codes = self.load_invite_codes()
            available_codes = [code for code in invite_codes if code[self.count_field] < self.max_count]
            if not available_codes:
                print("没有可用的邀请码")
                return None
            return random.choice(available_codes)[self.code_field]

    def use_code(self, ref_code):
        """使用邀请码（增加使用次数）"""
        with self.lock:  # 加锁，确保线程安全
            invite_codes = self.load_invite_codes()
            for code in invite_codes:
                if code[self.code_field] == ref_code:
                    code[self.count_field] += 1
                    break
            self.save_invite_codes(invite_codes)

    def add_code(self, code_info):
        """
        添加一个新的邀请码。
        如果邀请码已存在，则以当前添加的为准（覆盖旧数据）。
        :param code_info: 邀请码信息，包含 code_field 和 count_field 等字段
        """
        with self.lock:  # 加锁，确保线程安全
            invite_codes = self.load_invite_codes()

            # 检查邀请码是否已存在
            code_exists = False
            for i, code in enumerate(invite_codes):
                if code[self.code_field] == code_info[self.code_field]:
                    # 如果存在，覆盖旧数据
                    invite_codes[i] = code_info
                    code_exists = True
                    break

            # 如果不存在，添加到列表中
            if not code_exists:
                invite_codes.append(code_info)

            # 保存更新后的邀请码数据
            self.save_invite_codes(invite_codes)

    def reset_code(self, ref_code, new_count=0):
        """重置邀请码的使用次数"""
        with self.lock:  # 加锁，确保线程安全
            invite_codes = self.load_invite_codes()
            for code in invite_codes:
                if code[self.code_field] == ref_code:
                    code[self.count_field] = new_count
                    break
            self.save_invite_codes(invite_codes)


if __name__ == '__main__':
    manager_a = QGInviteMgr(file_path="system_a_codes.json", max_count=20)
    # 添加一个新的邀请码
    manager_a.add_code({"owner": "user1", "ref_code": "code1", "count": 5})
    # 添加一个已存在的邀请码（会覆盖旧数据）
    manager_a.add_code({"owner": "user1", "ref_code": "code1", "count": 10})
    manager_a.add_code({"owner": "user2", "ref_code": "code2", "count": 6})
    print(manager_a.load_invite_codes())
    for i in range(33):
        code = manager_a.get_available_code()
        if code:
            print(code)
            manager_a.use_code(code)
            print(manager_a.load_invite_codes())
        else:
            break
