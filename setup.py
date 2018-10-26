import versioneer # https://github.com/warner/python-versioneer
from distutils.core import setup

setup(name="finddata",
      version=versioneer.get_version(), #"0.2.2",
      cmdclass=versioneer.get_cmdclass(),
      description = "Find data files using ONCat",
      author = "Pete Peterson",
      author_email = "petersonpf@ornl.gov",
      url = "http://github.com/peterfpeterson/finddata/",
      long_description = """This package uses ONCat at SNS to find NeXus files.""",
      license = "The MIT License (MIT)",
      scripts=["scripts/finddata"],
      packages=["finddata"],
      package_dir={},#'finddata': '.'},
      data_files=[('/etc/bash_completion.d/', ['finddata.bashcomplete'])]
)
