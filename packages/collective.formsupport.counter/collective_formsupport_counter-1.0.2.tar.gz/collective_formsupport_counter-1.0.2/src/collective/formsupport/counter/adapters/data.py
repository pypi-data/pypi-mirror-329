from collective.formsupport.counter import logger
from collective.formsupport.counter.config import COUNTER_ANNOTATIONS_NAME
from collective.formsupport.counter.config import COUNTER_BLOCKS_FIELD_ID
from collective.formsupport.counter.config import COUNTER_ENABLED_FORM_FLAG_NAME
from collective.formsupport.counter.interfaces import ICollectiveFormsupportCounterLayer
from collective.volto.formsupport.interfaces import IDataAdapter
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IDataAdapter)
@adapter(Interface, ICollectiveFormsupportCounterLayer)
class DataAdapterWithCounter:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_block(self, block_id):
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
                    return block

    def __call__(self, result, block_id=None):
        block = self.get_block(block_id)
        if block and block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
            annotations = IAnnotations(self.context)
            result["form_data"][COUNTER_BLOCKS_FIELD_ID] = annotations.get(
                COUNTER_ANNOTATIONS_NAME, {}
            ).get(block_id, 0)
        return result
