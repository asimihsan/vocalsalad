import logging
import sys
import traceback


logging_identifiers = [
    "tornado.access",
    "tornado.application",
    "tornado.general",
    "vocalsalad.test",
]


def enable_console_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    f = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(f)
    logger.addHandler(ch)


def disable_existing_logging():
    for identifier in logging_identifiers:
        logger = logging.getLogger(identifier)
        logger.handlers = []


class QueueHandler(logging.Handler):
    """
    This handler sends events to a queue. Typically, it would be used
    together with a multiprocessing Queue to centralise logging to file
    in one process (in a multi-process application), so as to avoid file
    write contention between processes.

    This code is new in Python 3.2, but this class can be copy pasted
    into user code for use with earlier Python versions.
    """

    def __init__(self, queue):
        """
        Initialise an instance, using the passed queue.
        """
        logging.Handler.__init__(self)
        self.queue = queue

    def enqueue(self, record):
        """
        Enqueue a record.

        The base implementation uses put_nowait. You may want to
        override this method if you want to use blocking, timeouts or
        custom queue implementations.
        """
        self.queue.put_nowait(record)

    def prepare(self, record):
        """
        Prepares a record for queuing. The object returned by this
        method is enqueued.

        The base implementation formats the record to merge the message
        and arguments, and removes unpickleable items from the record
        in-place.

        You might want to override this method if you want to convert
        the record to a dict or JSON string, or send a modified copy of
        the record while leaving the original intact.
        """
        # The format operation gets traceback text into record.exc_text
        # (if there's exception data), and also puts the message into
        # record.message. We can then use this to replace the original
        # msg + args, as these might be unpickleable. We also zap the
        # exc_info attribute, as it's no longer needed and, if not None,
        # will typically not be pickleable.
        self.format(record)
        record.msg = record.message
        record.args = None
        record.exc_info = None
        return record

    def emit(self, record):
        """
        Emit a record.

        Writes the LogRecord to the queue, preparing it for pickling
        first.
        """
        try:
            self.enqueue(self.prepare(record))
        except Exception:
            self.handleError(record)


def listener_configurer():
    root = logging.getLogger()
    h = logging.StreamHandler()
    f = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    h.setFormatter(f)
    root.addHandler(h)


def null_configurer():
    """nosetests captures logs directly from the logging handler. Hence
    when running tests the listener thread does not need to have
    any handlers configured. If you need logs to be sent to e.g.
    console you should instead use the 'listener_configurer'.
    """
    pass


def listener_thread(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            sys.stderr.write("Whoops! Problem:\n")
            traceback.print_exc(file=sys.stderr)


def worker_configurer(queue):
    """The worker configuration is done at the start of the worker
    process run. Note that on Windows you can't rely on fork semantics,
    so each process will run the logging configuration code when it
    starts.
    """
    h = QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.DEBUG)
