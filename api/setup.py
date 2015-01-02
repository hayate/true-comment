# -*- coding: utf-8 -*-

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension


setup(
    name='True Comments',
    ext_modules=cythonize([
        Extension('bin.papi.papi',
                  sources=['bin/papi/papi.py'],
                  extra_compile_args=["-O3", "-Wall", "-Wno-strict-prototypes"]
                  ),
        Extension('bin.papi.controllers.async',
                  sources=['bin/papi/controllers/async.py'],
                  extra_compile_args=["-O3", "-Wall", "-Wno-strict-prototypes"]
                  ),
        Extension('bin.papi.controllers.status',
                  sources=['bin/papi/controllers/status.py'],
                  extra_compile_args=["-O3", "-Wall", "-Wno-strict-prototypes"]
                  ),
        Extension('bin.papi.controllers.tm',
                  sources=['bin/papi/controllers/tm.py'],
                  extra_compile_args=["-O3", "-Wall", "-Wno-strict-prototypes"]
                  ),
        Extension('bin.papi.libs.async',
                  sources=['bin/papi/libs/async.py'],
                  extra_compile_args=["-O3", "-Wall", "-Wno-strict-prototypes"]
                  ),
        Extension('bin.papi.libs.config',
                  sources=['bin/papi/libs/config.py'],
                  extra_compile_args=["-O3", "-Wall", "-Wno-strict-prototypes"]
                  ),
        Extension('bin.papi.libs.logger',
                  sources=['bin/papi/libs/logger.py'],
                  extra_compile_args=["-O3", "-Wall", "-Wno-strict-prototypes"]
                  ),
        Extension('bin.papi.libs.processor',
                  sources=['bin/papi/libs/processor.py'],
                  extra_compile_args=["-O3", "-Wall", "-Wno-strict-prototypes"]
                  ),
    ])
)
