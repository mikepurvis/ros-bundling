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
- a `debian/control` file is generated, containing the system deps.
- `dpkg-buildpackage` is invoked, to create a dsc (sourcedeb). In native format, the dsc creation process handles creating the source tarball, so it is created at this time.

This example is driven by bash, and (apart from the dependency resolution) relies entirely on ROS command line tools. One of its major limitations is that in the course of the construction, you have no idea which packages are and are not actually part of the build. This doesn't matter as much when fetching from GBP repos, since there's a 1:1 mapping of repos to packages, but it matters much more if you try to do a devel build, because then you're pulling in repos which may contain packages you don't actually want, and have no information from which to construct a whitelist for `catkin_tools`.


Quilt Format
------------

This example generates a package using Debian source format `3.0 (quilt)`, taking advantage of its ability to handle _multiple_ upstream tarballs to directly consume the tarballs supplied by Github and other git hosts, rather than unpacking them all and then having `dpkg-buildpackage` create a new one. In contrast to the above, the process here is driven entirely by Python:

- the debian changelog is parsed to determine the upstream version.
- the rosdistro distribution.yaml is fetched from the tag matching the upstream version.
- the rosdistro cache is updated to match the versions specified in the tagged `distribution.yaml`.
- rosinstall_generator is invoked with the cache to get a full list of required packages.
- the list of non-workspace dependencies is resolved against rosdep to get system dependencies.
- the debian metadata folder is generated with the appropriate `control` file.
- the package list is generated into a list of tarballs, which are downloaded in parallel by `aria2`. If you require an API key or other auth to be sent to your git host, it's easy to specify additional headers on a per-URL basis, see [the aria2 docs](https://aria2.github.io/manual/en/html/aria2c.html#input-file).
- `dpkg-source` is invoked to construct a dsc.

This is a bit unconventional in that a normal `dpkg-buildpackage -S` invocation would require all the tarballs to be unpacked. However, we can get out of that step by jumping right to invoking `dpkg-source` with the unexpanded source tarballs. For more on details, see [this article](https://www.joachim-breitner.de/blog/564-Creating_a_Debian_source_package_without_unpacking_the_source).
