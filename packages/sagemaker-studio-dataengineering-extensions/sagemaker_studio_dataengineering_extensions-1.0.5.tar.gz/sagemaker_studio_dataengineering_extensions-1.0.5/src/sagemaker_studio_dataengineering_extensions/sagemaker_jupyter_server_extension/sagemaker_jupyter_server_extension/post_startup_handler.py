import json
import logging
import subprocess

from jupyter_server.extension.handler import ExtensionHandlerMixin
from jupyter_server.base.handlers import APIHandler
import tornado

from .workflow_utils import (
    check_file_exists
)

logger = logging.getLogger(__name__)

POST_STARTUP_SCRIPT_FILE = "/etc/sagemaker-ui/sagemaker_ui_post_startup.sh"
LOG_FILE = "/var/log/apps/post_startup_default.log"

class SageMakerPostStartupHandler(ExtensionHandlerMixin, APIHandler):
    @tornado.web.authenticated
    async def post(self):
        logger.info(f"received request to execute post startup script")
        result = await self.run_post_startup_script()
        await self.finish(json.dumps(result))

    @check_file_exists(POST_STARTUP_SCRIPT_FILE)
    async def run_post_startup_script(self):
        """
        If POST_STARTUP_SCRIPT_FILE doesn't exist, it will throw FileNotFoundError (404)
        If exists, it will start the execution and add the execution logs in LOG_FILE.
        """
        try:
            with open(LOG_FILE, "w+") as log_file:
                subprocess.Popen(
                    ["bash", POST_STARTUP_SCRIPT_FILE],
                    cwd="/",
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                )
        except Exception as e:
            logger.exception("encountered error when attempting to execute post startup script", e)
            raise web.HTTPError(500, ErrorMessage.UNEXPECTED_ERROR % e)
        else:
            logger.info(f"successfully triggered post startup script")
            return {"success": "true"}