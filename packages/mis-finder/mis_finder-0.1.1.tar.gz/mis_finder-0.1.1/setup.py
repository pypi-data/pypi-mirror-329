from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import numpy


class build_ext_subclass(build_ext):
    def run(self):
        self.include_dirs.append(numpy.get_include())
        super().run()

setup(
    name="mis_finder",
    packages=["mis_finder"],
    package_dir={"": "src"},
    ext_modules=[
        Extension(
            "mis_finder.mis",
            sources=["src/mis_finder/_core/mis.c"],
            include_dirs=[numpy.get_include()],
            # Make sure you set the right compiler flags for mingw
            extra_compile_args=["-O2"],
            extra_link_args=[],
        )
    ],
    cmdclass={"build_ext": build_ext_subclass},
    options={"build_ext": {"compiler": "mingw32"}},
)
