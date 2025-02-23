"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for proto Flux class

"""

# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey_utils.sankey_object import SankeyObject
from SankeyExcelParser.sankey_utils.protos.node import _ProtoNode


# CLASS ----------------------------------------------------------------------------
class _ProtoFlux(SankeyObject):
    """
    Define a prototype for flux object.
    Does nothing except defining attributes.
    Inherits from `SankeyObject`

    Parameters
    ----------
    :param id: Flux id (standardized))
    :type id: str

    :param orig: Flux starting node
    :type orig: _ProtoNode

    :param dest: Flux ending node
    :type dest: _ProtoNode

    :param datas: All datas for the flux
    :type datas: list [Data, ...]

    :param results: All datas (as results) for the flux
    :type results: list [Data, ...]
    """

    def __init__(
        self,
        orig: _ProtoNode,
        dest: _ProtoNode,
        **kwargs
    ):
        # Init super constructor
        SankeyObject.__init__(self)
        # Create attributs
        self._id = orig.id+'---'+dest.id
        self._orig = orig
        self._dest = dest

    @property
    def id(self):
        return self._id

    @property
    def orig(self):
        return self._orig

    @property
    def dest(self):
        return self._dest

    @property
    def natural_unit(self):
        return self._orig.get_natural_unit()

    @natural_unit.setter
    def natural_unit(self, _):
        # Unit apply only to origin
        self._orig._add_natural_unit(_)

    @property
    def factor(self):
        return self._orig.get_factor()

    @factor.setter
    def factor(self, _):
        # Unit apply only to origin
        self._orig.add_factor(_)

    @property
    def tooltips(self):
        return self._orig.tooltips
