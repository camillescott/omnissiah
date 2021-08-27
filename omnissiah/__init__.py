import os

__author__ = """Camille Scott"""
__email__ = 'cswel@ucdavis.edu'
__version__ = '0.1'

__splash__ = f'''
                       _         _       _     
  ___  _ __ ___  _ __ (_)___ ___(_) __ _| |__  
 / _ \| '_ ` _ \| '_ \| / __/ __| |/ _` | '_ \ 
| (_) | | | | | | | | | \__ \__ \ | (_| | | | |
 \___/|_| |_| |_|_| |_|_|___/___/_|\__,_|_| |_|
                                v{__version__}
                                by {__author__}
'''
__about__ = 'Tools for Rogue Trader'
__testing__ = bool(os.environ.get('OMNISSIAH_DEBUG', False))

from .__main__ import main
