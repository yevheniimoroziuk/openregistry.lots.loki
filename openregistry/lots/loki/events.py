# -*- coding: utf-8 -*-


class PublicationInitializeEvent(object):
    """ Publication initialization event. """

    def __init__(self, publication):
        self.publication = publication


class ItemInitializeEvent(object):
    """ Publication initialization event. """

    def __init__(self, item):
        self.item = item
