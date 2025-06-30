# 🪙 Octra Testnet Multi-Send Tool

A simple, fast, and reliable Python script to perform **bulk token transfers** on the [Octra Testnet](https://octra.network).  
Supports automatic nonce handling, timestamp deduplication, configurable delays, and logging.

---

## ✨ Features

- 🚀 Multi-send to 10+ wallets in one run
- 🔐 Safe signing with local private key
- 🔁 Optional delay to prevent nonce/mempool collision
- 🧠 Timestamp randomization to prevent duplicate TX rejection
- 📝 Logs each transaction to `log.txt`

---

## 🧩 Requirements

```bash
pip install aiohttp pynacl
```

> ✅ Supports Python 3.8+  
> ⚠️ Use only with Octra **Testnet**

---

## 🗂 Files

| File                             | Description                                  |
|----------------------------------|----------------------------------------------|
| `wallet.json`                    | Your sender account + private key (base64)   |
| `recipients_human.json`         | Easy-to-edit list of recipients (0.01 format)|
| `buildRecipients.py`            | Converts human format → blockchain format    |
| `multi_send_simple_with_log.py` | Main script to send and log multi-transfers  |
| `log.txt`                        | Output log of all transactions               |

---

## 🔐 wallet.json Format

```json
{
  "priv": "BASE64_PRIVATE_KEY_32_BYTES",
  "addr": "oct1xxxxxx...",
  "rpc": "https://octra.network"
}
```

---

## 📥 How to Use

### 1. Edit `recipients_human.json`

```json
[
  { "address": "oct1abc...", "amount_token": 0.01 },
  { "address": "oct1def...", "amount_token": 0.03 }
]
```

### 2. Generate `recipients.json`

```bash
python buildRecipients.py
```

### 3. Run the Multi-Send

```bash
python multi_send_simple_with_log.py
```

---

## 📄 Example Output

```bash
👛 Address : oct1abcxyz...
💰 Balance : 672.180993 OCT
🔢 Nonce   : 7
📤 Sending to 10 recipients...

✅ [1] Sent 0.010000 OCT to oct1xxx | tx_hash: abc123...
❌ [2] Failed to oct1yyy: {"error": "Duplicate transaction"}
...
```

---

## 🧪 Notes

- This tool is designed for **testnet only**
- TXs go into the **staging pool** before being finalized
- Duplicate TXs with same content will be rejected unless timestamp is randomized

---

## 📜 License

MIT — free for personal & testing use.