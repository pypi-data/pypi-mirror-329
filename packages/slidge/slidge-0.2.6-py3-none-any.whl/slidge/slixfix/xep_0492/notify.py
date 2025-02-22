from slixmpp.plugins import BasePlugin
from . import stanza


class XEP_0492(BasePlugin):
    """
    XEP-0492: Chat notification settings
    """

    name = "xep_0492"
    description = "XEP-0492: Chat notification settings"
    dependencies = {"xep_0402"}
    stanza = stanza

    def plugin_init(self):
        stanza.register_plugin()
