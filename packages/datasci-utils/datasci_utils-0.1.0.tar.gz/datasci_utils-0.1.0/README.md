# Create a python environment
poetry config --list
poetry config virtualenvs.in-project true
poetry env activate
poetry run which python

# Install dependencies
poetry install
poetry lock

# Poetry publish package
poetry pubñish