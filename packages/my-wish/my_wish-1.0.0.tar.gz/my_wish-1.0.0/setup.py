from setuptools import setup

setup(
    name="my_wish",
    version="1.0.0",
    py_modules=["my_wish"],
    install_requires=["rich"],
    entry_points={
        "console_scripts": [
            "my-wish=my_wish:main",
        ],
    },
)
