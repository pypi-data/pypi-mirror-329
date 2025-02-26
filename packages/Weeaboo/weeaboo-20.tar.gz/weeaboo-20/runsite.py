'Website entrypoint.'
from aridity.config import ConfigCtrl
from pathlib import Path
import lagoon.sic.text, os

mod_wsgi_express = getattr(lagoon.sic.text, 'mod_wsgi-express')

def main():
    cc = ConfigCtrl()
    cc.load('/site/deploy/LOADME.arid')
    config = cc.node
    stat = Path(config.img.root).stat()
    os.setgid(stat.st_gid)
    os.setuid(stat.st_uid)
    del os.environ['HOME']
    mod_wsgi_express.start_server.__application_type.module[exec](*config.start_server, 'weeaboo.wsgi')

if '__main__' == __name__:
    main()
