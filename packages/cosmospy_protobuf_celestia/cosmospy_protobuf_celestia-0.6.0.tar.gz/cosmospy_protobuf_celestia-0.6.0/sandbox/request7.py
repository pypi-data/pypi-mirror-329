import hashlib
from pprint import pprint

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

from google.protobuf.message import DecodeError
from src.celestia_proto.cosmos.tx.v1beta1 import tx_pb2 as cosmos_tx_tx_pb2
from src.celestia_proto.celestia.blob.v1 import tx_pb2 as celestia_blob_tx_pb2
from src.celestia_proto.tendermint.types import types_pb2 as cmt_types_pb2
from google.protobuf import any_pb2
from src.celestia_proto.proto.blob.v1.blob_pb2 import BlobTx
from google.protobuf.json_format import MessageToDict

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(levelname)s %(lineno)d: %(message)s")
logger = logging.getLogger(__name__)

def decoded_transaction(tx_bytes: bytes) -> dict:
    """
    Decode a Celestia transaction, handling BlobTx and regular Tx types.
    Returns a dictionary with transaction data, including MsgPayForBlobs if present.
    """
    tx_hash = hashlib.sha256(tx_bytes).hexdigest()
    tx_data = {"hash": tx_hash}  # Initialize tx_data with the hash

    # Step 1: Try decoding as BlobTx
    try:
        blob_tx = BlobTx()
        blob_tx.ParseFromString(tx_bytes)
        if blob_tx.type_id == "BLOB":  # Verify it's a BlobTx
            logger.info(f"Transaction is a BlobTx: {blob_tx.__slots__}")
            # Step 2: Decode the inner transaction
            inner_tx = cosmos_tx_tx_pb2.Tx()
            inner_tx.ParseFromString(blob_tx.tx)
            tx_data["hash"] = hashlib.sha256(blob_tx.tx).hexdigest()
            logger.info(f"Decoded inner transaction: {inner_tx}")

            # Step 3: Extract MsgPayForBlobs from inner_tx.body.messages
            messages = []
            for msg in inner_tx.body.messages:
                if msg.type_url == "/celestia.blob.v1.MsgPayForBlobs":
                    pfb = celestia_blob_tx_pb2.MsgPayForBlobs()
                    pfb.ParseFromString(msg.value)
                    messages.append({
                        "type": "MsgPayForBlobs",
                        "data": {
                            "signer": pfb.signer,
                            "namespace_ids": [ns.hex() for ns in pfb.namespaces],
                            "blob_sizes": pfb.blob_sizes,
                            # Add other fields as needed
                        }
                    })
                    logger.info(f"Decoded MsgPayForBlobs: {pfb}")
                else:
                    messages.append({
                        "type": msg.type_url,
                        "data": "Unhandled message type"
                    })

            tx_data.update({
                "type": "BlobTx",
                "inner_tx": {
                    "messages": messages,
                    "memo": inner_tx.body.memo,
                    # Add other Tx fields as needed
                    "auth_info": MessageToDict(inner_tx.auth_info),
                },
                # "blobs": [{"namespace_id": b.namespace_id.hex(), "data": b.data.hex()} for b in blob_tx.blobs],
            })
            logger.info(f"Decoded BlobTx: {tx_data}")
            return tx_data
    except DecodeError:
        logger.debug("Transaction is not a BlobTx or failed to decode as BlobTx")

    # Fallback: Decode as regular Cosmos Tx
    try:
        tx = cosmos_tx_tx_pb2.Tx()
        tx.ParseFromString(tx_bytes)
        logger.info("Transaction is a regular Cosmos Tx")
        messages = []
        for msg in tx.body.messages:
            if msg.type_url == "/celestia.blob.v1.MsgPayForBlobs":
                pfb = celestia_blob_tx_pb2.MsgPayForBlobs()
                pfb.ParseFromString(msg.value)
                messages.append({
                    "type": "MsgPayForBlobs",
                    "data": {
                        "signer": pfb.signer,
                        "namespace_ids": [ns.hex() for ns in pfb.namespace_ids],
                        "blob_sizes": pfb.blob_sizes,
                    }
                })
                logger.info(f"Decoded MsgPayForBlobs: {pfb}")
            else:
                messages.append({
                    "type": msg.type_url,
                    "data": "Unhandled message type"
                })

        tx_data.update({
            "type": "Tx",
            "messages": messages,
            "memo": tx.body.memo,
            # Add other Tx fields as needed
        })
        return tx_data
    except DecodeError as e:
        raise DecodeError(f"Failed to decode transaction: {tx_bytes}") from e

def main():
    block_number = 3805069
    with grpc.insecure_channel("celestia-rpc.brightlystake.com:9090") as channel:
        from src.celestia_proto.cosmos.base.tendermint.v1beta1 import query_pb2, query_pb2_grpc
        stub = query_pb2_grpc.ServiceStub(channel)
        request = query_pb2.GetBlockByHeightRequest(height=block_number)
        response = stub.GetBlockByHeight(request)

    txs = response.block.data.txs
    logger.info(f"Number of transactions in block {block_number}: {len(txs)}")

    for i, tx_bytes in enumerate(txs):
        try:
            logger.info(f"Decoding transaction {i}")
            tx_data = decoded_transaction(tx_bytes)
            pprint(tx_data)
        except Exception as e:
            logger.error(f"Failed to parse transaction {i}", exc_info=True)
            raise Exception(f"Failed to parse transaction {i}") from e

if __name__ == "__main__":
    main()