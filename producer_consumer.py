# import libraries
import Queue
import threading
import time
import random

exitFlag = 0                            # flag indicates threads to stop
variation = 2.                          # defines the span for random time interval


# Parameters
# threadID  :  assigns unique ID to the thread
# name      :  assigns name to the thread
# priority  :  assigns priority for execution (ranges from 1 to 10)
# q         :  queue - data structure

# class for Producer : produces items and fills the queue
class Producer (threading.Thread):
    def __init__(self, threadID, name, q, priority=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.priority = priority

    def run(self):
        print("Producer " + self.name + " has started")

        while not exitFlag:
            if self.priority is not None:
                time.sleep(self.priority / 10)                  # if priority is set
            else:
                time.sleep(variation * random.random())         # if priority is not set

            self.q.put(1)

        print("Producer " + self.name + " has stopped")

# Parameters
# threadID  :  assigns unique ID to the thread
# name      :  assigns name to the thread
# priority  :  assigns priority for execution (ranges from 1 to 10)
# q         :  queue - data structure

# class for Consumer : consumes item from the queue
class Consumer (threading.Thread):
    def __init__(self, threadID, name, q, priority=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.priority = priority

    def run(self):
        print("Consumer " + self.name + " has started")

        while not exitFlag:
            if self.priority is not None:
                time.sleep(self.priority / 10)                  # if priority is set
            else:
                time.sleep(variation * random.random())         # if priority is not set

            self.q.get()

        print("Consumer " + self.name + " has stopped")

size = 100                              # queue size
q = Queue.Queue(size)                   # create queue

# fill the half queue
for i in range(int(size/2)):
    q.put(1)

threadLock = threading.Lock()
threads = []

producer = Producer(1, "prod1", q, 6.)          # create producer object with priority 6
consumer = Consumer(2, "cons1", q, 2.)          # create consumer object with priority 2

# start producer and consumer threads
producer.start()
consumer.start()

threads.append(producer)
threads.append(consumer)

# logging the current queue size
while True:
    if q.empty():                                   # if consumer completely empties the queue, wins
        print("Consumer Wins!")
        exitFlag = 1
        break
    elif q.full():                                  # if producer completely fills the queue, wins
        print("Producer Wins!")
        exitFlag = 1
        break
    else:                                           # otherwise log the current queue size
        print("Queue Size : " + str(q.qsize()))

# waiting for the producer and consumer threads to stop
for t in threads:
    t.join()

# program exits
print("Exit Program")
