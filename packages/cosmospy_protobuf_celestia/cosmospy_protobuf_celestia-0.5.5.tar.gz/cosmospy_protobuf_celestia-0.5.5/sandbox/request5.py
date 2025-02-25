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
from google.protobuf.json_format import MessageToDict
from google.protobuf import any_pb2
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
            logger.warning(f"Failed to decode transaction with message type: {msg.DESCRIPTOR.name}")
            continue
    else:
        raise DecodeError(f"Failed to decode transaction")

    logger.info(f"Decodec tx: {tx}")
    # Convert basic transaction info to dict
    tx_data = {
        'body': {
            'messages': [],
            'memo': tx.body.memo,
            'timeout_height': tx.body.timeout_height,
        },
        'auth_info': MessageToDict(tx.auth_info),
        'signatures': [sig.hex() for sig in tx.signatures]
    }

    # Decode each message in the transaction
    for msg in tx.body.messages:
        try:
            # Unpack the Any message
            msg_any = any_pb2.Any()
            msg_any.CopyFrom(msg)

            # Add the message type and content to the result
            decoded_msg = {
                'type_url': msg_any.type_url,
                'value': MessageToDict(msg_any)
            }
            tx_data['body']['messages'].append(decoded_msg)

            logger.info(f"Decoded message type: {msg_any.type_url}")
        except Exception as e:
            logger.error(f"Failed to decode message: {str(e)}")

    return tx_data

def _decoded_transaction(tx_bytes: bytes):
    logger.info(f"Decoding transaction")


def main():
    with grpc.insecure_channel("celestia-rpc.brightlystake.com:9090") as channel:
        stub = query_pb2_grpc.ServiceStub(channel)
        request = query_pb2.GetBlockByHeightRequest(height=3805069)
        response = stub.GetBlockByHeight(request)

    txs = response.block.data.txs
    logger.info(f"Number of transactions in block 3805069: {len(txs)}")

    # Iterate over each transaction and decode it
    for i, tx_bytes in enumerate(txs):
        try:
            logger.info(f"Decoding transaction {i}")
            tx_data = decoded_transaction(tx_bytes)
            logger.info(str(tx_data)[:100])
        except Exception:
            logger.error(f"Failed to parse transaction {i}: {str(tx_bytes)[:100]}", exc_info=True)
            # raise Exception("Failed to parse transaction")


if __name__ == '__main__':
    main()
