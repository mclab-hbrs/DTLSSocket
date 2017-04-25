import subprocess

from distutils.core import setup
from distutils.extension import Extension
from distutils.command.build_ext import build_ext
from Cython.Build import cythonize

class prepare_tinydtls(build_ext):
    def run(self):
        def run_command(args):
            print("Running:", " ".join(args))
            subprocess.check_call(args, cwd="./tinydtls")
        commands = [
            ["autoreconf", "-i"],
            ["./configure", "--without-ecc"],
            ]
        for command in commands:
            run_command(command)
        build_ext.run(self)

cy_build = cythonize([
      Extension("dtls", 
                ["dtls.pyx", "tinydtls/dtls.c", "tinydtls/crypto.c", "tinydtls/ccm.c",
                 "tinydtls/hmac.c", "tinydtls/netq.c", "tinydtls/peer.c", "tinydtls/dtls_time.c",
                 "tinydtls/session.c", "tinydtls/dtls_debug.c",
                 "tinydtls/aes/rijndael.c", "tinydtls/sha2/sha2.c"],
                include_dirs=['tinydtls'],
                define_macros=[('DTLSv12', '1'),
                               ('WITH_SHA256', '1'),
                               ('DTLS_CHECK_CONTENTTYPE', '1'),
                               ('_GNU_SOURCE', '1')],
                undef_macros = [ "NDEBUG" ],
                )])

setup(
    name="DTLSSocket",
    version='0.1',
    description = "DTLSSocket is a cython wrapper for tinydtls with a Socket like interface",
    author      = "Jannis Konrad",
    author_email= "Jannis.Konrad@h-brs.de",
    url         = "https://git.fslab.de/jkonra2m/tinydtls-cython"
    py_modules  = [ "DTLSSocket", ],
    cmdclass    = {"build_ext": prepare_tinydtls},
    ext_modules = cy_build,
    )
