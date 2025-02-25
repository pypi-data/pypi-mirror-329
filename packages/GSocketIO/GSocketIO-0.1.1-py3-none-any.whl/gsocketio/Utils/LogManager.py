from logging import WARNING, Formatter, Logger, StreamHandler, getLogger

Date = "%Y/%m/%d %H:%M:%S"
Fmt = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"


def get_logger(name: str, log_level: int = WARNING) -> Logger:

    logger = getLogger(name)
    logger.setLevel(log_level)

    formatter = Formatter(Fmt, datefmt=Date)

    handler = StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
