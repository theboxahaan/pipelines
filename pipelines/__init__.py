# -*- coding: utf-8 -*-

art = \
"""
       _         _ _             
   ___|_|___ ___| |_|___ ___ ___ 
  | . | | . | -_| | |   | -_|_ -|
  |  _|_|  _|___|_|_|_|_|___|___|
  |_|   |_|                      
"""

import asyncio
import logging
print(art)
logging.getLogger(__name__).addHandler(logging.NullHandler())
