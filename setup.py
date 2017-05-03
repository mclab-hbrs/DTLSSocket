import subprocess

from distutils.core import setup
from distutils.extension import Extension
from distutils.command.build_ext import build_ext
from Cython.Build import cythonize

class prepare_tinydtls(build_ext):
    def run(self):
        def run_command(args):
            print("Running:", " ".join(args))
            subprocess.check_call(args, cwd="./lowlevel/tinydtls")
        commands = [
            ["autoconf"],
            ["autoheader"],
            ["./configure", "--without-ecc"],
            ]
        for command in commands:
            run_command(command)
        build_ext.run(self)

cy_build = cythonize([
      Extension("lowlevel.dtls",
                ["lowlevel/dtls.pyx", "lowlevel/tinydtls/dtls.c", "lowlevel/tinydtls/crypto.c",
                 "lowlevel/tinydtls/ccm.c", "lowlevel/tinydtls/hmac.c", "lowlevel/tinydtls/netq.c",
                 "lowlevel/tinydtls/peer.c", "lowlevel/tinydtls/dtls_time.c",
                 "lowlevel/tinydtls/session.c", "lowlevel/tinydtls/dtls_debug.c",
                 "lowlevel/tinydtls/aes/rijndael.c", "lowlevel/tinydtls/sha2/sha2.c"],
                include_dirs=['lowlevel/tinydtls'],
                define_macros=[('DTLSv12', '1'),
                               ('WITH_SHA256', '1'),
                               ('DTLS_CHECK_CONTENTTYPE', '1'),
                               ('_GNU_SOURCE', '1')],
                undef_macros = [ "NDEBUG" ],
                )])

setup(
    name="DTLSSocket",
    version='0.1.0',
    description = "DTLSSocket is a cython wrapper for tinydtls with a Socket like interface",
    author      = "Jannis Konrad",
    author_email= "Jannis.Konrad@h-brs.de",
    url         = "https://git.fslab.de/jkonra2m/tinydtls-cython",
    py_modules  = [ "DTLSSocket", ],
    cmdclass    = {"build_ext": prepare_tinydtls},
    ext_modules = cy_build,
    )
