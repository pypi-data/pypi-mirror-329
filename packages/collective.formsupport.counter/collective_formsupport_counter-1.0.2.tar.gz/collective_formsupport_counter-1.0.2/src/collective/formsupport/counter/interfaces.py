"""Module where all interfaces, events and exceptions live."""

from collective.volto.formsupport.interfaces import ICollectiveVoltoFormsupportLayer


class ICollectiveFormsupportCounterLayer(ICollectiveVoltoFormsupportLayer):
    """Marker interface that defines a browser layer."""
