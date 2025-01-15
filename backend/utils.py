scam_addresses = ["0x123...", "0x456..."]

def check_scam(address):
    if address in scam_addresses:
        return {"warning": "This address is flagged as a scam."}
    return {"status": "Safe"}
