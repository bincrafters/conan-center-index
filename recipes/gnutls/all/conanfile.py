from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv
from conan.tools.build import check_min_cppstd, cross_building
from conan.tools.files import copy, get, rm, rmdir, replace_in_file
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps, PkgConfigDeps
from conan.tools.layout import basic_layout
import os


required_conan_version = ">=1.51.3"


class GnuTLSConan(ConanFile):
    name = "gnutls"
    description = "The GnuTLS Transport Layer Security Library"
    license = "LGPL-2.1-or-later"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://gnutls.org/index.html"
    topics = ("ssl", "tls", "crypto")
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            try:
                del self.options.fPIC
            except Exception:
                pass
        try:
            del self.settings.compiler.libcxx
        except Exception:
            pass
        try:
            del self.settings.compiler.cppstd
        except Exception:
            pass

    def layout(self):
        basic_layout(self, src_folder="src")

    def requirements(self):
        self.requires("gmp/6.2.1")
        self.requires("libidn2/2.3.0")
        self.requires("nettle/3.8.1")
        self.requires("libtasn1/4.16.0")
        self.requires("libunistring/0.9.10")

    def validate(self):
        return
        if self.info.settings.compiler.cppstd:
            check_min_cppstd(self, 11)
        if self.info.settings.os not in ["Linux", "FreeBSD", "MacOS"]:
            raise ConanInvalidConfiguration(f"{self.ref} is not supported on {self.info.settings.os}.")

    def build_requirements(self):
        self.tool_requires("autoconf/2.71")
        self.tool_requires("pkgconf/1.7.4")

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
                  destination=self.source_folder, strip_root=True)

    def generate(self):
        yes_no = lambda v: "yes" if v else "no"
        tc = AutotoolsToolchain(self)
        tc.configure_args.append("--disable-tests")
        tc.configure_args.append("--without-p11-kit")
        tc.generate()
        tc = PkgConfigDeps(self)
        tc.generate()
        tc = AutotoolsDeps(self)
        tc.generate()
        env = VirtualBuildEnv(self)
        env.generate()
        if not cross_building(self):
            env = VirtualRunEnv(self)
            env.generate(scope="build")

    def _patch_sources(self):
        replace_in_file(self, os.path.join(self.source_folder, "configure"), 'PKG_CONFIG --exists --print-errors \\"hogweed', 'PKG_CONFIG --exists --print-errors \\"nettle-hogweed')
        replace_in_file(self, os.path.join(self.source_folder, "configure"), '$PKG_CONFIG --exists --print-errors "hogweed', '$PKG_CONFIG --exists --print-errors "nettle-hogweed')
        replace_in_file(self, os.path.join(self.source_folder, "configure"), '$PKG_CONFIG --cflags "hogweed', '$PKG_CONFIG --cflags "nettle-hogweed')
        replace_in_file(self, os.path.join(self.source_folder, "configure"), '$PKG_CONFIG --cflags "hogweed', '$PKG_CONFIG --cflags "nettle-hogweed')

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        copy(self, pattern="LICENSE", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        autotools = Autotools(self)
        autotools.install()

        rm(self, "*.la", os.path.join(self.package_folder, "lib"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = ["gnutls"]
        self.cpp_info.set_property("pkg_config_name", "gnutls")

        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs = ["m", "pthread", "dl"]
