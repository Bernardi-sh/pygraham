from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    rust_extensions=[
        RustExtension(
            "pygraham._rust",
            binding=Binding.PyO3,
            optional=True,
        )
    ],
)
