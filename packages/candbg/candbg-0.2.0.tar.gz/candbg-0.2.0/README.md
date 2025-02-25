# candbg


`candbg` is a simple tool that decodes canbus messages using a provided `dbc` file and shows them as a table.


    usage: candbg [-h] [-i INTERFACE] [-c CHANNEL] dbc_file

    candbg CLI

    positional arguments:
    dbc_file              Path to the DBC file

    options:
    -h, --help            show this help message and exit
    -i INTERFACE, --interface INTERFACE
                            Interface type (default: socketcan)
    -c CHANNEL, --channel CHANNEL
                            CAN channel (default: can0)


## Other tools

You can build your own canbus testing nodes with boards that support Circuitpython.
See stuff in `embedded` folder.


## Development


*  develop and test in devcontainer (VSCode)
*  CI
    - trigger ci builds by bumping version with a tag. (see `.gitlab-ci.yml`)
    - run locally on host with `invoke ci`

## Tooling

* Automation: `invoke` - run `invoke -l` to list available commands. (uses `tasks.py`)
* Verisoning : `setuptools_scm`
* Linting and formatting : `ruff`
* Typechecking: `mypy`

## What goes where
* `src/candbg` app code. `pip install .` .
* `tasks.py` automation tasks.



