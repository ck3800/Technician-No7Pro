import os

def get_all_accounts():
    result = []
    base = "accounts"
    for group in os.listdir(base):
        group_path = os.path.join(base, group)
        if os.path.isdir(group_path):
            for session in os.listdir(group_path):
                status = "✅ 正常" if session.endswith(".session") else "❌ 异常"
                result.append([f"{group}/{session}", status])
    return result
