from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os


class TweetNaClConan(ConanFile):
    name = "tweetnacl"
    description = "TweetNaCl is a crypto library in 100 tweets"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://tweetnacl.cr.yp.to"
    topics = ("nacl", "cryptographic", "security", "tweet")
    license = "Public Domain"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        for fl in self.conan_data["sources"][self.version]:
            sha256 = fl.get("sha256")
            url = fl.get("url")
            filename = url[url.rfind("/")+1:]
            tools.download(url, filename)
            tools.check_sha256(filename, sha256)
        tools.download("https://unlicense.org/UNLICENSE", "LICENSE")
        tools.check_sha256("LICENSE", "7e12e5df4bae12cb21581ba157ced20e1986a0508dd10d0e8a4ab9a4cf94e85c")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = [self.name]
