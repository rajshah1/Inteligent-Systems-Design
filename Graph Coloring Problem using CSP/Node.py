#!/usr/bin/env python


class Node:
    def __init__(self,mycolor,myname=None):
        self.next = []
        self.nextnode = None
        self.mycolor = mycolor
        self.myname = myname

    def put_child(self,node):
        self.next.append(node)



