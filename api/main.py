"""FastAPI Backend for ColdCase Detective AI — Criminal Investigation Console."""

import json
import os
import uuid
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from coldcase_agent.tools import fetch_live_online_case

MOCK_MODE = os.getenv("MOCK_MODE", "1") == "1"

app = FastAPI(title="ColdCase Detective AI — Investigation Intelligence OS")

WEB_DIR = os.path.join(os.path.dirname(__file__), "..", "web")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
if os.path.exists(WEB_DIR):
    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


class CaseInvestigationRequest(BaseModel):
    query: str
    case_id: str = "CASE-1998-BERLIN-VAULT"
    suspect_name: str = "Victor Vance"
    session_id: str | None = None


class LiveFetchRequest(BaseModel):
    query: str


@app.get("/")
def index():
    index_file = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({"status": "ColdCase Detective API running"})


@app.get("/api/cases")
def get_cases():
    """Retrieve all cold case files with categories."""
    cases_file = os.path.join(DATA_DIR, "cases.json")
    if os.path.exists(cases_file):
        with open(cases_file, "r", encoding="utf-8") as f:
            return JSONResponse(json.load(f))
    return JSONResponse([])


@app.post("/api/fetch-live")
def fetch_live(req: LiveFetchRequest):
    """Download live criminal records and photos from public web endpoints in real-time."""
    result = fetch_live_online_case(req.query)
    return JSONResponse(result)


@app.post("/api/investigate")
async def investigate(req: CaseInvestigationRequest):
    if MOCK_MODE:
        return JSONResponse(_mock_investigation_trail(req.case_id, req.suspect_name))
    return JSONResponse(await _run_live_agents(req))


def _mock_investigation_trail(case_id: str, suspect: str) -> dict:
    trails = {
        "CASE-1998-BERLIN-VAULT": {
            "case_id": case_id,
            "suspect": suspect or "Victor Vance",
            "contradiction": {
                "case_id": case_id,
                "suspect_name": "Victor Vance",
                "original_statement": "Claimed uninterrupted sleeper train travel Berlin->Zurich starting 20:15 (Cabin 4B).",
                "conflicting_statement_or_evidence": "Conductor log confirms Cabin 4B empty until Nuremberg at 01:45 AM. Motorway toll gate logged private sedan at 23:12.",
                "sources": ["STMT-1998-01", "STMT-2012-04", "TOLL-BERLIN-A9"],
                "diverging_facts": ["departure_time", "mode_of_transit", "physical_location_at_heist_time"]
            },
            "hypothesis": {
                "hypothesis_id": "H-COLD-01",
                "suspect_or_theory": "Vance handed off cryptographic bypass keys in Berlin at 23:00 to Marcus Thorne before driving south to stage an alibi boarding in Nuremberg.",
                "motive_and_opportunity": "Offshore gambling debt liquidation + Direct administrative cryptographic credentials.",
                "confidence": 0.88,
                "key_vulnerabilities": "Requires tracing the anonymous Zurich safe deposit box payout recipient."
            },
            "critic": {
                "verdict": "Theory solidly supported by spatial-temporal contradictions. Physical recovery of 1998 hard drive corroborates cryptographic token creation.",
                "evidence_quality": "Strong",
                "lead_strength_score": 0.92,
                "unresolved_blindspots": ["Who assisted with the physical vault lock bypass while Vance drove south?"],
                "corroborated_leads_count": 6
            },
            "next_action": {
                "action_id": "LEAD-EXEC-01",
                "objective": "Execute cross-jurisdiction warrant on Zurich Deposit Box 402 and confront Vance with Nuremberg conductor log.",
                "recommended_forensics_or_interrogation": "Forensic fingerprint extraction on preserved 1998 train ticket stub.",
                "expected_breakthrough_gain": 0.94,
                "targeted_suspects": ["Victor Vance", "Marcus Thorne", "Elena Rostova"]
            }
        },
        "CASE-1990-BOSTON-GARDNER": {
            "case_id": case_id,
            "suspect": suspect or "Bobby Donati",
            "contradiction": {
                "case_id": case_id,
                "suspect_name": "Bobby Donati / Richard Abath",
                "original_statement": "Night guard claimed routine perimeter check triggered rear security door opening at 1:00 AM.",
                "conflicting_statement_or_evidence": "Hardwired alarm logs confirm rear door was unlocked and left ajar for 3 minutes without security protocol justification, matching Donati crew vehicle arrival timestamp.",
                "sources": ["ALARM-GARDNER-1990", "FBI-BO-TAPE-04"],
                "diverging_facts": ["door_state", "guard_movement_pattern", "breach_timeline"]
            },
            "hypothesis": {
                "hypothesis_id": "H-GARDNER-01",
                "suspect_or_theory": "Donati organized the theft with inside cooperation from night security to secure collateral for Vincent Ferrara's bail.",
                "motive_and_opportunity": "Mafia leadership leverage + exact knowledge of taped VHS surveillance gaps.",
                "confidence": 0.91,
                "key_vulnerabilities": "Works estimated to have been fragmented across multiple international private collections."
            },
            "critic": {
                "verdict": "Corroborated by motion sensor telemetry printouts and informant wiretaps. DNA recovery on duct tape bindings remains highest-priority physical lead.",
                "evidence_quality": "Strong",
                "lead_strength_score": 0.95,
                "unresolved_blindspots": ["Current geographic whereabouts of Vermeer's 'The Concert'."],
                "corroborated_leads_count": 8
            },
            "next_action": {
                "action_id": "ACTION-GARDNER-DNA",
                "objective": "Perform next-generation Touch DNA sequencing on preserved duct tape bindings from guard restraint room.",
                "recommended_forensics_or_interrogation": "Targeted forensic genealogy database match against Guarente / Donati crime family lineages.",
                "expected_breakthrough_gain": 0.97,
                "targeted_suspects": ["Bobby Donati (Estate)", "Robert Guarente Lineage"]
            }
        },
        "CASE-1969-ZODIAC-CIPHER": {
            "case_id": case_id,
            "suspect": suspect or "Arthur Leigh Allen",
            "contradiction": {
                "case_id": case_id,
                "suspect_name": "Arthur Leigh Allen",
                "original_statement": "Allen claimed he was diving at Salt Point on the weekend of the Lake Berryessa attack (Sept 27, 1969).",
                "conflicting_statement_or_evidence": "Military surplus boot size 10.5 Wing Walker prints at the crime scene matched Allen's footwear seized in 1971 search warrant.",
                "sources": ["SFPD-CASE-69", "NAPA-SHERIFF-LOGS"],
                "diverging_facts": ["alibi_location", "footwear_imprint", "watch_brand_possession"]
            },
            "hypothesis": {
                "hypothesis_id": "H-ZODIAC-340",
                "suspect_or_theory": "Arthur Leigh Allen operated with multiple typewriter models and deliberate handwriting distortion to evade 1970s forensic document examiners.",
                "motive_and_opportunity": "Psychopathic notoriety + High familiarity with naval cryptology codes.",
                "confidence": 0.86,
                "key_vulnerabilities": "Partial DNA profile from stamp glue in 2002 did not definitively match Allen."
            },
            "critic": {
                "verdict": "Circumstantial evidence overwhelming (watch symbol, Royal typewriter, confessions to Don Cheny), but mitochondrial DNA requires re-testing with modern single-cell lysis.",
                "evidence_quality": "Moderate",
                "lead_strength_score": 0.89,
                "unresolved_blindspots": ["Exclusion of secondary letter hoaxes."],
                "corroborated_leads_count": 12
            },
            "next_action": {
                "action_id": "ACTION-ZODIAC-GENEALOGY",
                "objective": "Apply Investigative Genetic Genealogy (IGG) on original 1969 envelope stamps preserved by San Francisco Chronicle.",
                "recommended_forensics_or_interrogation": "Rootless hair / saliva SNP micro-array sequencing.",
                "expected_breakthrough_gain": 0.98,
                "targeted_suspects": ["Arthur Leigh Allen", "Secondary Persons of Interest"]
            }
        },
        "CASE-2017-ONECOIN-CRYPTO": {
            "case_id": case_id,
            "suspect": suspect or "Ruja Ignatova",
            "contradiction": {
                "case_id": case_id,
                "suspect_name": "Ruja Ignatova",
                "original_statement": "Claimed legitimate decentralized blockchain cryptocurrency with 3 million global users.",
                "conflicting_statement_or_evidence": "Recovered internal SQL server databases confirm zero blockchain existed; tokens were generated via simple database incrementation scripts.",
                "sources": ["DOJ-INDICTMENT-2017", "EUROPOL-RED-NOTICE"],
                "diverging_facts": ["blockchain_existence", "fund_routing", "passport_usage_athens"]
            },
            "hypothesis": {
                "hypothesis_id": "H-CRYPTOQUEEN-01",
                "suspect_or_theory": "Ruja Ignatova fled Athens with falsified diplomatic passports and underwent facial reconstructive surgery in Dubai before laundering 230,000 BTC.",
                "motive_and_opportunity": "4B USD Ponzi liquidation + Transnational organized crime protection network.",
                "confidence": 0.93,
                "key_vulnerabilities": "Conflicting intelligence regarding alleged assassination vs living under luxury cover in UAE/Southeast Asia."
            },
            "critic": {
                "verdict": "On-chain crypto tracking of historical Bitcoin wallets links directly to Dubai real estate transactions in 2021-2023.",
                "evidence_quality": "Strong",
                "lead_strength_score": 0.94,
                "unresolved_blindspots": ["Biometric facial recognition match on recent Mediterranean yacht manifests."],
                "corroborated_leads_count": 15
            },
            "next_action": {
                "action_id": "ACTION-ONECOIN-BLOCKCHAIN",
                "objective": "Issue international freezing order on 4 designated multi-sig BTC clusters and subpoena Greek marina surveillance tapes.",
                "recommended_forensics_or_interrogation": "Crypto forensic graph tracing + AI satellite imagery analysis of registered offshore vessels.",
                "expected_breakthrough_gain": 0.96,
                "targeted_suspects": ["Ruja Ignatova", "Key Money Launderers"]
            }
        }
    }
    return trails.get(case_id, trails["CASE-1998-BERLIN-VAULT"])


async def _run_live_agents(req: CaseInvestigationRequest) -> dict:
    from google.adk.runners import InMemoryRunner
    from google.genai import types
    from coldcase_agent.agent import root_agent

    runner = InMemoryRunner(agent=root_agent, app_name="coldcase_investigator")
    user_id = "detective"
    session_id = req.session_id or str(uuid.uuid4())

    await runner.session_service.create_session(
        app_name="coldcase_investigator", user_id=user_id, session_id=session_id
    )

    prompt = f"Case ID: {req.case_id}. Suspect: {req.suspect_name}. Question: {req.query}"
    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for _event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=message
    ):
        pass

    session = await runner.session_service.get_session(
        app_name="coldcase_investigator", user_id=user_id, session_id=session_id
    )
    state = session.state if session else {}

    return {
        "case_id": req.case_id,
        "suspect": req.suspect_name,
        "session_id": session_id,
        "contradiction": state.get("contradiction"),
        "hypothesis": state.get("hypothesis"),
        "critic": state.get("critic"),
        "next_action": state.get("next_action"),
    }
