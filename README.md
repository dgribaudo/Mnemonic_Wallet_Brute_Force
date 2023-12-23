# Wallet Brute Force
This is a Brute Force program with the aim of finding balance-positive wallets by generating mnemonics.

## Installation of ETH node:
Use [this guide](https://docs.prylabs.network/docs/install/install-with-script) to run a full ETH node. Approximately 1.5T of disk and 30-40Gb of RAM is required. 
These are the flags I use to run the node:

**PRYSM**

    prysm.bat beacon-chain `
    --execution-endpoint=http://localhost:8551 `
    --mainnet `
    --jwt-secret=C:\Users\Administrator\Desktop\ethereum\jwt.hex `
    --checkpoint-sync-url=https://beaconstate.info `
    --genesis-beacon-api-url=https://beaconstate.info

**GETH**

    geth `
    --mainnet `
    --http `
    --http.api eth,net,engine,admin `
    --authrpc.jwtsecret=C:\Users\Administrator\Desktop\ethereum\jwt.hex `
    --cache 8192 `
    --maxpeers 200 `
    --rpc.batch-request-limit=10000 `
    --rpc.batch-response-max-size=250000000 `
    --rpc.evmtimeout 0

