import os
from datetime import datetime

try:
    from apscheduler.schedulers.background import BackgroundScheduler
except Exception:  # pragma: no cover
    BackgroundScheduler = None

from sender import run_mass_send_web_group

_scheduler = None

def _get_scheduler():
    global _scheduler
    if _scheduler is None:
        if BackgroundScheduler is None:
            raise RuntimeError("APScheduler not installed")
        _scheduler = BackgroundScheduler(timezone="UTC")
    return _scheduler

def schedule_group_send(group_name: str, hour: int = 12, minute: int = 0):
    sch = _get_scheduler()
    sch.add_job(
        run_mass_send_web_group,
        'cron',
        hour=hour,
        minute=minute,
        args=[group_name],
        id=f"send_{group_name}",
        replace_existing=True,
    )

def start():
    sch = _get_scheduler()
    if not sch.running:
        sch.start()
