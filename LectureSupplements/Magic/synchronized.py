"""
synchronized.py implements a few techniques for implementing
Java style synchronized keyword semantics on methods of a 
class.
"""
from threading import Lock


# The only way to ensure that our lock is injected once on the object instance
# is to maintain a global lock that's used to perform the check for the existance
# of the lock.
decorator_lock = Lock()
def synchronized(method):
    """
    A decorator object that can be used to declare that execution of a particular
    method should be done synchronous. This works by maintaining a lock object on
    the object instance, constructed for you if you don't have one already, and
    then acquires the lock before allowing the method to execute. This provides
    similar semantics to Java's synchronized keyword on methods.
    """
    # This is the new version of the function that will replace the decorated
    # version. Since method is a free variable in it's definition, this will
    # create a closure, which allows it to still have access to the actual
    # method when it executes.
    def new_synchronized_method(self, *args, **kwargs):
        # Here we check for the _auto_lock member of the object instance. If
        # it doesn't exist, we then obtain the lock and check again. This avoids
        # the overhead of obtaining the lock in most of the calling cases but also
        # acknowledges that after the lock is obtained, the state may have been
        # changed.
        if not hasattr(self, "_auto_lock"):
            with decorator_lock:
                if not hasattr(self, "_auto_lock"):
                    self._auto_lock = Lock()

        # The lines of code we were trying to eliminate in the first place.
        # Grab the lock and then call the method.
        with self._auto_lock:
            return method(self, *args, **kwargs)
    return new_synchronized_method



# This is a function that looks like it's a method on a class. It will be added
# via our metaclass AutoSynchronized. It acts just like the method_missing in
# Ruby except that methods beginning with 'synchronized_' will actually resolve
# to their base method but within the context of a mutex.
def method_missing(cls, name):
    if name.startswith("synchronized_") and hasattr(cls, name[13:]):
        def new_synchronized_method(*args, **kwargs):
            with cls._auto_lock:
                return getattr(cls, name[13:])(*args, **kwargs)
        return new_synchronized_method
    else:
        raise AttributeError


# This is a function that looks like a decorator but used by AutoSynchronized to
# inject a _auto_lock member on every instance of a class that uses our metaclass.
# This way we don't have to think about locking on methods.
def wrap_init_with_lock(org_init):
    def wrapped_init(self, *args, **kwargs):
       org_init(self, *args, **kwargs)
       self._auto_lock = Lock()
    return wrapped_init


class AutoSynchronized(type):
    """
    This is a metaclass, a class describing how classes should be built. This
    new metaclass wraps the init method with a new version that will add a lock
    object to self.

    It then provides a hook so that calling a method and prepending 'synchronized_'
    to the method name will obtain the injected lock before calling the method and 
    release it when leaving the method. No further work is required other than calling
    the method.
    """
    def __init__(cls, name, bases, namespaces):
        super(type, cls).__init__(name, bases, namespaces)
        cls.__init__ = wrap_init_with_lock(cls.__init__)
        cls.__getattr__ = method_missing


