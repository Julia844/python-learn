#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pandas as pd
import sys
import os
import logging
import logging.config

if __name__=="__main__":
  print("abc")
  print(os.path.join(os.getcwd(),'data', 'log.txt'))
  logging.basicConfig(filename = os.path.join(os.getcwd(),"data", 'log.txt'), level = logging.DEBUG)
  log = logging.getLogger('root')
  log.debug('%s, %s, %s', *('error', 'debug', 'info'))
  log.debug('%(module)s, %(info)s', {'module': 'log', 'info': 'error'})
  log.info("acc")
  log.error("error")
  print("bcd")