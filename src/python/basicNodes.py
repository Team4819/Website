__author__ = 'christian'

class Node:
    permissions = "r-r-r-"
    group = "public"
    user = "public user"

    def read(self):
        pass

    def write(self):
        pass

class DirNode(Node):
    pass