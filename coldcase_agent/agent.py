"""ColdCase Detective AI — Multi-Agent Criminal Investigation Workflow.

Six specialized autonomous agents structured behind an Investigative Director:
1. FBI & OSINT Archive Agent — queries FBI Wanted API & cold case archives.
2. Timeline & Forensics Agent — reconstructs temporal checkpoints and alibi logs.
3. Alibi Contradiction Agent — detects inconsistencies between statements & telemetries.
4. Profiler & Hypothesis Agent — formulates motive, means & opportunity theories.
5. Senior Detective Critic — adversarially challenges the leading hypothesis.
6. Breakthrough Lead Agent — prescribes high-impact next investigative actions.

Built with google-adk.
"""

from google.adk import Agent, Workflow

from . import tools
from .schemas import (
    ContradictionResult,
    DetectiveReviewResult,
    InvestigationHypothesis,
    NextLeadAction,
)

MODEL = "gemini-3.5-flash"

# 1. FBI & OSINT Archive Agent
fbi_osint_agent = Agent(
    name="fbi_osint_agent",
    model=MODEL,
    instruction=(
        "You are an intelligence and criminal archive specialist. "
        "Call fetch_fbi_wanted_cases or load_local_cases to retrieve all files and "
        "dossiers associated with the unsolved crime query. Summarize the key "
        "elements: date, location, known modus operandi, and named persons of interest."
    ),
    tools=[tools.fetch_fbi_wanted_cases, tools.load_local_cases],
)

# 2. Timeline & Forensics Agent
timeline_agent = Agent(
    name="timeline_agent",
    model=MODEL,
    instruction=(
        "You analyze movement timelines and forensic telemetry. "
        "Call load_witness_statements for the given case id. Outline the chronological "
        "claims made by each suspect and highlight any gaps where physical location "
        "cannot be verified."
    ),
    tools=[tools.load_witness_statements],
)

# 3. Alibi Contradiction Agent
contradiction_agent = Agent(
    name="alibi_contradiction_agent",
    model=MODEL,
    instruction=(
        "You are an interrogation and contradiction detection expert. "
        "Call detect_alibi_contradictions for the suspects. Compare statements given "
        "across different years against digital, forensic, and witness evidence. "
        "Output strictly the structured ContradictionResult fields: case_id, suspect_name, "
        "original_statement, conflicting_statement_or_evidence, sources, diverging_facts."
    ),
    tools=[tools.detect_alibi_contradictions],
    output_schema=ContradictionResult,
    output_key="contradiction",
)

# 4. Profiler & Hypothesis Agent
hypothesis_agent = Agent(
    name="criminal_profiler_agent",
    model=MODEL,
    instruction=(
        "Contradiction identified: {contradiction}\n\n"
        "Call mine_cold_case_network to inspect hidden relationship graphs. Formulate ONE "
        "compelling investigative hypothesis (ID H1) detailing the suspect's motive, "
        "co-conspirators, and method. Assign a calibrated confidence score between 0.0 and 1.0."
    ),
    tools=[tools.mine_cold_case_network],
    output_schema=InvestigationHypothesis,
    output_key="hypothesis",
)

# 5. Senior Detective Critic Agent (Adversarial)
critic_agent = Agent(
    name="senior_detective_critic",
    model=MODEL,
    instruction=(
        "Contradiction: {contradiction}\nProposed Hypothesis: {hypothesis}\n\n"
        "You are a seasoned homicide and cold case detective playing devil's advocate. "
        "Critically stress-test this theory. Could the suspect have been framed? Is there an "
        "alternative suspect with equal access? Are the telemetries circumstantial? "
        "Report your verdict, evidence_quality (Strong/Moderate/Circumstantial), "
        "unresolved_blindspots, and corroborated_leads_count."
    ),
    tools=[],
    output_schema=DetectiveReviewResult,
    output_key="critic",
)

# 6. Breakthrough Lead Agent
lead_action_agent = Agent(
    name="lead_action_agent",
    model=MODEL,
    instruction=(
        "Senior Detective Review: {critic}\n\n"
        "Call recommend_breakthrough_lead to determine the single highest-value action "
        "that can definitively prove or disprove the leading theory (e.g. DNA re-testing, "
        "warrant on specific accounts, target re-interrogation). Return structured NextLeadAction."
    ),
    tools=[tools.recommend_breakthrough_lead],
    output_schema=NextLeadAction,
    output_key="next_action",
)

# Root Workflow Orchestrator
root_agent = Workflow(
    name="coldcase_investigation_director",
    edges=[
        (
            "START",
            fbi_osint_agent,
            timeline_agent,
            contradiction_agent,
            hypothesis_agent,
            critic_agent,
            lead_action_agent,
        )
    ],
)
