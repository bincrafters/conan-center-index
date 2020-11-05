import tempfile
import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class ResiprocateConan(ConanFile):
    name = "resiprocate"
    version = "1.12.0"
    license = "https://github.com/resiprocate/resiprocate/blob/master/COPYING"
    url = "http://www.resiprocate.org"
    author = "resiprocate-devel@resiprocate.org"
    description = "The project is dedicated to maintaining a complete, correct, and commercially usable implementation of SIP and a few related protocols. "
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports = "LICENSE"
    release_name = "%s-%s" % (name, version)
    install_dir = tempfile.mkdtemp(suffix=name)

    def source(self):
        print(os.path.join(self.install_dir, "lib"))
        tools.get("https://www.resiprocate.org/files/pub/reSIProcate/releases/resiprocate-%s.tar.gz" % self.version)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = True
        env_build.cxx_flags.append("-w")
        with tools.environment_append(env_build.vars):
            configure_args = ['--prefix=%s' % self.install_dir]
            with tools.chdir(self.release_name):
                env_build.configure(args=configure_args)
                env_build.make(args=["clean"])
                env_build.make(args=["install"])

    def package(self):
        self.copy(pattern="*", dst="include/repro", src=os.path.join(self.release_name, "repro"))
        self.copy(pattern="*", dst="include/resip", src=os.path.join(self.release_name, "resip"))
        self.copy(pattern="*", dst="include/rutil", src=os.path.join(self.release_name, "rutil"))
        self.copy(pattern="*.a", dst="lib", src=os.path.join(self.install_dir, "lib"))
        self.copy(pattern="*.la", dst="lib", src=os.path.join(self.install_dir, "lib"))
        self.copy(pattern="*.so", dst="lib", src=os.path.join(self.install_dir, "lib"))
        self.copy(pattern="*.lib", dst="lib", src=os.path.join(self.install_dir, "lib"))

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.cpp_info.libs = ["resip", "rutil", "dum", "resipares"]
