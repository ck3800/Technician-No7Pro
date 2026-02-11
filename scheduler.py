from apscheduler.schedulers.background import BackgroundScheduler
from sender import run_mass_send_web_group

scheduler = BackgroundScheduler()

def schedule_group_send(group, hour, minute):
    scheduler.add_job(run_mass_send_web_group, 'cron', args=[group], hour=hour, minute=minute, id=group)

def start():
    scheduler.start()
