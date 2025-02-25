# NeurionPy

NeurionPy is the official Python SDK for interacting with the **Neurion** blockchain, a Cosmos SDK-based network designed for **privacy-preserving AI, federated learning, and decentralized automation**. NeurionPy provides developers with all the necessary tools to create wallets, sign transactions, and interact with various modules on the blockchain.

## Features
- **Wallet Management**: Generate wallets from private keys, mnemonics, or existing addresses.
- **Transaction Signing**: Sign and broadcast transactions securely.
- **Querying the Blockchain**: Retrieve blockchain state, account balances, and contract data.
- **Module Interactions**: Full support for all Neurion modules:
  - **Sanctum**: Privacy-preserving dataset sharing and usage requests.
  - **Crucible**: Federated learning, model training, and validation.
  - **Fusion**: AI model aggregation and dispute resolution.
  - **Ganglion**: AI agent and workflow automation.
- **GRPC & REST Support**: Seamlessly interact with the Neurion blockchain via GRPC and REST APIs.

## Installation
Install NeurionPy using pip:
```sh
pip install neurionpy
```

Package available on PyPI: [NeurionPy](https://pypi.org/project/neurionpy/)

## Getting Started
### Importing NeurionPy
```python
import grpc
from neurionpy.synapse.client import NeurionClient, NetworkConfig
from neurionpy.synapse.wallet import LocalWallet
```

### Creating a Wallet
```python
wallet = LocalWallet.from_mnemonic(
    "your mnemonic here",
    "neurion"
)
print("Address:", wallet.address)
```

### Connecting to Neurion
```python
client = NeurionClient(NetworkConfig.neurion_localnet(), wallet)
```

## Module Interactions

Below are **examples** of interactions with the different Neurion modules. More operations are supported; refer to the API documentation for the full list.

### Sanctum (Privacy-Preserving Dataset Management)
#### Example: Submitting a Dataset Application
```python
tx = client.sanctum.tx.SubmitDatasetApplication(
    message=MsgSubmitDatasetApplication(
        creator=str(wallet.address()),
        encrypted_data_link="https://encrypted_data_link",
        explanation_link="https://explanation_link",
        contact="contact",
        stake=100000000,
        proof_of_authenticity="proof_of_authenticity",
        dataset_usage_fee=100000000
    )
)
print(f"TX {tx.tx_hash} submitted.")
```
Other available Sanctum operations:
- Approve dataset applications
- Request to use datasets
- Manage dataset processing

### Crucible (Federated Learning & Model Validation)
#### Example: Registering as a Model Trainer
```python
tx = client.crucible.tx.RegisterTrainer(
    message=MsgRegisterTrainer(
        creator=str(wallet.address()),
        task_id=1
    )
)
print(f"Trainer Registration TX: {tx.tx_hash}")
```
Other available Crucible operations:
- Submit training results
- Stake tokens to tasks
- Report model plagiarism

### Fusion (AI Model Aggregation & Dispute Resolution)
#### Example: Proposing a Model for a Task
```python
tx = client.fusion.tx.ProposeModel(
    message=MsgProposeModel(
        creator=str(wallet.address()),
        task_id=1,
        model_link="https://model_link",
        metadata_link="https://metadata_link"
    )
)
print(f"Model Proposal TX: {tx.tx_hash}")
```
Other available Fusion operations:
- Register as a proposer or validator
- Dispute model scores
- Claim rewards from tasks

### Ganglion (AI Agent & Workflow Automation)
#### Example: Registering an AI Agent (Ion)
```python
tx = client.ganglion.tx.RegisterIon(
    message=MsgRegisterIon(
        capacities=["SCRAPER", "EXTRACTOR"],
        stake=10000000,
        endpoints=["http://localhost", "http://66.63.66.66"],
        description="A scraper and extractor",
        input_schema='{"name":"string","flag":"boolean"}',
        output_schema='{"another_flag":"boolean","fullname":"string"}',
        fee_per_thousand_calls=18,
    )
)
print(f"Ion Registration TX: {tx.tx_hash}")
```
Other available Ganglion operations:
- Report and validate Ions
- Register and update pathways
- Stake and claim rewards from Ganglion

## License
This project is licensed under the **MIT License**.

## Disclaimer
Use NeurionPy at your own risk. Ensure you store private keys securely and follow best security practices when interacting with blockchain assets.

