import grpc
from concurrent import futures

# Assuming generated classes would be available as summit_pb2_grpc and summit_pb2
# from app.grpc import summit_pb2_grpc, summit_pb2


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    # summit_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
