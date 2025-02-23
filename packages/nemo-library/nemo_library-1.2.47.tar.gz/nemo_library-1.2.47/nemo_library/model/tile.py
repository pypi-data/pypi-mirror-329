from dataclasses import dataclass, field, asdict
from typing import Dict, Optional

@dataclass
class Tile:
    aggregation: str
    description: str
    descriptionTranslations: Dict[str, str]
    displayName: str
    displayNameTranslations: Dict[str, str]
    frequency: str
    graphic: str
    internalName: str
    status: str
    tileGroup: str
    tileGroupTranslations: Dict[str, str]
    tileSourceID: str
    tileSourceInternalName: str
    type: str
    unit: str
    id: str
    projectId: str
    tenant: str

    def to_dict(self):
        return asdict(self)

