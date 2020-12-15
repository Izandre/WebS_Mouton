
import Checkers
import AlbertHein
from flask import Flask
from flask_apscheduler import APScheduler


app = Flask(__name__)
scheduler = APScheduler()

@app.route("/")
def index():
   return "Welcome"      

def scheduledTask():
      AlbertHein.ScrapeFunction() 
      Checkers.ScrapeFunction() 

if __name__ == "__main__":
    scheduler.add_job(id='Scheduled task', func =scheduledTask, trigger = 'interval', minutes=360)
    scheduler.start()
    app.run(host = '0.0.0.0', port =8080)
    

# schedule.every(10).seconds.do(job)


# while True: schedule.run_pending()
# time.sleep(1)
