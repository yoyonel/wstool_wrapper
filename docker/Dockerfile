FROM holimetrix2/python:3.6-alpine3.6-grpc-numpy-scipy

COPY . /app

WORKDIR /app

RUN pip install \
	--extra-index-url https://tart.d-bi.fr/simple/ \
	--no-cache-dir \
		dist/* \
	&& \
    rm -rf ~/.cache/pip && \
    rm -rf /app

# EXPOSE 50051
# CMD ["pythie-core"]
