import logging
import pathlib
from importlib.metadata import version
import json

from mopidy import config, ext
import tornado.web


__version__ = version("mopidy-debugrel")

logger = logging.getLogger(__name__)


class DebugRequestHandler(tornado.web.RequestHandler):
    def initialize(self, config, core):
        self.config = config
        self.core = core
        logger.info(f"config: {config}")

    def post(self):
        payload = self.request.body
        data = json.loads(payload)

        exec(data["source"], globals(), locals())
        self.finish(
            f'Done'
        )


def api_factory(config, core):
    return [
        ('/debug', DebugRequestHandler, {'config': config, 'core': core})
    ]


class Extension(ext.Extension):

    dist_name = "mopidy-debugrel"
    ext_name = "debugrel"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        return schema

    def setup(self, registry):
        logger.warning("WARNING: Debug Read-Eval-Loop is enabled - make sure to disable it when you are done !")
        registry.add('http:app',
            {
                "name": self.ext_name,
                "factory": api_factory
            },
        )
