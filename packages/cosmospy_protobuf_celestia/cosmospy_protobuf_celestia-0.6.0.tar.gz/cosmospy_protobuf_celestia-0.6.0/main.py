import base64
from tx_data import txs
from src.celestia_proto.cosmos.tx.v1beta1 import tx_pb2

def main():
    for raw_tx in txs:
        tx_binary = base64.b64decode(raw_tx)
        tx = tx_pb2.Tx()
        res = tx.ParseFromString(tx_binary)
        print(res)
        for msg in tx.body.messages:
            print(msg)



if __name__ == '__main__':
    main()
