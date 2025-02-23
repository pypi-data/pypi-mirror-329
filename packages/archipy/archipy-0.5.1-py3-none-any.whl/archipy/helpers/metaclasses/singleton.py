import threading


class Singleton(type):
    """A thread-safe Singleton metaclass that ensures only one instance of a class is created.

    This metaclass can be used to create Singleton classes. It supports an optional `thread_safe`
    parameter to control whether thread-safety mechanisms (e.g., locks) should be used.

    Attributes:
        _instances (dict): A dictionary to store instances of Singleton classes.
        _lock (threading.Lock): A lock to ensure thread-safe instance creation.

    Example:
        To create a Singleton class, use the `Singleton` metaclass and optionally specify
        whether thread-safety should be enabled:

        ```python
        class MySingletonClass(metaclass=Singleton, thread_safe=True):
            def __init__(self, value):
                self.value = value

        # Create instances of MySingletonClass
        instance1 = MySingletonClass(10)
        instance2 = MySingletonClass(20)

        # Verify that both instances are the same
        print(instance1.value)  # Output: 10
        print(instance2.value)  # Output: 10
        print(instance1 is instance2)  # Output: True
        ```
    """

    _instances = {}  # Stores instances of Singleton classes
    _lock = threading.Lock()  # Lock for thread-safe instance creation

    def __new__(cls, name, bases, dct, **kwargs):
        """Create a new Singleton metaclass instance.

        Args:
            name (str): The name of the class.
            bases (tuple): The base classes of the class.
            dct (dict): The namespace containing the class attributes.
            **kwargs: Additional keyword arguments, including `thread_safe`.

        Returns:
            type: A new metaclass instance.
        """
        # Extract the `thread_safe` parameter from kwargs
        thread_safe = kwargs.pop("thread_safe", True)
        # Create the new class
        new_class = super().__new__(cls, name, bases, dct, **kwargs)
        # Set the `thread_safe` attribute for the class
        new_class._thread_safe = thread_safe
        return new_class

    def __call__(cls, *args, **kwargs):
        """Create or return the Singleton instance of the class.

        If `thread_safe` is True, a lock is used to ensure that only one instance is created
        even in a multi-threaded environment. If `thread_safe` is False, no locking mechanism
        is used, which may result in multiple instances being created in a multi-threaded context.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            object: The Singleton instance of the class.
        """
        if cls not in cls._instances:
            if cls._thread_safe:
                with cls._lock:
                    if cls not in cls._instances:
                        cls._instances[cls] = super().__call__(*args, **kwargs)
            else:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
