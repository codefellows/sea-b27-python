import os

def fork_process():
    pid = os.fork()
    if pid == 0:
        raise RuntimeError("oops, the child has soiled themselves")
    else:
        while True:
            print "I'm the parent and I haven't terminated yet. My child pid is %s" % (pid,)


if __name__ == "__main__":
    fork_process()
