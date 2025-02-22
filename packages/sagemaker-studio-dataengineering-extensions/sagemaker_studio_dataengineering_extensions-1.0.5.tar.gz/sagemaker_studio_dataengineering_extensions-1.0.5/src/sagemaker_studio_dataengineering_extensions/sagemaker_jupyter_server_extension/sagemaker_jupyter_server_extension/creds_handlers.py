import json
import boto3
import asyncio

from jupyter_server.extension.handler import ExtensionHandlerMixin
from jupyter_server.base.handlers import APIHandler
import tornado
import logging

logger = logging.getLogger(__name__)

class SageMakerCredsHandler(ExtensionHandlerMixin, APIHandler):
    @tornado.web.authenticated
    async def get(self):
        try:
            logger.info('Received request to get credentials')
            self.set_header('Cache-Control', 'no-store')
            self.set_header('Expires', '0')

            loop = asyncio.get_running_loop()

            def get_credentials():
                session = boto3.Session(profile_name='DomainExecutionRoleCreds')
                credentials = session.get_credentials()
                credentials = credentials.get_frozen_credentials()
                return {
                    "access_key": credentials.access_key,
                    "secret_key": credentials.secret_key,
                    "session_token": credentials.token
                }

            credentials = await loop.run_in_executor(None, get_credentials)
            await self.finish(json.dumps(credentials))
        except Exception as e:
            logger.exception(e)
