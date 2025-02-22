from slixmpp.plugins.base import register_plugin

from . import stanza
from .notify import XEP_0492

register_plugin(XEP_0492)

__all__ = ["stanza", "XEP_0492"]
