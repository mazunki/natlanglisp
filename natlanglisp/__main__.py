#!/usr/bin/env python

from .definitions import *
from .words import *
import json

to_be_nice = Concept(to_be, nice)
nice_jekyll = UnsaturatedProposition(2).saturate(to_be_nice, Concept(dr_jekyll))

saying_the_thing = UnsaturatedProposition(4).saturate(says, nice_jekyll)

claim = UnsaturatedProposition(2).saturate(Concept(annie), saying_the_thing)

claim.pprint()

#  vim: set sts=4 sw=4 ts=4 expandtab
