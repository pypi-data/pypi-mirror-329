"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for sankey proto class

"""


# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey_utils.protos.sankey_object import _ProtoSankeyObject
from SankeyExcelParser.sankey_utils.tag_group import TagGroup
from SankeyExcelParser.sankey_utils.tag import Tag
from SankeyExcelParser.sankey_utils.functions import _stdStr


# CLASS ----------------------------------------------------------------------------
class SankeyObject(_ProtoSankeyObject):
    """
    Define a generic sankey object.
    Inherits from _ProtoSankeyObject but add methods to deal with Tag and TagGroup
    """

    def __init__(self):
        # Initialize from proto
        _ProtoSankeyObject.__init__(self)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, _):
        if type(_) is list:
            if len(_) > 0:
                self._tags = []
                for item in _:
                    if type(item) is Tag:
                        self._update_tags(item)
            else:
                self._tags = _
        elif type(_) is Tag:
            self._update_tags(_)

    def add_tag(self, tag: Tag):
        if type(tag) is Tag:
            if tag not in self._tags:
                self._update_tags(tag)
            return

    def get_taggroups_from_tagtype(self, tagtype):
        taggs = []
        for tagg in self._taggs:
            if tagg.type == tagtype:
                taggs.append(tagg)
        return taggs

    def get_tags_from_taggroup(
        self,
        tagg,
        return_names_instead_of_refs=False
    ):
        """
        Return the list of tags from given tag group and that are related
        to this object.

        Parameters
        ----------
        :param tagg: Tagg group from which the tags must belong to.
        :type tagg: TagGroup

        :param return_names_instead_of_refs: Return a list of tags names.
        :type return_names_instead_of_refs: bool (default=False)

        Returns
        -------
        :return: List of the tags or None
        :rtype: list[Tag] | list[str] | None
        """
        tags = []
        if type(tagg) is TagGroup:
            for tag in self._tags:
                if tag.group == tagg:
                    if return_names_instead_of_refs:
                        tags.append(tag.name_unformatted)
                    else:
                        tags.append(tag)
        if type(tagg) is str:
            tagg = _stdStr(tagg)
            for tag in self._tags:
                if tag.group.name == tagg:
                    if return_names_instead_of_refs:
                        tags.append(tag.name_unformatted)
                    else:
                        tags.append(tag)
        if len(tags) == 0:
            tags = None
        return tags

    def get_tags_from_taggroups(
        self,
        taggs,
        return_names_instead_of_refs=False
    ):
        """
        Return the list of tags from given list of tag groups and
        that are related to this object.

        Parameters
        ----------
        :param taggs: List of tagg group from which the tags must belong to.
        :type taggs: list[TagGroup]

        :param return_names_instead_of_refs: Return a list of tags names.
        :type return_names_instead_of_refs: bool (default=False)

        Returns
        -------
        :return: List of the tags as [or None
        :rtype: list[Tag] | None
        """
        output = []
        if type(taggs) is list:
            for tagg in taggs:
                try:
                    tags = self.get_tags_from_taggroup(tagg)
                    if tags is not None:
                        if return_names_instead_of_refs:
                            output.append(
                                ':'.join([tag.name_unformatted for tag in tags]))
                        else:
                            output.append(tags)
                    else:
                        output.append(None)
                except AttributeError:
                    output.append(None)
        return output

    def has_specific_tag(self, tagg, tag):
        # Find list of tags related to tag group and applied to self
        tags = self.get_tags_from_taggroup(tagg)
        # If no tag found
        if tags is None:
            return False
        # Some tags where found
        if type(tag) is Tag:
            return (tag in tags)
        if type(tag) is str:
            for _ in tags:
                if _.name_unformatted == tag:
                    return True
            return False
        # Default answer
        return False

    def _update_tags(self, _):
        if type(_) is Tag:
            self._tags.append(_)
            self._update_taggs(_)
            _.add_reference(self)

    def _update_taggs(self, _):
        if type(_) is Tag:
            if _.group not in self._taggs:
                self._taggs.append(_.group)
