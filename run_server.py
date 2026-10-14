import sys
import os
import traceback
import logging

logging.basicConfig(
    filename="server_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("Starting server launcher...")

try:
    from streamlit.web import bootstrap
    
    flag_options = {
        "server.port": 8501,
        "server.headless": True,
        "browser.gatherUsageStats": False,
        "server.fileWatcherType": "none",
        "server.enableCORS": False,
        "server.enableXsrfProtection": False
    }
    
    logging.info(f"Invoking bootstrap.run with options: {flag_options}")
    bootstrap.run("app.py", "", [], flag_options=flag_options)
except SystemExit as e:
    logging.info(f"SystemExit caught with code: {e.code}")
    sys.exit(e.code)
except Exception as e:
    logging.error(f"Exception caught: {e}\n{traceback.format_exc()}")
    sys.exit(1)
finally:
    logging.info("Server process exiting.")
