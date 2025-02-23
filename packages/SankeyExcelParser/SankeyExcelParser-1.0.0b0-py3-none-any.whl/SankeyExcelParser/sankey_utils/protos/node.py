"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for proto Node class

"""

# External libs ---------------------------------------------------------------
import re

# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey_utils.sankey_object import SankeyObject
from SankeyExcelParser.sankey_utils.functions import _stdStr, _convertColorToHex


# CLASS ----------------------------------------------------------------------------
LOCALISATION_OPTIONS = {
    'Local': ['locale?', 'domestique'],
    'Echange': ['echanges?']}


class _ProtoNodeUnit(object):
    """
    Define unit for a data object
    """

    def __init__(
        self,
        **kwargs
    ):
        self._natural_unit = None
        self._equivalent_unit = None
        self._equivalent_to_natural = None
        self._natural_to_equivalent = None
        self._other_conversions = {}
        self.update(**kwargs)

    def update(
        self,
        **kwargs
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def natural_unit(self):
        return self._natural_unit

    @natural_unit.setter
    def natural_unit(self, _):
        # None case
        if _ is None:
            self._natural_unit = None
            return
        # Real affectation
        try:
            self._natural_unit = str(_)
        except Exception:
            pass

    @property
    def equivalent_unit(self):
        return self._equivalent_unit

    @property
    def equivalent_to_natural(self):
        return self._equivalent_to_natural

    @property
    def natural_to_equivalent(self):
        return self._natural_to_equivalent

    @natural_to_equivalent.setter
    def natural_to_equivalent(self, _):
        # None case
        if _ is None:
            self._natural_to_equivalent = None
            return
        # Real affectation
        try:
            self._natural_to_equivalent = float(_)
            # TODO: div 0 protection ? Or enough with try ?
            self._equivalent_to_natural = (1.0/self._natural_to_equivalent)
        except Exception:
            pass

    @property
    def other_conversions(self):
        return self._other_conversions

    def add_other_conversion(self, name, value):
        try:
            f_value = float(value)
            s_name = str(name)
            # NAN protection
            if (f_value != f_value):
                return
            self._other_conversions[s_name] = f_value
        except Exception:
            pass


class _ProtoNode(SankeyObject):
    """
    Define a prototype for node object.
    Does nothing except defining attributes.
    Inherits from `SankeyObject`

    Parameters
    ----------

    :param id: Node id (standardized)
    :type id: str

    :param name: Node name (not standardized, as set by the user)
    :type name: str

    :param level: Parenthood level of the node.
                  1=Node without parents,
                  2+: Node with parents, ...
    :type level: int

    :param type: parenthood relationships
                 'SR': Single root,
                 'PR': parent root,
                 'BC': base child,
                 'PC': parent child
    :type level: str

    :param parents: Lists the parent nodes of the 'self' node.
    :type parents: list [Node, ...]

    :param children_grps: Lists the groups of child nodes of the 'self' node.
    :type children_grps: list [list[Node, ...], ...]

    :param input_flux: List of all flux that arrive to this node.
    :type input_flux: list [Flux, ...]

    :param output_flux: List of all flux that depart from this node.
    :type output_flux: list [Flux, ...]

    :param mat_balance: Do we respect or not of the matter balance.
                        1: matter balance is respected,
                        0: not respected.
    :type mat_balance: int

    :param color: Color applied to the node on application
    :type color: str

    :param definition: Node definition
    :type definition: str
    """

    def __init__(
        self,
        name: str,
        level: int,
        **kwargs
    ):
        # Init super
        SankeyObject.__init__(self)
        # Id : keep only lower alphanumeric + spaces replaced with "_"
        self._id = re.sub(r'[^a-z0-9 ]', '', _stdStr(name))\
            .title().replace(' ', '')
        # Init default value
        self._name = name
        self._level = level
        # Parents & children
        self._type = None
        self._parents = []
        self._children_grps = [[]]
        self._create_new_children_grp = False
        # Flux
        self._input_flux = []
        self._output_flux = []
        # MFA
        self._unit = {}
        self._mat_balance = None
        # Display on OpenSankey
        self._color = None
        self._definition = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, _):
        try:
            self._level = max(1, int(_))
        except Exception:
            pass

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _):
        if isinstance(_, str):
            upper_ = _.upper()
            if upper_ in ['SR', 'PR', 'BC', 'PC']:
                self._type = upper_

    @property
    def mat_balance(self):
        return self._mat_balance

    @mat_balance.setter
    def mat_balance(self, _):
        try:
            self._mat_balance = int(_)
        except Exception:
            pass

    @property
    def color(self):
        return self._color

    @property
    def color_in_hex(self):
        return _convertColorToHex(self._color, default_color='#808080')  # Grey by default

    @color.setter
    def color(self, _):
        if type(_) is str:
            if len(_) > 0:
                self._color = _

    @property
    def definition(self):
        return self._definition

    @definition.setter
    def definition(self, _):
        if type(_) is str:
            self._definition = None
            if len(_) > 0:
                self._definition = _
            return
        if _ is None:
            self._definition = None

    @property
    def parents(self):
        return self._parents.copy()

    def get_all_parents(self, limit=-1):
        # if limit < 0, output = all existing parent, grand-parents, grand-grand-parents, etc...
        if limit < 0:
            if len(self._parents) == 0:
                return []
            else:
                all_parents = self._parents.copy()  # Beware modifying references
                for parent in self._parents:
                    all_parents += parent.get_all_parents()
                return all_parents
        # if limit = 0, output = current node parents
        # if limit = 1, output = current node parents + grand-parents
        # if limit = 2, outpur = current node parents + grand-parents + grand-grand-parents
        # etc...
        elif limit == 0:
            return self._parents
        else:
            all_parents = self._parents.copy()
            for parent in self._parents:
                all_parents += parent.get_all_parents(limit=limit-1)
            return all_parents

    @property
    def children_grps(self):
        return [_.copy() for _ in self._children_grps]

    def get_brothers_grps(self):
        """
        Return dict of list of brothers nodes, ie nodes that share the same parent as self.
        Brothers are referenced by their shared parents

        Returns
        -------
        :return: Groups of existing brothers per parents
        :rtype: list[ list[bro1, bro2, ...], ... ]
        """
        brothers = []
        # No parents -> No brothers
        if len(self.parents) == 0:
            return brothers
        # There are parents
        for parent in self.parents:
            for grp in parent.children_grps:
                # Parent can have children grp where self does not belong
                if self in grp:
                    # Remove self from brothers
                    grp.remove(self)  # Safe : With children_grps setter, grp is a copy
                    brothers.append(grp)
        return brothers

    @property
    def input_flux(self):
        return self._input_flux.copy()

    @property
    def output_flux(self):
        return self._output_flux.copy()

    @property
    def unit(self):
        return self._unit

    @property
    def has_unit(self):
        return len(self._unit) > 0

    @property
    def unit_localisation(self):
        return list(self._unit.keys())

    def get_natural_unit(self, localisation=None):
        try:
            if localisation is None:
                return self._unit[self.unit_localisation[0]].natural_unit
            else:
                return self._unit[localisation].natural_unit
        except Exception:
            pass
        return None

    def add_natural_unit(self, _, localisation='Local'):
        if localisation is not None:
            if localisation in self._unit.keys():
                self._unit[localisation].natural_unit = _
            else:
                self._unit[localisation] = _ProtoNodeUnit(natural_unit=_)

    def get_factor(self, localisation=None):
        try:
            if localisation is None:
                return self._unit[self.unit_localisation[0]].natural_to_equivalent
            else:
                return self._unit[localisation].natural_to_equivalent
        except Exception:
            pass
        return None

    def add_factor(self, _, localisation='Local'):
        if localisation is not None:
            if localisation in self._unit.keys():
                self._unit[localisation].natural_to_equivalent = _
            else:
                self._unit[localisation] = _ProtoNodeUnit(natural_to_equivalent=_)

    def get_other_factors(self, localisation=None):
        try:
            if localisation is None:
                return self._unit[self.unit_localisation[0]].other_conversions
            else:
                return self._unit[localisation].other_conversions
        except Exception:
            pass
        return None

    def add_other_factor(self, name, factor, localisation='Local'):
        if localisation is not None:
            if localisation not in self._unit.keys():
                self._unit[localisation] = _ProtoNodeUnit()
            self._unit[localisation].add_other_conversion(name, factor)

    def match_localisation(self, _):
        try:
            localisation = str(_)
            for localisation_option, localisation_res in LOCALISATION_OPTIONS.items():
                for localisation_re in localisation_res:
                    if re.fullmatch(localisation_re, _stdStr(localisation)):
                        return localisation_option
        except Exception:
            pass
        return None
