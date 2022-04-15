from datetime import datetime,timedelta
dt = 5
num = 18
now = datetime.utcnow()
#print(now.minute%5)
shift = now - timedelta(minutes=now.minute%5)
print(shift)
for t in range(1,num):
    newTime = shift + timedelta(minutes=(-t*dt))
    print(newTime)


