# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import astrometrics as ions


def rand_string(length=15):
    """Generate a Random string."""

    import random
    import string

    chr_set = string.ascii_uppercase
    output = ''
    for _ in range(length):
        output += random.choice(chr_set)
    return output


def basic_deque(iters=None):
    """Create Basic Deque.

    :param iters: Places interables into a deque
    """

    import collections

    worker_q = collections.deque([])
    if iters:
        for _dt in iters:
            worker_q.append(_dt)
    return worker_q


def basic_queue(iters=None):
    """Create basic work queue.

    :param iters: Places interables into a deque
    """

    import multiprocessing

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

    import multiprocessing

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

    import multiprocessing

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

    import time

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

    import random

    # Stupid Hack For Public Cloud so that it is not
    # overwhemled with instance creations
    timer = random.randrange(1, 10)
    return timer


def ret_conn(args):
    """Returns an active connection."""

    import astrometrics.cloud_connect.cloudapi_setup as cls
    conn = cls.api_conn(args=args)
    if not conn:
        raise ions.SystemError('No Connection Available')
    else:
        return conn


def print_horiz_table(data):
    """Print a horizontal pretty table from data."""

    import prettytable
    table = prettytable.PrettyTable(dict(data[0]).keys())

    for info in data:
        table.add_row(dict(info).values())
    for tbl in table.align.keys():
        table.align[tbl] = 'l'
    print(table)


def print_virt_table(data):
    """Print a virtical pretty table from data."""

    import prettytable
    table = prettytable.PrettyTable()
    table.add_column('Keys', data.keys())
    table.add_column('Values', data.values())
    for tbl in table.align.keys():
        table.align[tbl] = 'l'
    print(table)


def parse_dictionary(dictionary):
    """Parse all keys in a dictionary for Values that are None.

    :param default_args: all parsed arguments
    :returns dict: all arguments which are not None.
    """

    return dict([(key, value) for key, value in dictionary.iteritems()
                 if value is not None])


def list_pop(data, pat):
    """Remove an index from a list and return the list.

    :param data: list
    :param pat: pattern to index and pop
    """

    index = data.index(pat)
    return data.pop(index)


def ret_ipv4(data):
    """Validate and return IPv4 addresses."""

    for ipa in data:
        for octet in ipa.strip().split('.'):
            if not octet.isdigit():
                list_pop(data=data, pat=ipa)
            else:
                if not int(octet) < 256:
                    list_pop(data=data, pat=ipa)
    return data
