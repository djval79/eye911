"""Mock version of enrichment module for testing"""

async def vin_lookup(plate, state):
    return ("1HGBH41JXMN109186", {"fname": "Jane", "lname": "Doe"})
    
async def phone_from_vin(vin):
    return "+15551234567"
    
async def enrich(msg):
    vin, owner = await vin_lookup(msg["plate"], msg["state"])
    phone = await phone_from_vin(vin)
    return {
        "fname": owner["fname"],
        "lname": owner["lname"],
        "phone": phone,
        "vin": vin
    }
