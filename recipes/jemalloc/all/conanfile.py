import os
from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools


class JemallocConan(ConanFile):
    name = "jemalloc"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://jemalloc.net"
    description = "jemalloc is a general purpose malloc(3) implementation"
    license = "BSD-2-Clause"
    topics = ("malloc", "memory-allocator", "fragmentation")
    generators = "cmake"
    exports_sources = ["CMakeLists.txt", "CMakeListsOriginal.txt", "Utilities.cmake"]
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.libstd

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["GIT_FOUND"] = False
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_Git"] = False
        cmake.definitions["without-export"] = "${BUILD_STATIC_LIBRARY}"
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self)
            args = ["--enable-static", "--disable-shared"]
            if self.options.shared:
                args = ["--enable-shared", "--disable-static"]
            self._autotools.configure(configure_dir=self._source_subfolder, args=args)
        return self._autotools

    def build(self):
        if self.settings.os == "Windows":
            os.rename("CMakeListsOriginal.txt", os.path.join(self._source_subfolder, "CMakeLists.txt"))
            os.rename("Utilities.cmake", os.path.join(self._source_subfolder, "Utilities.cmake"))
            cmake = self._configure_cmake()
            cmake.build()
        else:
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        self.copy(pattern="COPYING", src=self._source_subfolder, dst="licenses")
        if self.settings.os == "Windows":
            cmake = self._configure_cmake()
            cmake.install()
        else:
            autotools = self._configure_autotools()
            autotools.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))
        tools.rmdir(os.path.join(self.package_folder, "bin"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(["m", "dl", "pthread"])
