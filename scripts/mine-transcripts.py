"""Count skill use and friction in local Claude Code transcripts.

Prints aggregate counts only. It never prints or stores message text.
Run: python3 -I scripts/mine-transcripts.py [--days 14] [--projects-dir ~/.claude/projects] [--json]
"""

import argparse
import collections
import datetime
import glob
import json
import os
import re
import sys

SKILL_LIBRARY_SKILLS = {
    "grill", "triage", "setup-repo", "git-guardrails", "setup-pre-commit", "catch-up",
    "wait-what", "handoff", "reflect", "verify", "diagnose", "implement", "spec", "review",
    "pr", "research", "blast-radius", "correct", "why", "how", "domain-modeling",
    "writing-for-agents", "codebase-design", "improve-codebase-architecture", "statechart",
    "no-comments", "wizard", "ask",
}
SKILL_LIBRARY_PREFIX = "skill-library:"
MESSAGES_AFTER_LOAD = 3
MAX_CORRECTION_MESSAGE_LENGTH = 400
CORRECTION_PATTERN = re.compile(
    r"\b(stop|don'?t|dont|just do it|skip|why did you|too much|overkill|i said|again|wtf|"
    r"fuck\w*|no,|no\.|i told you|stop asking|not what i)\b",
    re.IGNORECASE,
)
COMMAND_PATTERN = re.compile(r"<command-name>/?([^<]+)</command-name>")
SKIPPED_PREFIXES = ("<", "Caveat:", "This session is being continued")
BUILT_IN_COMMANDS = {
    "add-dir", "agents", "bug", "clear", "config", "context", "cost", "doctor", "exit", "export",
    "fast", "help", "hooks", "ide", "init", "login", "logout", "mcp", "memory", "model", "output-style",
    "permissions", "plugin", "plugins", "release-notes", "resume", "rewind", "status", "statusline",
    "terminal-setup", "theme", "usage", "vim",
}


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--days", type=int, default=14, help="only sessions changed in the last N days")
    parser.add_argument("--projects-dir", default="~/.claude/projects")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    return parser.parse_args()


def text_blocks(content):
    if isinstance(content, str):
        return [content]
    return [block.get("text", "") for block in content or [] if isinstance(block, dict) and block.get("type") == "text"]


def normalize_skill(name):
    if name.startswith(SKILL_LIBRARY_PREFIX):
        return name
    if ":" not in name and name in SKILL_LIBRARY_SKILLS:
        return SKILL_LIBRARY_PREFIX + name
    return name


def new_skill_counts():
    return {"loads": 0, "slash_uses": 0, "interrupts_after_load": 0, "corrections_after_load": 0}


def mine_session(path, totals, skills):
    last_loaded_skill = None
    user_messages_since_load = MESSAGES_AFTER_LOAD + 1
    session_user_messages = 0
    with open(path, errors="replace") as handle:
        for line in handle:
            if '"type":"user"' not in line and '"type":"assistant"' not in line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                totals["unreadable_lines"] += 1
                continue
            if entry.get("isSidechain"):
                continue
            content = (entry.get("message") or {}).get("content")

            if entry.get("type") == "assistant":
                for block in content or []:
                    if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                        skill = normalize_skill((block.get("input") or {}).get("skill", "unknown"))
                        skills[skill]["loads"] += 1
                        last_loaded_skill = skill
                        user_messages_since_load = 0
                continue

            if entry.get("isMeta"):
                continue
            is_recent_load = last_loaded_skill is not None and user_messages_since_load < MESSAGES_AFTER_LOAD
            for text in text_blocks(content):
                stripped = text.strip()
                if not stripped:
                    continue
                if stripped.startswith("[Request interrupted"):
                    totals["interrupts"] += 1
                    if is_recent_load:
                        skills[last_loaded_skill]["interrupts_after_load"] += 1
                    continue
                command = COMMAND_PATTERN.search(stripped)
                if command:
                    name = command.group(1).strip()
                    if name == "compact":
                        totals["compacts"] += 1
                    elif name not in BUILT_IN_COMMANDS:
                        skills[normalize_skill(name)]["slash_uses"] += 1
                    continue
                if stripped.startswith(SKIPPED_PREFIXES) or "Base directory for this skill" in stripped:
                    continue
                totals["user_messages"] += 1
                session_user_messages += 1
                if len(stripped) < MAX_CORRECTION_MESSAGE_LENGTH and CORRECTION_PATTERN.search(stripped):
                    totals["correction_messages"] += 1
                    if is_recent_load:
                        skills[last_loaded_skill]["corrections_after_load"] += 1
                user_messages_since_load += 1
    return session_user_messages


def main():
    arguments = parse_arguments()
    projects_dir = os.path.expanduser(arguments.projects_dir)
    if not os.path.isdir(projects_dir):
        print(f"No transcripts folder at {projects_dir}", file=sys.stderr)
        return 1
    cutoff = datetime.datetime.now().timestamp() - arguments.days * 86400
    paths = [path for path in glob.glob(os.path.join(projects_dir, "*", "*.jsonl")) if os.path.getmtime(path) >= cutoff]

    totals = collections.Counter()
    skills = collections.defaultdict(new_skill_counts)
    for path in paths:
        try:
            if mine_session(path, totals, skills):
                totals["sessions"] += 1
        except OSError as error:
            print(f"Skipped one transcript: {error.strerror}", file=sys.stderr)

    result = {
        "days": arguments.days,
        "sessions": totals["sessions"],
        "user_messages": totals["user_messages"],
        "interrupts": totals["interrupts"],
        "correction_messages": totals["correction_messages"],
        "compacts": totals["compacts"],
        "skills": dict(sorted(skills.items(), key=lambda item: -(item[1]["loads"] + item[1]["slash_uses"]))),
    }
    if arguments.json:
        json.dump(result, sys.stdout, indent=2)
        print()
        return 0

    print(f"Last {result['days']} days: {result['sessions']} sessions, {result['user_messages']} user messages, "
          f"{result['interrupts']} interrupts, {result['correction_messages']} corrections, {result['compacts']} /compact")
    print(f"\n{'skill or command':45} {'loads':>6} {'slash':>6} {'intr':>5} {'corr':>5}")
    for name, counts in result["skills"].items():
        print(f"{name[:45]:45} {counts['loads']:>6} {counts['slash_uses']:>6} "
              f"{counts['interrupts_after_load']:>5} {counts['corrections_after_load']:>5}")
    print("\nintr/corr = interrupts and corrections within 3 user messages after Claude loaded the skill.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
