# Claude Skills

A snapshot of my personal Claude Code skills, synced from `~/.zepher/skills/` (linked into `~/.claude/skills/`). Each subdirectory is a self-contained skill with its own `SKILL.md` (and any supporting scripts/templates).

## Install

Drop the skills you want into your own Claude Code skills directory:

```bash
cp -r <skill-name> ~/.claude/skills/
```

Once present, Claude Code picks them up automatically and they become invokable via `/<skill-name>` (or by description match).

## Skills

| Skill | What it does |
|---|---|
| [agy-orchestrator](agy-orchestrator/) | Orchestrate Antigravity (`agy`) CLI agents as cheap workers while Claude acts as senior manager. |
| [architecture-building](architecture-building/) | Design the software architecture from the system definition and NFRs: architectural drivers, C4 L2/L3 diagrams, style & patterns with trade-offs, technology selection with justified alternatives, cross-cutting conce… |
| [business-pitch-writing](business-pitch-writing/) | Write or sharpen a business pitch — elevator pitch, one-pager, investor pitch, pitch deck narration, or "sell me your idea" summary — so it reads like a compelling story instead of a corporate brochure. |
| [cad-3d-print](cad-3d-print/) | Design parametric 3D printable models, mechanical parts, brackets, adapters, and enclosures using OpenSCAD, compile them into STL/3MF, and verify fit tolerances. |
| [deep-research](deep-research/) | Use this skill instead of WebSearch for ANY question requiring web research. |
| [faculty-review-csv](faculty-review-csv/) | Generate a faculty/teacher review CSV from a WhatsApp group chat export. |
| [find-skills](find-skills/) | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. |
| [frontend-aesthetic](frontend-aesthetic/) | Build polished, human-crafted web interfaces with restrained visual systems, strong hierarchy, authentic product UI, and deliberate responsive behavior. |
| [frontend-design](frontend-design/) | Create distinctive, production-grade frontend interfaces with high design quality. |
| [functional-requirements](functional-requirements/) | Turn prioritized requirements into precise, testable functional requirements using Use Cases and User Stories plus a FURPS+ coverage check. |
| [gamma-ui-style](gamma-ui-style/) | Use this skill whenever the user wants a UI, landing page, or dashboard built in the "Gamma.app style" — warm cream backgrounds, soft pastel gradient blobs, big rounded pill buttons, generous whitespace, sparkle/badge… |
| [graphify](graphify/) | any input (code, docs, papers, images, videos) to knowledge graph. |
| [implementation-plan-reviewer](implementation-plan-reviewer/) | Use this skill whenever an agent or user submits an implementation plan for review, critique, or gap analysis. |
| [new-issue](new-issue/) | Create a new GitHub issue interactively from any repo. |
| [non-functional-requirements](non-functional-requirements/) | Capture quality attributes using ISO/IEC 25010, quantify each with a measurable target and measurement method, record trade-offs and compliance. |
| [notebooklm-obsidian-notes](notebooklm-obsidian-notes/) | Ingest, clean, and format Google NotebookLM or Gemini study outputs into publication-grade Obsidian exam notes. |
| [pcb-design](pcb-design/) | Design printed circuit boards (PCBs) and electronic circuits, calculate passive components, generate KiCad schematics, script component placement via Python (pcbnew), route traces using Freerouting, run DRC, and expor… |
| [plan-project](plan-project/) | Set up a GitHub Project board for the current repo if one does not exist, gather requirements from the user, refine them into properly ordered user stories, create GitHub issues, plan sprints with milestones, and assi… |
| [project-research](project-research/) | Deep research a project idea. |
| [project-review-deck](project-review-deck/) | Build a visually appealing presentation for a project review by reviewing the actual codebase and generating slides — including data-flow / architecture diagrams — that match the user's stated requirements. |
| [pyq-topic-doc](pyq-topic-doc/) | Build a verified, exam-ready markdown document covering every real past-year-question on one topic. |
| [requirements-analysis](requirements-analysis/) | Elicit, prioritize, and validate requirements using mixed techniques (interviews, workshops, observation, documents, prototypes) and MoSCoW / weighted voting, then validate against IEEE 830 checks and emit a traceab… |
| [scrum-board](scrum-board/) | Builds a scrum board from project tasks. |
| [sdlc-init](sdlc-init/) | Run the full set of software-development INITIAL phases for a project: stakeholder analysis, requirements elicitation, functional requirements, non-functional requirements, requirement validation / SRS, system build… |
| [se-docs](se-docs/) | Generate professional Microsoft Word (.docx) documents for software-engineering projects — WBS + Gantt, SRS, design docs, test plans, vision/scope, project reports. |
| [setup-nix-shell](setup-nix-shell/) | Detect the codebase language/framework, identify dependencies, generate a corresponding shell.nix file (and language-specific manifests if missing), and test/verify the nix-shell environment. |
| [software-inception](software-inception/) | Run the full front end of the software lifecycle — stakeholder analysis, requirements elicitation, functional and non-functional requirements, use cases and system modeling, architecture design, ADRs, and traceability… |
| [stakeholder-requirements](stakeholder-requirements/) | Identify, classify, and analyze all project stakeholders; build a stakeholder register, engagement plan, and RACI. |
| [start-task](start-task/) | Pick up an assigned GitHub issue from the project Backlog, refine it into a detailed user story, move it to Ready, create the correct feature branch, implement the feature or fix, commit, verify with the user, merge t… |
| [system-building](system-building/) | Define the system as a whole before detailed architecture: scope (in/out), build/ buy/reuse, C4 Level 0/1 context, high-level subsystems, and core data flows. |
| [vhelpcc-pyq](vhelpcc-pyq/) | Download VIT past year question papers (PYQs) from vhelpcc.com for a given course. |
| [zepher-data-vault](zepher-data-vault/) | Automate team data management, secure secret vaulting (.env encryption & passhash generation), and heavy asset distribution via blob storage (AWS S3, Cloudflare R2, Google Drive). |

## Layout

Each skill follows the standard Claude Code skill format:

```
<skill-name>/
  SKILL.md      # frontmatter (name, description) + instructions
  ...           # optional scripts, templates, assets
```

The `description` field in each `SKILL.md` is what Claude Code matches against to decide when to invoke a skill automatically.
