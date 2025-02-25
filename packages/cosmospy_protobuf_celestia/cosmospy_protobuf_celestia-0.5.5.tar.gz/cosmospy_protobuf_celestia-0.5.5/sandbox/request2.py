import grpc
from google.protobuf.json_format import MessageToJson

# Import the compiled proto modules from src/
# Adjust these imports based on your actual file structure if needed
from src.celestia_proto.cosmos.base.tendermint.v1beta1 import query_pb2
from src.celestia_proto.cosmos.base.tendermint.v1beta1 import query_pb2_grpc

# Create an insecure gRPC channel to the Celestia node
channel = grpc.insecure_channel("celestia-rpc.brightlystake.com:9090")

# Create a stub (client) for the Tendermint Service
stub = query_pb2_grpc.ServiceStub(channel)

# Create a request to get block 3805069
request = query_pb2.GetBlockByHeightRequest(height=3805069)

try:
    # Call the GetBlockByHeight method
    response = stub.GetBlockByHeight(request)

    # Extract the block from the response and convert it to JSON
    # response.block contains the block data
    block_json = MessageToJson(response.block)

    # Print the decoded block data
    print("Decoded block data for height 3805069:")
    print(block_json)

except grpc.RpcError as e:
    # Handle any gRPC errors (e.g., connection issues, invalid height)
    print(f"An error occurred: {e.code()} - {e.details()}")