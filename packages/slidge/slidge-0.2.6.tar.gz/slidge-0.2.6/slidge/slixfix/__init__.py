# This module contains patches for slixmpp; some have pending requests upstream
# and should be removed on the next slixmpp release.

# ruff: noqa: F401

import slixmpp.plugins
from slixmpp import Iq, Message
from slixmpp.exceptions import _DEFAULT_ERROR_TYPES, XMPPError
from slixmpp.plugins.xep_0004.stanza.field import FormField
from slixmpp.plugins.xep_0050 import XEP_0050, Command
from slixmpp.plugins.xep_0231 import XEP_0231
from slixmpp.plugins.xep_0425.stanza import Moderate
from slixmpp.plugins.xep_0469.stanza import NS as PINNED_NS
from slixmpp.plugins.xep_0469.stanza import Pinned
from slixmpp.xmlstream import StanzaBase

from . import (
    link_preview,
    xep_0077,
    xep_0100,
    xep_0153,
    xep_0292,
    xep_0492,
)

# TODO: remove this when the fix is included in slixmpp
Moderate.interfaces.add("id")

_DEFAULT_ERROR_TYPES["policy-violation"] = "modify"  # type:ignore


async def _handle_bob_iq(self, iq: Iq):
    cid = iq["bob"]["cid"]

    if iq["type"] == "result":
        await self.api["set_bob"](iq["from"], None, iq["to"], args=iq["bob"])
        self.xmpp.event("bob", iq)
    elif iq["type"] == "get":
        data = await self.api["get_bob"](iq["to"], None, iq["from"], args=cid)

        if data is None:
            raise XMPPError(
                "item-not-found",
                f"Bits of binary '{cid}' is not available.",
            )

        if isinstance(data, Iq):
            data["id"] = iq["id"]
            data.send()
            return

        iq = iq.reply()
        iq.append(data)
        iq.send()


def set_pinned(self, val: bool):
    extensions = self.parent()
    if val:
        extensions.enable("pinned")
    else:
        extensions._del_sub(f"{{{PINNED_NS}}}pinned")


Pinned.set_pinned = set_pinned


XEP_0231._handle_bob_iq = _handle_bob_iq


def session_bind(self, jid):
    self.xmpp["xep_0030"].add_feature(Command.namespace)
    # awful hack to for the disco items: we need to comment this line
    # related issue: https://todo.sr.ht/~nicoco/slidge/131
    # self.xmpp['xep_0030'].set_items(node=Command.namespace, items=tuple())


XEP_0050.session_bind = session_bind  # type:ignore


def reply(self, body=None, clear=True):
    """
    Overrides slixmpp's Message.reply(), since it strips to sender's resource
    for mtype=groupchat, and we do not want that, because when we raise an XMPPError,
    we actually want to preserve the resource.
    (this is called in RootStanza.exception() to handle XMPPErrors)
    """
    new_message = StanzaBase.reply(self, clear)
    new_message["thread"] = self["thread"]
    new_message["parent_thread"] = self["parent_thread"]

    del new_message["id"]
    if self.stream is not None and self.stream.use_message_ids:
        new_message["id"] = self.stream.new_id()

    if body is not None:
        new_message["body"] = body
    return new_message


Message.reply = reply  # type: ignore


FormField.set_value_base = FormField.set_value  # type:ignore


def set_value(self: FormField, value):
    if not self._type:
        if isinstance(value, bool):
            self._type = "boolean"
        elif isinstance(value, str):
            self._type = "text-single"
        elif isinstance(value, (list, tuple)):
            self._type = "text-multi"

    FormField.set_value_base(self, value)


def get_value(self, convert=True, convert_list=False):
    valsXML = self.xml.findall("{%s}value" % self.namespace)
    if len(valsXML) == 0:
        return None
    elif self._type == "boolean":
        if convert:
            return valsXML[0].text in self.true_values
        return valsXML[0].text
    elif self._type in self.multi_value_types or len(valsXML) > 1:
        values = []
        for valXML in valsXML:
            if valXML.text is None:
                valXML.text = ""
            values.append(valXML.text)
        if self._type == "text-multi" and convert_list:
            values = "\n".join(values)
        return values
    else:
        if valsXML[0].text is None:
            return ""
        return valsXML[0].text


FormField.set_value = set_value  # type:ignore
FormField.get_value = get_value  # type:ignore


slixmpp.plugins.PLUGINS.extend(
    [
        "link_preview",
        "xep_0292_provider",
        "xep_0492",
    ]
)
