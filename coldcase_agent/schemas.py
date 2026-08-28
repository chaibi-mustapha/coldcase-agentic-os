"""Pydantic schemas defining the structured outputs passed between agents."""
from typing import List, Optional
from pydantic import BaseModel, Field


class TimelineBreakdown(BaseModel):
    case_id: str
    event_timestamp: str
    location: str
    witnesses_present: List[str]
    suspect_claimed_location: str
    inconsistency_flag: bool = Field(
        description="True if the suspect alibi conflicts with physical evidence or witness statements."
    )
    notes: str


class ContradictionResult(BaseModel):
    case_id: str
    suspect_name: str
    original_statement: str
    conflicting_statement_or_evidence: str
    sources: List[str]
    diverging_facts: List[str] = Field(
        description="List of factual fields that directly contradict the suspect's claims."
    )


class InvestigationHypothesis(BaseModel):
    hypothesis_id: str
    suspect_or_theory: str
    motive_and_opportunity: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Probability score (0.0 to 1.0) based on graph correlation and corroborated evidence."
    )
    key_vulnerabilities: str = Field(
        description="Unverified assumptions or gaps in this hypothesis."
    )


class DetectiveReviewResult(BaseModel):
    verdict: str = Field(
        description="Senior detective critical evaluation of the leading theory."
    )
    evidence_quality: str = Field(
        description="Strong, Moderate, or Circumstantial"
    )
    lead_strength_score: float = Field(ge=0.0, le=1.0)
    unresolved_blindspots: List[str]
    corroborated_leads_count: int


class NextLeadAction(BaseModel):
    action_id: str
    objective: str
    recommended_forensics_or_interrogation: str
    expected_breakthrough_gain: float = Field(
        ge=0.0,
        le=1.0,
        description="Expected informational value of executing this action."
    )
    targeted_suspects: List[str]
