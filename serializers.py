from models import Partner
from shapely import wkb

class PartnerSerializer:
    def serialize(partner: Partner):
        if partner:
            return {
                "id": partner.id,
                "tradingName": partner.tradingName,
                "ownerName": partner.ownerName,
                "document": partner.document,
                "coverageArea": str(wkb.loads(str(partner.coverageArea), hex=True)),
                "address": str(wkb.loads(str(partner.address), hex=True))
            }
        return {}