import grpc
# from google.protobuf import symbol_database
from src.celestia_proto.cosmos.tx.v1beta1 import service_pb2, service_pb2_grpc
# from src.celestia_proto.celestia.blob.v1 import tx_pb2 as celestia_tx_pb2


def register_types():
    """Register Celestia-specific message types"""
    # Create a mapping of type URLs to message types
    type_urls = {
        "/celestia.blob.v1.MsgPayForBlobs": celestia_tx_pb2.MsgPayForBlobs,
    }
    sym_db = symbol_database.Default()
    for type_url, message_class in type_urls.items():
        sym_db.RegisterMessage(message_class)



def main():
    # register_types()
    channel = grpc.insecure_channel("celestia-rpc.brightlystake.com:9090")
    stub = service_pb2_grpc.ServiceStub(channel)
    request = service_pb2.GetBlockWithTxsRequest(height=3805069)
    block = stub.GetBlockWithTxs(request)
    print(block)


if __name__ == '__main__':
    main()