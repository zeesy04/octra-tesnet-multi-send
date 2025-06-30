import json, asyncio, base64, time, hashlib
import aiohttp
import nacl.signing

μ = 1_000_000

with open("wallet.json") as f:
    wallet = json.load(f)

with open("recipients.json") as f:
    recipients = json.load(f)

priv = wallet["priv"]
addr = wallet["addr"]
rpc = wallet.get("rpc", "https://octra.network")

sk = nacl.signing.SigningKey(base64.b64decode(priv))
pub = base64.b64encode(sk.verify_key.encode()).decode()

async def send_tx(tx):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{rpc}/send-tx", json=tx) as resp:
            try:
                return await resp.json()
            except:
                return {"status": "error", "detail": await resp.text()}

async def get_nonce_balance():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{rpc}/balance/{addr}") as resp:
            text = await resp.text()
            try:
                balance_str, nonce_str = text.strip().split()
                return int(nonce_str), float(balance_str)
            except Exception as e:
                raise Exception(f"Gagal parsing balance dari server: {text}")

def make_tx(to, amount, nonce):
    tx = {
        "from": addr,
        "to_": to,
        "amount": str(amount),
        "nonce": nonce,
        "ou": "1" if amount < 1000 * μ else "3",
        "timestamp": time.time() + 0.001
    }
    body = json.dumps(tx, separators=(",", ":"))
    sig = base64.b64encode(sk.sign(body.encode()).signature).decode()
    tx["signature"] = sig
    tx["public_key"] = pub
    return tx

async def main():
    nonce, balance = await get_nonce_balance()
    print(f"👛 Address : {addr}")
    print(f"💰 Balance : {balance:.6f} OCT")
    print(f"🔢 Nonce   : {nonce}")
    print(f"📤 Sending to {len(recipients)} recipients...\n")

    for i, r in enumerate(recipients):
        amount = int(r["amount"])
        tx = make_tx(r["address"], amount, nonce + 1 + i)
        result = await send_tx(tx)
        if result.get("status") == "accepted":
            print(f"✅ [{i+1}] Sent {amount/μ:.6f} OCT to {r['address']}")
        else:
            print(f"❌ [{i+1}] Failed to {r['address']}: {result}")

asyncio.run(main())