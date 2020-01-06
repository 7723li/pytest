import sys

class Me:
    def fuck(self, name):
        assert(type(name) is str)
        print("fuck" + name)

try:
    me = Me()
    me.fuck("you")
except:
    sys.exit(0)