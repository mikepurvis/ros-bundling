#!/usr/bin/env python

import requests
import yaml

DEFAULT_URLS = (
    'https://github.com/ros/rosdistro/raw/master/rosdep/base.yaml',
    'https://github.com/ros/rosdistro/raw/master/rosdep/python.yaml')

DEFAULT_EXTRA_SYSTEM_DEPS = ['cmake', 'debhelper', 'python-catkin-tools']


def get_rosdeps(packages):
    deps = set()

    for pkg in packages:
        for dep in pkg.build_depends + pkg.run_depends:
            deps.add(dep.name)

    deps -= set([pkg.name for pkg in packages])
    return deps


def get_rosdep_data(distro, urls=DEFAULT_URLS):
    ROSDEP_PATHS = (
        lambda p: p['ubuntu'],
        lambda p: p['ubuntu'][distro],
        lambda p: p['ubuntu'][distro]['packages'],
        lambda p: p['ubuntu']['apt']['packages'],
        lambda p: p['ubuntu'][distro]['apt']['packages'])

    def _parse(data):
        for key, data in data.iteritems():
            for path in ROSDEP_PATHS:
                try:
                    if isinstance(path(data), str):
                        yield key, [path(data)]
                    if isinstance(path(data), list):
                        yield key, path(data)
                except (KeyError, TypeError):
                    pass

    data = {}
    for url in urls:
        data.update(_parse(yaml.safe_load(requests.get(url).text)))
    return data
    

def resolve_deps(rosdep_data, deps, extra_system_deps=DEFAULT_EXTRA_SYSTEM_DEPS):
    return sorted(set([pkg for dep in deps for pkg in rosdep_data[dep]] + extra_system_deps))
