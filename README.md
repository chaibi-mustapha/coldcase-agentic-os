# 🕵️‍♂️ ColdCase Detective AI — Autonomous Criminal Investigation OS

> **Built for Devpost "All Things Agentic" Hackathon 2026**  
> *Autonomous multi-agent system & Knowledge Graph for cracking unsolved criminal cold cases.*

---

## 🎯 The Problem
Unresolved criminal cases remain unsolved for decades not because clues don't exist, but because **vital connections are buried across fragmented police logs, contradictory testimonies given years apart, and isolated digital telemetry**.

## 🧠 The Agentic Solution
ColdCase Detective AI deploys a coordinated pipeline of **6 autonomous agents** powered by **Google ADK & Gemini 3.5 Flash**:

1. **FBI & OSINT Archive Agent**: Queries live open endpoints (`api.fbi.gov/wanted`) and cold case databases.
2. **Timeline & Forensics Agent**: Reconstructs minute-by-minute temporal checkpoints and tracks spatial alibis.
3. **Alibi Contradiction Agent**: Pairs conflicting testimonies and highlights mathematical/temporal impossibilities.
4. **Criminal Profiler & Hypothesis Agent**: Formulates high-probability theories with confidence scoring.
5. **Senior Detective Critic (Adversarial)**: Actively stress-tests hypotheses to eliminate cognitive bias.
6. **Breakthrough Lead Agent**: Prescribes the single highest-yield next operational action (warrants, DNA re-sequencing, target interrogation).

---

## 🚀 Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the investigation console
uvicorn api.main:app --reload --port 8000
```
Open `http://localhost:8000` to view the interactive **Murder Board & Agentic Reasoning Console**.
