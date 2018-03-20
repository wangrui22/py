import threading
import time

def run():
    print('thread: %s is running.\n' % threading.current_thread())
    time.sleep(2)
    print('thread: %s is end.\n' % threading.current_thread())

print('thread: %s is running.\n'% threading.current_thread())

th = []
for i in range(0,10):
    t = threading.Thread(target=run)
    t.start()
    th.append(t)

for t in th:
    t.join()

print('thread: %s is end.\n' % threading.current_thread())
