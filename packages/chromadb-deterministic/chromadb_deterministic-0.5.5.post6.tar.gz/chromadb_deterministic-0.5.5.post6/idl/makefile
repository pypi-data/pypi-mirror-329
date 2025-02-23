.PHONY: proto

proto_python:
	@echo "Generating gRPC code for python..."
	@python -m grpc_tools.protoc -I ./ --python_out=. --pyi_out=. --grpc_python_out=. ./chromadb_deterministic/proto/cchromadb_deterministicoto ./chromadb_deterministichromadb_deterministiccoordinator.proto ./chromadb_deterministic/proto/logservice.proto
	@mv chromadb_deterministic/chromadb_deterministicpy ../chromadb_deterministic/proto/
	@mv chromadb_deterministic/pchromadb_deterministicyi ../chromadb_deterministic/proto/
	@echo "Done"

proto_go:
	@echo "Generating gRPC code for golang..."
	@protoc \
		--go_out=../go/pkg/proto/coordinatorpb \
		--go_opt paths=source_relative \
		--plugin protoc-gen-go="${GOPATH}/bin/protoc-gen-go" \
    	--go-grpc_out=../go/pkg/proto/coordinatorpb \
    	--go-grpc_opt paths=source_relative \
    	--plugin protoc-gen-go-grpc="${GOPATH}/bin/protoc-gen-go-grpc" \
			chromadb_deterministic/proto/chroma.proto \
			chromadb_deterministic/proto/coordinator.proto \
			chromadb_deterministic/proto/logservice.proto
	@mv ../go/pkg/proto/coordinatorpb/chromadb_deterministic/proto/logservice*.go ../go/pkg/proto/logservicepb/
	@mv ../go/pkg/proto/coordinatorpb/chromadb_deterministic/proto/*.go ../go/pkg/proto/coordinatorpb/
	@rm -rf ../go/pkg/proto/coordinatorpb/chromadb_deterministic
	@echo "Done"
