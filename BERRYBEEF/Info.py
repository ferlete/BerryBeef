# -*- coding: utf-8 -*-


"""BERRYBEEF.info: stuff module within the beef package."""


class Info(object):

    def __init__(self, author, email):
        self.author = author
        self.email = email

    def showinfo(self, version):
        return self.author + version
