from apscheduler.schedulers.background import BackgroundScheduler
from sender import run_mass_send_web_group

scheduler = BackgroundScheduler()
scheduler.add_job(run_mass_send_web_group, 'cron', hour=12, minute=0)
scheduler.start()
