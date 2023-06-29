from models import Partner

import json

class PartnerSerializer:
    def serialize(partner: Partner):
        if partner:
            # Convert the result to a dictionary and parse 'coverageArea' and 'address' to GeoJSON
            partner_dict = dict(partner)
            partner_dict["coverageArea"] = json.loads(partner_dict["coverageArea"])
            partner_dict["address"] = json.loads(partner_dict["address"])
            return {
                "id": partner_dict["id"],
                "tradingName": partner_dict["tradingName"],
                "ownerName": partner_dict["ownerName"],
                "document": partner_dict["document"],
                "coverageArea": partner_dict["coverageArea"],
                "address": partner_dict["address"]
            }
        return {}