ROS Bundling [![Build Status](https://travis-ci.org/mikepurvis/ros-bundling.svg?branch=master)](https://travis-ci.org/mikepurvis/ros-bundling)
============

This repo serves as a minimalist demonstration of bundling multiple catkin/cmake packages into a single deployment unit.

It is the companion to a planned talk at [ROSCON 2016 in Seoul](http://roscon.ros.org/2016/#program).


Native Format
-------------

This example generates a package using Debian source format `3.0 (native)`. The package is built up like so:

- rosinstall_generator generates a workspace yaml for a package with dependencies.
- wstool downloads sources for all packages.
- a python script examines the workspace and generates a list of system dependencies.
- a debian metadata folder is copied into the workspace.
- a debian/control file is generated, containing the system deps.
- dpkg-buildpackage is invoked, to create a dsc (sourcedeb). In native format, the dsc creation process handles creating the source tarball, so it is created at this time.

At this point, the dsc could be built locally, in an environment like sbuild or pbuilder, or pushed to an external server to build.


Quilt Format
------------

This example generates a package using Debian source format `3.0 (quilt)`, taking advantage of its ability to handle multiple "upstream" tarballs to directly consume the tarballs supplied by Github.
