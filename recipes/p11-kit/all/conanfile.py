from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv
from conan.tools.build import check_min_cppstd, cross_building
from conan.tools.files import copy, get, rm, rmdir, apply_conandata_patches, export_conandata_patches
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps, PkgConfigDeps
from conan.tools.meson import Meson, MesonToolchain, MesonDeps
from conan.tools.layout import basic_layout
import os


required_conan_version = ">=1.52.0"


class P11KitConan(ConanFile):
    name = "p11-kit"
    description = "The p11-kit package provides a way to load and enumerate PKCS"
    license = "BSD-3-Clause"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://p11-glue.github.io/p11-glue/p11-kit.html"
    topics = ("pkcs", "crypto", "token")
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "with_libffi": [True, False],
        "enable_nls": [True, False],
    }
    default_options = {
        "with_libffi": True,
        "enable_nls": True,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def configure(self):
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
        self.requires("libtasn1/4.16.0")
        if self.options.with_libffi:
            self.requires("libffi/3.4.3")

    def build_requirements(self):
        self.tool_requires("meson/0.63.2")
        self.tool_requires("pkgconf/1.7.4")

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
                  destination=self.source_folder, strip_root=True)

    def generate(self):
        tc = MesonToolchain(self)
        tc.project_options["libffi"] = "enabled" if self.options.with_libffi else "disabled"
        tc.project_options["nls"] = self.options.enable_nls
        tc.project_options["bash_completion"] = "disabled"
        tc.project_options["systemd"] = "disabled"
        tc.project_options["test"] = False
        tc.generate()
        tc = PkgConfigDeps(self)
        tc.generate()

        env = VirtualBuildEnv(self)
        env.generate()

    def build(self):
        apply_conandata_patches(self)
        meson = Meson(self)
        meson.configure()
        meson.build()

    def package(self):
        copy(self, pattern="COPYING", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        copy(self, "libp11-kit.so*", dst=os.path.join(self.package_folder, "lib"), src=self.build_folder, keep_path=False)
        copy(self, "*.h", dst=os.path.join(self.package_folder, "include"), src=self.source_folder)

    def package_info(self):
        self.cpp_info.libs = ["p11-kit"]
        self.cpp_info.set_property("pkg_config_name", "p11-kit")
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("m")
            self.cpp_info.system_libs.append("pthread")
            self.cpp_info.system_libs.append("dl")
