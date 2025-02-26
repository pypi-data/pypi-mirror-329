from collective.formsupport.counter import _
from collective.formsupport.counter.config import COUNTER_ANNOTATIONS_NAME
from collective.formsupport.counter.config import COUNTER_BLOCKS_FIELD_ID
from collective.formsupport.counter.config import COUNTER_ENABLED_FORM_FLAG_NAME
from collective.formsupport.counter.interfaces import ICollectiveFormsupportCounterLayer
from collective.volto.formsupport.adapters.post import PostAdapter
from collective.volto.formsupport.interfaces import IPostAdapter
from copy import deepcopy
from plone import api
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface


@implementer(IPostAdapter)
@adapter(Interface, ICollectiveFormsupportCounterLayer)
class PostAdapterWithCounter(PostAdapter):

    _block = {}

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, new_value):
        block = deepcopy(new_value)

        if block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
            block["subblocks"].append({"field_id": COUNTER_BLOCKS_FIELD_ID})

        self._block = block

    def extract_data_from_request(self):
        form_data = super().extract_data_from_request()
        block_id = form_data.get("block_id", "")
        block = None

        if block_id:
            block = self.get_block_data(block_id=block_id)

        if not block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
            return form_data

        annotations = IAnnotations(self.context)

        value = annotations.get(COUNTER_ANNOTATIONS_NAME, {}).get(block_id, 0) + 1
        form_data["data"].append(
            {
                "field_id": COUNTER_BLOCKS_FIELD_ID,
                "label": translate(
                    _("Form counter"), target_language=api.portal.get_current_language()
                ),
                "value": value,
            }
        )

        return form_data
