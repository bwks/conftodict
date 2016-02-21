"""
Convert Cisco ISO config to a python dictionary
The idea is that a dictionary has hashes of key/value pairs
which will be very fast to perform config auditing against.
version: 0.1
TO-DO: Build test suite and work on edge cases
"""


class ConfToDict(object):
    """
    Convert Cisco IOS config to a python dictionary
    """

    def __init__(self, full_config, delimiter='\n', from_file=False):
        """
        Initialization method
        :param full_config: Either a mulit-line string or a path to a file
        :param delimiter: Delimiter used to split the lines
        :param from_file: Set to true if config is coming from a file
        """
        self.full_config = full_config
        self.delimiter = delimiter
        self.from_file = from_file

        # Clean config with a file as the input
        if self.from_file:
            with open(self.full_config, 'r') as f:
                full_config = f.readlines()
                # Just config, remove trailing new lines, !
                config = []
                for i in full_config:
                    if not (i.startswith('!') or i.startswith(' !\n') or i.startswith('\n')):
                        config.append(i.replace('\n', ''))

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
        numbered_config = [i for i in enumerate(self.config)]
        zero_level = []
        first_level = []
        second_level = []
        third_level = []

        for i in numbered_config:
            # The number of spaces at the start of the line indicates the child level
            child_level = len(i[1]) - len(i[1].lstrip(' '))
            if not i[1].startswith(' '):
                zero_level.append(i)
            elif child_level == 1:
                first_level.append((i[0], i[1].lstrip(' ')))
            elif child_level == 2:
                second_level.append((i[0], i[1].lstrip(' ')))
            elif child_level == 3:
                third_level.append((i[0], i[1].lstrip(' ')))
            elif child_level > 3:
                print('More than 3 levels of nesting')
                print(i)

        conf_dict = {}
        for i in zero_level:
            next_element = zero_level.index(i) + 1
            if next_element == len(zero_level):
                # end of top level parents
                if i[0] > first_level[-1][0] and i[0] > second_level[-1][0]:
                    conf_dict.update({i[1]: None})
                else:
                    print('last zero level parent has children')

            elif zero_level[next_element][0] - zero_level[zero_level.index(i)][0] == 1:
                # element has no children
                conf_dict.update({i[1]: None})
            else:
                parent_index = zero_level[zero_level.index(i)][0]
                next_parent_index = zero_level[next_element][0]

                # find child elements between parent elements
                first_level_children = ConfToDict.find_children(first_level, parent_index,
                                                                next_parent_index)
                second_level_children = ConfToDict.find_children(second_level, parent_index,
                                                                 next_parent_index)
                third_level_children = ConfToDict.find_children(third_level, parent_index,
                                                                next_parent_index)

                # Parent only has first level children
                if not second_level_children:
                    children = [j[1] for j in first_level_children]
                    if len(children) == 1:
                        conf_dict.update({i[1]: children[0]})
                    else:
                        conf_dict.update({i[1]: children})

                elif second_level_children and third_level_children:
                    # multiple children at different levels 1 child per level
                    # level 0
                    #  level 1
                    #   level 2
                    #    level 3
                    if (len(first_level_children) and len(second_level_children) and
                            len(third_level_children)) == 1:
                        conf_dict.update({
                            i[1]: {
                                first_level_children[0][1]: {
                                    second_level_children[0][1]: third_level_children[0][1]
                                }
                            }
                        })

                elif second_level_children:
                    # multiple children at different levels 1 child per level
                    # level 0
                    #  level 1
                    #   level 2
                    if (len(first_level_children) and len(second_level_children)) == 1:
                        conf_dict.update({
                            i[1]: {
                                first_level_children[0][1]: second_level_children[0][1]
                            }
                        })

                    # multiple children at different levels 2 child levels
                    # level 0
                    #  level 1
                    #   level 2
                    #   level 2
                    #  level 1
                    #   level 2
                    #   level 2
                    else:
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
                        conf_dict.update({i[1]: all_children})

        return conf_dict
