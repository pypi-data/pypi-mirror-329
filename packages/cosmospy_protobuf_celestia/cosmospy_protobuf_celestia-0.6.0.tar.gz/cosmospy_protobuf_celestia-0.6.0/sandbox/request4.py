import requests
import base64
import logging
import src.celestia_proto.cosmos.crypto.secp256k1.keys_pb2
import src.celestia_proto.cosmos.distribution.v1beta1.distribution_pb2
import src.celestia_proto.cosmos.distribution.v1beta1.tx_pb2
import src.celestia_proto.ibc.core.client.v1.client_pb2
import src.celestia_proto.ibc.core.client.v1.tx_pb2
import src.celestia_proto.ibc.core.channel.v1.channel_pb2
import src.celestia_proto.ibc.core.channel.v1.tx_pb2
import src.celestia_proto.ibc.lightclients.tendermint.v1.tendermint_pb2
import src.celestia_proto.cosmos.staking.v1beta1.tx_pb2
from src.celestia_proto.cosmos.tx.v1beta1 import tx_pb2
from google.protobuf.message import DecodeError
from google.protobuf.json_format import MessageToDict
from google.protobuf import any_pb2

url = "http://celestia-rpc.brightlystake.com"

logger = logging.getLogger(__name__)

def get_block_by_height(height: int):
    method = "/block"
    res = requests.get(
        url=url + method,
        params={"height": height}
    )
    return res.json()


def decoded_transaction(tx_bytes: bytes) -> dict:
    # First decode the transaction wrapper
    try:
        tx = tx_pb2.Tx()
        tx.ParseFromString(tx_bytes)
    except DecodeError as e:
        logger.error(f"Failed to decode transaction")
        raise e

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


def decoded_transactions(txs: list[str]) -> list[dict]:
    for tx in txs:
        tx_bytes = base64.b64decode(tx)
        decoded_tx = decoded_transaction(tx_bytes)
        print(decoded_tx)
    return []


def main():
    block = get_block_by_height(3805069)
    print(block.get("result",{}).get("block", {}).get("header",{}))
    raw_txs = block.get("result",{}).get("block", {}).get("data",{}).get("txs", [])
    txs = decoded_transactions(raw_txs)


if __name__ == '__main__':
    main()