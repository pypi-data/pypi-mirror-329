import logging.config

from src.utils.path_helper import get_data_dir


def setup_logging():
    """
    Set up logging configuration for the application.
    """

    log_file_path = get_data_dir() / 'logs' / 'digitizer.log'
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': str(log_file_path),
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
    }

    logging.config.dictConfig(logging_config)
