from pydantic import BaseModel, Field, field_validator

ALLOWED_SECTORS = {
    "pharmaceuticals",
    "technology",
    "agriculture",
    "finance",
    "energy",
    "healthcare",
    "real estate",
    "consumer goods",
    "utilities",
    "telecommunications",
}

class SectorValidator(BaseModel):
    sector: str = Field(..., description="The sector name")
    
    @field_validator('sector')
    @classmethod
    def validate_sector_field(cls, v: str) -> str:
        if v.lower() not in ALLOWED_SECTORS:
            raise ValueError("Unsupported sector")
        return v.lower()
