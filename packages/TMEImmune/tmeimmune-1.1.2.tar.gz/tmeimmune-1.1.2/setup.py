from setuptools import setup, find_packages

VERSION = '1.1.2' 
DESCRIPTION = 'Python package for calculating TME scores'


# Setting up
setup(
        name="TMEImmune", 
        version=VERSION,
        author="Qilu Zhou",
        author_email="<qiluzhou@umass.edu>",
        url="https://github.com/qiluzhou/TMEImmune",
        description=DESCRIPTION,
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=["pandas>=1.5.0", "numpy>=1.23.5", "cmapPy", "rnanorm", "gseapy == 0.11.0",
                          "inmoose", "lifelines", "scikit-learn", "matplotlib", "requests"], 
        keywords=['python', 'TME score'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        python_requires=">=3.10"
)