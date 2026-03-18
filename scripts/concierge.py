#!/usr/bin/env python3
"""
CheatCodes Skill Library — Concierge
=====================================
Your personal guide to discovering, launching, and saving skills.

Run locally:
    python scripts/concierge.py

Run without cloning (one-liner):
    curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/concierge.py | python -

No external packages needed — pure Python 3.8+ standard library.
"""

import json
import os
import platform
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Optional

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = REPO_ROOT / "skills"
CONFIG_DIR = Path.home() / ".cheatcodes"
FAVORITES_FILE = CONFIG_DIR / "favorites.json"

# ── ANSI colours ──────────────────────────────────────────────────────────────
def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if not hasattr(sys.stdout, "isatty"):
        return False
    return sys.stdout.isatty()

USE_COLOR = _supports_color()

def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text

def bold(t):    return _c("1", t)
def dim(t):     return _c("2", t)
def cyan(t):    return _c("36", t)
def green(t):   return _c("32", t)
def yellow(t):  return _c("33", t)
def red(t):     return _c("31", t)
def magenta(t): return _c("35", t)
def blue(t):    return _c("34", t)
def white(t):   return _c("97", t)

# ── Embedded skill catalog ────────────────────────────────────────────────────
# This is the built-in catalog so the concierge works even without the repo.
# When run inside the repo, it auto-loads from YAML files and merges.
CATALOG: dict = {
    "productivity": [
        {
            "id": "task-planner",
            "name": "Task Planner",
            "emoji": "📋",
            "tagline": "Break any goal into clear, prioritised steps",
            "description": (
                "Tell it your goal and it gives you a full, phased action plan "
                "with priorities, effort estimates, and dependencies."
            ),
            "status": "stable",
            "latest_version": "v1",
            "beta_version": "v2-beta",
            "good_for": ["Projects", "Planning", "Teams", "Solo work"],
            "versions": {
                "v1": {
                    "label": "v1 — Stable ✅",
                    "status": "stable",
                    "note": "Simple, reliable task breakdown. Safe for everyday use.",
                    "placeholders": {
                        "GOAL": "What is your goal or project?",
                        "TEAM SIZE": "Who is involved? (e.g. 'just me', '4-person team', 'PM + 2 engineers')",
                        "TIMELINE": "What is your deadline or available time? (e.g. '2 weeks', 'by Friday')",
                        "CONSTRAINTS": "Any limitations? (e.g. 'no budget', 'must use Google Sheets') — or type 'none'",
                    },
                    "prompt": (
                        "You are a strategic project planner. Your job is to break down the "
                        "following goal into a clear, prioritised, actionable task list.\n\n"
                        "Goal: [GOAL]\n"
                        "Team: [TEAM SIZE]\n"
                        "Timeline: [TIMELINE]\n"
                        "Constraints: [CONSTRAINTS]\n\n"
                        "Please produce:\n"
                        "1. A brief restatement of the goal and success criteria.\n"
                        "2. A phased task breakdown (Phase 1, Phase 2, ...) where each phase has a clear outcome.\n"
                        "3. Within each phase, list individual tasks with: task name, description (1–2 sentences), "
                        "estimated effort, priority (Critical / High / Medium / Low), and dependencies.\n"
                        "4. A final summary table sorted by priority.\n\n"
                        "Format the output in clean Markdown."
                    ),
                },
                "v2-beta": {
                    "label": "v2-beta — Beta ⚠️",
                    "status": "beta",
                    "note": "Adds parallel tracks and dependency graphs. Try it and share feedback!",
                    "placeholders": {
                        "GOAL": "What is your goal or project?",
                        "TEAM": "Team size and roles (e.g. '1 PM, 2 engineers, 1 designer')",
                        "TIMELINE": "Target completion date or duration",
                        "CONSTRAINTS": "Any hard constraints — budget, tools, integrations, etc. (or 'none')",
                    },
                    "prompt": (
                        "You are an expert project planner specialising in parallel execution.\n\n"
                        "Goal: [GOAL]\n"
                        "Team: [TEAM]\n"
                        "Timeline: [TIMELINE]\n"
                        "Constraints: [CONSTRAINTS]\n\n"
                        "Produce the following in Markdown:\n\n"
                        "## 1. Goal & Success Criteria\n"
                        "## 2. Parallel Tracks\n"
                        "Identify independent workstreams. For each: track name, task list with effort ranges, priorities, dependencies.\n"
                        "## 3. Dependency Graph\n"
                        "Text-based: TaskA → TaskB → TaskC\n"
                        "## 4. Milestone Summary\n"
                        "3–5 milestones with target dates.\n"
                        "## 5. Risk Register\n"
                        "Top 3 risks with likelihood, impact, and mitigation."
                    ),
                },
            },
        }
    ],
    "automation": [
        {
            "id": "code-reviewer",
            "name": "Code Reviewer",
            "emoji": "🔍",
            "tagline": "Get an expert code review in seconds",
            "description": (
                "Paste any code or diff and get a structured review with bug severity, "
                "security issues, and clear fix suggestions — ready to paste into a PR."
            ),
            "status": "stable",
            "latest_version": "v1",
            "beta_version": None,
            "good_for": ["Developers", "Code quality", "Pull requests", "Security"],
            "versions": {
                "v1": {
                    "label": "v1 — Stable ✅",
                    "status": "stable",
                    "note": "Comprehensive code review with severity ratings.",
                    "placeholders": {
                        "LANGUAGE / FRAMEWORK": "What language and framework? (e.g. 'Python / FastAPI', 'JavaScript / React')",
                        "REVIEW FOCUS": "What should I focus on? (e.g. 'correctness, security', or just 'all')",
                        "CODE OR DIFF": "Paste your code or diff below:",
                    },
                    "prompt": (
                        "You are an expert software engineer conducting a thorough code review.\n\n"
                        "Language / Framework: [LANGUAGE / FRAMEWORK]\n"
                        "Review Focus: [REVIEW FOCUS]\n\n"
                        "Code / Diff:\n[CODE OR DIFF]\n\n"
                        "Produce the following in Markdown:\n\n"
                        "## Summary\n"
                        "One paragraph overview of the code and your overall assessment.\n\n"
                        "## Issues Found\n"
                        "| Severity | File / Line | Issue | Suggestion |\n"
                        "|----------|-------------|-------|------------|\n"
                        "(🔴 Critical, 🟠 Major, 🟡 Minor, 🔵 Suggestion)\n\n"
                        "## Security Checklist\n"
                        "- [ ] No hardcoded secrets\n- [ ] Input validation present\n"
                        "- [ ] No injection vectors\n- [ ] Sensitive data handled safely\n\n"
                        "## Test Coverage Assessment\n\n"
                        "## Overall Recommendation\n"
                        "APPROVE / REQUEST CHANGES / NEEDS DISCUSSION — and why."
                    ),
                },
            },
        }
    ],
    "communication": [
        {
            "id": "meeting-summarizer",
            "name": "Meeting Summarizer",
            "emoji": "📝",
            "tagline": "Turn messy notes into a clean action plan",
            "description": (
                "Paste your raw meeting transcript or bullet points and get a structured "
                "summary with decisions, action items (with owners), and a shareable TL;DR."
            ),
            "status": "stable",
            "latest_version": "v1",
            "beta_version": None,
            "good_for": ["Teams", "Managers", "Async work", "Any meeting type"],
            "versions": {
                "v1": {
                    "label": "v1 — Stable ✅",
                    "status": "stable",
                    "note": "Works with transcripts, bullet notes, or rough scribbles.",
                    "placeholders": {
                        "MEETING TYPE": "What kind of meeting? (e.g. 'sprint planning', 'standup', 'decision meeting', 'brainstorm')",
                        "PARTICIPANTS": "Who was there? (e.g. 'Alice (PM), Bob (Eng), Carol (Design)')",
                        "DATE": "When was the meeting? (e.g. '2024-03-15' or 'today')",
                        "NOTES OR TRANSCRIPT": "Paste your raw notes or transcript here:",
                    },
                    "prompt": (
                        "You are an expert meeting facilitator and note-taker.\n\n"
                        "Meeting Type: [MEETING TYPE]\n"
                        "Participants: [PARTICIPANTS]\n"
                        "Date: [DATE]\n\n"
                        "Raw Notes / Transcript:\n[NOTES OR TRANSCRIPT]\n\n"
                        "Produce the following in Markdown:\n\n"
                        "## TL;DR\n"
                        "2–3 sentences capturing the most important outcome.\n\n"
                        "## Decisions Made\n"
                        "Bullet list of concrete decisions.\n\n"
                        "## Action Items\n"
                        "| # | Task | Owner | Due Date | Notes |\n"
                        "|---|------|-------|----------|-------|\n\n"
                        "## Open Questions / Parking Lot\n\n"
                        "## Key Discussion Points\n"
                        "3–5 bullet points.\n\n"
                        "## Next Steps"
                    ),
                },
            },
        }
    ],
    "data": [
        {
            "id": "data-analyzer",
            "name": "Data Analyzer",
            "emoji": "📊",
            "tagline": "Get insights from any dataset",
            "description": (
                "Describe your data or paste a CSV sample and ask a business question. "
                "Get back key findings, anomalies, trends, and the exact charts to build."
            ),
            "status": "stable",
            "latest_version": "v1",
            "beta_version": None,
            "good_for": ["Analysts", "Business teams", "CSV data", "Reporting"],
            "versions": {
                "v1": {
                    "label": "v1 — Stable ✅",
                    "status": "stable",
                    "note": "Works with any tabular data. Describe it or paste up to ~50 rows.",
                    "placeholders": {
                        "BUSINESS QUESTION": "What do you want to learn from this data? (e.g. 'Which products are underperforming?')",
                        "DATASET DESCRIPTION": "Brief description of your data (rows, columns, time range, source)",
                        "SAMPLE DATA": "Paste your CSV header + up to 50 rows here:",
                    },
                    "prompt": (
                        "You are a senior data analyst.\n\n"
                        "Business Question: [BUSINESS QUESTION]\n"
                        "Dataset Description: [DATASET DESCRIPTION]\n\n"
                        "Sample Data:\n[SAMPLE DATA]\n\n"
                        "Produce the following in Markdown:\n\n"
                        "## Dataset Overview\n"
                        "Row/column count, data types, missing values.\n\n"
                        "## Summary Statistics\n"
                        "Key stats for numeric columns.\n\n"
                        "## Key Findings\n"
                        "5 most important insights answering the business question.\n\n"
                        "## Anomalies & Outliers\n\n"
                        "## Trends & Correlations\n\n"
                        "## Recommended Visualisations\n"
                        "List 3–5 charts (type, axes, insight revealed).\n\n"
                        "## Recommended Next Steps"
                    ),
                },
            },
        }
    ],
}

CATEGORY_EMOJI = {
    "productivity": "🚀",
    "automation": "⚙️",
    "communication": "💬",
    "data": "📊",
    "devops": "🔧",
    "security": "🔒",
    "custom": "🎨",
}

REPO_ISSUES_URL = "https://github.com/jac007x/CheatCodes-Skill-Library/issues/new"


# ── Terminal helpers ───────────────────────────────────────────────────────────

def clear_screen() -> None:
    os.system("cls" if platform.system() == "Windows" else "clear")


def terminal_width() -> int:
    return shutil.get_terminal_size((80, 24)).columns


def hr(char: str = "─", color_fn=dim) -> None:
    print(color_fn(char * min(terminal_width(), 70)))


def print_wrapped(text: str, indent: int = 0, width: int = 68) -> None:
    prefix = " " * indent
    for line in textwrap.wrap(text, width - indent):
        print(prefix + line)


def pause(msg: str = "Press Enter to continue…") -> None:
    try:
        input(dim(f"\n  {msg}"))
    except (EOFError, KeyboardInterrupt):
        pass


def ask(prompt: str, default: str = "") -> str:
    """Prompt for input with an optional default."""
    hint = f" [{dim(default)}]" if default else ""
    try:
        value = input(f"\n  {cyan('?')} {prompt}{hint}\n  {bold('›')} ").strip()
        return value if value else default
    except (EOFError, KeyboardInterrupt):
        return default


def ask_multiline(prompt: str) -> str:
    """Prompt for multi-line input. User types END on a blank line to finish."""
    print(f"\n  {cyan('?')} {prompt}")
    print(dim("  (Type or paste your content. When done, type END on a new line and press Enter.)"))
    lines = []
    try:
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
    except (EOFError, KeyboardInterrupt):
        pass
    return "\n".join(lines)


def menu(title: str, options: list[tuple[str, str]], back_label: str = "← Back") -> int:
    """
    Display a numbered menu. Returns 0-indexed selection, or -1 for back/quit.
    options: list of (emoji+label, sublabel) tuples
    """
    print()
    hr()
    print(f"  {bold(title)}")
    hr()
    for i, (label, sub) in enumerate(options, 1):
        num = cyan(f"  {i:>2}.")
        sub_str = f"  {dim(sub)}" if sub else ""
        print(f"{num}  {label}{sub_str}")
    print(f"  {dim('  0.')  }  {dim(back_label)}")
    hr()

    while True:
        try:
            raw = input(f"  {bold('Enter a number:')} ").strip()
        except (EOFError, KeyboardInterrupt):
            return -1
        if raw == "0":
            return -1
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return idx
        print(red("  Please enter a valid number from the list."))


# ── Clipboard ─────────────────────────────────────────────────────────────────

def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard. Returns True on success."""
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True, timeout=5)
            return True
        elif system == "Linux":
            for cmd in (["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]):
                if shutil.which(cmd[0]):
                    subprocess.run(cmd, input=text.encode(), check=True, timeout=5)
                    return True
        elif system == "Windows":
            subprocess.run(["clip"], input=text.encode("utf-16"), check=True, timeout=5)
            return True
    except Exception:
        pass
    return False


# ── Favorites ─────────────────────────────────────────────────────────────────

def load_favorites() -> list[dict]:
    if FAVORITES_FILE.exists():
        try:
            return json.loads(FAVORITES_FILE.read_text())
        except Exception:
            return []
    return []


def save_favorites(favs: list[dict]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    FAVORITES_FILE.write_text(json.dumps(favs, indent=2))


def add_favorite(category: str, skill_id: str, version: str, skill_name: str) -> None:
    favs = load_favorites()
    entry = {
        "category": category,
        "skill_id": skill_id,
        "version": version,
        "name": skill_name,
    }
    # De-duplicate
    existing = [
        f for f in favs
        if not (f["category"] == category and f["skill_id"] == skill_id and f["version"] == version)
    ]
    existing.append(entry)
    save_favorites(existing)


def remove_favorite(idx: int) -> None:
    favs = load_favorites()
    if 0 <= idx < len(favs):
        favs.pop(idx)
        save_favorites(favs)


# ── Skill helpers ──────────────────────────────────────────────────────────────

def all_skills() -> list[tuple[str, dict]]:
    """Return flat list of (category, skill_dict) pairs."""
    result = []
    for cat, skills in CATALOG.items():
        for skill in skills:
            result.append((cat, skill))
    return result


def find_skill(category: str, skill_id: str) -> Optional[tuple[str, dict]]:
    for cat, skill in all_skills():
        if cat == category and skill["id"] == skill_id:
            return cat, skill
    return None


def status_badge(status: str) -> str:
    return {"stable": green("✅ stable"), "beta": yellow("⚠️  beta"),
            "deprecated": red("🔻 deprecated"), "archived": dim("🗄️  archived")}.get(status, status)


# ── Screens ───────────────────────────────────────────────────────────────────

def banner() -> None:
    clear_screen()
    width = min(terminal_width(), 72)
    lines = [
        "",
        cyan("  ╔══════════════════════════════════════════════════════════╗"),
        cyan("  ║") + bold(white("         ⚡ CheatCodes Skill Library Concierge ⚡         ")) + cyan("║"),
        cyan("  ║") + dim("       Your personal guide to skills — no tech skills needed  ") + cyan("║"),
        cyan("  ╚══════════════════════════════════════════════════════════╝"),
        "",
    ]
    for line in lines:
        print(line)


def show_welcome() -> None:
    banner()
    print(f"  {bold('Welcome!')} 👋  I'm your CheatCodes Concierge.")
    print()
    print_wrapped(
        "I'll help you find the right skill, walk you through using it, and "
        "set it up so you can launch it again in one click. You don't need to "
        "know anything about coding or AI — just answer a few questions and "
        "I'll do the rest.",
        indent=2,
    )
    print()
    print(f"  {dim('What is a skill?')}")
    print_wrapped(
        "A skill is a ready-made prompt you paste into an AI assistant (like "
        "ChatGPT, Claude, or Copilot). Each skill is designed to do one thing "
        "really well — like planning a project, reviewing code, or summarising "
        "a meeting.",
        indent=4,
    )
    pause("Press Enter to get started…")


def main_menu() -> str:
    """Show main menu, return action key."""
    banner()
    favs = load_favorites()
    fav_label = f"⭐  My Favourites  {dim(f'({len(favs)} saved)')}" if favs else "⭐  My Favourites  " + dim("(none yet)")
    options = [
        ("🗂️   Browse skills by category", "See all available skills, grouped by what they do"),
        ("🔎  Search for a skill", "Type keywords and I'll find the best match"),
        (fav_label, "Quickly re-launch a skill you've used before"),
        ("📥  Clone a skill to your computer", "Save a skill locally so you can use it offline"),
        ("🆕  Request a new skill", "Tell us what skill you need and we'll build it"),
        ("💡  Recommend an improvement", "Have an idea to make a skill better?"),
        ("❓  What is this? How does it work?", "New here? Start here for a quick tour"),
    ]
    choice = menu("What would you like to do?", options, back_label="Quit")
    actions = ["browse", "search", "favorites", "clone", "request", "recommend", "help"]
    return actions[choice] if choice >= 0 else "quit"


def screen_help() -> None:
    clear_screen()
    banner()
    print(bold("  ❓ How CheatCodes Works\n"))
    sections = [
        ("What is a skill?",
         "A skill is a carefully crafted prompt — a set of instructions — that "
         "you paste into an AI assistant like ChatGPT, Claude, or Microsoft Copilot. "
         "The skill tells the AI exactly what to do, so you get a great result "
         "without having to figure out the right words yourself."),
        ("How do I use a skill?",
         "1. Use this concierge (or browse skills/) to pick a skill.\n"
         "    2. I'll walk you through filling in your specific details.\n"
         "    3. Copy the completed prompt.\n"
         "    4. Paste it into your AI assistant.\n"
         "    5. Read the AI's response — done!"),
        ("What are versions?",
         "Each skill has versions — like v1 (stable) and v2-beta (new features "
         "being tested). Use the stable version for everyday work. Try the beta "
         "to get new features early and share feedback."),
        ("What is stable vs beta?",
         "✅ Stable means it's been tested and works reliably.\n"
         "    ⚠️  Beta means new features are available but may behave unexpectedly.\n"
         "       Always check the beta warning before using it for important work."),
        ("How do I save a skill?",
         "Use option 4 (Clone a skill) to save a copy to your computer. "
         "Or use Favourites to quickly re-launch skills you love."),
        ("How do I request a new skill?",
         "Use option 5 (Request a new skill) and fill in the short form. "
         "The team reviews requests 2–3 times a week."),
    ]
    for title, body in sections:
        print(f"\n  {bold(cyan(title))}")
        hr("·")
        # Handle multi-line bodies
        for para in body.split("\n"):
            print_wrapped(para.strip(), indent=4)
    pause()


def screen_browse() -> None:
    while True:
        clear_screen()
        banner()
        cats = list(CATALOG.keys())
        options = []
        for cat in cats:
            skills = CATALOG[cat]
            emoji = CATEGORY_EMOJI.get(cat, "📁")
            names = ", ".join(s["name"] for s in skills)
            options.append((f"{emoji}  {bold(cat.title())}", f"{len(skills)} skill(s): {names}"))
        choice = menu("Browse by Category", options)
        if choice < 0:
            return
        selected_cat = cats[choice]
        _browse_category(selected_cat)


def _browse_category(category: str) -> None:
    while True:
        clear_screen()
        banner()
        skills = CATALOG[category]
        emoji = CATEGORY_EMOJI.get(category, "📁")
        options = []
        for skill in skills:
            badge = status_badge(skill["status"])
            options.append((
                f"{skill['emoji']}  {bold(skill['name'])}  {badge}",
                skill["tagline"],
            ))
        choice = menu(f"{emoji} {category.title()} Skills", options)
        if choice < 0:
            return
        _skill_detail(category, skills[choice])


def _skill_detail(category: str, skill: dict) -> None:
    while True:
        clear_screen()
        banner()
        print(f"\n  {skill['emoji']}  {bold(skill['name'])}  —  {status_badge(skill['status'])}")
        hr()
        print_wrapped(skill["description"], indent=4)
        print()
        print(f"    {dim('Good for:')} {', '.join(skill['good_for'])}")
        print()

        # Show versions
        print(f"  {bold('Available Versions:')}")
        for vid, vinfo in skill["versions"].items():
            print(f"    {cyan(vid)}  {vinfo['label']}")
            print_wrapped(vinfo["note"], indent=8)
        print()

        options = [
            ("🚀  Use this skill now", "I'll guide you through it step by step"),
            ("⭐  Save to favourites", "Add to your quick-launch list"),
            ("📥  Clone to my computer", "Save the skill files locally"),
            ("📖  View the full README on GitHub", "Open in your browser"),
        ]
        choice = menu(f"What do you want to do with {skill['name']}?", options)

        if choice < 0:
            return
        elif choice == 0:
            _launch_wizard(category, skill)
        elif choice == 1:
            _add_to_favorites_ui(category, skill)
        elif choice == 2:
            _clone_ui(category, skill)
        elif choice == 3:
            url = (
                f"https://github.com/jac007x/CheatCodes-Skill-Library"
                f"/tree/main/skills/{category}/{skill['id']}"
            )
            _open_browser(url)


def _launch_wizard(category: str, skill: dict) -> None:
    """Step-by-step wizard to fill in a skill's prompt and copy it."""
    clear_screen()
    banner()
    print(f"\n  🚀  {bold('Skill Launch Wizard')}  —  {skill['emoji']} {skill['name']}")
    hr()
    print()
    print_wrapped(
        "I'll ask you a few questions. Your answers will be placed directly into "
        "the skill's prompt. When you're done, you can copy the full prompt and "
        "paste it into your AI assistant (ChatGPT, Claude, Copilot, etc.).",
        indent=4,
    )

    # Pick version if multiple
    version_ids = list(skill["versions"].keys())
    chosen_version_id = version_ids[0]  # default to first (stable)
    if len(version_ids) > 1:
        print()
        ver_options = [
            (vinfo["label"], vinfo["note"])
            for vinfo in skill["versions"].values()
        ]
        choice = menu("Which version?", ver_options)
        if choice < 0:
            return
        chosen_version_id = version_ids[choice]

    version = skill["versions"][chosen_version_id]

    # Beta warning
    if version["status"] == "beta":
        print()
        print(yellow("  ⚠️  Beta Warning"))
        hr("·")
        print_wrapped(
            "This is a beta version. It has new features that are still being "
            "tested. It should work well, but results may vary. Please share "
            "any feedback by opening an issue on GitHub.",
            indent=4,
        )
        proceed = ask("Continue with the beta version? (yes/no)", default="yes")
        if proceed.lower() not in ("yes", "y"):
            return

    # Collect placeholder values
    print()
    hr()
    print(f"  {bold('Step 1 of 2 — Fill in your details')}")
    hr()
    print()
    print_wrapped(
        "Answer each question below. Press Enter to accept a suggestion shown "
        "in [brackets], or type your own answer.",
        indent=4,
    )

    filled: dict[str, str] = {}
    placeholders = version["placeholders"]
    multiline_keys = {"CODE OR DIFF", "NOTES OR TRANSCRIPT", "SAMPLE DATA"}

    for key, question in placeholders.items():
        if key.upper() in multiline_keys:
            value = ask_multiline(question)
        else:
            value = ask(question)
        filled[key] = value or f"[{key}]"

    # Build completed prompt
    prompt_text = version["prompt"]
    for key, value in filled.items():
        prompt_text = prompt_text.replace(f"[{key}]", value)

    # Step 2 — Show and copy
    clear_screen()
    banner()
    print(f"\n  {bold('Step 2 of 2 — Your completed prompt')}")
    hr()
    print()
    print_wrapped(
        "Here is your completed prompt. Copy it and paste it into your "
        "AI assistant (ChatGPT, Claude, Copilot, etc.).",
        indent=4,
    )
    print()
    hr("═", color_fn=cyan)
    print()
    # Print the prompt, line-wrapped
    for line in prompt_text.split("\n"):
        if len(line) > 0:
            print(f"  {line}")
        else:
            print()
    print()
    hr("═", color_fn=cyan)

    # Clipboard
    print()
    copied = copy_to_clipboard(prompt_text)
    if copied:
        print(green("  ✅  Prompt copied to clipboard! Paste it into your AI assistant."))
    else:
        print(yellow(
            "  ℹ️  Clipboard not available in this environment.\n"
            "     Select all text between the ═══ lines above and copy it manually."
        ))

    # Save to file option
    print()
    save = ask("Save this prompt to a file for later? (yes/no)", default="no")
    if save.lower() in ("yes", "y"):
        filename = ask("File name", default=f"{skill['id']}-{chosen_version_id}-prompt.txt")
        try:
            Path(filename).write_text(prompt_text)
            print(green(f"  ✅  Saved to {filename}"))
        except Exception as e:
            print(red(f"  Could not save: {e}"))

    # Favourite
    print()
    fav = ask("Add this skill to your favourites? (yes/no)", default="yes")
    if fav.lower() in ("yes", "y"):
        add_favorite(category, skill["id"], chosen_version_id, skill["name"])
        print(green(f"  ⭐  Added {skill['name']} ({chosen_version_id}) to favourites!"))

    pause("Press Enter to return to the main menu…")


def _add_to_favorites_ui(category: str, skill: dict) -> None:
    version_ids = list(skill["versions"].keys())
    chosen = version_ids[0]
    if len(version_ids) > 1:
        opts = [(vinfo["label"], vinfo["note"]) for vinfo in skill["versions"].values()]
        choice = menu("Which version to favourite?", opts)
        if choice < 0:
            return
        chosen = version_ids[choice]
    add_favorite(category, skill["id"], chosen, skill["name"])
    print(green(f"\n  ⭐  {skill['name']} ({chosen}) added to favourites!"))
    pause()


def _clone_ui(category: str, skill: dict) -> None:
    clear_screen()
    banner()
    print(f"\n  📥  {bold('Clone a Skill to Your Computer')}")
    hr()
    print()
    print_wrapped(
        "Cloning saves the skill's files to your computer so you can use "
        "them offline, customise them, or build on top of them.",
        indent=4,
    )
    print()
    print(f"  {bold('Command to run:')}")
    print()
    clone_cmd = (
        f"bash <(curl -fsSL "
        f"https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/clone-skill.sh"
        f") {category}/{skill['id']}"
    )
    print(cyan(f"    {clone_cmd}"))
    print()
    print_wrapped(
        "Open your Terminal (Mac/Linux) or Command Prompt (Windows + Git Bash) "
        "and paste the command above. It will download the skill into a new "
        f"folder called '{skill['id']}' in your current directory.",
        indent=4,
    )
    print()
    copied = copy_to_clipboard(clone_cmd)
    if copied:
        print(green("  ✅  Command copied to clipboard. Paste it into your terminal!"))
    pause()


def screen_search() -> None:
    clear_screen()
    banner()
    print(f"\n  🔎  {bold('Search for a Skill')}")
    hr()
    query = ask("What do you want to do? (e.g. 'plan a project', 'review code', 'summarise meeting')").lower()
    if not query:
        return

    # Simple keyword match against name, tagline, description, good_for, tags
    STOP_WORDS = {
        "a", "an", "the", "and", "or", "for", "to", "in", "of", "is",
        "it", "i", "my", "me", "do", "how", "can", "with", "that",
    }
    search_words = [w for w in query.split() if w not in STOP_WORDS and len(w) > 1]

    results: list[tuple[str, dict, int]] = []
    for cat, skill in all_skills():
        score = 0
        # Name and tagline matches are worth extra weight
        name_blob = (skill["name"] + " " + skill["tagline"]).lower()
        full_blob = " ".join([
            skill["name"],
            skill["tagline"],
            skill["description"],
            " ".join(skill.get("good_for", [])),
            cat,
        ]).lower()
        for word in search_words:
            if word in name_blob:
                score += name_blob.count(word) * 3
            elif word in full_blob:
                score += full_blob.count(word)
        if score > 0:
            results.append((cat, skill, score))

    results.sort(key=lambda x: -x[2])

    if not results:
        print()
        print(yellow("  No skills matched that search."))
        print_wrapped(
            f"Try different words, or browse by category. You can also "
            f"request a new skill if it doesn't exist yet.",
            indent=4,
        )
        pause()
        return

    clear_screen()
    banner()
    options = []
    for cat, skill, _ in results:
        badge = status_badge(skill["status"])
        options.append((
            f"{skill['emoji']}  {bold(skill['name'])}  {dim(f'[{cat}]')}  {badge}",
            skill["tagline"],
        ))
    choice = menu(f"Search results for '{query}'", options)
    if choice >= 0:
        cat, skill, _ = results[choice]
        _skill_detail(cat, skill)


def screen_favorites() -> None:
    while True:
        clear_screen()
        banner()
        favs = load_favorites()
        if not favs:
            print(f"\n  {yellow('No favourites saved yet.')}")
            print_wrapped(
                "Browse skills and use a skill to add it to your favourites.",
                indent=4,
            )
            pause()
            return

        options = []
        for fav in favs:
            options.append((
                f"{fav.get('name', fav['skill_id'])}  {dim(fav['version'])}  {dim('[' + fav['category'] + ']')}",
                "Press to launch",
            ))

        choice = menu("⭐ My Favourites", options)
        if choice < 0:
            return

        fav = favs[choice]
        result = find_skill(fav["category"], fav["skill_id"])
        if result:
            cat, skill = result
            fav_options = [
                ("🚀  Launch this skill now", "Fill in your details and get your prompt"),
                ("🗑️   Remove from favourites", ""),
            ]
            action = menu(f"What do you want to do with {fav['name']}?", fav_options)
            if action == 0:
                _launch_wizard(cat, skill)
            elif action == 1:
                remove_favorite(choice)
                print(green(f"  Removed {fav['name']} from favourites."))
                pause()
        else:
            print(red(f"  Skill '{fav['skill_id']}' not found in catalog."))
            pause()


def screen_clone() -> None:
    clear_screen()
    banner()
    print(f"\n  📥  {bold('Clone a Skill to Your Computer')}")
    hr()
    print_wrapped(
        "Browse the skills below and I'll give you the exact command to "
        "clone it onto your computer.",
        indent=4,
    )
    cats = list(CATALOG.keys())
    cat_options = [
        (f"{CATEGORY_EMOJI.get(c, '📁')}  {c.title()}", "")
        for c in cats
    ]
    cat_choice = menu("Which category?", cat_options)
    if cat_choice < 0:
        return
    selected_cat = cats[cat_choice]
    skills = CATALOG[selected_cat]
    skill_options = [(f"{s['emoji']}  {s['name']}", s["tagline"]) for s in skills]
    skill_choice = menu(f"Which skill?", skill_options)
    if skill_choice < 0:
        return
    skill = skills[skill_choice]
    _clone_ui(selected_cat, skill)


def screen_request() -> None:
    clear_screen()
    banner()
    print(f"\n  🆕  {bold('Request a New Skill')}")
    hr()
    print_wrapped(
        "Don't see a skill you need? Request it! Fill in the short form on "
        "GitHub and the team will review it within a few days.",
        indent=4,
    )
    print()
    url = f"{REPO_ISSUES_URL}?template=skill_request.yml"
    print(f"  {bold('Open this link:')}")
    print()
    print(cyan(f"    {url}"))
    print()
    copied = copy_to_clipboard(url)
    if copied:
        print(green("  ✅  Link copied to clipboard!"))
    _open_browser(url)
    pause()


def screen_recommend() -> None:
    clear_screen()
    banner()
    print(f"\n  💡  {bold('Recommend a Skill Improvement')}")
    hr()
    print_wrapped(
        "Have an idea to make an existing skill better? We'd love to hear it! "
        "Open the form below and describe your suggestion.",
        indent=4,
    )
    print()
    url = f"{REPO_ISSUES_URL}?template=skill_recommendation.yml"
    print(f"  {bold('Open this link:')}")
    print()
    print(cyan(f"    {url}"))
    print()
    copied = copy_to_clipboard(url)
    if copied:
        print(green("  ✅  Link copied to clipboard!"))
    _open_browser(url)
    pause()


def _open_browser(url: str) -> None:
    """Try to open URL in the system browser."""
    try:
        import webbrowser
        webbrowser.open(url)
    except Exception:
        pass


def screen_quit() -> None:
    clear_screen()
    banner()
    print(f"\n  {bold('Thanks for using CheatCodes! 👋')}")
    print()
    print_wrapped(
        "Your favourites are saved at ~/.cheatcodes/favorites.json — "
        "they'll be here next time you run the concierge.",
        indent=4,
    )
    print()
    print(dim("  Tip: Add an alias to your shell for instant access:"))
    print(dim("       alias cheat='python ~/CheatCodes-Skill-Library/scripts/concierge.py'"))
    print()


# ── Main loop ─────────────────────────────────────────────────────────────────

def main() -> None:
    # First run: show welcome
    first_run = not FAVORITES_FILE.exists()
    if first_run:
        show_welcome()

    while True:
        try:
            action = main_menu()
        except KeyboardInterrupt:
            action = "quit"

        if action == "browse":
            screen_browse()
        elif action == "search":
            screen_search()
        elif action == "favorites":
            screen_favorites()
        elif action == "clone":
            screen_clone()
        elif action == "request":
            screen_request()
        elif action == "recommend":
            screen_recommend()
        elif action == "help":
            screen_help()
        elif action == "quit":
            screen_quit()
            sys.exit(0)


if __name__ == "__main__":
    main()
