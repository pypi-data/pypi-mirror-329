"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for Tag class

"""


# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey_utils.tag_group import _ProtoTagGroup
from SankeyExcelParser.sankey_utils.sankey_object import _ProtoSankeyObject
from SankeyExcelParser.sankey_utils.functions import _stdStr, _convertColorToHex


# CLASS ----------------------------------------------------------------------------
class Tag(object):
    """
    Define any Tag.

    Parameters
    ----------
    :param name: name of the Tag
    :type name: str

    :param group: Reference to the tag group from which the tag belongs to.
    :type group: _ProtoTagGroup

    :param references: Sankey object linked to the tag.
    :type references: list [SankeyObject, ...]
    """

    def __init__(
        self,
        name: str,
        group: _ProtoTagGroup
    ):
        # Default values
        self._name = _stdStr(name)
        self._name_unformatted = name.strip().replace('.0', '')
        self._color = ''
        self._group = group
        self._references = []

    @property
    def name(self):
        return self._name

    @property
    def name_unformatted(self):
        return self._name_unformatted

    @property
    def color(self):
        return self._color

    @property
    def color_in_hex(self):
        return _convertColorToHex(self._color)

    @color.setter
    def color(self, _):
        if type(_) is str:
            self._color = _

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, _):
        if isinstance(_, _ProtoTagGroup):
            self._group = _

    @property
    def references(self):
        return self._references.copy()

    def add_reference(
        self,
        ref: _ProtoSankeyObject
    ):
        self._references.append(ref)

    def __repr__(self):
        """
        Gives a string representation of Tag object.

        Returns
        -------
        :return: String format of self.
        :rtype: str
        """
        s = '{}'.format(self.name_unformatted)
        return s
