# Stock catcher

This repo contains a little script which reads the french CAC40 stock tickers, and get the basic info of these
stocks.

We use this project to learn how to:

- Prepare your Python package for publication
- Handle versioning of your package
- Build your package and upload it to PyPI
- Understand and use different build systems

You can find the main doc on how to Prepare your Python package for publication [here](https://github.com/pengfei99/py-packaging/blob/main/docs/packaging_python_scripts.md).

The python packaging standard is **reviewed** by `Python Enhancement Proposals (PEPs)`, and **implemented** by the 
`Python Packaging Authority (PyPA)` working group.

The most important documents that define how Python packaging works are the following PEPs:

- [PEP 427](https://peps.python.org/pep-0427/) describes how wheels should be packaged.
- [PEP 440](https://peps.python.org/pep-0440/) describes how version numbers should be parsed.
- [PEP 508](https://peps.python.org/pep-0508/) describes how dependencies should be specified.
- [PEP 517](https://peps.python.org/pep-0517/) describes how a build backend should work.
- [PEP 518](https://peps.python.org/pep-0518/) describes how a build system should be specified.
- [PEP 621](https://peps.python.org/pep-0621/) describes how project metadata should be written.
- [PEP 660](https://peps.python.org/pep-0660/) describes how editable installs should be performed.

## Test the package

After installation, you can test the package by running the below command

```shell
# install the package
pip install stock_catcher

# run the command
stock_catcher
```

