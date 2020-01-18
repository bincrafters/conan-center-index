from conans import ConanFile, tools, AutoToolsBuildEnvironment, MSBuild
import os


class PremakeConan(ConanFile):
    name = "premake"
    version = "5.0.0-alpha14"
    topics = ("conan", "premake", "build", "build-systems")
    description = "Describe your software project just once, using Premake's simple and easy to read syntax, and build it everywhere"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://premake.github.io/"
    license = "BSD-3-Clause"
    settings = "os_build", "arch_build", "compiler"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    @property
    def _platform(self):
        return {'Windows': 'gmake.windows',
                'Linux': 'gmake.unix',
                'Macos': 'gmake.macosx'}.get(str(self.settings.os_build))

    def build(self):
        if self.settings.os_build == "Windows" and self.settings.compiler == "Visual Studio":
            platform = "vs2017"
        else:
            platform = self._platform

        with tools.chdir(os.path.join(self._source_subfolder, 'build', platform)):
            if self.settings.os_build == "Windows": 
                if self.settings.compiler == "Visual Studio":
                    msbuild = MSBuild(self)
                    msbuild.build("Premake5.sln", platforms={'x86': 'Win32', 'x86_64': 'x64'}, build_type="Release", arch=self.settings.arch_build)
                else:
                    env_build = AutoToolsBuildEnvironment(self)
                    arch = "x86" if self.settings.arch_build == "x86" else "x64"
                    env_build.make(args=['config=release_{}'.format(arch)])
            else:
                env_build = AutoToolsBuildEnvironment(self)
                env_build.make(args=['config=release'])

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*premake5.exe", dst="bin", keep_path=False)
        self.copy(pattern="*premake5", dst="bin", keep_path=False)


    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)

    def package_id(self):
        del self.info.settings.compiler
