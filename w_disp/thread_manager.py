# thread_manager.py
import _thread

def start_thread(target, arg):
    """
    Starts a new thread to run the target function with the given argument.

    :param target: The function to run in the thread.
    :param arg: The argument to pass to the target function.
    """
    try:
        _thread.start_new_thread(target, (arg,))
    except Exception as e:
        print(f"Error starting thread for {target.__name__}: {e}")
