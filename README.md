# finddata

A program to find data files using ONCat.

## Getting Started with Pixi

This project uses [Pixi](https://pixi.sh) for managing dependencies and development environments.

### Prerequisites

1.  **Install Pixi**: Follow the instructions on the [official Pixi installation guide](https://pixi.sh/latest/installation/).
2.  **Git**: You'll need Git to clone the repository.

### Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/neutrons/finddata.git
    cd finddata
    ```

2.  **Install dependencies:**
    Run the following command in the project root to install all dependencies defined in the `pyproject.toml` file and set up the Pixi environment:
    ```bash
    pixi install
    ```
    This command creates a virtual environment in `.pixi` and installs all necessary tools and libraries. Bash completion, if supported via `argcomplete`, should be available in the Pixi environment.

### Running Tests

To run the test suite, use the following command:
```bash
pixi run test
```

### Building Packages

You can build PyPI and Conda packages using Pixi tasks:

*   **Build PyPI packages (wheel and sdist):**
    ```bash
    pixi run build-pypi
    ```
    The built packages will be located in the `dist/` directory.

*   **Build Conda package:**
    ```bash
    pixi run build-conda
    ```
    The built Conda package will be located in the `conda.recipe/` directory (typically under a subdirectory like `noarch/`).

## Configuration

If you want to use `finddata.publish_plot()`, the configuration file `/etc/autoreduce/post_processing.conf` must be in place with the url and credentials. It is advised that this be readable only by the process using the functionality.
