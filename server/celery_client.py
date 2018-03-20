import time
from celery_server import add
import threading
def run():
    result = add.delay(1,2)
    print(result.get())

ths = []
for i in range(0,4):
    print('th ', i);
    th = threading.Thread(target=run)
    th.start()
    ths.append(th)

for t in ths:
    t.join()


# t1 = time.time()
# #result = add.delay(1,2)
# add.apply_async(args=[2,2])
# #print(result.get())
print('end\n')