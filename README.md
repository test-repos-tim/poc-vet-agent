# README

## POC Vet Agent Demo

This repo contains the local proof-of-concept (POC) for a veterinary clinic AI agent service as described in the Hermes `biz_service1` skill (AI Agent Service Business). It demonstrates an AI agent that answers clinic inquiries (appointments, emergencies, prescriptions) via a web chat widget running locally on the laptop.

### What’s Included

- **`/app/`** – Static frontend with a floating chat widget (`index.html`, `chat.css`, `chat.js`)
- **`/config/`** – Configuration files for the vet knowledge base and agent prompts
- **`/docs/`** – Development plan (`development_plan.md`) and progress tracker (`poc_progress.md`)
- **`/data/`** – SQLite database (`vet_agent.db`) for agent memory, appointments, prescriptions
- **`/logs/`** – Local logs for debugging

### How to Run (Local Testing)

1. Start Hermes Agent and its API bridge (see `docs/development_plan.md` Phase 2)
2. Open a browser and navigate to the website (hosted locally, e.g., `http://localhost:3000` if using a simple static server)
3. Use the chat widget to interact with the agent.

### Key Highlights

- **Local testing only** – no hosting or payment processing included in this POC.
- **Single niche** – veterinary clinic (“Paws & Claws Animal Hospital”) for focused development.
- **Prototype** – Core features: appointment booking, emergency triage, prescription refill.
- **Extensible** – The full `biz_service1` business model (billing, marketing, scaling) uses the open-source tool stack from `biz_tools` (PostHog, Chatwoot, Typebot, etc.) and is planned for the production phase.

### Development Status

- **Phase 0** completed (environment setup)
- **Phase 1** ongoing (website stub)
- **Phase 2** upcoming (Hermes agent integration)
- ... (see `docs/poc_progress.md` for full details)

### Backed-Up Skills

The repo does NOT include the Hermes skills themselves (skills are managed by Hermes internally). The skills are:

- `meta_income_skill` (metaskill for money/income skills)
- `biz_ideas` (business idea catalog)
- `biz_tools` (open-source repo replacements for paid SaaS)
- `biz_service1` (step-by-step plan for the AI Agent Service Business)

All of these live under `~/.hermes/skills/` on the current system. This repo simply stores the POC website and development artifacts.
