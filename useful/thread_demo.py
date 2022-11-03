import threading

gLock = threading.Semaphore(1)
gCount = 0

def threadcode(id):
    global gCount
    gLock.acquire()
    print("Thread " + str(id) + " has count " + str(gCount))
    gCount = gCount+1
    gLock.release()

for i in range(0,5):
    t = threading.Thread(target=threadcode,args=(i,))
    t.start()
