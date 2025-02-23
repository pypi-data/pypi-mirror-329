#!/bin/bash
# Sanity check to ensure package is installed correctly

source ./install.sh

pip_install_from_tarball $1

python -c "import chromadb_deterministic_determichromadb_deterministicprint(chromadb_deterministic.__version__)"
