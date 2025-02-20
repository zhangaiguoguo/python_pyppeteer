from datetime import datetime
import os
import uuid
from urllib.parse import quote


def first_letter_lowercase(s):
    if not s:
        return s
    else:
        return s[0].lower() + s[1:]


def is_empty(value):
    if value is None or value == "":
        return True
    return False


def generate_uuid():
    # 生成一个随机的 UUID
    unique_id = uuid.uuid4()
    # 可以选择将 UUID 转换为字符串形式
    unique_id_str = str(unique_id)
    return unique_id_str


def make_file_info(sub_dir, suffix):
    file_name = generate_uuid() + suffix
    date = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(sub_dir, date)
    if not os.path.isfile(file_path):
        os.makedirs(file_path, exist_ok=True)

    return {
        'full_path': os.path.join(file_path, file_name),
        "file_name": file_name,
        "file_id": os.path.join(date, file_name)
    }


def patch_encoded_path(path_str):
    return quote(path_str, safe='')
