from collective.formsupport.counter.config import COUNTER_ANNOTATIONS_NAME
from collective.formsupport.counter.config import COUNTER_ENABLED_FORM_FLAG_NAME
from collective.formsupport.counter.interfaces import ICollectiveFormsupportCounterLayer
from Persistence import PersistentMapping
from zope.annotation.interfaces import IAnnotations
from zope.globalrequest import getRequest


def add_counter(context, event):
    """Add forms counter on the context if form requires"""

    if not ICollectiveFormsupportCounterLayer.providedBy(getRequest()):
        return

    if not event.form.get(COUNTER_ENABLED_FORM_FLAG_NAME):
        return

    block_id = event.form_data.get("block_id")
    annotations = IAnnotations(context)

    if COUNTER_ANNOTATIONS_NAME not in annotations:
        annotations[COUNTER_ANNOTATIONS_NAME] = PersistentMapping()

    if block_id not in annotations[COUNTER_ANNOTATIONS_NAME]:
        annotations[COUNTER_ANNOTATIONS_NAME][block_id] = 1

    else:
        annotations[COUNTER_ANNOTATIONS_NAME][block_id] += 1
