from subprocess import Popen, PIPE
import sys

DEFAULT_ENCODING = 'utf-8'


def _get_encoding():
    if sys.stdin.encoding is None:
        return DEFAULT_ENCODING
    else:
        return sys.stdin.encoding


def run_cmd(cmd):
    encoding = _get_encoding()
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    p.wait()
    if p.returncode:
        if stdout:
            print('STDOUT...')
            sys.stdout.write(stdout.decode(encoding))
            print('END STDOUT')
        if stderr:
            print('STDERR...')
            sys.stdout.write(stderr.decode(encoding))
            print('END STDERR')
        raise Exception(f'Exit code [{p.returncode}] returned by command [{cmd}]')
    return stdout.decode(encoding)
