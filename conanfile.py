import glob
import os

from conans import CMake, ConanFile, tools


class NLOptConan(ConanFile):
    name = "nlopt"
    version = "2.6.1"
    description = (
        "library for nonlinear optimization, wrapping many"
        " algorithms for global and local, constrained or unconstrained, optimization"
    )
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("non-linear", "optimization")
    url = "https://github.com/rhololkeolke/conan-nlopt"
    homepage = "https://nlopt.readthedocs.io/en/latest/"
    author = "Devin Schwab <dschwab@andrew.cmu.edu>"
    license = (
        "LGPL-2.0-or-later"
    )  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]  # Packages the license for the
    exports_sources = ["CMakeLists.txt"]
    # conanfile.py
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/stevengj/nlopt"
        tools.get(
            "{0}/archive/v{1}.tar.gz".format(source_url, self.version),
            sha256="66d63a505187fb6f98642703bd0ef006fedcae2f9a6d1efa4f362ea919a02650",
        )
        extracted_dir = self.name + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["NLOPT_TESTS"] = False
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        # Disable optional components
        cmake.definitions["NLOPT_GUILE"] = False
        cmake.definitions["NLOPT_MATLAB"] = False
        cmake.definitions["NLOPT_OCTAVE"] = False
        cmake.definitions["NLOPT_PYTHON"] = False
        cmake.definitions["NLOPT_SWIG"] = False
        cmake.definitions["NLOPT_TESTS"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.libs.append("m")
