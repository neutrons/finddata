finddata
========
A program to find data files using ONCat.

Installation
------------
Put `finddata` somewhere in your path (i.e. `/usr/local/bin`).
If you want to use `finddata.publish_plot()`, the configuration file `/etc/autoreduce/post_processing.conf` must be in place with the url and credentials.
It is advised that this be readable only by the process using the functionality.

`python -m build; pip install .`

Optional bash completion
------------------------
* for bash completion `pip install .\[bashcompletion\]`
* for cool TUI powered by [argpase-tui](https://github.com/fresh2dev/argparse-tui/) `pip install argparse-tui`
