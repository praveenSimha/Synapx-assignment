from typing import List, Optional
from pydantic import BaseModel, Field


class PolicyInfo(BaseModel):
    policy_number: Optional[str] = Field(None, description="Policy number associated with the claim")
    policyholder_name: Optional[str] = Field(None, description="Name of the policyholder")
    effective_date: Optional[str] = Field(None, description="Policy effective start date")
    expiration_date: Optional[str] = Field(None, description="Policy expiration date")


class IncidentInfo(BaseModel):
    date: Optional[str] = Field(None, description="Date of the incident")
    time: Optional[str] = Field(None, description="Time of the incident")
    location: Optional[str] = Field(None, description="Location where the incident occurred")
    description: Optional[str] = Field(None, description="Brief description of how the loss occurred")


class InvolvedParty(BaseModel):
    name: Optional[str] = Field(None, description="Name of the involved party")
    role: Optional[str] = Field(None, description="Role: Claimant, Driver, Passenger, Witness, etc.")
    contact_info: Optional[str] = Field(None, description="Phone number or email")


class AssetDetails(BaseModel):
    asset_type: Optional[str] = Field(None, description="Type of asset (e.g., Vehicle, Property)")
    asset_id: Optional[str] = Field(None, description="VIN, License Plate, or Property Address")
    estimated_damage: Optional[str] = Field(None, description="Estimated damage amount")


class ExtractedFields(BaseModel):
    policy_info: PolicyInfo
    incident_info: IncidentInfo
    involved_parties: List[InvolvedParty] = Field(default_factory=list)
    asset_details: List[AssetDetails] = Field(default_factory=list)
    claim_type: Optional[str] = Field(None, description="Type of claim (e.g., Collision, Injury, Theft)")
    initial_estimate: Optional[float] = Field(None, description="Numeric value of initial estimate")


class AgentOutput(BaseModel):
    extractedFields: ExtractedFields
    missingFields: List[str] = Field(default_factory=list, description="List of mandatory fields that were not found")
    recommendedRoute: str = Field(..., description="Fast-track, Manual review, Specialist Queue, or Investigation Flag")
    reasoning: str = Field(..., description="Explanation for the routing decision")
