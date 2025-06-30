import json

TOKEN_DECIMALS = 6  # Octra biasanya 6 desimal

with open("recipients_human.json") as f:
    raw = json.load(f)

converted = [
    {
        "address": r["address"],
        "amount": str(int(float(r["amount_token"]) * 10**TOKEN_DECIMALS))
    } for r in raw
]

with open("recipients.json", "w") as f:
    json.dump(converted, f, indent=2)

print("✅ recipients.json berhasil dibuat dari recipients_human.json.")