import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_all_accounts():
    """Return list of [account_path, status] from accounts/*/*.session

    If the accounts directory doesn't exist, return an empty list.
    """
    result = []
    base = os.path.join(BASE_DIR, "accounts")
    if not os.path.isdir(base):
        return result

    for group in sorted(os.listdir(base)):
        group_path = os.path.join(base, group)
        if os.path.isdir(group_path):
            for session in sorted(os.listdir(group_path)):
                status = "✅ 正常" if session.endswith(".session") else "❌ 异常"
                result.append([f"{group}/{session}", status])
    return result
