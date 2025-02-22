import logging

def parse_log_level(log_level: str) -> int:
    log_level_i = getattr(logging, log_level.upper(), None)
    match log_level_i:
        case logging.NOTSET:
            return -100
        case logging.DEBUG:
            return 0
        case logging.INFO:
            return 100
        case logging.WARNING:
            return 200
        case logging.ERROR:
            return 300
        case logging.FATAL:
            return 400
        case _:
            raise ValueError(f"Unable to convert log level to value: {log_level}")