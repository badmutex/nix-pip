

from os import listdir
from os.path import abspath, dirname, join, isdir, isfile
from subprocess import check_call


def list_tests():
    testdir = dirname(abspath(__file__))
    tests = []
    for name in listdir(testdir):
        if name.startswith('.') or name.startswith('_'):
            continue
        path = join(testdir, name)
        if isfile(path):
            continue
        tests.append(path)

    return tests


def test():
    for testdir in list_tests():
        cmd = ['make', '-C', testdir]
        check_call(cmd)


if __name__ == '__main__':
    print test()

