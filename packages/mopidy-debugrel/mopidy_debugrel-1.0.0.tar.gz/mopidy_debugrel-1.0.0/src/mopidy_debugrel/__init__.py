import logging
import pathlib
from importlib.metadata import version
import json
from datetime import date

from mopidy import config, ext
import tornado.web


__version__ = version("mopidy-debugrel")

logger = logging.getLogger(__name__)


class DebugRequestHandler(tornado.web.RequestHandler):
    def initialize(self, config, core):
        self.config = config
        self.core = core

    def post(self):
        payload = self.request.body
        data = json.loads(payload)

        exec(data["source"], globals(), locals())
        self.finish(
            f'Done'
        )


def api_factory(config, core):

    logger.info("HELLOOOOOOOOOOo")
    enabled_until_str = config["debugrel"]["enabled_until"]
    try:
        enabled_until = date.fromisoformat(enabled_until_str)
    except Exception:
        logger.exception(
            f"Warning: failed to parse {enabled_until_str} as a date.\n"
            "Expected format: 'YYYY-MM-DD'\n."
            f"The debug route will not be enabled."
        )
        return []
    if enabled_until < date.today():
        logger.warning(
            f"Warning: Extension debugrel has been automatically disabled.\n"
            "Adapt 'enable_until' to re-enable, or disable in config."
        )
        return []

    logger.warning(
        f"Warning: Extension debugrel is enabled until {enabled_until}.\n"
        "Disable when you are done."
    )

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
        schema["enabled_until"] = config.String()
        return schema

    def setup(self, registry):
        logger.warning("WARNING: Debug Read-Eval-Loop is enabled - make sure to disable it when you are done !")
        registry.add('http:app',
            {
                "name": self.ext_name,
                "factory": api_factory
            },
        )
