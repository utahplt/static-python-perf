from enum import Enum

__author__ = 'Edwin Cowart, Kevin McDonough'


class HTML_Tag(Enum):
    HEAD = "head"
    TITLE = "title"
    META = "meta"
    P = "p"
    PRE = "pre"
    BODY = "body"
    H1 = "h1"
    EM = "em"
    STYLE = "style"
    TABLE = "table"
    TR = "tr"
    TH = "th"
    TD = "td"
    A = "a"
    DIV = "div"
    H2 = "h2"

    @staticmethod
    def all_tags():
        """ Get all the tags in this enum
        :return: All the tags in this Enum
        """
        return [HTML_Tag.HEAD, HTML_Tag.TITLE, HTML_Tag.META, HTML_Tag.P, HTML_Tag.PRE, HTML_Tag.BODY, HTML_Tag.H1,
                HTML_Tag.EM, HTML_Tag.STYLE, HTML_Tag.TABLE, HTML_Tag.TR, HTML_Tag.TH, HTML_Tag.TD, HTML_Tag.A,
                HTML_Tag.DIV, HTML_Tag.H2]

    @staticmethod
    def all_tag_values():
        """ Get the values of all the tags in this enum
        :return: The value of all the tags in this enum
        :rtype: [String,...]
        """
        return [tag.value for tag in HTML_Tag.all_tags()]

    @staticmethod
    def is_tag(value):
        """ Is the given value a HTML Tag?
        :param value: The value being checked
        :type value: Any
        :return: True if the given value is a HTML Tag, False otherwise
        :rtype: Boolean
        """
        return any(value == tag for tag in HTML_Tag.all_tag_values())

    @staticmethod
    def is_h2(value):
        return value == HTML_Tag.H2.value

    @staticmethod
    def is_pre(value):
        return value == HTML_Tag.PRE.value