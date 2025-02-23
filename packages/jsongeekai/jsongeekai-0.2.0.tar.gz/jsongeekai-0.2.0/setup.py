from setuptools import setup, find_packages

setup(
    name="jsongeekai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "numba>=0.57.0",
        "py-cpuinfo>=9.0.0",
        "json5>=0.9.14",
        "pyyaml>=6.0.1",
        "msgpack>=1.0.7",
        "psutil>=5.9.0"
    ],
    extras_require={
        "test": [
            "pytest>=7.4.0",
            "pytest-benchmark>=4.0.0"
        ]
    }
)
