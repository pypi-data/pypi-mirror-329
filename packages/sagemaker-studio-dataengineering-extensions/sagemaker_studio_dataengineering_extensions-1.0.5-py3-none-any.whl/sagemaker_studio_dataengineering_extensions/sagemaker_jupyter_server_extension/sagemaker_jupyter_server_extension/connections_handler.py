from jupyter_server.extension.handler import ExtensionHandlerMixin
from jupyter_server.base.handlers import APIHandler
import tornado
import json
import logging
from tornado import web
import asyncio

from sagemaker_jupyter_server_extension.connection_utils.connection_utils import list_connection

logger = logging.getLogger(__name__)

class SageMakerConnectionsHandler(ExtensionHandlerMixin, APIHandler):
    @tornado.web.authenticated
    async def get(self):
        try:
            logger.info('received request to get connections')
            loop = asyncio.get_running_loop()
            connections = await loop.run_in_executor(None, list_connection)
            await self.finish(json.dumps(connections, default=str))
        except Exception as e:
            logger.exception(e)
