"""schemadisplay magic"""
__version__ = '0.0.1'

from .schemadisplay import SQLSchemaDisplayMagic


def load_ipython_extension(ipython):
    ipython.register_magics(SQLSchemaDisplayMagic)