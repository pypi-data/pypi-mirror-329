"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for proto TagGroup class

"""

# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey_utils.table_object import TableObject
from SankeyExcelParser.sankey_utils.functions import _stdStr


# CLASS ----------------------------------------------------------------------------
class _ProtoTagGroup(TableObject):
    """
    Proto class for TagGroup
    Define a Tag Group object.

    Parameters
    ----------
    :param name: Name of the groupe (standardized)
    :type name: str

    :param name_unformatted: Name of the groupe (not standardized, as written by the user)
    :type name_unformatted: str

    :param tags: All tags contained by the group as dictionnary, with standardized tags name as entries.
    :type tags: dict = {str: Tag, ...}

    :param is_palette: Is the tag group a palette.
    :type is_palette: int

    :param colormap: Color map for tags colors.
    :type colormap: str

    :param color: Colors for each tags.
    :type color: str
    """

    def __init__(
        self,
        name: str,
        taggtype: str
    ):
        # Init parent class
        TableObject.__init__(self)
        # Init attributes
        self._name = _stdStr(name)
        self._name_unformatted = name
        self._type = taggtype
        self._tags = {}
        self._anti_tags = None
        self._antagonists_taggs = []
        self._is_palette = None
        self._colormap = None

    @property
    def name(self):
        return self._name

    @property
    def name_unformatted(self):
        return self._name_unformatted

    @property
    def type(self):
        return self._type

    @property
    def is_palette(self):
        return self._is_palette

    @is_palette.setter
    def is_palette(self, _):
        try:
            self._is_palette = int(_)
        except Exception:
            pass

    @property
    def has_palette(self):
        try:
            return (self._is_palette > 0)
        except Exception:
            return False

    @property
    def colormap(self):
        return self._colormap

    @colormap.setter
    def colormap(self, _):
        if type(_) is str:
            self._colormap = _
