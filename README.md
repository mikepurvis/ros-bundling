ROS Bundling [![Build Status](https://travis-ci.org/mikepurvis/ros-bundling.svg?branch=master)](https://travis-ci.org/mikepurvis/ros-bundling)
============

This repo serves as a minimalist demonstration of bundling multiple catkin/cmake packages into a single deployment unit. In each case, you may execute the `build_package` script to demonstrate creating a DSC file, which can then be built into a binary using pbuilder, sbuild, or an external service such as Launchpad (assuming any dependencies are present). Please see the travis config for further details.

This repo is the companion to a planned talk at [ROSCON 2016 in Seoul](http://roscon.ros.org/2016/#program).


Native Format
-------------

This example generates a package using Debian source format `3.0 (native)`. The package is built up like so:

- rosinstall_generator generates a workspace yaml for a package with dependencies.
- wstool downloads sources for all packages.
- a python script examines the workspace and generates a list of system dependencies.
- a debian metadata folder is copied into the workspace.
- a debian/control file is generated, containing the system deps.
- dpkg-buildpackage is invoked, to create a dsc (sourcedeb). In native format, the dsc creation process handles creating the source tarball, so it is created at this time.

This example is driven by bash, and (apart from the dependency resolution) relies entirely on ROS command line tools. One of its major limitations is that in the course of the construction, you have no idea which packages are and are not actually part of the build. This doesn't matter as much when fetching from GBP repos, since there's a 1:1 mapping of repos to packages, but it matters much more if you try to do a devel build, because then you're pulling in repos which may contain packages you don't actually want, and have no information from which to construct a whitelist for `catkin_tools`.


Quilt Format
------------

This example generates a package using Debian source format `3.0 (quilt)`, taking advantage of its ability to handle multiple "upstream" tarballs to directly consume the tarballs supplied by Github and other git hosts. In contrast to the above, the process here is driven entirely by Python, calling into the underlying modules of the rosdistro and rosinstall_generator packages (and using aria2 to do the actual tarball downloading).

See: https://www.joachim-breitner.de/blog/564-Creating_a_Debian_source_package_without_unpacking_the_source
