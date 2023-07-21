__author__ = 'Edwin Cowart, Kevin McDonough'


class JSONTestCase:
    """ A JSON Test Case
    """
    def __init__(self, name=None, in_json=None, out_json=None):
        """ Construct a JSON Test Case
        :param name: The name of the JSON Test Cases
        :type name: String or None
        :param in_json: The in_json data
        :type in_json: String or None
        :param out_json: The out_json data
        :type out_json: String or None
        """
        self.name = name
        self.in_json = in_json
        self.out_json = out_json

    def has_name(self):
        """ Does this Test Case have a name?
        :return: True if this Test Case has a name, False otherwise
        :rtype: Boolean
        """
        return self.name is not None

    def has_in_json(self):
        """ Does this Test Case have a in_json?
        :return: True if this Test Case has a in_json, False otherwise
        :rtype: Boolean
        """
        return self.in_json is not None

    def has_out_json(self):
        """ Does this Test Case have a out_json?
        :return: True if this Test Case has a out_json, False otherwise
        :rtype: Boolean
        """
        return self.out_json is not None

    def is_complete(self):
        """ Is this Test Case complete?
        :return: True if this Test Case complete, False otherwise
        :rtype: Boolean
        """
        return self.has_name() and self.has_in_json() and self.has_out_json()

    def get_in_json_filename(self):
        """ Get the full in filename
        :return: The in filename
        :rtype: String
        """
        return self.name + "-in.json"

    def get_out_json_filename(self):
        """ Get the full out filename
        :return: The out filename
        :rtype: String
        """
        return self.name + "-out.json"