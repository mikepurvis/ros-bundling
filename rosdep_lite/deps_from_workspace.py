#!/usr/bin/env python

from sys import argv
from catkin_pkg.topological_order import topological_order
from . import resolve_deps, get_rosdep_data, get_rosdeps

packages = zip(*topological_order(argv[1]))[1]
print ', '.join(resolve_deps(get_rosdep_data(argv[2]), get_rosdeps(packages)))
