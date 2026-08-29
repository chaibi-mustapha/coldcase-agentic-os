# 🏆 ColdCaseAI — Dossier de Soumission Devpost (Solo Developer)

## 📌 Project Name (< 60 caractères)
`ColdCaseAI: Autonomous Crime Board OS`

---

## ⚡ Elevator Pitch / Tagline
> **The first autonomous forensic operating system orchestrating 6 specialized AI agents across an interactive cinematic crime pinboard to solve history's most baffling cold cases.**

---

## 💡 1. Inspiration

Like many people, I've always been captivated by detective stories and crime movies where investigators connect Polaroid photos, yellow sticky notes, vintage newspaper clippings, and secret reports with red strings on a corkboard.

In reality, homicide cold case squads and forensic genetic genealogists are drowning in thousands of un-indexed, fragmented archives: contradictory alibis, electronic toll telemetry, private investigator surveillance logs, and millions of crowdsourced web sleuth discussions. A human detective simply cannot cross-correlate decades of scattered evidence in their head.

**My core question was:** What if an elite squad of **6 specialized AI agents** could collaborate in real time—each handling a distinct forensic role (Archivist, Chronologist, Alibi Disprover, Criminal Profiler, Senior Detective Critic, and Rogatory Action Planner)—to dynamically reconstruct the crime board, test hypotheses, and deliver an **auditable Official Investigation Verdict**? That vision drove me to build **ColdCaseAI**.

---

## 🔍 2. What it does

**ColdCaseAI** is an AI-powered forensic investigation workstation that turns real unsolved cold cases into fully interactive, multimodal crime boards:

1. **Cinematic Crime Pinboard Canvas:** A zoomable, pannable, physics-enabled corkboard where you can freely drag suspect Polaroids, read contradictory alibi notes, inspect historic newspaper clippings, review PI stakeouts, and see **dynamic red elastic threads** linking correlated evidence in real time.
2. **Interactive Forensic Multimedia Player (CRT Surveillance / Audio):** Clicking any video or audio evidence card launches a declassified retro CRT player with real-time animated audio spectrogram equalizers, ticking timecodes, and speech synthesis narration of key witness depositions.
3. **Collaborative 6-Agent Reasoning Pipeline:**
   * 🕵️ **Agent 01 (OSINT & Classified Archives):** Mines declassified records, public archives, and live open intelligence.
   * ⏱️ **Agent 02 (Timeline & Telemetry):** Reconstructs minute-by-minute movements and isolates unaccounted temporal gaps.
   * ⚖️ **Agent 03 (Alibi Contradiction Detector):** Pits suspect sworn affidavits against hard physical telemetry to detect lies.
   * 🧠 **Agent 04 (Criminal Profiler & Hypotheses):** Analyzes criminal motive, psychological MO, and operational opportunities.
   * 🛡️ **Agent 05 (Senior Detective Critic):** Assigns NATO/Interpol-grade intelligence reliability ratings (Grade A1 to D4) to eliminate hallucinations.
   * ⚡ **Agent 06 (Official Synthesis & Next Action):** Formulates formal charges and an immediate rogatory subpoena plan.
4. **Official Investigation Verdict & Classified Dossier:** Displays a centered, prominent verdict card and opens a formal judicial ruling report with actionable next steps.

---

## 🛠️ 3. How I built it

As a solo developer, I designed ColdCaseAI to be fast, lightweight, and resilient:

* **Multi-Agent Orchestrator & Backend:** Built with **FastAPI** and **Python 3.11**, coordinating all 6 agentic prompts and structured Pydantic schemas.
* **AI Intelligence & LLM:** Powered by the **Google Gemini 2.5 / 3.7** API through the Google AI SDK, with a sovereign deterministic fallback engine guaranteeing zero downtime during judge evaluation.
* **Frontend Canvas & UI:** Crafted in pure, high-performance HTML5, CSS3, and Vanilla JavaScript—no heavy frontend frameworks—ensuring 60 FPS drag-and-drop mechanics, dynamic SVG trigonometric string calculations with drop shadows, and responsive glassmorphism.
* **Live OSINT Engine:** Live API connector to Wikimedia / global open intelligence endpoints to fetch real-time background context.
* **Deployment & Infrastructure:** Containerized with **Docker** and deployed on **Google Cloud Run (Serverless)** with automated Google Cloud Build and GitHub integration.

---

## 🧗 4. Challenges I ran into

* **Real-Time Red String Geometry:** Calculating responsive SVG vector coordinates `(x1, y1) -> (x2, y2)` connecting rotated evidence cards that users can drag anywhere on the board without UI lag.
* **Eliminating AI Hallucinations in Forensics:** Judicial intelligence cannot tolerate made-up evidence. I solved this by implementing Agent 05 (Critic), which enforces strict NATO/Interpol grading scales and cross-checks every clue before certifying a verdict.
* **Information Density vs. Ergonomics:** Balancing 9 complex historical case files, an interactive corkboard, live web intelligence, and a 6-agent feed within a clean, intuitive layout that looks stunning on screens of all sizes.

---

## 🏅 5. Accomplishments that I'm proud of

* Building an end-to-end multi-agent operating system solo, from architectural design and backend orchestration to UI/UX and serverless cloud deployment.
* Creating an immersive, dark-mode forensic aesthetic that makes users feel like lead investigators in an elite tactical cold case squad.
* Giving **every single case a unique, realistic evidence topology** (6 to 8 forensic items per case: decoded cipher matrices, DNA evidence, titanium metallurgy reports, surgical autopsy bisections, and offshore cryptocurrency flowcharts).
* Achieving sub-second agentic synthesis response times.

---

## 📚 6. What I learned

* Multi-agent collaboration thrives when each agent has a strictly demarcated persona and schema, outperforming a single monolithic prompt.
* Subtle sensory details (the ticking timecode, the pulsing audio spectrogram, the tactile snap of dragging evidence on cork) make AI software feel alive and engaging.

---

## 🚀 7. What's next for ColdCaseAI

* **User Evidence Uploads:** Allowing real detectives, journalists, and enthusiasts to upload their own case PDFs and crime scene photos to auto-generate a custom investigative crime board.
* **Investigative Genetic Genealogy (IGG) Module:** Adding DNA kinship clustering and timeline prediction.
* **Collaborative Multiplayer Squad Room:** Enabling multiple investigators across the globe to collaborate live on the same crime board.

---

## 🏷️ Built With (Tags)
`python` • `fastapi` • `google-gemini` • `gemini-api` • `google-cloud-run` • `docker` • `html5-canvas` • `svg-animations` • `multi-agent-systems` • `osint` • `ai-for-good`

---

## 🌐 Liens de Déploiement & Code
* 🔴 **Live Cloud Run URL :** https://coldcase-agentic-os-448033705367.us-central1.run.app
* 💻 **GitHub Repository :** https://github.com/chaibi-mustapha/coldcase-agentic-os
