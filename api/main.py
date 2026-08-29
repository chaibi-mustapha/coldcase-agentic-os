"""FastAPI Backend for ColdCase Detective AI — Criminal Investigation Console."""

import json
import os
import uuid
import httpx
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


async def _get_best_gemini_model(client: httpx.AsyncClient, api_key: str) -> str:
    """Auto-discover the exact supported Gemini model for this API key via Google Generative Language API."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        resp = await client.get(url)
        if resp.status_code == 200:
            models_data = resp.json().get("models", [])
            # Priority 1: Flash models
            for m in models_data:
                methods = m.get("supportedGenerationMethods", [])
                if "generateContent" in methods:
                    name = m.get("name", "").replace("models/", "")
                    if "flash" in name.lower():
                        return name
            # Priority 2: Any model supporting generateContent
            for m in models_data:
                methods = m.get("supportedGenerationMethods", [])
                if "generateContent" in methods:
                    return m.get("name", "").replace("models/", "")
    except Exception:
        pass
    return "gemini-1.5-flash"


@app.get("/api/gemini-status")
async def gemini_status():
    """Verify Gemini API connection status and active model."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
    has_key = bool(api_key and len(api_key) > 10 and not api_key.startswith("VOTRE_"))
    key_preview = f"{api_key[:6]}...{api_key[-4:]}" if has_key else "None"

    if not has_key:
        return JSONResponse({"status": "no_key", "message": "No API key configured", "key_preview": key_preview})

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            model = await _get_best_gemini_model(client, api_key)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": "Reply with only word OK"}]}]}
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                return JSONResponse({"status": "active", "model": model, "key_preview": key_preview, "live": True})
            else:
                return JSONResponse({"status": "api_error", "http_code": resp.status_code, "error": resp.text, "model_tried": model, "key_preview": key_preview})
    except Exception as e:
        return JSONResponse({"status": "network_error", "error": str(e), "key_preview": key_preview})


@app.post("/api/investigate")
async def investigate(req: CaseInvestigationRequest):
    # Try live Gemini agents first whenever an API key is present
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
    if api_key and len(api_key) > 10 and not api_key.startswith("VOTRE_"):
        try:
            live_result = await _run_live_agents(req)
            if live_result and live_result.get("hypothesis"):
                return JSONResponse(live_result)
        except Exception as e:
            print(f"[Live Agent Error]: {e}")
    
    # Fallback to rich curated case intelligence
    return JSONResponse(_mock_investigation_trail(req.case_id, req.suspect_name))


def _mock_investigation_trail(case_id: str, suspect: str) -> dict:
    trails = {
        "CASE-1998-BERLIN-VAULT": {
            "case_id": case_id,
            "suspect": suspect or "Victor Vance",
            "live_gemini": False,
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
                "suspect_name": suspect or "Victor Vance",
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
                "targeted_suspects": [suspect or "Victor Vance", "Marcus Thorne"]
            }
        },
        "CASE-1990-BOSTON-GARDNER": {
            "case_id": case_id,
            "suspect": suspect or "Bobby Donati",
            "live_gemini": False,
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
                "suspect_name": suspect or "Bobby Donati / Richard Abath",
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
                "targeted_suspects": [suspect or "Bobby Donati (Estate)", "Myles Connor Associates"]
            }
        },
        "CASE-2003-ANTWERP-DIAMOND": {
            "case_id": case_id,
            "suspect": suspect or "Leonardo Notarbartolo",
            "live_gemini": False,
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
                "suspect_name": suspect or "Leonardo Notarbartolo",
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
                "targeted_suspects": [suspect or "Leonardo Notarbartolo", "The 'Genius' Locksmith"]
            }
        },
        "CASE-1969-ZODIAC-CIPHER": {
            "case_id": case_id,
            "suspect": suspect or "Arthur Leigh Allen",
            "live_gemini": False,
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
                "suspect_name": suspect or "Arthur Leigh Allen",
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
                "targeted_suspects": [suspect or "Arthur Leigh Allen Lineage", "Gary Francis Poste Lineage"]
            }
        },
        "CASE-1947-BLACK-DAHLIA": {
            "case_id": case_id,
            "suspect": suspect or "Dr. George Hodel",
            "live_gemini": False,
            "agent_osint": {
                "agent_id": "AGENT-01-OSINT",
                "title": "LAPD 1947 Homicide & Grand Jury Files",
                "summary": "Extracted LAPD secret 1950 electronic wiretaps on Dr. George Hodel's Sowden house and 1947 medical hemicorporectomy forensic autopsy records.",
                "sources_scanned": 16,
                "reliability_rating": "A1 (LAPD Grand Jury Wiretaps)"
            },
            "agent_timeline": {
                "agent_id": "AGENT-02-TIMELINE",
                "title": "Leimert Park Discovery Timeline",
                "summary": "Jan 9 1947: Elizabeth Short departs Biltmore Hotel. Jan 14 23:30: Black sedan spotted at Norton Ave vacant lot. Jan 15 10:00: Body discovered.",
                "temporal_gap": "5-day unaccounted captivity window",
                "reliability_rating": "A1 (LAPD Autopsy & Surveillance)"
            },
            "contradiction": {
                "case_id": case_id,
                "suspect_name": suspect or "Dr. George Hodel",
                "original_statement": "Dr. Hodel claimed zero personal acquaintance with Elizabeth Short and denied ever meeting her in Hollywood.",
                "conflicting_statement_or_evidence": "1950 LAPD bugged microphone audio recording captures Hodel stating: 'Supposin' I did kill the Black Dahlia. They couldn't prove it now.' In addition, personal photo album contained confirmed Short portraits.",
                "sources": ["LAPD-WIRETAP-1950", "STEVE-HODEL-INVESTIGATION", "LA-EXAMINER-1947"],
                "reliability_rating": "A1 (Audio Wiretap Transcript)",
                "diverging_facts": ["acquaintance_denial", "surgical_skillset", "wiretap_admission"]
            },
            "hypothesis": {
                "hypothesis_id": "H-DAHLIA-01",
                "suspect_or_theory": "Dr. George Hodel utilized his surgical clinic and Sowden mansion basement for professional hemicorporectomy dissection before staging at Norton Avenue.",
                "motive_and_opportunity": "Psychopathic misogyny + High surgical dissection expertise + LAPD vice protection payoffs.",
                "confidence": 0.94,
                "multi_channel_corroboration": "Corroborated by retired LAPD detective Steve Hodel, Grand Jury transcripts, and cement bag receipt found at crime scene."
            },
            "critic": {
                "verdict": "Surgical precision and wiretap recordings constitute overwhelming circumstantial proof. Soil samples match Sowden property.",
                "evidence_quality": "High (Grade A1/B1)",
                "lead_strength_score": 0.96,
                "unresolved_blindspots": ["Secondary accomplice who mailed victim's personal effects to the Los Angeles Examiner."],
                "corroborated_leads_count": 12
            },
            "next_action": {
                "action_id": "ACTION-DAHLIA-SOIL-DNA",
                "objective": "Subject the preserved 1947 Los Angeles Examiner mailings to touch DNA extraction and vacuum swab envelope glue.",
                "recommended_forensics_or_interrogation": "Compare mitochondrial DNA against living Hodel direct descendants.",
                "expected_breakthrough_gain": 0.98,
                "targeted_suspects": [suspect or "Dr. George Hodel (Lineage)", "Fred Sexton (Associate)"]
            }
        },
        "CASE-1971-DB-COOPER": {
            "case_id": case_id,
            "suspect": suspect or "Richard Floyd McCoy / Sheridan Peterson",
            "live_gemini": False,
            "agent_osint": {
                "agent_id": "AGENT-01-OSINT",
                "title": "FBI NORJAK Unclassified Investigation Files",
                "summary": "Mined 60+ volumes of FBI NORJAK transcripts, Boeing 727 aft-stair aerodynamics reports, and recovered $20 bill serial lists.",
                "sources_scanned": 22,
                "reliability_rating": "A1 (FBI NORJAK Archive)"
            },
            "agent_timeline": {
                "agent_id": "AGENT-02-TIMELINE",
                "title": "Flight 305 Drop Zone Timeline",
                "summary": "Nov 24 1971 14:50: Flight 305 departs Portland. 19:40: $200k delivered in Seattle. 20:13: Pressure bump indicates aft-stair parachute jump over Ariel, WA.",
                "temporal_gap": "Drop zone search across Gifford Pinchot forest",
                "reliability_rating": "A1 (Cockpit Altimeter Telemetry)"
            },
            "contradiction": {
                "case_id": case_id,
                "suspect_name": suspect or "Richard Floyd McCoy",
                "original_statement": "McCoy claimed he was home with his family in Utah during Thanksgiving weekend 1971.",
                "conflicting_statement_or_evidence": "Executed identical Boeing 727 aft-stair skyjacking with $500k ransom just 5 months later in April 1972 using identical handwritten instructions.",
                "sources": ["FBI-NORJAK-EVIDENCE", "FAA-TELEMETRY-1971", "TENA-BAR-1980"],
                "reliability_rating": "A1 (Identical Modus Operandi)",
                "diverging_facts": ["skyjacking_technique", "parachute_rigging", "handwritten_notes"]
            },
            "hypothesis": {
                "hypothesis_id": "H-NORJAK-01",
                "suspect_or_theory": "Cooper was an experienced military smokejumper or Boeing flight test engineer familiar with aft-stair pressure seals and titanium alloy micro-particles on his tie.",
                "motive_and_opportunity": "$200,000 extortion + Elite skydiving military experience.",
                "confidence": 0.91,
                "multi_channel_corroboration": "Corroborated by Citizen Sleuths electron microscope analysis of titanium particles on clip-on tie and 1980 Tena Bar money find."
            },
            "critic": {
                "verdict": "Titanium alloy metallurgy on tie points directly to Boeing contract facility in Seattle. High survival probability despite weather.",
                "evidence_quality": "Solid (Grade A1/B2)",
                "lead_strength_score": 0.93,
                "unresolved_blindspots": ["River sedimentation rate explaining why only $5,800 washed up at Tena Bar in 1980."],
                "corroborated_leads_count": 11
            },
            "next_action": {
                "action_id": "ACTION-NORJAK-TIE-DNA",
                "objective": "Apply Next-Gen Y-STR and autosomal DNA sequencing to the JC Penney clip-on tie knot preserved in FBI Seattle vault.",
                "recommended_forensics_or_interrogation": "Upload autosomal profile to GEDmatch / FTDNA genetic genealogy databases.",
                "expected_breakthrough_gain": 0.99,
                "targeted_suspects": [suspect or "Richard Floyd McCoy Lineage", "Sheridan Peterson Lineage", "Vince Petersen"]
            }
        },
        "CASE-2016-BANGLADESH-SWIFT": {
            "case_id": case_id,
            "suspect": suspect or "Park Jin Hyok / Lazarus Group",
            "live_gemini": False,
            "agent_osint": {
                "agent_id": "AGENT-01-OSINT",
                "title": "SWIFT Telemetry & US DOJ Cyber Indictment",
                "summary": "Analyzed Bangladesh Bank RTGS printer logs, Federal Reserve NY transactions, and DOJ criminal complaint against Chosun Expo fronts.",
                "sources_scanned": 17,
                "reliability_rating": "A1 (US Federal Indictment)"
            },
            "agent_timeline": {
                "agent_id": "AGENT-02-TIMELINE",
                "title": "Weekend Cyber-Exfiltration Timeline",
                "summary": "Feb 4 2016 20:00 (Dhaka): 35 fraudulent SWIFT orders sent to NY Fed. Feb 5: Printer jammed intentionally. Feb 6-8: $81M routed to RCBC Makati branch.",
                "temporal_gap": "Weekend holiday alignment (Dhaka Fri/Sat + Manila Mon Chinese New Year)",
                "reliability_rating": "A1 (SWIFT Network MT103 Telemetry)"
            },
            "contradiction": {
                "case_id": case_id,
                "suspect_name": suspect or "RCBC Jupiter Branch / Kim Wong",
                "original_statement": "Branch officials claimed the 4 beneficiary accounts were legitimate verified corporate trading accounts opened under strict KYC rules.",
                "conflicting_statement_or_evidence": "Seized bank documentation revealed all 4 accounts used fake driver's licenses with identical fictitious employers and zero prior transaction history before the $81M dump.",
                "sources": ["PHILIPPINE-SENATE-HEARING-2016", "DOJ-LAZARUS-COMPLAINT", "SWIFT-FORENSIC-REPORT"],
                "reliability_rating": "A1 (Senate Sworn Testimony)",
                "diverging_facts": ["kyc_authenticity", "speed_of_cash_withdrawal", "casino_junket_routing"]
            },
            "hypothesis": {
                "hypothesis_id": "H-SWIFT-01",
                "suspect_or_theory": "Lazarus Group deployed spear-phishing malware to compromise HP switches and patch SWIFT alliance software, routing through Manila casino junkets.",
                "motive_and_opportunity": "State-sponsored hard currency exfiltration ($951M attempted, $81M executed).",
                "confidence": 0.96,
                "multi_channel_corroboration": "Corroborated by Mandiant incident response telemetry, BAE Systems malware reverse engineering, and Senate AMLA logs."
            },
            "critic": {
                "verdict": "Cyber attribution indisputable based on shared codebase with Sony Pictures 2014 and WannaCry 2017.",
                "evidence_quality": "Exceptional (Grade A1)",
                "lead_strength_score": 0.97,
                "unresolved_blindspots": ["Recovery of $43M laundered through Solaire and Midas VIP gaming rooms."],
                "corroborated_leads_count": 15
            },
            "next_action": {
                "action_id": "ACTION-SWIFT-CASINO-SEIZURE",
                "objective": "Enforce international asset forfeiture on designated junket accounts in Macau and Singapore linked to the RCBC withdrawals.",
                "recommended_forensics_or_interrogation": "Cross-reference casino surveillance facial recognition logs from Feb 5-9 2016 in Manila VIP rooms.",
                "expected_breakthrough_gain": 0.95,
                "targeted_suspects": [suspect or "Park Jin Hyok", "RCBC Branch Manager", "Junket Operators"]
            }
        },
        "CASE-2017-ONECOIN-CRYPTO": {
            "case_id": case_id,
            "suspect": suspect or "Ruja Ignatova",
            "live_gemini": False,
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
                "suspect_name": suspect or "Ruja Ignatova",
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
                "targeted_suspects": [suspect or "Ruja Ignatova", "Emirati Nominee Brokers"]
            }
        },
        "CASE-2014-GHOST-YACHT": {
            "case_id": case_id,
            "suspect": suspect or "Captain Jonathan Miller",
            "live_gemini": False,
            "agent_osint": {
                "agent_id": "AGENT-01-OSINT",
                "title": "Maritime AIS Logs & Coast Guard Archives",
                "summary": "Extracted North Sea satellite transponder tracks, Lloyds maritime insurance declarations, and Rotterdam harbormaster logs.",
                "sources_scanned": 14,
                "reliability_rating": "A1 (Satellite AIS Telemetry)"
            },
            "agent_timeline": {
                "agent_id": "AGENT-02-TIMELINE",
                "title": "North Sea Drifting Telemetry",
                "summary": "Aug 12 2014 22:00: AIS transponder manually switched off. Aug 13 04:00: EPIRB beacon not deployed. Aug 15: Vessel found adrift with engine idling in neutral.",
                "temporal_gap": "54-hour total radar and AIS blackout",
                "reliability_rating": "A1 (Coast Guard Radar Logs)"
            },
            "contradiction": {
                "case_id": case_id,
                "suspect_name": suspect or "Captain Jonathan Miller",
                "original_statement": "Shipowner claimed vessel suffered catastrophic electrical failure during severe gale forcing emergency life raft abandonment.",
                "conflicting_statement_or_evidence": "Coast Guard boarding team found main navigation table with fresh warm coffee, fully functional dual generators, and zero structural sea water intrusion.",
                "sources": ["DUTCH-COAST-GUARD-LOGS", "LLOYDS-DAMAGE-SURVEY", "SAT-RADAR-TRACKS"],
                "reliability_rating": "A1 (Physical Inspection Report)",
                "diverging_facts": ["storm_damage_claim", "generator_state", "life_raft_lashing"]
            },
            "hypothesis": {
                "hypothesis_id": "H-GHOST-01",
                "suspect_or_theory": "Crew transferred to an unflagged offshore rendezvous vessel carrying unregistered gold bullion before setting autopilot and cutting transponder.",
                "motive_and_opportunity": "€8.5M maritime insurance claim + Offshore asset smuggling.",
                "confidence": 0.93,
                "multi_channel_corroboration": "Corroborated by Danish radar sweep logging a fast zodiac approaching the yacht at 23:15."
            },
            "critic": {
                "verdict": "Absence of distress call on VHF Channel 16 confirms pre-planned staged disappearance.",
                "evidence_quality": "High (Grade A1)",
                "lead_strength_score": 0.94,
                "unresolved_blindspots": ["Port of registry of the secondary pickup vessel."],
                "corroborated_leads_count": 10
            },
            "next_action": {
                "action_id": "ACTION-MARITIME-SUBPOENA",
                "objective": "Cross-match radar contact velocity vectors against Baltic bunkering manifests in Gdynia and Klaipeda.",
                "recommended_forensics_or_interrogation": "Forensic digital recovery of deleted Garmin waypoint memory chips from yacht bridge.",
                "expected_breakthrough_gain": 0.96,
                "targeted_suspects": [suspect or "Captain Jonathan Miller", "Charter Company Directors"]
            }
        }
    }
    return trails.get(case_id, trails["CASE-1998-BERLIN-VAULT"])


async def _run_live_agents(req: CaseInvestigationRequest) -> dict:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
    
    if api_key and api_key != "VOTRE_CLE_ICI":
        case_data = get_case_by_id(req.case_id) or {}
        case_title = case_data.get("title", req.case_id)
        case_summary = case_data.get("summary", "")
        clues_summary = ", ".join([f"[{c.get('type')}: {c.get('title')} - {c.get('snippet') or c.get('handwritten') or ''}]" for c in case_data.get("board_elements", [])])
        
        prompt = f"""You are the Multi-Agent Director of ColdCase Detective AI (powered by Google ADK & Gemini).
Case Title: {case_title} (ID: {req.case_id})
Case Summary: {case_summary}
Target Suspect / POI: {req.suspect_name}
Investigative Query: {req.query}
Physical Evidence Clues on Murder Board: {clues_summary}

Perform a deep multi-agent criminal synthesis across 6 specialized agents. Return STRICTLY a valid JSON object matching this schema:
{{
  "live_gemini": true,
  "model": "gemini-2.5-flash",
  "case_id": "{req.case_id}",
  "suspect": "{req.suspect_name}",
  "agent_osint": {{
    "agent_id": "AGENT-01-OSINT",
    "title": "Classified Archives & Open Intelligence",
    "summary": "Deep OSINT summary of criminal records, background, and declassified archives for this case",
    "sources_scanned": 15,
    "reliability_rating": "A2 (FBI & Press Archives)"
  }},
  "agent_timeline": {{
    "agent_id": "AGENT-02-TIMELINE",
    "title": "Chronological Reconstruction & Telemetry",
    "summary": "Precise chronological movement checkpoints, timestamps, and sensor suppressions",
    "temporal_gap": "Key unverified timeline gap",
    "reliability_rating": "A1 (Physical & Sensor Telemetry)"
  }},
  "contradiction": {{
    "case_id": "{req.case_id}",
    "suspect_name": "{req.suspect_name}",
    "original_statement": "Suspect's sworn claim or initial alibi",
    "conflicting_statement_or_evidence": "Physical evidence or telemetry directly contradicting the alibi",
    "sources": ["ARCHIVE-EVIDENCE-1", "TELEMETRY-LOG"],
    "reliability_rating": "A1 (Certified Evidence)",
    "diverging_facts": ["fact_1", "fact_2"]
  }},
  "hypothesis": {{
    "hypothesis_id": "H-LIVE-01",
    "suspect_or_theory": "Compelling investigative hypothesis detailing modus operandi, accomplice channels, and key findings",
    "motive_and_opportunity": "Detailed motive and opportunity",
    "confidence": 0.95,
    "multi_channel_corroboration": "Corroborated across forensic, press, and informant channels"
  }},
  "critic": {{
    "verdict": "Adversarial stress-test review by senior detective critic challenging assumptions",
    "evidence_quality": "Strong (Grade A1/B2)",
    "lead_strength_score": 0.94,
    "unresolved_blindspots": ["Key blindspot to verify before indictment"],
    "corroborated_leads_count": 8
  }},
  "next_action": {{
    "action_id": "ACTION-BREAKTHROUGH-01",
    "objective": "High-impact actionable operational next step (e.g., Touch DNA sequencing, international rogatory subpoena)",
    "recommended_forensics_or_interrogation": "Forensic protocol and interrogation strategy",
    "expected_breakthrough_gain": 0.97,
    "targeted_suspects": ["{req.suspect_name}"]
  }}
}}"""

        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                best_model = await _get_best_gemini_model(client, api_key)
                models_to_try = [best_model, "gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-pro"]
                for model_name in dict.fromkeys(models_to_try):
                    for api_ver in ["v1beta", "v1"]:
                        url = f"https://generativelanguage.googleapis.com/{api_ver}/models/{model_name}:generateContent?key={api_key}"
                        payload = {
                            "contents": [{"parts": [{"text": prompt}]}],
                            "generationConfig": {
                                "responseMimeType": "application/json",
                                "temperature": 0.2
                            }
                        }
                        try:
                            resp = await client.post(url, json=payload)
                            if resp.status_code == 200:
                                data = resp.json()
                                text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                                parsed = json.loads(text_content)
                                parsed["live_gemini"] = True
                                parsed["model"] = model_name
                                parsed["case_id"] = req.case_id
                                parsed["suspect"] = req.suspect_name
                                return parsed
                        except Exception:
                            pass
        except Exception as e:
            print(f"[Live Agents Global Error]: {e}")

    mock = _mock_investigation_trail(req.case_id, req.suspect_name)
    mock["live_gemini"] = False
    return mock
