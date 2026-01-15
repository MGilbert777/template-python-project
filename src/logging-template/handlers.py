import logging
import sys
import logfire
from loguru import logger
from .formatters import GCPJsonFormatter

def setup_logging(service_name: str, environment: str = "local"):
    # 1. Configure Logfire (Local/Offline Mode)
    # environment='local' + manual console config avoids cloud connection requirements
    logfire.configure(
        service_name=service_name,
        environment=environment,
        send_to_logfire=False,  # <--- Crucial: Disables cloud telemetry
        console=logfire.ConsoleOptions(include_timestamp=True)
    )

    # 2. Setup Standard Python Logging to route through Logfire
    # This ensures 3rd party libs using 'logging' are caught by Logfire/Loguru
    logging.basicConfig(handlers=[logfire.LogfireLoggingHandler()])

    # 3. Configure Loguru
    # Remove default handler to avoid double-logging
    logger.remove()

    # Sink A: Human-readable Console (Standard Loguru style)
    logger.add(
        sys.stdout, 
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG" if environment == "local" else "INFO"
    )

    # Sink B: Logfire Integration
    # This passes Loguru records into the Logfire spans/logs
    logger.add(logfire.loguru_handler(), level="DEBUG")

    # Sink C: JSON File (Optional, for GCP parity testing)
    if environment != "local":
        logger.add(
            "logs/service.json", 
            serialize=True, 
            level="INFO"
        )

    return logger