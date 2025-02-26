from collective.formsupport.counter.config import COUNTER_BLOCKS_FIELD_ID
from collective.formsupport.counter.config import COUNTER_ENABLED_FORM_FLAG_NAME
from collective.formsupport.counter.interfaces import ICollectiveFormsupportCounterLayer
from collective.volto.formsupport.datamanager.catalog import FormDataStore
from collective.volto.formsupport.interfaces import IFormDataStore
from collective.volto.formsupport.utils import get_blocks
from copy import deepcopy
from plone.dexterity.interfaces import IDexterityContent
from zope.component import adapter
from zope.interface import implementer


@implementer(IFormDataStore)
@adapter(IDexterityContent, ICollectiveFormsupportCounterLayer)
class FormDataStoreWithCounter(FormDataStore):
    def get_form_fields(self):
        blocks = get_blocks(self.context)

        if not blocks:
            return {}

        form_block = {}

        for id, block in blocks.items():

            if id != self.block_id:
                continue

            block_type = block.get("@type", "")

            if block_type == "form":
                form_block = deepcopy(block)

        if not form_block:
            return {}

        subblocks = form_block.get("subblocks", [])

        if form_block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
            subblocks.append({"field_id": COUNTER_BLOCKS_FIELD_ID})

        # Add the 'custom_field_id' field back in as this isn't stored with each subblock
        for index, field in enumerate(subblocks):
            if form_block.get(field["field_id"]):
                subblocks[index]["custom_field_id"] = form_block.get(field["field_id"])

        return subblocks
