# promptgraph

A lightweight, highly concurrent execution graph framework.

1. For development, build a virtual env with: `python3 -m venv env`
2. Activate the env with the relevant activation command for your OS.
3. Run: `pip3 install -r requirements.txt`

Build distribution archives: `rm -rf dist/ && rm -rf build/ && rm -rf promptgraphtools.egg-info && python3 setup.py sdist bdist_wheel`

Upload: `python3 -m twine upload dist/*`

# NOTE:

This software is currently experimental and should not be used in a production context.

