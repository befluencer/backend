# Define the image names and version
BACKEND_IMAGE = befluencer/bef
BACKEND_VERSION = 3.0
BACKEND_NAME = backend-server

push:
	# Create and use buildx builder (skip if exists)
	docker buildx create --name multi-builder --use || true

	# Build and push frontend image
	docker buildx build \
		--platform linux/amd64 \
		--tag $(BACKEND_IMAGE):$(BACKEND_VERSION) \
		-f Dockerfile.prod .. \
		--push