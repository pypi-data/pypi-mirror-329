import logging
import os
import structlog


def configure_logging(log_level=logging.INFO, output_dir="output", module_name=None):
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Use the module_name for the log file if provided, otherwise use a default name
    if module_name:
        log_file = os.path.join(output_dir, f"{module_name}.log")
    else:
        log_file = os.path.join(output_dir, "default.log")

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter("%(message)s"))
    root_logger.addHandler(handler)


def get_logger(name):
    return structlog.get_logger(name)
