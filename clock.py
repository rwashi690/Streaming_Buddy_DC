from apscheduler.schedulers.blocking import BlockingScheduler
from app import addMovies, addTrendingMovies

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    addMovies()
    addTrendingMovies()


sched.start()
