"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for Data class

"""

# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey_utils.sankey_object import SankeyObject
from SankeyExcelParser.sankey_utils.protos.flux import _ProtoFlux
import SankeyExcelParser.io_excel_constants as CONST


# CLASS ----------------------------------------------------------------------------
class ProtoData(object):
    """
    Define Data simple object.

    Parameters
    ----------
    :param natural_unit: Unité naturelle de reference pour la donnée.
    :type natural_unit: str

    :param factor: Facteur de conversion
    :type factor: float

    :param source: source de la donnée.
    :type source: str

    :param hypothesis: Descriptions des hypothèes de données
    :type hypothesis: str
    """

    def __init__(
        self,
        **kwargs
    ):
        # Attributes
        self._natural_unit = None
        self._factor = None
        self._source = None
        self._hypothesis = None
        self.update(**kwargs)

    def update(
        self,
        **kwargs
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _set_as_int(
        self,
        key,
        value
    ):
        # None case
        if value is None:
            setattr(self, key, None)
            return
        # Real affectation
        try:
            value_as_int = int(value)
            setattr(self, key, value_as_int)
        except Exception:
            pass

    def _set_as_float(
        self,
        key,
        value
    ):
        # None case
        if value is None:
            setattr(self, key, None)
            return
        # Real affectation
        try:
            value_as_float = float(value)
            # NAN protection
            if (value_as_float != value_as_float):
                return
            setattr(self, key, value_as_float)
        except Exception:
            pass

    def _get_as_round_value(
        self,
        key,
        digits
    ):
        try:
            return round(getattr(self, key), digits)
        except Exception:
            return getattr(self, key)

    def _set_as_str(
        self,
        key,
        value
    ):
        # None case
        if value is None:
            setattr(self, key, None)
            return
        # Real affectation
        try:
            value_as_str = str(value)
            setattr(self, key, value_as_str)
        except Exception:
            pass

    @property
    def natural_unit(self):
        return self._natural_unit

    @natural_unit.setter
    def natural_unit(self, _):
        self._set_as_str('_natural_unit', _)

    @property
    def factor(self):
        return self._factor

    @factor.setter
    def factor(self, _):
        self._set_as_float('_factor', _)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, _):
        self._set_as_str('_source', _)

    @property
    def hypothesis(self):
        return self._hypothesis

    @hypothesis.setter
    def hypothesis(self, _):
        self._set_as_str('_hypothesis', _)


class DataMinMax(ProtoData):
    """
    Define Data constraint object.
    Inherits from ProtoData.

    Parameters
    ----------
    :param reference: Reference of the object on that the min max applies to.
    :param reference: Flux | Data

    :param min_val: Value that reference value must be superior to
    :type min_val: float

    :param min_quantity: Quantity that reference value must be superior to
    :type min_quantity: float

    :param max_val: Value that reference value must be inferior to
    :type max_val: float

    :param max_quantity: Quantity that reference value must be inferior to
    :type max_quantity: float
    """
    def __init__(
        self,
        reference,
        **kwargs
    ):
        # Attributes
        self._reference = reference
        self._min_val = None
        self._min_quantity = None
        self._max_val = None
        self._max_quantity = None
        # Init parent attributes
        ProtoData.__init__(self)
        # Update initial values
        self.update(**kwargs)

    @property
    def min_val(self):
        return self._min_val

    @min_val.setter
    def min_val(self, _):
        self._set_as_float('_min_val', _)

    @property
    def min_quantity(self):
        return self._min_quantity

    @min_quantity.setter
    def min_quantity(self, _):
        self._set_as_float('_min_quantity', _)

    @property
    def max_val(self):
        return self._max_val

    @max_val.setter
    def max_val(self, _):
        self._set_as_float('_max_val', _)

    @property
    def max_quantity(self):
        return self._max_quantity

    @max_quantity.setter
    def max_quantity(self, _):
        self._set_as_float('_max_quantity', _)

    def update_table(
        self,
        columns_datataggs_names: list,
        columns_fluxtaggs_names: list,
        extra_infos_names: list,
        table: list
    ):
        """
        Update a panda table with this data infos.
        The columns are organized as :

        2. Origin
        3. Destination
        4. All data tags (multiple columns) : for each column we have the respective tags or None
        5. All flux tags (multiple columns) : for each column we have the respective tags or None
        6. Min value
        7. Max value
        8. Min Quantity
        9. Max quantity
        10. Natural unit
        11. Factor
        12. Sources
        13. Hypothesis
        14. All remaining extra infos (if present, multiple columns)

        Parameters
        ----------
        :param columns_datataggs_names: List of tag groups for data tags columns
        :type columns_datataggs_names: list[str] | list[TagGroup]

        :param columns_fluxtaggs_names: List of tag groups for flux tags columns
        :type columns_fluxtaggs_names: list[str] | list[TagGroup]

        :param extra_infos_names: List of extra infos to search for extra infos columns
        :type extra_infos_names: list[str]

        :param table: Table (2D-list) where all infos will be added
        :type table: list (modified)

        """
        # Only for data with value
        if (self._min_val is None) and \
           (self._min_quantity is None) and \
           (self._max_val is None) and \
           (self._max_quantity is None):
            return
        # Create table line with corresponding data
        line = [
            self._reference.orig.name,
            self._reference.dest.name]
        # Get tags
        line += self._reference.get_tags_from_taggroups(
            columns_datataggs_names, return_names_instead_of_refs=True)
        line += self._reference.get_tags_from_taggroups(
            columns_fluxtaggs_names, return_names_instead_of_refs=True)
        # Create table line with corresponding data
        line += [
            self._min_val,
            self._max_val,
            self._min_quantity,
            self._max_quantity,
            self._natural_unit,
            self._factor,
            self._source,
            self._hypothesis]
        # Add extra info cols if needed
        for extra_info_name in extra_infos_names:
            if extra_info_name in self._reference.extra_infos.keys():
                line.append(self._reference.extra_infos[extra_info_name])
            else:
                line.append(None)
        # We can add it directly in the table
        table.append(line)


class DataConstraint(ProtoData):
    """
    Define Data constraint object.

    Parameters
    ----------
    :param reference: Reference of the object on that the constraint applies to.
    :param reference: Flux | Data

    :param eq: Value that reference value must be equal to
    :type eq: float

    :param ineq_inf: Value that reference value must be superior to
    :type ineq_inf: float

    :param ineq_sup: Value that reference value must be inferior to
    :type ineq_sup: float

    :param traduction: What the constraint value mean for the reference.
    :type traduction: str
    """
    def __init__(
        self,
        id,
        reference,
        **kwargs
    ):
        # Attributes
        self._id = -1
        self._set_as_int('_id', id)
        self._reference = reference
        self._eq = None
        self._ineq_inf = None
        self._ineq_sup = None
        self._traduction = None
        # Init parent attributes
        ProtoData.__init__(self)
        # Update initial values
        self.update(**kwargs)

    @property
    def id(self):
        return self._id

    @property
    def reference(self):
        return self._reference

    @property
    def eq(self):
        return self._eq

    @eq.setter
    def eq(self, _):
        self._set_as_float('_eq', _)

    @property
    def ineq_inf(self):
        return self._ineq_inf

    @ineq_inf.setter
    def ineq_inf(self, _):
        self._set_as_float('_ineq_inf', _)

    @property
    def ineq_sup(self):
        return self._ineq_sup

    @ineq_sup.setter
    def ineq_sup(self, _):
        self._set_as_float('_ineq_sup', _)

    @property
    def traduction(self):
        return self._traduction

    @traduction.setter
    def traduction(self, _):
        self._set_as_str('_traduction', _)

    def update_table(
        self,
        columns_datataggs_names: list,
        columns_fluxtaggs_names: list,
        extra_infos_names: list,
        table: list
    ):
        """
        Update a panda table with this data infos.
        The columns are organized as :

        1. Id
        2. Origin
        3. Destination
        4. All data tags (multiple columns) : for each column we have the respective tags or None
        5. All flux tags (multiple columns) : for each column we have the respective tags or None
        6. Eq
        7. Ineq inf
        8. Ineq sup
        9. traduction
        10. source
        11. hypothesis
        12. All remaining extra infos (if present, multiple columns)


        Parameters
        ----------
        :param columns_datataggs_names: List of tag groups for data tags columns
        :type columns_datataggs_names: list[str] | list[TagGroup]

        :param columns_fluxtaggs_names: List of tag groups for flux tags columns
        :type columns_fluxtaggs_names: list[str] | list[TagGroup]

        :param extra_infos_names: List of extra infos to search for extra infos columns
        :type extra_infos_names: list[str]

        :param table: Table (2D-list) where all infos will be added
        :type table: list[list] (modified)

        """
        # Only for data with value
        if (self._eq is None) and \
           (self._ineq_inf is None) and \
           (self._ineq_sup is None):
            return
        # Create table line with corresponding data
        line = [
            self._id,
            self._reference.orig.name,
            self._reference.dest.name]
        # Get tags
        line += self._reference.get_tags_from_taggroups(
            columns_datataggs_names, return_names_instead_of_refs=True)
        line += self._reference.get_tags_from_taggroups(
            columns_fluxtaggs_names, return_names_instead_of_refs=True)
        # Create table line with corresponding data
        line += [
            self._eq,
            self._ineq_inf,
            self._ineq_sup,
            self._traduction,
            self._source,
            self._hypothesis]
        # Add extra info cols if needed
        for extra_info_name in extra_infos_names:
            if extra_info_name in self._reference.extra_infos.keys():
                line.append(self._reference.extra_infos[extra_info_name])
            else:
                line.append(None)
        # We can add it directly in the table
        table.append(line)

    def get_as_dict(self):
        # Init output
        output = {}
        # Get values
        output['reference'] = {}
        if isinstance(self._reference, _ProtoFlux):
            output['reference']['orig'] = self.reference.orig.name
            output['reference']['dest'] = self.reference.dest.name
        if isinstance(self._reference, Data):
            output['reference']['orig'] = self.reference.flux.orig.name
            output['reference']['dest'] = self.reference.flux.dest.name
            output['tags'] = [
                [_.group.name, _.name]
                for _ in self.reference.tags]
        output['eq'] = self.eq
        output['ineq_inf'] = self.ineq_inf
        output['ineq_suo'] = self.ineq_sup
        return output


class Data(ProtoData, SankeyObject):
    """
    Define Data object.
    Inherits from `ProtoData` and `SankeyObject`

    Parameters
    ----------
    :param flux: Flux associé à la donnée.
    :type flux: Flux

    :param tags: list of tags associated to the data
    :type tags: list

    :param sigma: Ecart type (Incertitude de la donnée).
        L'incertitude porte sur les données. \
        Elle est soit renseignée par la source et recopiée ici, \
        soit renseignée de manière arbitraire par la personne faisant \
        l'AFM en fonction de la confiance dans les données présentées \
        par la source, selon la méthodologie décrite dans la première \
        feuille de cet Excel.
    :type sigma: float

    :param min: Borne inférieure de la valeur possible de la donnée. \
        Valeur obligatoire pour réaliser l'AFM.
    :type min: DataMinMax

    :param max: Borne supérieur de la valeur possible de la donnée. \
        Valeur obligatoire pour réaliser l'AFM.
    :type max: DataMinMax

    :param constraints: TODO
    :type constraints: dict

    :param alterego: If data, then alterego is the associated result and vice-versa
    :type alterego: Data
    """

    def __init__(
        self,
        **kwargs
    ):
        # Data values attributes
        self._value = None
        self._quantity = None
        # Flux attribute
        self._flux = None
        # Uncertainty attributes
        self._sigma = None
        self._min_max = DataMinMax(self)
        # Reconcilliation attributes
        self._constraints = {}
        self._alterego = None
        self._analysis_vector = []
        # Init super constructor
        ProtoData.__init__(self)
        SankeyObject.__init__(self)
        # Update all present attributes
        self.update(**kwargs)

    def update_unknown_only(
        self,
        **kwargs
    ):
        for key, value in kwargs.items():
            if getattr(self, key) is None:
                setattr(self, key, value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, _):
        self._set_as_float('_value', _)

    def value_rounded(self, _):
        return self._get_as_round_value('_value', _)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, _):
        self._set_as_float('_quantity', _)

    def quantity_rounded(self, _):
        return self._get_as_round_value('_quantity', _)

    @property
    def flux(self):
        return self._flux

    @flux.setter
    def flux(self, _):
        # None case
        if _ is None:
            self._flux = None
            return
        # Real affectation
        if isinstance(_, _ProtoFlux):
            self._flux = _

    @property
    def orig(self):
        return self.flux.orig

    @property
    def dest(self):
        return self.flux.dest

    @property
    def natural_unit(self):
        if (self._natural_unit is None) and (self._flux is not None):
            return self._flux.natural_unit
        return self._natural_unit

    @natural_unit.setter
    def natural_unit(self, _):
        self._set_as_str('_natural_unit', _)

    def natural_unit_rounded(self, _):
        return self._get_as_round_value('_natural_unit', _)

    @property
    def factor(self):
        if (self._factor is None) and (self._flux is not None):
            return self._flux.factor
        return self._factor

    @factor.setter
    def factor(self, _):
        self._set_as_float('_factor', _)

    def factor_rounded(self, _):
        return self._get_as_round_value('_factor', _)

    @property
    def sigma(self):
        if (self._sigma is not None):
            return self._sigma
        if (self._value is not None):
            return self._value*CONST.DEFAULT_SIGMA_RELATIVE
        return None

    @sigma.setter
    def sigma(self, _):
        self._set_as_float('_sigma', _)

    def sigma_rounded(self, _):
        return self._get_as_round_value('_sigma', _)

    @property
    def sigma_relative(self):
        if (self._value is not None):
            if (self._sigma is not None):
                if abs(self._value) > 0.0:
                    return self._sigma/self._value
                else:
                    return self._sigma
        return None

    @sigma_relative.setter
    def sigma_relative(self, _):
        if _ is None:
            _ = CONST.DEFAULT_SIGMA_RELATIVE
        try:
            self._set_as_float('_sigma', self._value*_)
        except Exception:
            pass

    def sigma_relative_rounded(self, _):
        return self._get_as_round_value('sigma_relative', _)

    @property
    def sigma_percent(self):
        if (self._value is not None):
            if (self._sigma is not None):
                if abs(self._value) > 0.0:
                    return (self._sigma/self._value)*100.0
                else:
                    return self._sigma*100.0
        return None

    @sigma_percent.setter
    def sigma_percent(self, _):
        if _ is None:
            _ = CONST.DEFAULT_SIGMA_PERCENT
        try:
            self._set_as_float('_sigma', _*self._value/100.0)
        except Exception:
            pass

    @property
    def min_max(self):
        return self._min_max

    @property
    def min_val(self):
        return self._min_max.min_val

    @min_val.setter
    def min_val(self, _):
        self._min_max.min_val = _

    @property
    def max_val(self):
        return self._min_max.max_val

    @max_val.setter
    def max_val(self, _):
        self._min_max.max_val = _

    @property
    def constraints(self):
        return self._constraints

    def add_constraint(self, id_constraint, **kwargs):
        # Create a new piece of constraint
        constraint = DataConstraint(id_constraint, self, **kwargs)
        # Update constraint for given id
        if id_constraint in self._constraints.keys():
            self._constraints[id_constraint].append(constraint)
        else:
            self._constraints[id_constraint] = [constraint]
        # Return constraint
        return constraint

    @property
    def alterego(self):
        return self._alterego

    @alterego.setter
    def alterego(self, _):
        if self._alterego is None:
            if isinstance(_, Data):
                self._alterego = _
                _.alterego = self
        else:
            # Reset alterego link
            if _ is None:
                old_alterego = self._alterego
                self._alterego = None
                old_alterego.altergo = None

    @property
    def analysis_vector(self):
        # Protection with copy
        return self._analysis_vector.copy()

    @analysis_vector.setter
    def analysis_vector(self, _):
        if isinstance(_, list):
            self._analysis_vector = _

    def update_table(
        self,
        columns_datataggs_names: list,
        columns_fluxtaggs_names: list,
        extra_infos_names: list,
        table: list,
        rounding_digits: int = 2,
        as_result: bool = False,
        table_for_analysis: list = None
    ):
        """
        Update a panda table with this data infos.

        Parameters
        ----------
        :param columns_datataggs_names: List of tag groups for data tags columns
        :type columns_datataggs_names: list[str] | list[TagGroup]

        :param columns_fluxtaggs_names: List of tag groups for flux tags columns
        :type columns_fluxtaggs_names: list[str] | list[TagGroup]

        :param extra_infos_names: List of extra infos to search for extra infos columns
        :type extra_infos_names: list[str]

        :param table: Table (2D-list) where all infos will be added
        :type table: list[list] (modified)

        :param rounding_digits: Rounding precision for floating values
        :type rounding digits: int (default=2)

        :param as_result: Table columns are differents if data is a result.
        :type as_result: bool (default=False)

        :param table_for_analysis: Table (2D-list) analysis can be updated if data is result
        :type table_for_analysis: list[list] (default=None)
        """
        if as_result is True:
            # Result table
            self._update_results_table(
                columns_datataggs_names,
                columns_fluxtaggs_names,
                table,
                rounding_digits=rounding_digits)
            # Analysis table if needed
            if table_for_analysis is not None:
                self._update_analysis_table(
                    columns_datataggs_names,
                    columns_fluxtaggs_names,
                    table_for_analysis,
                    rounding_digits=rounding_digits)
        else:
            self._update_data_table(
                columns_datataggs_names,
                columns_fluxtaggs_names,
                extra_infos_names,
                table,
                rounding_digits=rounding_digits)

    def _update_data_table(
        self,
        columns_datataggs_names: list,
        columns_fluxtaggs_names: list,
        extra_infos_names: list,
        table: list,
        rounding_digits: int = 2
    ):
        """
        Update a panda table with this data infos.
        The columns are organized as :

        1. Origin
        2. Destination
        3. All data tags (multiple columns) : for each column we have the respective tags or None
        4. All flux tags (multiple columns) : for each column we have the respective tags or None
        5. Value
        6. Quantity
        7. Natural unit
        8. factor
        9. Sigma relative to value
        10. source
        11. hypothesis
        12. All remaining extra infos (if present, multiple columns)

        Parameters
        ----------
        :param columns_datataggs_names: List of tag groups for data tags columns
        :type columns_datataggs_names: list[str] | list[TagGroup]

        :param columns_fluxtaggs_names: List of tag groups for flux tags columns
        :type columns_fluxtaggs_names: list[str] | list[TagGroup]

        :param extra_infos_names: List of extra infos to search for extra infos columns
        :type extra_infos_names: list[str]

        :param table: Table (2D-list) where all infos will be added
        :type table: list[list] (modified)

        """
        # Write only if we have something to write
        if (self.value is None) & (self.quantity is None):
            return
        # Create table line with corresponding data
        line = [
            self.orig.name,
            self.dest.name]
        # Get tags
        line += self.get_tags_from_taggroups(
            columns_datataggs_names, return_names_instead_of_refs=True)
        line += self.get_tags_from_taggroups(
            columns_fluxtaggs_names, return_names_instead_of_refs=True)
        # Create table line with corresponding data
        line += [
            self.value_rounded(rounding_digits),
            self.quantity_rounded(rounding_digits),
            self.natural_unit,
            self.factor_rounded(rounding_digits),
            self.sigma_relative_rounded(rounding_digits),
            self.source,
            self.hypothesis]
        # Add extra info cols if needed
        for extra_info_name in extra_infos_names:
            if extra_info_name in self.extra_infos.keys():
                line.append(self.extra_infos[extra_info_name])
            else:
                line.append(None)
        # We can add it directly in the table
        table.append(line)

    def _update_results_table(
        self,
        columns_datataggs_names: list,
        columns_fluxtaggs_names: list,
        table: list,
        rounding_digits: int = 2
    ):
        """
        Update a panda table with this data infos.
        The columns are organized as :

        1. Origin
        2. Destination
        3. All data tags (multiple columns) : for each column we have the respective tags or None
        4. All flux tags (multiple columns) : for each column we have the respective tags or None
        5. Value
        6. Free min
        7. Free max

        Parameters
        ----------
        :param columns_datataggs_names: List of tag groups for data tags columns
        :type columns_datataggs_names: list[str] | list[TagGroup]

        :param columns_fluxtaggs_names: List of tag groups for flux tags columns
        :type columns_fluxtaggs_names: list[str] | list[TagGroup]

        :param table: Table (2D-list) where all infos will be added
        :type table: list[list] (modified)

        """
        # Create table line with corresponding data
        line = [
            self.orig.name,
            self.dest.name]
        # Get tags
        line += self.get_tags_from_taggroups(
            columns_datataggs_names, return_names_instead_of_refs=True)
        line += self.get_tags_from_taggroups(
            columns_fluxtaggs_names, return_names_instead_of_refs=True)
        # Create table line with corresponding data
        line += [
            self.value_rounded(rounding_digits),
            self.min_val,
            self.max_val]
        # We can add it directly in the table
        table.append(line)

    def _update_analysis_table(
        self,
        columns_datataggs_names: list,
        columns_fluxtaggs_names: list,
        table: list,
        rounding_digits: int = 2
    ):
        """
        Update a panda table with this data infos.
        The columns are organized as :

        1. Origin
        2. Destination
        3. All data tags (multiple columns) : for each column we have the respective tags or None
        4. All flux tags (multiple columns) : for each column we have the respective tags or None
        5. Result Value
        6. Result Free min
        7. Result Free max
        8. Input Value
        9. Input Sigma
        10. Input relative Sigma (percent)
        11. Input min value
        12. Input max value
        13. Relative difference between Input and Result (relative to Input Sigma)
        14. Result classification = (Mesurée / Redondandes / Determinable / Indeterminable (libre))
        15+. Ai Matrix (if asked) = Liste de lignes dans lesquelles la donnée est
             impliquée dans la matrice de contrainte.

        Parameters
        ----------
        :param columns_datataggs_names: List of tag groups for data tags columns
        :type columns_datataggs_names: list[str] | list[TagGroup]

        :param columns_fluxtaggs_names: List of tag groups for flux tags columns
        :type columns_fluxtaggs_names: list[str] | list[TagGroup]

        :param table: Table (2D-list) where all infos will be added
        :type table: list[list] (modified)

        """
        # Only if we have something to put inside
        if (len(self._analysis_vector) > 0):
            # Create table line with corresponding data
            line = [
                self.orig.name,
                self.dest.name]
            # Get tags
            line += self.get_tags_from_taggroups(
                columns_datataggs_names, return_names_instead_of_refs=True)
            line += self.get_tags_from_taggroups(
                columns_fluxtaggs_names, return_names_instead_of_refs=True)
            # Create table line with corresponding result data
            line += [
                self.value_rounded(rounding_digits),
                self.min_val,
                self.max_val]
            # Create table line with corresponding analysis data
            line += [
                round(_, rounding_digits)
                if isinstance(_, float)
                else _
                for _ in self._analysis_vector]
            # We can add it directly in the table
            table.append(line)

    def get_as_dict(self):
        # Init output
        output = {}
        # Get values
        output['value'] = self.value
        output['tags'] = [
            [_.group.name, _.name] for _ in self.tags]
        try:
            output['alterego'] = self.alterego.value
        except Exception:
            pass
        return output

    def __repr__(self):
        s = '{}'.format(self._value)
        for tag in self._tags:
            s += ' | {}'.format(tag)
        return s


def MCData(SankeyObject):
    """
    Define a MonteCarlo Data object.
    Inherits from `SankeyObject`

    Parameters
    ----------
    :param flux: Flux associé à la donnée.
    :type flux: Flux

    :param tags: list of tags associated to the data
    :type tags: list

    :param starting_data: Input data
    :type starting_data: Data

    :param result_data: Output data
    :type result_data: Data
    """

    def __init__(
        self,
        **kwargs
    ):
        # Flux attribute
        self._flux = None
        # Input and output data
        self._starting_data = None
        self._result_data = None
        # Probalities and histogrammes
        self._probas = {}
        self._hists = {}
        # Update all present attributes
        self.update(**kwargs)

    def update(
        self,
        **kwargs
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def flux(self):
        return self._flux

    @flux.setter
    def flux(self, _):
        # None case
        if _ is None:
            self._flux = None
            return
        # Real affectation
        if isinstance(_, _ProtoFlux):
            self._flux = _

    @property
    def starting_data(self):
        return self._starting_data

    @starting_data.setter
    def starting_data(self, _):
        # None case
        if _ is None:
            self._starting_data = None
            return
        # Real affectation
        if isinstance(_, Data):
            self._starting_data = _

    @property
    def result_data(self):
        return self._result_data

    @result_data.setter
    def result_data(self, _):
        # None case
        if _ is None:
            self._result_data = None
            return
        # Real affectation
        if isinstance(_, Data):
            self._result_data = _

    @property
    def min(self):
        return self._result_data.min_val

    @min.setter
    def min(self, _):
        self._result_data.min_val = _

    @property
    def max(self):
        return self._result_data.max_val

    @max.setter
    def max(self, _):
        self._result_data.max_val = _

    def add_proba(self, _key, _value):
        if (_key is not None):
            try:
                value = float(_value)
                key = str(_key)
                # NAN protection
                if (value == value):
                    self._probas[key] = value
            except Exception:
                pass

    def get_proba(self, _key):
        if (_key is not None):
            try:
                key = str(_key)
                return self._probas[key]
            except Exception:
                pass
        return None

    def add_hist(self, _key, _value):
        if (_key is not None):
            try:
                value = float(_value)
                key = str(_key)
                # NAN protection
                if (value == value):
                    self._hists[key] = value
            except Exception:
                pass

    def get_hist(self, _key):
        if (_key is not None):
            try:
                key = str(_key)
                return self._hists[key]
            except Exception:
                pass
        return None
