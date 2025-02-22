from jupyter_server.extension.application import ExtensionApp

from .connections_handler import SageMakerConnectionsHandler
from .ping_handlers import SageMakerPingHandler
from .creds_handlers import SageMakerCredsHandler
from .env_handlers import SageMakerEnvHandler
from .connection_handler import SageMakerConnectionHandler
from .workflow_handler import SageMakerWorkflowHandler
from .spark_history_server import SageMakerSparkHistoryServerHandler
from .post_startup_handler import SageMakerPostStartupHandler


class Extension(ExtensionApp):
    name = "sagemaker_jupyter_server_extension"

    handlers = [
        ("sagemaker/ping", SageMakerPingHandler),
        ("api/creds", SageMakerCredsHandler),
        ("api/aws/datazone/connections", SageMakerConnectionsHandler),
        ("api/env", SageMakerEnvHandler),
        ("api/aws/datazone/connection", SageMakerConnectionHandler),
        ("api/sagemaker/workflows/(.*)", SageMakerWorkflowHandler),
        ("api/spark-history-server", SageMakerSparkHistoryServerHandler),
        ("api/poststartup", SageMakerPostStartupHandler),
    ]
