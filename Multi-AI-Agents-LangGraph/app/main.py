
import os
import subprocess
import threading
import time 
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from dotenv import load_dotenv
load_dotenv()


logger = get_logger(__name__)


def run_backend():
    try:
        logger.info(f"Starting backend service")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"], check=True)
    except CustomException as e:
        logger.error(f"Problem with backend service")
        raise CustomException(f"Failed to start backend", e)
    

def run_frontend():
    try:
        logger.info(f"Starting frontend service")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)
    except CustomException as e:
        logger.error(f"Problem with frontend service")
        raise CustomException(f"Failed to start frontend", e)
    


if __name__ == "__main__":
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        run_frontend()
    except CustomException as e:
        logger.exception(f"CustomException occurred: {str(e)}")