"""
Convert Cisco ISO config to a python dictionary
The idea is that a dictionary has hashes of key/value pairs
which will be very fast to perform config auditing against.

Note: Config must be in the same format as it is from a show run

version: 0.1.6
TO-DO: - Building test suite and work on edge cases
       - Update to work with config with more than one space
         between parent/child elements # Done need tests
"""


class ConfToDict(object):
    """
    Convert Cisco IOS config to a python dictionary
    """

    def __init__(self, full_config, delimiter='\n', from_file=False, spaces=1):
        """
        Initialization method
        :param full_config: Either a multi-line string or a path to a file
        :param delimiter: Delimiter used to split the lines
        :param from_file: Set to true if config is coming from a file
        :param spaces: Number of spaces for child indent
                       # IOS = 1
                       # NXOS = 2
        """
        self.full_config = full_config
        self.delimiter = delimiter
        self.from_file = from_file
        self.spaces = spaces

        # Clean config with a file as the input
        if self.from_file:
            with open(self.full_config, 'r') as f:
                full_config = f.readlines()
                # Just config, remove trailing new lines, !
                config = []
                for i in full_config:
                    if not (i.startswith('!') or
                            i.startswith(' !{0}'.format(self.delimiter)) or
                            i.startswith(self.delimiter)):
                        config.append(i.replace(self.delimiter, ''))

            self.config = config

        # Clean config with a sting is the input
        else:
            conf_list = self.full_config.split(self.delimiter)
            config = []
            for i in conf_list:
                if not (i.startswith('!') or i == ' !' or i == ''):
                    config.append(i)

            self.config = config

    @staticmethod
    def find_children(child_list, parent_index, next_parent_index):
        """
        Get the slice of config between parent elements
        :param child_list: A child list
        :param parent_index: Index of current parent
        :param next_parent_index: Index of next parent
        :return: A list of children between current and next parent elements
        """
        children = []
        for i in child_list:
            if parent_index < i[0] < next_parent_index:
                children.append(i)
        return children

    def to_dict(self):
        """
        Convert a list of IOS config to a dictionary.
        :return: A dictionary of config elements
        """
        conf_dict = {}

        # Find lines with banners and add them to the conf_dict
        banners = []

        # Find start of banner
        for i in self.config:
            if i.startswith('banner'):
                banner_start = self.config.index(i)
                terminator = i.split()[-1]

                # Find end of banner
                sentinel = banner_start + 1
                while not self.config[sentinel] == terminator:
                    sentinel += 1

                # Add start/finish of banner to banners list
                banners.append((banner_start, sentinel))

        # Add banners to conf_dict
        for i in banners:
            conf_dict.update({'\n'.join([j for j in self.config[i[0]:i[1] + 1]]): []})

        # List holds a range of banner line numbers
        banner_list = [i for j in [range(k[0], k[1] + 2) for k in banners] for i in j]

        numbered_config = [i for i in enumerate(self.config)]

        zero_level = []
        first_level = []
        second_level = []
        third_level = []

        for i in numbered_config:
            if i[0] in banner_list:
                pass
            else:
                # The number of spaces at the start of the line indicates the child level
                child_level = len(i[1]) - len(i[1].lstrip(' '))
                if not i[1].startswith(' '):
                    zero_level.append(i)
                elif child_level == 1 * self.spaces:
                    first_level.append((i[0], i[1].lstrip(' ')))
                elif child_level == 2 * self.spaces:
                    second_level.append((i[0], i[1].lstrip(' ')))
                elif child_level == 3 * self.spaces:
                    third_level.append((i[0], i[1].lstrip(' ')))
                elif child_level > 3 * self.spaces:
                    print('More than 3 levels of nesting')
                    print(i)

        for i in zero_level:
            next_element = zero_level.index(i) + 1
            if next_element == len(zero_level):
                # end of top level parents
                if i[0] > first_level[-1][0] and i[0] > second_level[-1][0]:
                    conf_dict.update({i[1]: []})
                else:
                    print('last zero level parent has children')

            elif zero_level[next_element][0] - zero_level[zero_level.index(i)][0] == 1:
                # element has no children
                conf_dict.update({i[1]: []})
            else:
                parent_index = zero_level[zero_level.index(i)][0]
                next_parent_index = zero_level[next_element][0]

                # find child elements between parent elements
                first_level_children = self.find_children(first_level, parent_index,
                                                          next_parent_index)
                second_level_children = self.find_children(second_level, parent_index,
                                                           next_parent_index)
                third_level_children = self.find_children(third_level, parent_index,
                                                          next_parent_index)

                # Parent only has first level children
                if not second_level_children:
                    # level 0
                    #  level 1
                    #  level 1
                    #
                    # output : {level 0: [level 1, level 1]}
                    children = [j[1] for j in first_level_children]
                    conf_dict.update({i[1]: children})

                elif second_level_children and third_level_children:
                    # multiple children at different levels 1 child per level
                    # level 0
                    #  level 1
                    #   level 2
                    #    level 3
                    #
                    # output: {level 0: {level 1: {level 2: [level 3]}}}
                    if (len(first_level_children) and len(second_level_children) and
                            len(third_level_children)) == 1:
                        conf_dict.update({
                            i[1]: {
                                first_level_children[0][1]: {
                                    second_level_children[0][1]: [third_level_children[0][1]]
                                }
                            }
                        })

                elif second_level_children:
                    if (len(first_level_children) and len(second_level_children)) == 1:
                        # multiple children at different levels 1 child per level
                        # level 0
                        #  level 1
                        #   level 2
                        #
                        # output: {level 0: {level 1: [level 2]}}
                        conf_dict.update({
                            i[1]: {
                                first_level_children[0][1]: [second_level_children[0][1]]
                            }
                        })

                    else:
                        # multiple children at different levels 2 child levels
                        # level 0
                        #  level 1
                        #   level 2
                        #   level 2
                        #  level 1
                        #   level 2
                        #   level 2
                        #
                        # output: {level 0:
                        #             {level 1: [level 2, level 2]},
                        #             {level 1: [level 2, level 2]}
                        #         }
                        all_children = []
                        for j in first_level_children:
                            next_element = first_level_children.index(j) + 1
                            children = []
                            # last element in list
                            if next_element == len(first_level_children):
                                for k in second_level_children:
                                    if j[0] < k[0]:
                                        children.append(k[1])
                            else:
                                for k in second_level_children:
                                    if j[0] < k[0] < first_level_children[next_element][0]:
                                        children.append(k[1])
                            all_children.append({j[1]: children})

                        conf_dict.update({i[1]: {}})
                        for j in all_children:
                            conf_dict[i[1]].update(j)

        return conf_dict
