from distutils.core import setup

setup(name="finddata",
      version="0.2.2",
      description = "Find data files using ICAT",
      author = "Pete Peterson",
      author_email = "petersonpf@ornl.gov",
      url = "http://github.com/peterfpeterson/finddata/",
      long_description = """This package uses ICAT4 at SNS to find NeXus files.""",
      license = "The MIT License (MIT)",
      scripts=["finddata"],
      data_files=[('/etc/bash_completion.d/', ['finddata.bashcomplete'])]
)
