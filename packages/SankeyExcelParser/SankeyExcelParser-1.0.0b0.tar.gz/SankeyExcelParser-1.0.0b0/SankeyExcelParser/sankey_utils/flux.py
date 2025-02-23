"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for Flux class

"""

# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey_utils.protos.flux import _ProtoFlux
from SankeyExcelParser.sankey_utils.data import Data
from SankeyExcelParser.sankey_utils.data import DataConstraint
from SankeyExcelParser.sankey_utils.data import DataMinMax
from SankeyExcelParser.sankey_utils.data import MCData
from SankeyExcelParser.sankey_utils.node import Node


# CLASS ----------------------------------------------------------------------------
class Flux(_ProtoFlux):
    """
    Define a flux.
    Inherits from `_ProtoFlux`

    Parameters
    ----------
    :param orig: Flux starting node
    :type orig: Node

    :param dest: Flux ending node
    :type dest: Node

    :param datas: All datas for the flux
    :type datas: list [Data, ...]

    :param results: All results for the flux
    :type results: list [Data, ...]
    """

    def __init__(
        self,
        orig: Node,
        dest: Node,
        **kwargs
    ):
        # Init super constructor
        _ProtoFlux.__init__(self, orig, dest)
        self._orig.add_output_flux(self)
        self._dest.add_input_flux(self)
        # Datas
        self._datatags_combinations = []
        self._datas = []
        self._results = []
        self._monte_carlo = None
        # Init contraints values for all datas
        self._min_max = DataMinMax(self)
        self._max = None
        self._constraints = {}
        # Update values
        self.update(**kwargs)

    def update(
        self,
        **kwargs
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def datas(self):
        return self._datas

    def add_data(self, _):
        if type(_) is float:
            data = Data(value=_)
            self._datas.append(data)
            data.flux = self
            return
        if type(_) is Data:
            self._datas.append(_)
            _.flux = self
            return

    def has_data(self):
        return len(self._datas) > 0

    def instanciate_all_datas(
        self,
        data_taggs={}
    ):
        """
        Create data according to data tags presents in a table line.
        Data can only have one tag for every given data tag group.
        If multiple tag are given, then we must create one data for each one and link them
        to the reference flux.

        Parameters
        ----------
        :param data_taggs: List of data tags
        :type data_taggs: dict as {key=TagGroup.name: value=TagGroup, ...} . (default={})

        Returns
        -------
        :return: List of created datas
        :rtype: list as [Data, ...]
        """
        # If no data tag -> Create only one data
        if len(data_taggs) == 0:
            # Add only one data
            self.add_data(Data())
            # Add empty datatags combinations
            self._datatags_combinations.append([])
            return
        # Otherwise create data recursivly
        self._recursive_instanciate_all_datas(
            [list(_.tags.values()) for _ in data_taggs.values()])

    def _recursive_instanciate_all_datas(
        self,
        data_tags_per_tagg,
        data_tags_per_datas=[[]]
    ):
        """
        Create data recursivly according to data tags presents in a table line.
        Data can only have one tag for every given data tag group.
        If multiple tag are given, then we must create one data for each one and link them
        to the reference flux.

        Parameters
        ----------
        :param data_tags_per_tagg: List of data tags regrouped per data tag groups.
        :type data_tags_per_tagg: list as [list as [Tag, ...], ...]

        :param data_tags_per_datas: Must not be touch. Used for recursivity
        :type data_tags_per_datas: list (default=[[]])

        Returns
        -------
        :return: List of created datas
        :rtype: list as [Data, ...]
        """
        # Check if we arrived at the end of recursivity on data tags
        if len(data_tags_per_tagg) == 0:
            # Create unique data for each data tag per data tag groups
            for data_tags in data_tags_per_datas:
                # Create Data
                data = Data()
                # Add tags
                for data_tag in data_tags:
                    data.add_tag(data_tag)
                # Add data to flux
                self.add_data(data)
                # Save data_tags_per_datas as keys
                self._datatags_combinations.append(data_tags.copy())
        # Otherwise we continue to recurse
        else:
            # Get data tags related to datas to create and to a unique data tag group
            data_tags = data_tags_per_tagg.pop()
            # Create the list of unique data tags for each data
            all_data_tags_per_datas = []
            for data_tag in data_tags:
                # data_tags_per_datas = [[tag1_1, tag2_1], [tag1_1, tag2_2], [tag1_2, tag2_1], ...]
                # with data tag group 1 = (tag1_1, tag1_2)
                #      data tag group 2 = (tag2_1, tag2_2)
                # So, if we have data tag group 3 = (tag3_1, tag3_2, ...)
                # we must copy each list from data_tags_per_datas and append tag3_1
                # then make anothers copies to append tag3_2, etc.
                new_data_tags_per_datas = []
                for data_tags_per_data in data_tags_per_datas:
                    new_data_tags_per_data = data_tags_per_data.copy()
                    new_data_tags_per_data.append(data_tag)
                    new_data_tags_per_datas.append(new_data_tags_per_data)
                all_data_tags_per_datas += new_data_tags_per_datas
            # We recurse to deal with data tag groups
            self._recursive_instanciate_all_datas(
                data_tags_per_tagg,
                data_tags_per_datas=all_data_tags_per_datas)

    def get_corresponding_datas_from_tags(
        self,
        datatags_to_match,
        fluxtags_to_match=[]
    ):
        """
        Get a list of data that correspond to the input list of tags

        Parameters
        ----------
        :param tags: list of tags to check
        :type tags: list[Tag, ...]

        Returns
        -------
        :return: List of corresponding datas
        :rtype: list[Data, ...]
        """
        # Init list of matched datas
        matched_datas = []
        # Match // datatags
        for datatags, data in zip(self._datatags_combinations, self._datas):
            ok_match_datatags = False
            # If all current datatags are contained in datatags to match list
            if set(datatags_to_match).issuperset(set(datatags)):
                ok_match_datatags = True
            # If all datatags to match are contained in current datatags list
            if set(datatags).issuperset(set(datatags_to_match)):
                ok_match_datatags = True
            # Check flux tags also
            if ok_match_datatags:
                # If flux tags are related to curren data
                if set(data.tags).issuperset(set(fluxtags_to_match)):
                    matched_datas.append(data)
        # Output
        return matched_datas

    @property
    def results(self):
        return self._results

    def add_result(self, _):
        if type(_) is float:
            result = Data(value=_)
            self._results.append(result)
            result.flux = self
            return
        if type(_) is Data:
            self._results.append(_)
            _.flux = self
            return

    def has_result(self):
        return len(self._results) > 0

    def reset_results(self):
        # remove altergo links with datas
        for result in self._results:
            result.alterego = None
        # Empty list
        self._results = []

    def get_corresponding_results_from_tags(self, tags):
        """
        Get a list of data that correspond to the input list of tags

        Parameters
        ----------
        :param tag: tag
        :type tag: str | Tag

        Returns
        -------
        :return: Corresponding data if it exist, else None
        :rtype: Data | None
        """
        results = set(self._results)
        for tag in tags:
            results &= set(tag.references)
        return list(results)

    @property
    def monte_carlo(self):
        return self._monte_carlo

    def add_monte_carlo(
        self,
        starting_mean_value,
        starting_sigma,
        result_mean_value,
        result_sigma,
        result_min,
        result_max
    ):
        self._monte_carlo = MCData(flux=self)
        self._monte_carlo.starting_data = Data(
            value=starting_mean_value,
            sigma=starting_sigma)
        self._monte_carlo.result_data = Data(
            value=result_mean_value,
            sigma=result_sigma)
        self._monte_carlo.min = result_min
        self._monte_carlo.max = result_max

    @property
    def min_max(self):
        return self._min_max

    @property
    def min(self):
        return self._min_max.min_val

    @min.setter
    def min(self, _):
        self._min_max.min = _

    @property
    def max(self):
        return self._min_max.max_val

    @max.setter
    def max(self, _):
        self._min_max.max = _

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

    def get_as_dict(self):
        # Init output
        output = {}
        # Get values
        output['orig'] = self.orig.name
        output['dest'] = self.dest.name
        output['datas'] = []
        for data in self.datas:
            output['datas'].append(data.get_as_dict())
        return output

    def __repr__(self):
        if self.has_data():
            if len(self.datas) > 1:
                return '{0} --- [{2}, ...] ---> {1}'.format(
                    self._orig.name,
                    self._dest.name,
                    self.datas[0])
            else:
                return '{0} --- {2} ---> {1}'.format(
                    self._orig.name,
                    self._dest.name,
                    self.datas[0])
        else:
            return '{0} --- {2} ---> {1}'.format(
                self._orig.name,
                self._dest.name,
                'No data')
