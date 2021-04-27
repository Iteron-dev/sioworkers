from __future__ import absolute_import
from sys import version_info
from setuptools import setup, find_packages

PYTHON_VERSION = version_info[0]

python2_specific_requirements = [
    'supervisor>=4.0,<4.3',
    'enum34>=1.1,<1.2',
]

python3_specific_requirements = [
    'bsddb3==6.2.7',
]

python23_universal_requirements = [
    'filetracker>=2.1.5,<3.0',
    'simplejson==3.14.0',
    'Twisted==20.3.0',
    'sortedcontainers==2.1.0',
    'six',
    'pytest>=4.6,<4.7',
    'pytest-runner==5.1',
    'pytest-timeout==1.3.3',
    'urllib3<2.0',  # urllib3 will drop support for python2 in version 2.0.
]

if PYTHON_VERSION == 2:
    final_requirements = python23_universal_requirements + python2_specific_requirements
else:
    final_requirements = python23_universal_requirements + python3_specific_requirements


setup(
    name = "sioworkers",
    version = '1.4',
    author = "SIO2 Project Team",
    author_email = 'sio2@sio2project.mimuw.edu.pl',
    description = "Programming contest judging infrastructure",
    url = 'https://github.com/sio2project/sioworkers',
    license = 'GPL',

    # we need twisted.plugins in packages to install the sio twisted command
    packages = find_packages() + ['twisted.plugins'],
    namespace_packages = ['sio', 'sio.compilers', 'sio.executors'],

    install_requires=final_requirements,

    setup_requires = [
        'pytest-runner',
    ],

    tests_require = [
        'pytest',
        'pytest-timeout'
    ],

    entry_points = {
        'sio.jobs': [
            'ping = sio.workers.ping:run',
            'compile = sio.compilers.job:run',
            'exec = sio.executors.executor:run',
            'sio2jail-exec = sio.executors.sio2jail_exec:run',
            'cpu-exec = sio.executors.executor:run',
            'unsafe-exec = sio.executors.unsafe_exec:run',
            'ingen = sio.executors.ingen:run',
            'inwer = sio.executors.inwer:run',
        ],
        'sio.compilers': [
            # Example compiler:
            'foo = sio.compilers.template:run',

            # Sandboxed compilers:
            'gcc4_8_2_c99 = sio.compilers.gcc:run_c_gcc4_8_2_c99',
            'g++4_8_2_cpp11 = sio.compilers.gcc:run_cpp_gcc4_8_2_cpp11',
            'fpc2_6_2 = sio.compilers.fpc:run_pas_fpc2_6_2',
            'java1_8 = sio.compilers.java:run_java1_8',

            # Non-sandboxed compilers
            'system-gcc = sio.compilers.system_gcc:run_gcc',
            'system-g++ = sio.compilers.system_gcc:run_gplusplus',
            'system-fpc = sio.compilers.system_fpc:run',
            'system-java = sio.compilers.system_java:run',

            # Compiler for output only tasks solutions
            'output-only = sio.compilers.output:run',

            ####################################
            # Deprecated, should be removed after 01.01.2021
            # Default extension compilers:
            'default-c = sio.compilers.gcc:run_c_default',
            'default-cc = sio.compilers.gcc:run_cpp_default',
            'default-cpp = sio.compilers.gcc:run_cpp_default',
            'default-pas = sio.compilers.fpc:run_pas_default',
            'default-java = sio.compilers.java:run_java_default',

            ####################################
            # Deprecated, should be removed after 01.01.2021
            # Sandboxed compilers:
            'c = sio.compilers.gcc:run_c_default',

            'cc = sio.compilers.gcc:run_cpp_default',
            'cpp = sio.compilers.gcc:run_cpp_default',

            'pas = sio.compilers.fpc:run_pas_default',

            'java = sio.compilers.java:run_java_default',

            ####################################
            # Deprecated, should be removed after 01.01.2021
            # Non-sandboxed compilers
            'system-c = sio.compilers.system_gcc:run_gcc',

            'system-cc = sio.compilers.system_gcc:run_gplusplus',
            'system-cpp = sio.compilers.system_gcc:run_gplusplus',

            'system-pas = sio.compilers.system_fpc:run',
            ####################################
        ],
        'console_scripts': [
            'sio-batch = sio.workers.runner:main',
            'sio-run-filetracker = sio.workers.ft:launch_filetracker_server',
            'sio-get-sandbox = sio.workers.sandbox:main',
            'sio-compile = sio.compilers.job:main',
            'sio-celery-worker = sio.celery.worker:main',
        ]
    }
)


# Make Twisted regenerate the dropin.cache, if possible.  This is necessary
# because in a site-wide install, dropin.cache cannot be rewritten by
# normal users.
try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
# HACK: workaround for hudson
except TypeError:
    pass
else:
    list(getPlugins(IPlugin))
