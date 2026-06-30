# Claude Skills

A snapshot of my personal Claude Code skills, copied from `~/.claude/skills/`. Each subdirectory is a self-contained skill with its own `SKILL.md` (and any supporting scripts/templates).

## Install

Drop the skills you want into your own Claude Code skills directory:

```bash
cp -r <skill-name> ~/.claude/skills/
```

Once present, Claude Code picks them up automatically and they become invokable via `/<skill-name>` (or by description match).

## Skills

| Skill | Trigger | What it does |
|---|---|---|
| [faculty-review-csv](faculty-review-csv/) | `/faculty-review-csv` | Mines a WhatsApp chat export for faculty mentions and writes a Take / Avoid / Mixed CSV with sentiment, traits, confidence, and verbatim evidence. Built for VIT FFCS slot planning. |
| [frontend-design](frontend-design/) | description match | Generates distinctive, production-grade frontend UI (components, pages, posters, dashboards) that avoids generic AI aesthetics. |
| [graphify](graphify/) | `/graphify` | Turns any input (code, docs, papers, images, videos) into a knowledge graph and answers questions against it. |
| [new-issue](new-issue/) | `/new-issue` | Interactively creates a GitHub issue: detects type (bug/feature/chore/docs), writes a structured body with acceptance criteria, and adds it to the project board as Backlog. |
| [plan-project](plan-project/) | `/plan-project` | Sets up a GitHub Project board, gathers requirements, refines them into ordered user stories, creates issues, plans sprints with milestones, and assigns tasks. |
| [project-research](project-research/) | description match | Deep-researches a project idea — features, tasks, tech decisions, competitors, risks — and outputs a structured report. |
| [project-review-deck](project-review-deck/) | description match | Reads the actual codebase and builds a project-review deck (PPTX or animated HTML) with data-flow / architecture diagrams. |
| [scrum-board](scrum-board/) | description match | Builds a scrum board from project tasks: 1-week sprint markdown files, sprint count auto-decided from task volume. Usually run after `project-research`. |
| [start-task](start-task/) | `/start-task` | Picks up an assigned issue from Backlog, refines it into a user story, moves to Ready, creates a feature branch, implements, commits, merges into `dev`, opens a PR to `main`, and moves the issue to In Review. |

## Layout

Each skill follows the standard Claude Code skill format:

```
<skill-name>/
  SKILL.md      # frontmatter (name, description) + instructions
  ...           # optional scripts, templates, assets
```

The `description` field in each `SKILL.md` is what Claude Code matches against to decide when to invoke a skill automatically.
