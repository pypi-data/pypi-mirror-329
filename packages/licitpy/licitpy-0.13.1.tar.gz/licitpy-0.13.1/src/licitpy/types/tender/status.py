from enum import Enum


class StatusFromImage(Enum):
    PUBLISHED = "publicadas"
    AWARDED = "adjudicada"
    CLOSED = "cerrada"
    REVOKED = "revocada"
    UNSUCCESSFUL = "desierta"
    SUSPENDED = "suspendida"


class StatusFromCSV(Enum):
    PUBLISHED = "Publicada"
    AWARDED = "Adjudicada"
    CLOSED = "Cerrada"
    REVOKED = "Revocada"
    UNSUCCESSFUL = "Desierta (o art. 3 ó 9 Ley 19.886)"
    SUSPENDED = "Suspendida"


class Status(Enum):
    PUBLISHED = "PUBLISHED"
    AWARDED = "AWARDED"
    CLOSED = "CLOSED"
    REVOKED = "REVOKED"
    UNSUCCESSFUL = "UNSUCCESSFUL"
    SUSPENDED = "SUSPENDED"


class StatusFromOpenContract(Enum):
    # https://standard.open-contracting.org/1.1/en/schema/codelists/#tender-status

    PUBLISHED = "active"
    AWARDED = "complete"
    CLOSED = "closed"
    REVOKED = "cancelled"
    UNSUCCESSFUL = "unsuccessful"
    SUSPENDED = "planned"
