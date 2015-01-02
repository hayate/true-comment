#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess


def clean(*args):
    """delete all *.so and *.c files"""
    basepath = os.path.dirname(os.path.realpath(__file__))
    build = os.path.join(basepath, 'build')
    bindir = os.path.join(basepath, 'bin')
    if os.path.exists(bindir):
        print("deleting: {0}".format(bindir))
        shutil.rmtree(bindir)
    if os.path.exists(build):
        print("deleting: {0}".format(build))
        shutil.rmtree(build)
    for path, dirs, files in os.walk(basepath):
        for d in dirs:
            if d == '__pycache__':
                dirpath = os.path.join(path, d)
                print("deleting: {0}".format(dirpath))
                shutil.rmtree(dirpath)
        for f in files:
            filepath = os.path.join(path, f)
            if filepath.endswith('.so') or filepath.endswith('.c'):
                print("deleting: {0}".format(filepath))
                os.remove(filepath)


def compile(*args):
    """create shared objects and c files"""
    basepath = os.path.dirname(os.path.realpath(__file__))
    srcdir = os.path.join(basepath, 'src/')
    bindir = os.path.join(basepath, 'bin/')
    if os.path.exists(bindir):
        shutil.rmtree(bindir)
    ignore = shutil.ignore_patterns(*['*.pyc', '*.md', '__pycache__'])
    shutil.copytree(srcdir, bindir, ignore=ignore)
    setup = os.path.join(basepath, 'setup.py')
    subprocess.call([sys.executable, setup, 'build_ext', '--inplace'],
                    shell=False)
    build = os.path.join(basepath, 'build')
    if os.path.exists(build):
        print("deleting: {0}".format(build))
        shutil.rmtree(build)
    exclude = ['__init__.py', 'main.py']
    for path, _, files in os.walk(bindir):
        for f in files:
            filepath = os.path.join(path, f)
            if filepath.endswith(('.py', '.c')) and f not in exclude:
                os.remove(filepath)


def requirements(*args):
    with open('install/requirements.txt') as fp:
        for package in fp.readlines():
            subprocess.call(['pip', 'install', '--upgrade', package.strip()], shell=False)


def test(target=None):
    try:
        nose = sys.modules['nose']
    except KeyError:
        nose = __import__('nose')
    if target is None:
        target = ''
    basepath = os.path.dirname(os.path.realpath(__file__))
    testpath = os.path.join(basepath, 'src', 'tests', target)
    os.chdir(testpath)
    sys.argv.pop()
    sys.argv.extend(['--nocapture', '--rednose', '--with-coverage', '--cover-package', 'papi'])
    nose.run()


def run(command):
    try:
        basepath = os.path.dirname(os.path.realpath(__file__))
        if command == 'live':
            bindir = os.path.join(basepath, 'bin')
            if not os.path.exists(bindir):
                compile()
            os.chdir(bindir)
            subprocess.call(['uwsgi', '--http', ':9090', '--wsgi-file',
                             'main.py', '--master', '--processes', '4',
                             '--threads', '2'], shell=False)
        elif command == 'dev':
            srcdir = os.path.join(basepath, 'src')
            os.chdir(srcdir)
            subprocess.call(['uwsgi', '--http', ':9090', '--wsgi-file',
                             'main.py', '--py-auto-reload', '1'], shell=False)
    except KeyboardInterrupt:
        print("Bye!")


commands = ['clean', 'compile', 'run-live', 'run-dev', 'requirements',
            'test', 'test-controllers', 'test-libs']


def usage():
    print("Run {0} with any combination of the following commands: ".format(sys.argv[0]))
    print(commands)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    for i in range(1, len(sys.argv)):
        name = sys.argv[i]
        if name in commands:
            param = None
            if '-' in name:
                name, param = sys.argv[i].split('-')
            command = getattr(sys.modules[__name__], name)
            command(param)
        else:
            print("unrecognized command: {0}".format(name))
            usage()
            sys.exit()
