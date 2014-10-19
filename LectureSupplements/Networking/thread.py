import threading

def say_hello():
    print "Hello, I'm %s\n" % (threading.current_thread().name,)


def thread_process():
    f = threading.Thread(name="Francis", target=say_hello)
    f.start()

    for i in range(1,10):
        george = threading.Thread(name="George Foreman " + str(i), target=say_hello)
        george.start()

    say_hello()


if __name__ == "__main__":
    thread_process()
