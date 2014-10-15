import sys, threading


class Adder:
    def __init__(self):
        self.total = 0
        self.done = False

    def add(self):
        for i in range(100000):
            self.total = self.total + i
        self.done = True


if __name__ == "__main__":
    anAdder = Adder()
    mutex = threading.Lock()
    condVar = threading.Condition(mutex)

    def threaded_adder():
        anAdder.add()
        condVar.acquire()
        condVar.notify()
        condVar.release()
    thread = threading.Thread(target=threaded_adder)
    thread.start()

    if len(sys.argv) > 1 and sys.argv[1] == "be-safe":
        condVar.acquire()
        while anAdder.done is False:
            condVar.wait()
        condVar.release()

    print "The sum is %s" % (anAdder.total,)
