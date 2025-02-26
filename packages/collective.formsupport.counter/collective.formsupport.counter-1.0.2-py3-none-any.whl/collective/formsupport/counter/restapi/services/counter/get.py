from collective.formsupport.counter import logger
from collective.formsupport.counter.config import COUNTER_ANNOTATIONS_NAME
from plone.restapi.services import Service
from zExceptions import NotFound
from zope.annotation.interfaces import IAnnotations


class CounterGet(Service):
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
        block_id = self.get_block_id(self.request.get("block_id"))

        if not block_id:
            raise NotFound(self.context, "", self.request)

        annotations = IAnnotations(self.context)
        counter_object = annotations.get(COUNTER_ANNOTATIONS_NAME, {})

        return {"counter_value": counter_object.get(block_id, 0)}
