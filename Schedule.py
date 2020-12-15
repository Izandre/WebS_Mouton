import schedule
import time
import AlbertHein

def Scheduler (Time, FunctionName):
    
    def job():
        FunctionName

schedule.every(Time).days.do(job)

while True: schedule.run_pending()
time.sleep(1)