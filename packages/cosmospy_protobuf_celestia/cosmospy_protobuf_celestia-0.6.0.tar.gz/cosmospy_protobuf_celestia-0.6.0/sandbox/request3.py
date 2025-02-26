import grpc
import logging
import base64
from google.protobuf.json_format import MessageToJson

from src.celestia_proto.cosmos.base.tendermint.v1beta1 import query_pb2
from src.celestia_proto.cosmos.base.tendermint.v1beta1 import query_pb2_grpc
from src.celestia_proto.cosmos.tx.v1beta1 import tx_pb2
from src.celestia_proto.celestia.blob.v1 import tx_pb2 as celestia_tx_pb2
import src.celestia_proto.cosmos.staking.v1beta1.tx_pb2
import src.celestia_proto.cosmos.distribution.v1beta1.tx_pb2
import src.celestia_proto.cosmos.crypto.secp256k1.keys_pb2
import src.celestia_proto.ibc.core.client.v1.tx_pb2
import src.celestia_proto.ibc.core.channel.v1.tx_pb2
import src.celestia_proto.ibc.lightclients.tendermint.v1.tendermint_pb2


logger = logging.getLogger(__name__)



# Create an insecure gRPC channel to the Celestia node
channel = grpc.insecure_channel("celestia-rpc.brightlystake.com:9090")

# Create a stub (client) for the Tendermint Service
stub = query_pb2_grpc.ServiceStub(channel)

# Create a request to get block 3805069
request = query_pb2.GetBlockByHeightRequest(height=3805069)

try:
    # Call the GetBlockByHeight method
    response = stub.GetBlockByHeight(request)

    print(response)
    channel.close()
    raise Exception("stop")
    # Extract the transactions from the block's data field
    txs = response.block.data.txs

    # Print the number of transactions found
    print(f"Number of transactions in block 3805069: {len(txs)}")

    # Iterate over each transaction and decode it
    for i, tx_bytes in enumerate(txs):
        try:
            # Create a Tx message object and parse the bytes
            tx = tx_pb2.Tx()
            tx.ParseFromString(tx_bytes)

            # Convert the Tx message to JSON
            tx_json = MessageToJson(tx)

            # Print the decoded transaction
            print(f"\nTransaction {i}:")
            print(tx_json)
        except Exception as e:
            # Handle any parsing errors for individual transactions
            logger.error(f"Failed to parse transaction {i}", exc_info=True)
            try:
                tx_bytes = base64.b64decode(tx_bytes)
                tx = celestia_tx_pb2.MsgPayForBlobs()
                tx = tx_pb2.Tx()
                tx.ParseFromString(tx_bytes)

                # Convert the Tx message to JSON
                tx_json = MessageToJson(tx)

                # Print the decoded transaction
                print(f"\nTransaction {i}:")
                print(tx_json)
            except Exception as e:
                logger.error(f"Failed to parse Celestia transaction {i}", exc_info=True)
                raise e
except grpc.RpcError as e:
    # Handle any gRPC errors (e.g., connection issues, invalid height)
    print(f"An error occurred: {e.code()} - {e.details()}")