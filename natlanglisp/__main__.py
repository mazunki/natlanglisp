#!/usr/bin/env python

from .definitions import *
from .words import *
import json

to_be_nice = Concept(to_be, nice)
jekyll_being_nice = Concept(to_be_nice, dr_jekyll)

nice_jekyll = Proposition(to_be_nice, Concept(dr_jekyll))

saying_the_thing = Proposition(Concept(says), nice_jekyll)

claim = Proposition(Concept(annie), saying_the_thing)

claim.pprint()

#  vim: set sts=4 sw=4 ts=4 expandtab
