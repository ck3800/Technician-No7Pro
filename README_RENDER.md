# 最终版（Render 部署）

## Render Web Service 配置
- Build Command：`pip install -r requirements.txt`
- Start Command：`gunicorn app:app --bind 0.0.0.0:$PORT`

## 建议环境变量
- `SECRET_KEY`：随机字符串（必须）
- `DATA_DIR`：建议挂载持久化磁盘后设置为 `/var/data`（可选）
- `DISABLE_SCHEDULER`：不需要定时任务就设为 `1`（默认启用）
- `DEFAULT_GROUP`：默认群组名（默认 `groupA`）
- `SCHEDULE_HOUR` / `SCHEDULE_MINUTE`：定时发送时间（UTC，默认 12:00）

## 默认账号
首次启动会自动创建：
- 用户名：`admin`
- 密码：`admin123`
用户文件位置：`DATA_DIR/users.json`

## 访问路径
- `/login` 登录
- `/` 首页（需要登录）
- `/admin/upload` 上传（需要登录）
- `/tg/*` Telegram 登录相关
- `/healthz` 健康检查
