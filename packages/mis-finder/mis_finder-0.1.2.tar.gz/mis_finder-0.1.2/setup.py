from setuptools import setup, Extension
import numpy


setup(
    name="mis_finder",
    packages=["mis_finder"],
    package_dir={"": "src"},
    ext_modules=[
        Extension(
            "mis_finder.mis",
            sources=["src/mis_finder/_core/mis.c"],
            include_dirs=[numpy.get_include()],
            extra_compile_args=["-O2"],
            extra_link_args=[],
            define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
        )
    ],
    options={"build_ext": {"compiler": "mingw32"}},
)
