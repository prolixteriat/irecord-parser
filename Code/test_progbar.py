from time import sleep
from progress.bar import Bar
from progress.spinner import MoonSpinner
import threading

'''
with MoonSpinner('Processing…') as bar:
    for i in range(100):
        sleep(0.02)
        bar.next()

with Bar('Processing...', max=150) as bar:
    for i in range(150):
        sleep(0.02)
        bar.next()
'''
def blackbox():
    sleep(10)

thread = threading.Thread(target=blackbox)
thread.start()

with MoonSpinner('Processing…') as bar:
    while thread.is_alive():
        bar.next()
        sleep(0.1)

thread.join()
print('Done      ')