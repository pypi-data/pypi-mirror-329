"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for Node class

"""

# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey_utils.protos.flux import _ProtoFlux
from SankeyExcelParser.sankey_utils.protos.node import _ProtoNode


# CLASS ----------------------------------------------------------------------------
class Node(_ProtoNode):
    """
    Define a node object.
    Inherits from `_ProtoNode`, but add methods to deal with other Nodes.
    """

    def __init__(
        self,
        name: str,
        level: int,
        **kwargs
    ):
        # Init super
        _ProtoNode.__init__(self, name, level)
        # Add constructor values
        self.update(**kwargs)

    def update(
        self,
        **kwargs
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def children_ids(self):
        if not self.has_at_least_one_child():
            return [[]]
        return [[_.id for _ in grp] for grp in self._children_grps if len(grp) > 0]

    @property
    def parents_ids(self):
        return [_.id for _ in self._parents]

    def add_child(self, node: _ProtoNode, childrengrp_id: int = -1):
        """
        Add child to a children list.

        Parameters
        ----------
        :param node: Child node to add.
        :type node: _ProtoNode

        :param childrengrp_id: Children group in which we should add child to.
        :type childrengrp_id: int, optionnal (default=-1)
        """
        # Verify that we don't already have that child
        # Add new groupe
        if self._create_new_children_grp:
            self._children_grps.append([])
            self._create_new_children_grp = False
        # Secure childgroup index
        if childrengrp_id > 0:
            while childrengrp_id >= len(self._children_grps):
                self._children_grps.append([])
        # Protection
        if node not in self._children_grps[childrengrp_id]:
            # Add child
            self._children_grps[childrengrp_id].append(node)
            # Add self to child's parent
            node._add_parent(self)

    def create_new_children_group(self):
        self._create_new_children_grp = True

    def has_at_least_one_child(self):
        for _ in self._children_grps:
            if len(_) > 0:
                return True
        return False

    def is_child_of_given_node(self, node: _ProtoNode):
        return (self in node.parents)

    def get_set_of_all_base_children(self):
        if self.has_at_least_one_child():
            children_set = set()
            for children_grp in self._children_grps:
                for child in children_grp:
                    children_set |= child.get_set_of_all_base_children()
            return children_set
        return set([self])

    def autocompute_level_and_children_levels(self, min_level=1):
        """
        Autocompute level based on parenthood leveling.
        Returns max level that has been reached from children.
        """
        # Update own level
        self._level = max(self._level, min_level)
        # Init max level value
        max_level = self._level
        # Update sub-levels
        for children_grp in self._children_grps:
            # Secure: Start from a common min level for given children grp
            min_children_level = min_level + 1
            for child in children_grp:
                min_children_level = max(child.level, min_children_level)
            # Propagate level computing
            for child in children_grp:
                max_children_level = \
                    child.autocompute_level_and_children_levels(min_level=min_children_level)
                max_level = max(max_children_level, max_level)
        # Return max level
        return max_level

    def _add_parent(self, node: _ProtoNode):
        """
        Add parent.

        Parameters
        ----------
        :param node: Parent node to add.
        :type node: _ProtoNode
        """
        if node not in self._parents:
            self._parents.append(node)

    def has_parents(self):
        return len(self._parents) > 0

    def is_parent_of_given_node(self, node: _ProtoNode):
        return node.is_child_of_given_node(self)

    def add_input_flux(self, flux: _ProtoFlux):
        self._input_flux.append(flux)

    def add_output_flux(self, flux: _ProtoFlux):
        self._output_flux.append(flux)

    def get_flux_from_given_node(self, node: _ProtoNode):
        """
        Return the flux node->self

        Parameters
        ----------
        :param node: Node where flux must arrive from
        :type node: _ProtoNode

        Returns
        -------
        :return: Flux that as been ask if found, otherwise None
        :rtype: _ProtoFlux | None
        """
        for flux in self._input_flux:
            if flux.orig == node:
                return flux
        return None

    def get_flux_to_given_node(self, node: _ProtoNode):
        """
        Return the flux self->node

        Parameters
        ----------
        :param node: Node where flux must go to
        :type node: _ProtoNode

        Returns
        -------
        :return: Flux that as been ask if found, otherwise None
        :rtype: _ProtoFlux | None
        """
        for flux in self._output_flux:
            if flux.dest == node:
                return flux
        return None

    def update_table(
        self,
        level: int,
        taggs_names: list,
        extra_infos_names: list,
        lineages_processed: list,
        lineages_tables: list,
        current_lineage_table: list,
        lineages_entries,
        current_lineage_entries,
        lineages_entries__levels,
        current_lineage_entries__levels
    ):
        """
        Update a panda table with this node infos.
        The columns are organized as :

        1. Level
        2. Name
        3. Mat balance
        4. Color
        5. All node tags (multiple columns) : for each column we have the respective tags or None
        6. Definition
        14. All remaining extra infos (if present, multiple columns)

        Parameters
        ----------
        :param level: Level that will be indicated on table for the node.
            Can be different form actual level because of multiplicity of parents
        :type level: int

        :param taggs_names: List of tag groups for node tags columns
        :type taggs_names: list[str] | list[TagGroup]

        :param extra_infos_names: List of extra infos to search for extra infos columns
        :type extra_infos_names: list[str]

        :param lineages_processed: List of children grp that have already been added to table
        :type lineages_processed: list[list[Node]] (modified)

        :param lineages_tables: List of all tables (2-D list) of all possible lineages of nodes
        :type lineages_tables: list[list[list[str]]] (modified)

        :param current_lineage_table: Table (2-D list) containing infos of all current lineage related nodes
        :type current_lineage_table: list[list[str]] (modified)

        :param lineages_entries:
            List of all lists of nodes that have been added to lineages_tables.
            Used to colorize table.
        :type lineages_entries: list[list[Node]] (modified)

        :param current_lineage_entries:
            List of nodes that have been added to current_lineage_table.
            Used to colorize table.
        :type current_lineage_entries: list[Node] (modified)

        :param lineages_entries__level:
            List of all lists of nodes' levels that have been added to lineages_tables.
            Used to colorize table.
        :type lineages_entries: list[list[int]] (modified)

        :param current_lineage_entries__level:
            List of nodes' levels that have been added to current_lineage_table.
            Used to colorize table.
        :type current_lineage_entries: list[int] (modified)
        """
        # Create table line with corresponding data for self
        line_node = [
            level,
            self.name,
            self.mat_balance,
            self.color]
        # Add tags
        line_node += self.get_tags_from_taggroups(
            taggs_names, return_names_instead_of_refs=True)
        # Add definition
        line_node.append(self.definition)
        # Add extra info cols if needed
        for extra_info_name in extra_infos_names:
            if extra_info_name in self.extra_infos.keys():
                line_node.append(self.extra_infos[extra_info_name])
            else:
                line_node.append(None)
        # Add line to the table
        current_lineage_table.append(line_node)
        current_lineage_entries.append(self)
        current_lineage_entries__levels.append(level)
        # If we have children for this node, we add them directly under
        if self.has_at_least_one_child():
            main_lineages_processed = False
            # I do not pass by decorator here, because I need the pointer to childgroup for lineages_processed
            for childgroup in self._children_grps:
                # Pass already processed lineage
                if childgroup in lineages_processed:
                    continue
                # Recursively process children for main lineage (first children grp)
                if not main_lineages_processed:
                    for child in childgroup:
                        child.update_table(
                            level+1,
                            taggs_names,
                            extra_infos_names,
                            lineages_processed,
                            lineages_tables,
                            current_lineage_table,
                            lineages_entries,
                            current_lineage_entries,
                            lineages_entries__levels,
                            current_lineage_entries__levels)
                        main_lineages_processed = True
                else:
                    if len(childgroup) > 0:  # Protection
                        # Start a new lineage (from level = 1)
                        new_line_node = line_node.copy()
                        new_line_node[0] = 1
                        new_lineage_table = [new_line_node]
                        lineages_tables.append(new_lineage_table)
                        # Update list of level / nodes for table colorization
                        new_lineage_entries = [self]
                        new_lineage_entries__levels = [1]
                        lineages_entries.append(new_lineage_entries)
                        lineages_entries__levels.append(new_lineage_entries__levels)
                        # Recursively process children for new lineage
                        for child in childgroup:
                            child.update_table(
                                2,
                                taggs_names,
                                extra_infos_names,
                                lineages_processed,
                                lineages_tables,
                                new_lineage_table,
                                lineages_entries,
                                new_lineage_entries,
                                lineages_entries__levels,
                                new_lineage_entries__levels)
                lineages_processed.append(childgroup)

    def get_as_dict(self):
        # Init output
        output = {}
        # Get values
        output['name'] = self.name
        output['tags'] = [
            [_.group.name, _.name] for _ in self.tags]
        output['parents'] = [_.name for _ in self.parents]
        output['childrens'] = \
            [[_.name for _ in grp]
             for grp in self.children_grps]
        output['mat_balance'] = self.mat_balance
        output['color'] = self.color
        output['definition'] = self.definition
        return output

    def __repr__(self):
        s = '{}'.format(self._name)
        for tag in self._tags:
            s += ' | {}'.format(tag)
        return s
