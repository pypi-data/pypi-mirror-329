import chromadb_deterministic
import chromadb_deterministic.config
from chromadb_deterministic.server.fastapi import FastAPI

settings = chromadb.config.Settings()
server = FastAPI(settings)
app = server.app()
