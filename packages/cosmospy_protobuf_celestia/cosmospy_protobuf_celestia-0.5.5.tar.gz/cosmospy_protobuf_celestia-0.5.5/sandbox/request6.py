import grpc
import logging
import sys
import src.celestia_proto.cosmos.crypto.secp256k1.keys_pb2
import src.celestia_proto.cosmos.distribution.v1beta1.distribution_pb2
import src.celestia_proto.cosmos.distribution.v1beta1.tx_pb2
import src.celestia_proto.ibc.core.client.v1.client_pb2
import src.celestia_proto.ibc.core.client.v1.tx_pb2
import src.celestia_proto.ibc.core.channel.v1.channel_pb2
import src.celestia_proto.ibc.core.channel.v1.tx_pb2
import src.celestia_proto.ibc.lightclients.tendermint.v1.tendermint_pb2
import src.celestia_proto.cosmos.staking.v1beta1.tx_pb2
from src.celestia_proto.cosmos.base.tendermint.v1beta1 import query_pb2
from src.celestia_proto.cosmos.base.tendermint.v1beta1 import query_pb2_grpc


from google.protobuf.message import DecodeError
from src.celestia_proto.cosmos.tx.v1beta1 import tx_pb2 as cosmos_tx_tx_pb2
from src.celestia_proto.celestia.blob.v1 import tx_pb2 as celestia_blob_tx_pb2


logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def decoded_transaction(tx_bytes: bytes) -> dict:
    candidate_messages = [
        cosmos_tx_tx_pb2.Tx,
        celestia_blob_tx_pb2.MsgPayForBlobs,
    ]
    for msg in candidate_messages:
        try:
            tx = msg()
            tx.ParseFromString(tx_bytes)
            logger.info(f"Decoded transaction with message type: {msg.DESCRIPTOR.name}")
            break
        except DecodeError:
            logger.warning(f"Failed to decode transaction with message type: {msg.DESCRIPTOR.name}", exc_info=True)
            continue
    else:
        raise DecodeError(f"Failed to decode transaction: {tx_bytes}")

    logger.info(f"Decodec tx: {tx}")
    # Convert basic transaction info to dict
    tx_data = {
        ...
    }
    return tx_data


def main():
    block_number = 3805069
    with grpc.insecure_channel("celestia-rpc.brightlystake.com:9090") as channel:
        stub = query_pb2_grpc.ServiceStub(channel)
        request = query_pb2.GetBlockByHeightRequest(height=block_number)
        response = stub.GetBlockByHeight(request)

    txs = response.block.data.txs
    logger.info(f"Number of transactions in block {block_number}: {len(txs)}")

    for i, tx_bytes in enumerate(txs):
        try:
            logger.info(f"Decoding transaction {i}")
            tx_data = decoded_transaction(tx_bytes)
            logger.info(str(tx_data)[:100])
        except Exception:
            logger.error(f"Failed to parse transaction {i}", exc_info=True)
            raise Exception("Failed to parse transaction")


if __name__ == '__main__':
    main()
