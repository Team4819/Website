__author__ = 'christian'
from basicNodes import Node, DirNode

class Blog(DirNode):
    group = "writer"
    permissions = "r-rwr-"

    def _read(self, path, args):
