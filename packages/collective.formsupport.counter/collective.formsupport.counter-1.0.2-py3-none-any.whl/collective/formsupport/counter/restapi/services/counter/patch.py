from collective.formsupport.counter import logger
from collective.formsupport.counter.config import COUNTER_ANNOTATIONS_NAME
from persistent.dict import PersistentDict
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import BadRequest
from zExceptions import NotFound
from zope.annotation.interfaces import IAnnotations


class CounterReset(Service):
    def get_block_id(self, block_id):
        if not block_id:
            logger.warning(
                "missing block_id for %s get the first formsupport block",
                self.context.absolute_url(),
            )

        blocks = getattr(self.context, "blocks", {})

        if not blocks:
            return

        for id, block in blocks.items():
            if block.get("@type", "") == "form":
                if not block_id or block_id == id:
                    return id

    def reply(self):
        data = json_body(self.request)
        block_id = self.get_block_id(data.get("block_id"))

        if not block_id:
            raise NotFound(self.context, "", self.request)

        try:
            counter_value = int(data.get("counter_value", 0))

        except ValueError:
            raise BadRequest(
                "Badly composed `counter_value` parameter, integer required."
            )

        annotations = IAnnotations(self.context)
        counter_object = annotations.setdefault(
            COUNTER_ANNOTATIONS_NAME, PersistentDict({})
        )
        counter_object[block_id] = counter_value

        self.request.response.setStatus(204)
