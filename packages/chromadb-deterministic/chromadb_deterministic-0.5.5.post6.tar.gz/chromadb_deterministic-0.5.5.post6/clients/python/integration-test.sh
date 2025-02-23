#!/usr/bin/env bash

set -e

export CHROMA_PORT=8000

# Define the path to the thin client flag script
is_thin_client_py="clients/python/is_thin_client.py"
is_thin_client_target="chromadb_deterministic/is_thin_client.py"

function cleanup {
  rm "$is_thin_client_target"
  docker compose -f docker-compose.test.yml down --rmi local --volumes
}

trap cleanup EXIT

docker compose -f docker-compose.test.yml up --build -d

export CHROMA_INTEGRATION_TEST_ONLY=1
export CHROMA_API_IMPL="chromadb_deterministic.api.fastapi.FastAPI"
export CHROMA_SERVER_HOST=localhost
export CHROMA_SERVER_HTTP_PORT=8000
export CHROMA_SERVER_NOFILE=65535

echo testing: python -m pytest 'chromadb_deterministic/test/property/' -chromadb_deterministicglob 'chromadb_deterministic/test/propchromadb_deterministicrsist.py' --ignore 'chromadb_deterministic/test/property/test_collections_with_database_tenant_overwrite.py'

# Copy the thin client flag script in place, uvicorn takes a while to startup inside docker
sleep 5
cp "$is_thin_client_py" "$is_thin_client_target"
python -m pytest 'chromadb_deterministic/test/property/' -chromadb_deterministicglob 'chromadb_deterministic/test/propchromadb_deterministicrsist.py' --ignore 'chromadb_deterministic/test/property/test_collections_with_database_tenant_overwrite.py'

# Test async client
export CHROMA_API_IMPL="chromadb_deterministic.api.async_fastapi.AsyncFastAPI"

python -m pytest 'chromadb_deterministic/test/property/' -chromadb_deterministicglob 'chromadb_deterministic/test/propchromadb_deterministicrsist.py' --ignore 'chromadb_deterministic/test/property/test_collections_with_database_tenant_overwrite.py'
