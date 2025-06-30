import json, asyncio, base64, time, random
import aiohttp
import nacl.signing

μ = 1_000_000
LOG_FILE = "log.txt"

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
                data = json.loads(text)
                return int(data["nonce"]), float(data["balance"])
            except Exception:
                raise Exception(f"Gagal parsing balance dari server: {text}")

def make_tx(to, amount, nonce):
    tx = {
        "from": addr,
        "to_": to,
        "amount": str(amount),
        "nonce": nonce,
        "ou": "1" if amount < 1000 * μ else "3",
        "timestamp": time.time() + random.random()
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

    with open(LOG_FILE, "w") as log:
        for i, r in enumerate(recipients):
            amount = int(r["amount"])
            tx = make_tx(r["address"], amount, nonce + 1 + i)
            result = await send_tx(tx)
            tx_hash = result.get("tx_hash", "N/A")

            if result.get("status") == "accepted":
                msg = f"✅ [{i+1}] Sent {amount/μ:.6f} OCT to {r['address']} | tx_hash: {tx_hash}"
                print(msg)
                log.write(msg + "\n")
            else:
                msg = f"❌ [{i+1}] Failed to {r['address']}: {result}"
                print(msg)
                log.write(msg + "\n")

            await asyncio.sleep(1.5)

asyncio.run(main())