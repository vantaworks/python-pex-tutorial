#!/usr/bin/env python3

import logging
from babble import launcher

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
LOG = logging.getLogger('dev')

launcher(live_reload=True)
