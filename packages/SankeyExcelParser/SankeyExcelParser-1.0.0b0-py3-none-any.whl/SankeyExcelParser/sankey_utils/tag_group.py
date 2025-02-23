"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for Tag class

"""

# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey_utils.protos.tag_group import _ProtoTagGroup
from SankeyExcelParser.sankey_utils.tag import Tag
from SankeyExcelParser.sankey_utils.functions import _stdStr

# CONSTANTS -----------------------------------------------------------------------
ANTI_TAGS_NAME = '0'


# CLASS ----------------------------------------------------------------------------
class TagGroup(_ProtoTagGroup):
    """
    Define a Tag Group object.
    Inherits from _ProtoTagGroup but adds methods to deal with Tags.
    """

    def __init__(
        self,
        name: str,
        taggtype: str,
        **kwargs
    ):
        # Init parent class
        _ProtoTagGroup.__init__(self, name, taggtype)
        # Update values
        self.update(**kwargs)

    def update(
        self,
        **kwargs
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, _):
        # Input as str
        if type(_) is str:
            if len(_) > 0:
                self._tags = {}
                names_tags = _.split(':')
                for name_tag in names_tags:
                    self._tags[_stdStr(name_tag)] = Tag(name_tag, self)
            return
        # Input as list of Tags
        if type(_) is list:
            self._tags = {}
            for tag in _:
                if type(tag) is Tag:
                    self._tags[_stdStr(tag.name)] = tag

    @property
    def anti_tags(self):
        return self._anti_tags

    def get_or_create_tag(self, tag):
        # Case tag already a Tag
        if type(tag) is Tag:
            # Check if ref name in dict of tags
            ref_tag = _stdStr(tag.name)
            if (ref_tag not in self._tags.keys()) and \
               (ref_tag != self._anti_tags):
                self.add_tag(tag)
            # Return already existing or newly created tag
            return tag
        # Case tag is a name
        if type(tag) is str:
            # Check if ref name in dict of tags
            ref_tag = _stdStr(tag)
            if (ref_tag not in self._tags.keys()) or \
               ((ref_tag == ANTI_TAGS_NAME) and (self._anti_tags is None)):
                self.add_tag(tag)
            # Return already existing or newly created tag
            return self.get_tag_from_name(tag)
        return None

    def add_tag(self, tag):
        # Case tag already a Tag
        if type(tag) is Tag:
            ref_tag = _stdStr(tag.name)
            tag.group = self
            if ref_tag == ANTI_TAGS_NAME:
                self._anti_tags = tag
            else:
                self._tags[ref_tag] = tag
            return
        # Case tag is a name
        if type(tag) is str:
            ref_tag = _stdStr(tag)
            if ref_tag == ANTI_TAGS_NAME:
                self._anti_tags = Tag(ANTI_TAGS_NAME, self)
            else:
                self._tags[ref_tag] = Tag(tag, self)
            return

    def get_tag_from_name(
        self,
        tag_name: str,
        include_anti_tags: bool = True
    ):
        ref_tag_name = _stdStr(tag_name)  # all the keys are standardized
        if ref_tag_name in self._tags.keys():
            return self._tags[ref_tag_name]
        # Special case : anti tag -> we create it if it does not exist
        if include_anti_tags and (ref_tag_name == ANTI_TAGS_NAME):
            if self._anti_tags is None:
                self._anti_tags = Tag(ANTI_TAGS_NAME, self)
            return self._anti_tags
        return None

    def get_previous_tag(self, _):
        prev_tag = None
        if type(_) is str:
            for tag_name in self.tags.keys():
                if tag_name == _:
                    return prev_tag
                prev_tag = self.tags[tag_name]
        if type(_) is Tag:
            for tag in self.tags.values():
                if tag == _:
                    return prev_tag
                prev_tag = tag
        return prev_tag

    @property
    def tags_str(self):
        return ":".join([tag.name_unformatted for tag in self._tags.values()])

    @property
    def antagonists_taggs(self):
        return self._antagonists_taggs

    def add_antagonist_tagg(self, tagg):
        if type(tagg) is TagGroup:
            if tagg not in self._antagonists_taggs:
                self._antagonists_taggs.append(tagg)
                tagg.add_antagonist_tagg(self)

    def has_antagonists(self):
        return (len(self._antagonists_taggs) > 0)

    @property
    def colors(self):
        if self.has_colors_defined():
            return ':'.join([tag.color for tag in self._tags.values()])
        else:
            return ''

    @colors.setter
    def colors(self, _):
        if type(_) is str:
            if len(_) > 0:
                colors = _.split(':')
                for color, tag in zip(colors, self._tags.values()):
                    tag.color = color
            return

    def has_colors_defined(self):
        for tag in self.tags.values():
            if tag.color != '':
                return True
        return False

    def get_as_dict(self):
        # Init output
        output = {}
        # Get values
        output['name'] = self.name
        output['tags'] = [_.name for _ in self.tags.values()]
        try:
            output['anti_tags'] = self.anti_tags.name
        except Exception:
            pass
        try:
            output['antagonists_taggs'] = self.antagonists_taggs.name
        except Exception:
            pass
        output['colormap'] = self.colormap
        output['is_palette'] = self.is_palette
        return output

    def __repr__(self):
        """
        Gives a string representation of Taggroup object.

        Returns
        -------
        :return: String format of self.
        :rtype: str
        """
        s = '{{{0} | {1}}}'.format(
            self.name_unformatted,
            self.tags_str)
        return s
