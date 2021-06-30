import tal_service_config
import logging
import os
import sys
import threading

defaults = {
    'example_service': {
        'host_port': [
            's4f-services04:9053',
            's4f-services09:9053'
        ]
    }
}

namespace = None


class Config(object):
    """
    This class is a singleton that returns
    a configured instance of the config
    """

    _lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Singleton """
        with cls._lock:
            if not cls._instance:
                cls._instance = super(
                    Config, cls).__new__(cls, *args, **kwargs)
                cls._instance.logger = logging.getLogger(__name__)
                cls._instance.service_config = None
        return cls._instance

    def get_config(self):
        """
        Get the service config
        """
        if self._instance:
            return self._instance.service_config
        else:
            logger = logging.getLogger(__name__)
            logger.warn('attempted to access service_config when config has not been configured yet')

    def configure(self, role):
        with self.__class__._lock:
            base_path = os.path.dirname(__file__)
            cfg = os.path.join(base_path, '{}.ini'.format(str(role).lower()))
            self._instance.service_config = tal_service_config.ServiceConfig(
                env_namespace=namespace,
                ini_files=[cfg],
                defaults=defaults)
            self._instance.logger.info('configured config client; role=%s', role)


def get_service_config():
    role = os.environ.get("ROLE")
    if role == "KUBERNETES":
        role += '-' + os.environ.get("ENVIRONMENT")
    config = Config()
    config.configure(role)
    return config.get_config()

CONFIG = get_service_config()
