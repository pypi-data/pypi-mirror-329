#!/bin/bash
# Sanity check to ensure package is installed correctly

source ./install.sh

pip_install_from_tarball $1

python -c "import chromadb_deterministic_determichromadb_deterministicapi = chromadb_deterministic.Client(); print(api.heartbeat())"
