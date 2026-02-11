import os
import json
import time
from datetime import datetime

def run_mass_send_web_group(group_name):
    os.makedirs('task_log', exist_ok=True)
    with open("config/groups.json", encoding="utf-8") as f:
        groups = json.load(f)
    group = groups.get(group_name)
    if not group:
        return f"❌ 未找到分组：{group_name}"

    account_dir = os.path.join("accounts", group_name)
    if not os.path.exists(account_dir):
        return f"❌ 账号目录不存在：{account_dir}"

    accounts = [f for f in os.listdir(account_dir) if f.endswith(".session")]
    if not accounts:
        return f"⚠️ 无可用账号（{group_name}）"

    log = [f"[{group_name}] 共检测到 {len(accounts)} 个账号"]
    for acc in accounts:
        try:
            log.append(f"→ 使用账号 {acc} 发送中...")
            time.sleep(1)
            if "fail" in acc:
                raise Exception("模拟发送失败")
            log.append(f"✅ {acc} 发送成功")
        except Exception as e:
            log.append(f"❌ {acc} 发送失败，原因：{str(e)}，尝试重试...")
            time.sleep(1)
            log.append(f"🔁 {acc} 重试成功（模拟）")

    # 保存日志文件
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"task_log/{group_name}_{ts}.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    return "\n".join(log)
