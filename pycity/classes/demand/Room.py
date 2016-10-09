# coding=utf-8


class Room(object):

    def __init__(self, environment):
        self.environment = environment
        self.__kind = "room"

    def __str__(self):
        return str('<Room object of apartment of pyCity>')

    @property
    def kind(self):
        """
        Return type of pyCity object
        """
        return self.__kind