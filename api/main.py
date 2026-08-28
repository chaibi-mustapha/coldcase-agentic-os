"""FastAPI Backend for ColdCase Detective AI — Criminal Investigation Console."""

import json
import os
import uuid
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from coldcase_agent.tools import (
    fetch_live_online_case,
    load_local_cases,
    get_case_by_id,
    search_press_and_media_archives,
    fetch_community_sleuth_theories,
    analyze_multimedia_video_report,
    cross_examine_pi_dossier,
    evaluate_source_reliability_matrix,
)

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
    """Retrieve all cold case files with categories, board elements and red strings."""
    return JSONResponse(load_local_cases())


@app.get("/api/cases/{case_id}")
def get_case(case_id: str):
    """Retrieve specific cold case details."""
    case = get_case_by_id(case_id)
    if case:
        return JSONResponse(case)
    return JSONResponse({"error": "Case not found"}, status_code=404)


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
            "agent_osint": {
                "agent_id": "AGENT-01-OSINT",
                "title": "Declassified Archives & Open Intelligence",
                "summary": "Mined 1998 Grand National Vault criminal files and Frankfurt financial archives. Background: Victor Vance, former military cryptographic engineer.",
                "sources_scanned": 12,
                "reliability_rating": "B2 (Historic Press & Archives)"
            },
            "agent_timeline": {
                "agent_id": "AGENT-02-TIMELINE",
                "title": "Chronological Reconstruction & Telemetry",
                "summary": "22:45: Vault biometric alarms suppressed. 23:12: Berlin A9 Toll transponder logs Vance's private sedan. 01:45: Boarded train in Nuremberg.",
                "temporal_gap": "2h 27m unverified movement gap",
                "reliability_rating": "A1 (Motorway Telemetry)"
            },
            "contradiction": {
                "case_id": case_id,
                "suspect_name": "Victor Vance",
                "original_statement": "Claimed uninterrupted sleeper train presence Berlin->Zurich (Cabin 4B) starting 20:15.",
                "conflicting_statement_or_evidence": "Conductor log confirms Cabin 4B empty until Nuremberg at 01:45 AM. Motorway toll gate logged private sedan at 23:12 exiting Berlin.",
                "sources": ["DB-TRAIN-MANIFEST-1998", "TOLL-GATE-A9", "PI-ARGUS-REPORT"],
                "reliability_rating": "A1 (Certified Evidence)",
                "diverging_facts": ["departure_time", "mode_of_transit", "physical_location_at_heist_time"]
            },
            "hypothesis": {
                "hypothesis_id": "H-BERLIN-01",
                "suspect_or_theory": "Vance handed off master cryptographic override keys in Berlin at 23:00 to Marcus Thorne before driving south to stage an alibi boarding in Nuremberg.",
                "motive_and_opportunity": "Offshore gambling debt liquidation + Direct administrative cryptographic access.",
                "confidence": 0.92,
                "multi_channel_corroboration": "Corroborated by Argus PI stakeout at Hotel Baur au Lac and Web Sleuths Usenet key trace."
            },
            "critic": {
                "verdict": "Theory solidly corroborated by spatial-temporal contradictions. Microfilms and sensor logs confirm zero forced entry.",
                "evidence_quality": "Strong (Grade A1/B2)",
                "lead_strength_score": 0.94,
                "unresolved_blindspots": ["Identity of the on-site mechanical locksmith accomplice."],
                "corroborated_leads_count": 7
            },
            "next_action": {
                "action_id": "ACTION-BERLIN-ZURICH-402",
                "objective": "Execute international rogatory subpoena on Zurich Safe Deposit Box 402 and confront Vance with Nuremberg conductor log.",
                "recommended_forensics_or_interrogation": "Touch DNA extraction and fingerprint analysis on preserved 1998 train ticket stub.",
                "expected_breakthrough_gain": 0.96,
                "targeted_suspects": ["Victor Vance", "Marcus Thorne"]
            }
        },
        "CASE-1990-BOSTON-GARDNER": {
            "case_id": case_id,
            "suspect": suspect or "Bobby Donati",
            "agent_osint": {
                "agent_id": "AGENT-01-OSINT",
                "title": "FBI NORJAK & Boston Mafia Archives",
                "summary": "Extracted Patriarca crime family wiretaps and Gardner Museum blueprints. Identified Bobby Donati syndicate ties.",
                "sources_scanned": 15,
                "reliability_rating": "A2 (FBI Official Archives)"
            },
            "agent_timeline": {
                "agent_id": "AGENT-02-TIMELINE",
                "title": "Museum Motion Sensor Telemetry",
                "summary": "01:00 AM: Guard opens Palace Road security door. 01:24 AM: Two fake police officers buzz intercom. 01:48 AM: Dutch Room frames sliced.",
                "temporal_gap": "Single intruder detected in Dutch Room",
                "reliability_rating": "A1 (Hardwired Alarm Telemetry)"
            },
            "contradiction": {
                "case_id": case_id,
                "suspect_name": "Bobby Donati / Richard Abath",
                "original_statement": "Night guard claimed routine perimeter check justified opening Palace Road exterior security door at 01:00 AM.",
                "conflicting_statement_or_evidence": "Hardwired alarm logs confirm rear door was unlocked and left ajar for 3 minutes without protocol justification, matching Donati crew vehicle arrival timestamp.",
                "sources": ["MUSEUM-ALARM-1990", "PI-CHARLEY-HILL-DOSSIER", "FBI-PATRIARCA-TAPES"],
                "reliability_rating": "A1 (Physical Log)",
                "diverging_facts": ["door_security_state", "guard_movement_pattern", "breach_timeline"]
            },
            "hypothesis": {
                "hypothesis_id": "H-GARDNER-01",
                "suspect_or_theory": "Donati coordinated the heist with inside guard compliance to use stolen Rembrandts as leverage for Vincent Ferrara's bail.",
                "motive_and_opportunity": "Mob leadership leverage + Exact knowledge of VHS CCTV blind spots.",
                "confidence": 0.94,
                "multi_channel_corroboration": "Corroborated by FBI wiretaps, Charley Hill's Dublin art recovery reports, and Netflix documentary motion analysis."
            },
            "critic": {
                "verdict": "Hypothesis strongly supported by motion sensor printouts and organized crime records. Dublin IRA fencing channel is highly credible.",
                "evidence_quality": "Solid (Grade A2/C2)",
                "lead_strength_score": 0.96,
                "unresolved_blindspots": ["Current geographic whereabouts of Vermeer's 'The Concert'."],
                "corroborated_leads_count": 9
            },
            "next_action": {
                "action_id": "ACTION-GARDNER-DNA-COLD",
                "objective": "Perform next-generation Touch DNA sequencing on preserved duct tape bindings from guard restraint room.",
                "recommended_forensics_or_interrogation": "Forensic genetic genealogy match against Patriarca / Donati crime family descendant lineages.",
                "expected_breakthrough_gain": 0.97,
                "targeted_suspects": ["Bobby Donati (Estate)", "Myles Connor Associates"]
            }
        },
        "CASE-2003-ANTWERP-DIAMOND": {
            "case_id": case_id,
            "suspect": suspect or "Leonardo Notarbartolo",
            "agent_osint": {
                "agent_id": "AGENT-01-OSINT",
                "title": "Belgian Judicial & Diamond Bourse Records",
                "summary": "Mined Antwerp Diamond Center tenant manifests and Italian police surveillance records on School of Turin members.",
                "sources_scanned": 11,
                "reliability_rating": "A1 (Belgian Judicial Verdict)"
            },
            "agent_timeline": {
                "agent_id": "AGENT-02-TIMELINE",
                "title": "Vault Sensor Timeline Reconstruction",
                "summary": "Friday 18:00: Vault sealed. Sat 02:30: PIR sensors blinded with hairspray. Sunday 05:00: 109 deposit boxes drained. Sunday 14:00: E19 trash bag dumped.",
                "temporal_gap": "Full weekend window utilized",
                "reliability_rating": "A1 (Seismic & Magnetic Logs)"
            },
            "contradiction": {
                "case_id": case_id,
                "suspect_name": "Leonardo Notarbartolo",
                "original_statement": "Claimed to be an innocent victim who had his own diamonds stolen from his safety deposit box.",
                "conflicting_statement_or_evidence": "DNA recovered from a half-eaten salami sandwich in trash bags discarded off the E19 highway matched Notarbartolo with 100% certainty.",
                "sources": ["BELGIAN-FORENSIC-POLICE", "LLOYDS-LONDON-AUDIT"],
                "reliability_rating": "A1 (DNA Evidence)",
                "diverging_facts": ["trash_dump_location", "possession_of_vault_key_copies"]
            },
            "hypothesis": {
                "hypothesis_id": "H-ANTWERP-01",
                "suspect_or_theory": "School of Turin infiltrated building over 24 months. Rough diamonds fenced via clandestine cutters in Tel-Aviv and Mumbai.",
                "motive_and_opportunity": "$100M rough gems + Diamond merchant insurance collusion.",
                "confidence": 0.95,
                "multi_channel_corroboration": "Corroborated by Lloyd's insurance risk logs and televised Masterminds interview."
            },
            "critic": {
                "verdict": "Direct physical involvement proven beyond doubt. Unrecovered diamond stash remains primary target.",
                "evidence_quality": "Excellent",
                "lead_strength_score": 0.95,
                "unresolved_blindspots": ["Secondary safety deposit boxes in Northern Italy."],
                "corroborated_leads_count": 8
            },
            "next_action": {
                "action_id": "ACTION-ANTWERP-TRACING",
                "objective": "Launch asset recovery audit on Turin real estate entities and trace recut diamond serial numbers surfacing in Asian bourses.",
                "recommended_forensics_or_interrogation": "Targeted subpoena on Mumbai diamond brokers identified in PI dossier.",
                "expected_breakthrough_gain": 0.93,
                "targeted_suspects": ["Leonardo Notarbartolo", "The 'Genius' Locksmith"]
            }
        },
        "CASE-1969-ZODIAC-CIPHER": {
            "case_id": case_id,
            "suspect": suspect or "Arthur Leigh Allen",
            "agent_osint": {
                "agent_id": "AGENT-01-OSINT",
                "title": "SF Chronicle & Naval Cryptology Archives",
                "summary": "Catalogued all authenticated Zodiac mailings, naval cryptographic symbols, and 1969 Vallejo police case notes.",
                "sources_scanned": 18,
                "reliability_rating": "A1 (SF Chronicle & FBI Files)"
            },
            "agent_timeline": {
                "agent_id": "AGENT-02-TIMELINE",
                "title": "Lake Berryessa Attack Timeline",
                "summary": "Sept 27 1969 18:15: Hartnell & Shepard attacked. 19:40: Payphone call placed to Napa PD. Allen's car seen parked near boat launch.",
                "temporal_gap": "Salt Point diving alibi refuted",
                "reliability_rating": "A2 (Wing Walker Boot Imprints)"
            },
            "contradiction": {
                "case_id": case_id,
                "suspect_name": "Arthur Leigh Allen",
                "original_statement": "Allen claimed he was diving at Salt Point during the Lake Berryessa attack on Sept 27, 1969.",
                "conflicting_statement_or_evidence": "Military surplus Wing Walker boot prints (size 10.5) found at the crime scene matched footwear seized from Allen in 1971 search warrant.",
                "sources": ["VALLEJO-PD-FILE", "SFPD-ARCHIVES", "CHRONICLE-LETTERS"],
                "reliability_rating": "A2 (Physical Imprints)",
                "diverging_facts": ["alibi_location", "footwear_model", "watch_symbol"]
            },
            "hypothesis": {
                "hypothesis_id": "H-ZODIAC-340",
                "suspect_or_theory": "Allen utilized multiple typewriters and deliberate handwriting distortion to deceive 1970s document examiners.",
                "motive_and_opportunity": "Notoriety obsession + High familiarity with naval cryptograms.",
                "confidence": 0.89,
                "multi_channel_corroboration": "Corroborated by 2020 computer cryptanalysis of 340 cipher by Web Sleuths and SF Chronicle letters."
            },
            "critic": {
                "verdict": "Circumstantial evidence extraordinarily dense. Requires modern rootless hair/SNP saliva re-sequencing on envelope stamps.",
                "evidence_quality": "Very Strong",
                "lead_strength_score": 0.91,
                "unresolved_blindspots": ["Verify alternate Gary Francis Poste lead submitted by Case Breakers."],
                "corroborated_leads_count": 14
            },
            "next_action": {
                "action_id": "ACTION-ZODIAC-IGG-2026",
                "objective": "Apply Investigative Genetic Genealogy (IGG) with SNP microarray on saliva traces from 1969 Chronicle envelopes.",
                "recommended_forensics_or_interrogation": "High-throughput sequencing of preserved envelope stamps in San Francisco archives.",
                "expected_breakthrough_gain": 0.98,
                "targeted_suspects": ["Arthur Leigh Allen Lineage", "Gary Francis Poste Lineage"]
            }
        },
        "CASE-2017-ONECOIN-CRYPTO": {
            "case_id": case_id,
            "suspect": suspect or "Ruja Ignatova",
            "agent_osint": {
                "agent_id": "AGENT-01-OSINT",
                "title": "FBI Most Wanted & Europol Red Notice Archives",
                "summary": "Extracted $4B OneCoin Ponzi intelligence, Bulgarian corporate registries, and international travel manifests.",
                "sources_scanned": 19,
                "reliability_rating": "A1 (FBI / DOJ Indictment)"
            },
            "agent_timeline": {
                "agent_id": "AGENT-02-TIMELINE",
                "title": "Athens Flight & Disappearance Timeline",
                "summary": "Oct 25 2017: Boarded Ryanair flight Sofia->Athens. 13:45: Walked through Athens terminal. Vanished into diplomatic protection convoy.",
                "temporal_gap": "Zero verified public sightings post-2017",
                "reliability_rating": "A1 (Airport CCTV Logs)"
            },
            "contradiction": {
                "case_id": case_id,
                "suspect_name": "Ruja Ignatova",
                "original_statement": "Claimed legitimate decentralized blockchain with 3 million active users worldwide.",
                "conflicting_statement_or_evidence": "Seized SQL databases confirm zero blockchain ever existed; coins were incremented via automated SQL stored procedures.",
                "sources": ["US-DOJ-INDICTMENT", "BBC-JAMIE-BARTLETT-INQUIRY", "ONCHAIN-BTC-LOGS"],
                "reliability_rating": "A1 (Seized Databases)",
                "diverging_facts": ["blockchain_existence", "fund_routing", "athens_flight_manifest"]
            },
            "hypothesis": {
                "hypothesis_id": "H-CRYPTOQUEEN-01",
                "suspect_or_theory": "Ruja fled Athens with forged diplomatic passports, underwent facial reconstruction, and laundered 230,000 Bitcoins via Dubai corporate conduits.",
                "motive_and_opportunity": "$4 Billion Ponzi liquidation + Balkan organized crime protection syndicate.",
                "confidence": 0.94,
                "multi_channel_corroboration": "Corroborated by BBC investigative findings, Dubai yacht stakeout, and on-chain analysis of 230,000 BTC."
            },
            "critic": {
                "verdict": "On-chain UTXO cluster tracking and luxury property purchases verify active laundering network.",
                "evidence_quality": "Excellent (Grade A1/B1)",
                "lead_strength_score": 0.95,
                "unresolved_blindspots": ["Biometric match on recent private yachts in Eastern Mediterranean."],
                "corroborated_leads_count": 16
            },
            "next_action": {
                "action_id": "ACTION-ONECOIN-FROST",
                "objective": "Issue international asset freezing orders on designated multi-sig BTC clusters and subpoena Greek marina surveillance logs.",
                "recommended_forensics_or_interrogation": "Crypto forensic graph tracing + AI satellite imagery facial recognition on registered vessels.",
                "expected_breakthrough_gain": 0.97,
                "targeted_suspects": ["Ruja Ignatova", "Emirati Nominee Brokers"]
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
