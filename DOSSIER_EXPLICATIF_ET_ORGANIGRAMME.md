# 🕵️‍♂️ ColdCase Detective AI — Dossier Explicatif & Organigramme Complet

> **Document de Référence & Architecture Technique**  
> *Système Multi-Agents Autonome & Graphe de Connaissances Criminelles pour la Résolution d'Affaires Non Résolues.*

---

## 🎯 1. But & Vision du Projet

### Le Problème Réel
Les affaires criminelles non résolues (Cold Cases) restent bloquées pendant des années ou des décennies pour trois raisons majeures :
1. **La fragmentation des preuves** : Les indices, procès-verbaux, dépositions et enregistrements sont éparpillés dans des cartons ou des formats hétérogènes.
2. **L'oubli des contradictions temporelles** : Un suspect a menti en 1998, mais l'incohérence n'est visible que lorsqu'on croise son alibi avec un témoignage de 2012 ou une télémétrie de péage d'autoroute.
3. **Le biais de confirmation humain** : Les enquêteurs peuvent s'enfermer dans une piste sans tester d'autres hypothèses.

### La Solution "ColdCase Detective AI"
Une **suite de 6 agents IA spécialisés et autonomes** orchestrés par Google ADK & Gemini, connectés à un **Graphe de Connaissances ("Murder Board")** et à l'API publique du FBI. Les agents analysent le dossier, identifient mathématiquement les mensonges d'alibi, formulent une théorie avec score de probabilité, la stress-testent de manière adverse, et prescrivent l'action d'enquête prioritaire.

---

## 📊 2. Organigramme & Architecture du Système

```mermaid
flowchart TD
    subgraph SOURCES["🌐 Sources de Données & Entrées"]
        A1["API FBI Open Data\n(api.fbi.gov/wanted)"] --> INGEST
        A2["Archives & Dépositions\n(alibis_and_statements.json)"] --> INGEST
        A3["Dossiers d'Affaires\n(cases.json)"] --> INGEST
        A4["Télémétrie & Preuves\n(Péages, Caméras, Horodatages)"] --> INGEST
        USER["👮‍♂️ Enquêteur / Utilisateur\n(Console Web)"] --> INGEST["🎯 Requête d'Investigation"]
    end

    subgraph PIPELINE["🤖 Chaîne Multi-Agents (Google ADK + Gemini 3.5 Flash)"]
        direction TB
        
        AG1["1. FBI & OSINT Archive Agent\n(Extraction des dossiers, modus operandi, suspects)"]
        AG2["2. Timeline & Forensics Agent\n(Reconstitution chronologique minute par minute)"]
        AG3["3. Alibi Contradiction Agent\n(Détection des mensonges et failles spatio-temporelles)"]
        AG4["4. Profiler & Hypothesis Agent\n(Génération de la théorie H1 + Score de Confiance)"]
        AG5["5. Senior Detective Critic (Adversarial)\n(Stress-test critique, avocat du diable, élimination des biais)"]
        AG6["6. Breakthrough Lead Agent\n(Prescription de l'action décisive : mandat, ADN, interrogatoire)"]

        INGEST --> AG1
        AG1 --> AG2
        AG2 --> AG3
        AG3 --> AG4
        AG4 --> AG5
        AG5 --> AG6
    end

    subgraph GRAPH["🕸️ Knowledge Graph ('Murder Board')"]
        N1["🔴 Nœud Suspect"] <-->|"ALIBI_CONTRADICTION"| N2["🟡 Nœud Témoignage Train"]
        N1 <-->|"TELEMETRY_CONFLICT"| N3["🔵 Nœud Péage A9 (23h12)"]
        N1 <-->|"ACCOMPLICE"| N4["🔴 Nœud Complice"]
        N4 <-->|"FINANCIAL_LINK"| N5["🟢 Nœud Coffre Zurich #402"]
    end

    subgraph OUTPUT["🖥️ Restitution & Prise de Décision"]
        OUT1["📊 Console Web Interactive (Murder Board SVG)"]
        OUT2["📑 Piste d'audit structurée (Schemas Pydantic)"]
        OUT3["⚡ Ordre de mission opérationnel (Next Lead)"]
    end

    AG3 -.-> GRAPH
    AG4 -.-> GRAPH
    AG6 --> OUTPUT
    GRAPH --> OUT1
```

---

## 🔬 3. Détail des 6 Rôles Agents

| # | Agent | Modèle / Outils | Rôle Opérationnel | Données Produites |
|---|---|---|---|---|
| **1** | **FBI OSINT Agent** | `fetch_fbi_wanted_cases`, `load_local_cases` | Récupère en direct les criminels recherchés, modus operandi, alias et photos. | Synthèse du profil criminel et antécédents |
| **2** | **Timeline Agent** | `load_witness_statements` | Reconstitue l'emploi du temps de chaque personne d'intérêt à la minute près. | Tableau chronologique des mouvements déclarés |
| **3** | **Contradiction Agent** | `detect_alibi_contradictions` | **Le cœur du système** : compare les déclarations entre elles et avec les faits matériels pour isoler les faux alibis. | `ContradictionResult` (champs contradictoires précis) |
| **4** | **Profiler Agent** | `mine_cold_case_network` | Construit la théorie du crime (mobile, complices, opportunité) et calcule un indice de confiance (0.0 à 1.0). | `InvestigationHypothesis` (théorie H1) |
| **5** | **Senior Detective Critic** | *Prompting Adversarial* | Attaque méthodiquement la théorie proposée pour vérifier s'il existe une variable cachée ou un risque d'erreur judiciaire. | `DetectiveReviewResult` (Verdict, solidité, points aveugles) |
| **6** | **Breakthrough Action Agent** | `recommend_breakthrough_lead` | Transforme l'analyse en action concrète et immédiate pour la police scientifique ou les juges d'instruction. | `NextLeadAction` (mandat, cible à confronter) |

---

## 💻 4. Structure Technique du Répertoire

```text
coldcase-detective-ai/
├── coldcase_agent/
│   ├── __init__.py           # Export du workflow root_agent
│   ├── agent.py              # Définition des 6 agents ADK et orchestration Workflow
│   ├── schemas.py            # Modèles de données Pydantic typés
│   └── tools.py              # Connecteurs API FBI (live), Graphe et archives
├── api/
│   └── main.py               # Serveur FastAPI (mode MOCK + mode LIVE Gemini)
├── data/
│   ├── cases.json            # Dossiers d'enquêtes criminelles
│   └── alibis_and_statements.json # Dépositions, témoignages et PV
├── web/
│   └── index.html            # Console d'investigation avec "Murder Board"
├── .env.example              # Configuration des clés
├── requirements.txt          # Dépendances Python
└── README.md                 # Guide de démarrage rapide
```

---

## 🎬 5. Argumentaire & Pitch pour Concours

* **Accroche :** *"Et si les affaires non résolues depuis 25 ans pouvaient être débloquées en 15 secondes grâce à un graphe d'agents détectant automatiquement les failles temporelles ?"*
* **Démonstration Clé :** Montrer comment l'agent met en échec l'alibi du suspect principal (déposition du train de 1998 confrontée au conducteur et au badge de télépéage) et allume en rouge les connexions du Murder Board.
* **Point fort pour le jury Devpost :** L'API FBI fonctionne en temps réel sans clé, offrant une démo immédiatement crédible et impressionnante.
