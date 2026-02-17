import structlog
import logging
import sys
from pathlib import Path

def setup_logging():
    """
    Configure structured logging for CODEX application
    Logs are output in JSON format for easy parsing and analysis
    """
    # Create logs directory
    log_dir = Path("/app/logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure structlog processors
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure Python logging to write to file and console
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(sys.stdout),  # Console output
            logging.FileHandler("/app/logs/codex.log")  # File output
        ]
    )
    
    # Get logger and log startup
    logger = structlog.get_logger()
    logger.info("logging_configured", 
                version="1.0.0", 
                log_format="json",
                log_file="/app/logs/codex.log")
    
    return logger
