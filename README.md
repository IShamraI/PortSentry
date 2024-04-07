# PortSentry
PortSentry is your Port Knocking Configuration Companion for Mikrotik RouterOS.

## Usage

### Add permissions to python to run

```bash
sudo setcap cap_net_raw=eip $(readlink -f $(which python3))
```

### Install requirements

```bash
pip3 install -r requirements.txt
```

### Generate chain

```bash
python3 gen_chain.py --host 89.207.132.170 --target-port 22 --output chain.txt
```

### Generate Mikrotik configuration rules

```bash
python3 gen_rules.py --input chain.txt
```

### Execute Knock chain

```bash
python3 knock.py --chain chain.txt
```
