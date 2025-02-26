from . import Application
from aridity.config import ConfigCtrl
from diapyr import DI
from diapyr.util import singleton
import logging

@singleton
def application():
    logging.basicConfig(format = "%(levelname)s %(message)s", level = logging.DEBUG)
    cc = ConfigCtrl()
    cc.load('/site/etc/LOADME.arid')
    config = cc.node
    di = DI()
    di.add(config)
    for cls in config.applicationcls:
        di.add(cls)
    return di(Application)
