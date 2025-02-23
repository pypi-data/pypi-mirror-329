import logging
import os

from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"

log_dir = 'logs'

logs_path = os.path.join(os.getcwd(), log_dir, LOG_FILE)


os.makedirs(log_dir, exist_ok=True)


logging.basicConfig(
    filename=logs_path,
    format="[ %(asctime)s ] - %(levelname)s - %(message)s",
    level=logging.DEBUG,)

logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger('s3transfer').setLevel(logging.WARNING)
logging.getLogger('git.cmd').setLevel(logging.WARNING)
logging.getLogger('neuro_mf').setLevel(logging.WARNING)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
