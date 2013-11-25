# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import collections
import multiprocessing
import random
import string
import time

import prettytable

import astrometrics as ions
import astrometrics.cloud_connect.cloudapi_setup as cls


def rand_string(length=15):
    """Generate a Random string."""

    chr_set = string.ascii_uppercase
    output = ''
    for _ in range(length):
        output += random.choice(chr_set)
    return output


def basic_deque(iters=None):
    """Create Basic Deque.

    :param iters: Places interables into a deque
    """

    worker_q = collections.deque([])
    if iters:
        for _dt in iters:
            worker_q.append(_dt)
    return worker_q


def basic_queue(iters=None):
    """Create basic work queue.

    :param iters: Places interables into a deque
    """

    worker_q = multiprocessing.Queue()
    if iters:
        for _dt in iters:
            worker_q.put(_dt)
    return worker_q


def worker_proc(job_action, num_jobs, t_args=None):
    """Requires the job_action and num_jobs variables for functionality.

    :param job_action: What function will be used
    :param num_jobs: The number of jobs that will be processed
    :param t_args: Optional

    All threads produced by the worker are limited by the number of concurrency
    specified by the user. The Threads are all made active prior to them
    processing jobs.
    """

    import collections
    import multiprocessing as multi

    if t_args:
        processes = collections.deque(
            [multi.Process(target=job_action, args=(t_args,))
             for _ in range(num_jobs)]
        )
    else:
        processes = collections.deque(
            [multi.Process(target=job_action,) for _ in range(num_jobs)]
        )
    process_threads(processes=processes)


def compute_workers(base_count=5):
    """Compute the MAX number of threads the system can handle."""

    try:
        max_threads = (multiprocessing.cpu_count() * base_count)
    except Exception:
        max_threads = base_count
    return max_threads


def process_threads(processes):
    """Process the built actions.

    :param processes: deque of threads to process.
    """

    max_threads = compute_workers()
    post_process = []
    while processes:
        jobs = len(processes)
        if jobs > max_threads:
            cpu = max_threads
        else:
            cpu = jobs

        for _ in xrange(cpu):
            try:
                _jb = processes.popleft()
                post_process.append(_jb)
                _jb.start()
            except IndexError:
                break
    for _pp in reversed(post_process):
        _pp.join()


def manager_dict(b_d=None):
    """Create a Multiprocessing Manager Dictionary.

    :param b_d: Base Dictionary

    If you use the "bd" variable you can specify a prebuilt dict
    the default is that bd=None
    """

    manager = multiprocessing.Manager()
    if b_d:
        managed_dictionary = manager.dict(b_d)
    else:
        managed_dictionary = manager.dict()
    return managed_dictionary


def retryloop(attempts, timeout=None, delay=None, backoff=1):
    """Create a shared dictionary using multiprocessing Managers.

    Enter the amount of retries you want to perform.
    The timeout allows the application to quit on "X".
    delay allows the loop to wait on fail. Useful for making REST calls.

    :param attempts:
    :param timeout:
    :param delay:
    :param backoff:

    Example:
        Function for retring an action.
        for retry in retryloop(attempts=10, timeout=30, delay=1, backoff=1):
            something
            if somecondition:
                retry()

    Borrowed from :
    ACTIVE STATE retry loop
    http://code.activestate.com/recipes/578163-retry-loop/
    """

    starttime = time.time()
    success = set()
    for _ in range(attempts):
        success.add(True)
        yield success.clear
        if success:
            return
        duration = time.time() - starttime
        if timeout is not None and duration > timeout:
            break
        if delay:
            time.sleep(delay)
            delay = delay * backoff
    raise ions.RetryError


def stupid_hack():
    """Return a random time between 1 - 10 Seconds."""

    # Stupid Hack For Public Cloud so that it is not
    # overwhemled with instance creations
    timer = random.randrange(1, 10)
    return timer


def ret_conn(args):
    """Returns an active connection."""

    conn = cls.api_conn(args=args)
    if not conn:
        raise ions.SystemError('No Connection Available')
    else:
        return conn
