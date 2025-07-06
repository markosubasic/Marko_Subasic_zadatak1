import logging, structlog, sys
from tickethub.core.config import get_settings

def configure_logging() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(message)s",
        stream=sys.stdout,          
                )
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(settings.log_level)),
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
    )
