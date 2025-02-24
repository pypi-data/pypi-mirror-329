"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for sankey proto class

"""


# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey_utils.table_object import TableObject


# CLASS ----------------------------------------------------------------------------
class _ProtoToolTip(object):
    """
    Proto class for Tooltip

    Parameters
    ----------
    :param name: Tooltip name
    :type name: str

    :param description: Tooltip description
    :type description: str

    :param content: Tooltip content
    :type content: str
    """
    def __init__(
        self,
        **kwargs
    ):
        self._name = None
        self._description = None
        self._content = None
        self.update(**kwargs)

    def update(
        self,
        **kwargs
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _):
        # None case
        if _ is None:
            self._name = None
            return
        # Real affectation
        try:
            self._name = str(_)
        except Exception:
            pass

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, _):
        # None case
        if _ is None:
            self._description = None
            return
        # Real affectation
        try:
            self._description = str(_)
        except Exception:
            pass

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, _):
        # None case
        if _ is None:
            self._content = None
            return
        # Real affectation
        try:
            self._content = str(_)
        except Exception:
            pass


class _ProtoSankeyObject(TableObject):
    """
    Proto class for SankeyObject.
    Define a generic sankey object.
    herits from TableObject.

    Parameters
    ----------
    :param tags: List of tags of this object.
    :type tags: list [_ProtoTag, ...]
    """

    def __init__(self):
        # Init parent class
        TableObject.__init__(self)
        # Init attributes
        self._tags = []
        self._taggs = []
        # List of tooltips
        self._tooltips = {}

    @property
    def tags(self):
        return self._tags

    @property
    def taggs(self):
        return self._taggs

    @property
    def tooltips(self):
        return self._tooltips

    def add_tooltip(self, name, description, content):
        self._tooltips[name] = _ProtoToolTip(
            name=name,
            description=description,
            content=content)

    def update_tooltip(self, name, **kwargs):
        self._tooltips[name].update(**kwargs)
