from setuptools import setup, find_packages

setup(
    name="cisco-product-ui",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A UI application for querying data about Cisco products.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "SPARQLWrapper",
        "PyQt5"  # or any other UI framework you choose
    ],
    entry_points={
        "console_scripts": [
            "cisco-product-ui=ui.main_window:main",  # Adjust based on your main function location
        ],
    },
)