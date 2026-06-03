from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from enum import Enum
from typing import List, Optional, Dict


# ══════════════════════════════════════════════════════════════════════
#  ANSI COLOUR HELPERS
# ══════════════════════════════════════════════════════════════════════

class C:
    """Terminal colour codes."""
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"

    RED    = "\033[91m"
    YELLOW = "\033[93m"
    GREEN  = "\033[92m"
    CYAN   = "\033[96m"
    BLUE   = "\033[94m"
    MAGENTA= "\033[95m"
    WHITE  = "\033[97m"
    GREY   = "\033[90m"

def colored(text: str, *codes: str) -> str:
    return "".join(codes) + str(text) + C.RESET

def line(char: str = "─", width: int = 66) -> str:
    return colored(char * width, C.GREY)


# ══════════════════════════════════════════════════════════════════════
#  PRIORITY LEVEL ENUM
# ══════════════════════════════════════════════════════════════════════

class PriorityLevel(Enum):
    CRITICAL = "CRITICAL"
    HIGH     = "HIGH"
    MEDIUM   = "MEDIUM"
    LOW      = "LOW"
    DONE     = "DONE"

    def order(self) -> int:
        return {
            PriorityLevel.CRITICAL: 0,
            PriorityLevel.HIGH:     1,
            PriorityLevel.MEDIUM:   2,
            PriorityLevel.LOW:      3,
            PriorityLevel.DONE:     4,
        }[self]

    def label(self) -> str:
        styles = {
            PriorityLevel.CRITICAL: colored(f"[{self.value}]", C.RED,    C.BOLD),
            PriorityLevel.HIGH:     colored(f"[{self.value}]",    C.YELLOW, C.BOLD),
            PriorityLevel.MEDIUM:   colored(f"[{self.value}]",  C.CYAN,   C.BOLD),
            PriorityLevel.LOW:      colored(f"[{self.value}]",      C.BLUE,   C.BOLD),
            PriorityLevel.DONE:     colored(f"[{self.value}]",      C.GREEN,  C.BOLD),
        }
        return styles[self]


# ══════════════════════════════════════════════════════════════════════
#  SUBTASK CLASS
# ══════════════════════════════════════════════════════════════════════

@dataclass
class Subtask:
    """Encapsulates a single subtask. Only toggle() mutates state."""
    _id:   str  = field(default_factory=lambda: str(uuid.uuid4())[:8])
    _text: str  = ""
    _done: bool = False

    # ── Constructors ────────────────────────────────────────────────
    @classmethod
    def create(cls, text: str) -> "Subtask":
        st = cls()
        st._text = text.strip()
        return st

    @classmethod
    def from_dict(cls, d: dict) -> "Subtask":
        st = cls()
        st._id   = d.get("id",   st._id)
        st._text = d.get("text", "")
        st._done = d.get("done", False)
        return st

    # ── Public interface ─────────────────────────────────────────────
    def toggle(self) -> None:
        self._done = not self._done

    def mark_done(self) -> None:
        self._done = True

    # ── Properties ──────────────────────────────────────────────────
    @property
    def id(self)   -> str:  return self._id
    @property
    def text(self) -> str:  return self._text
    @property
    def done(self) -> bool: return self._done

    def to_dict(self) -> dict:
        return {"id": self._id, "text": self._text, "done": self._done}


# ══════════════════════════════════════════════════════════════════════
#  HOMEWORK CLASS
# ══════════════════════════════════════════════════════════════════════

@dataclass
class Homework:
    """
    Central data entity. Private attributes; access via methods only.
    Encapsulation: no external module reads/writes fields directly.
    """
    _id:           str            = field(default_factory=lambda: str(uuid.uuid4())[:8])
    _title:        str            = ""
    _subject:      str            = ""
    _deadline:     str            = ""        # ISO YYYY-MM-DD
    _description:  str            = ""
    _done:         bool           = False
    _created_at:   str            = field(default_factory=lambda: datetime.now().isoformat())
    _completed_at: Optional[str]  = None
    _subtasks:     List[Subtask]  = field(default_factory=list)

    # ── Constructors ────────────────────────────────────────────────
    @classmethod
    def create(cls, title: str, subject: str, deadline: str,
               description: str = "", subtasks: List[str] = None) -> "Homework":
        hw = cls()
        hw._title       = title.strip()
        hw._subject     = subject.strip()
        hw._deadline    = deadline.strip()
        hw._description = description.strip()
        hw._subtasks    = [Subtask.create(t) for t in (subtasks or [])]
        return hw

    @classmethod
    def from_dict(cls, d: dict) -> "Homework":
        hw = cls()
        hw._id           = d.get("id",          hw._id)
        hw._title        = d.get("title",        "")
        hw._subject      = d.get("subject",      "")
        hw._deadline     = d.get("deadline",     "")
        hw._description  = d.get("description",  "")
        hw._done         = d.get("done",         False)
        hw._created_at   = d.get("created_at",   hw._created_at)
        hw._completed_at = d.get("completed_at", None)
        hw._subtasks     = [Subtask.from_dict(s) for s in d.get("subtasks", [])]
        return hw

    # ── Public methods ───────────────────────────────────────────────
    def save(self, title: str, subject: str, deadline: str,
             description: str = "") -> None:
        self._title       = title.strip()
        self._subject     = subject.strip()
        self._deadline    = deadline.strip()
        self._description = description.strip()

    def mark_done(self) -> None:
        self._done         = True
        self._completed_at = datetime.now().isoformat()

    def mark_pending(self) -> None:
        self._done         = False
        self._completed_at = None

    def add_subtask(self, text: str) -> None:
        self._subtasks.append(Subtask.create(text))

    def delete_subtask(self, idx: int) -> None:
        if 0 <= idx < len(self._subtasks):
            self._subtasks.pop(idx)

    # ── Properties ──────────────────────────────────────────────────
    @property
    def id(self)          -> str:          return self._id
    @property
    def title(self)       -> str:          return self._title
    @property
    def subject(self)     -> str:          return self._subject
    @property
    def deadline(self)    -> str:          return self._deadline
    @property
    def description(self) -> str:         return self._description
    @property
    def done(self)        -> bool:         return self._done
    @property
    def created_at(self)  -> str:          return self._created_at
    @property
    def completed_at(self)-> Optional[str]:return self._completed_at
    @property
    def subtasks(self)    -> List[Subtask]:return list(self._subtasks)

    def to_dict(self) -> dict:
        return {
            "id":           self._id,
            "title":        self._title,
            "subject":      self._subject,
            "deadline":     self._deadline,
            "description":  self._description,
            "done":         self._done,
            "created_at":   self._created_at,
            "completed_at": self._completed_at,
            "subtasks":     [s.to_dict() for s in self._subtasks],
        }


# ══════════════════════════════════════════════════════════════════════
#  VALIDATION CLASS  (Feature 1)
# ══════════════════════════════════════════════════════════════════════

class Validation:
    """
    Hides all form-checking rules internally.
    Only validate_homework() and show_error() are public.
    """

    @staticmethod
    def validate_homework(title: str, subject: str, deadline: str) -> Dict[str, str]:
        """Return a dict of {field: error_message}. Empty dict = valid."""
        errors: Dict[str, str] = {}

        if not title.strip():
            errors["title"] = "Title is required."
        elif len(title.strip()) < 3:
            errors["title"] = "Title must be at least 3 characters."

        if not subject.strip():
            errors["subject"] = "Subject is required."

        if not deadline.strip():
            errors["deadline"] = "Deadline is required."
        else:
            try:
                datetime.strptime(deadline.strip(), "%Y-%m-%d")
            except ValueError:
                errors["deadline"] = "Deadline must be in YYYY-MM-DD format."

        return errors

    @staticmethod
    def show_error(field: str, message: str) -> None:
        print(colored(f"  ⚠  {field}: {message}", C.RED))

    @staticmethod
    def clear_error() -> None:
        pass   # In console context: errors are shown once then loop re-prompts


# ══════════════════════════════════════════════════════════════════════
#  PRIORITY ENGINE  (Feature 2)
# ══════════════════════════════════════════════════════════════════════

class PriorityEngine:
    """
    Encapsulates today reference. Exposes only get_priority() and get_days_left().
    No external module touches the date logic directly.
    """

    def __init__(self, today: date = None):
        self._today = today or date.today()   # injectable for testing

    def get_days_left(self, deadline: str) -> int:
        due = datetime.strptime(deadline, "%Y-%m-%d").date()
        return (due - self._today).days

    def get_priority(self, hw: Homework) -> PriorityLevel:
        if hw.done:
            return PriorityLevel.DONE
        d = self.get_days_left(hw.deadline)
        if d < 0:   return PriorityLevel.CRITICAL   # overdue
        if d == 0:  return PriorityLevel.CRITICAL   # due today
        if d <= 3:  return PriorityLevel.HIGH
        if d <= 7:  return PriorityLevel.MEDIUM
        return PriorityLevel.LOW

    def days_label(self, hw: Homework) -> str:
        if hw.done:
            return colored("Completed", C.GREEN)
        d = self.get_days_left(hw.deadline)
        if d < 0:
            return colored(f"{abs(d)}d overdue", C.RED, C.BOLD)
        if d == 0:
            return colored("Due TODAY",  C.RED, C.BOLD)
        if d <= 3:
            return colored(f"{d}d left",  C.YELLOW)
        if d <= 7:
            return colored(f"{d}d left",  C.CYAN)
        return colored(f"{d}d left", C.BLUE)


# ══════════════════════════════════════════════════════════════════════
#  STORAGE INTERFACE + LOCAL FILE IMPLEMENTATION
# ══════════════════════════════════════════════════════════════════════

class Storage:
    """Abstract storage interface. Swap implementation without touching consumers."""

    def save_homework(self, entries: List[Homework]) -> None:
        raise NotImplementedError

    def load_homework(self) -> List[Homework]:
        raise NotImplementedError

    def delete_homework(self, hw_id: str, entries: List[Homework]) -> List[Homework]:
        raise NotImplementedError


class FileStorage(Storage):
    """Concrete implementation: persists to a JSON file."""

    def __init__(self, path: str = "homework_data.json"):
        self._path = path

    def save_homework(self, entries: List[Homework]) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([hw.to_dict() for hw in entries], f, indent=2)

    def load_homework(self) -> List[Homework]:
        if not os.path.exists(self._path):
            return []
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Homework.from_dict(d) for d in data]
        except (json.JSONDecodeError, KeyError):
            return []

    def delete_homework(self, hw_id: str, entries: List[Homework]) -> List[Homework]:
        updated = [hw for hw in entries if hw.id != hw_id]
        self.save_homework(updated)
        return updated


# ══════════════════════════════════════════════════════════════════════
#  REPORT DATA STRUCTURES  (Feature 3)
# ══════════════════════════════════════════════════════════════════════

@dataclass
class SubjectStats:
    name:  str
    done:  int
    total: int

    @property
    def pct(self) -> int:
        return round((self.done / self.total) * 100) if self.total else 0


@dataclass
class ReportData:
    total:         int
    done:          int
    pending:       int
    overdue:       int
    rate:          int
    subject_stats: List[SubjectStats]
    upcoming:      List[Homework]


# ══════════════════════════════════════════════════════════════════════
#  REPORT GENERATOR  (Feature 3)
# ══════════════════════════════════════════════════════════════════════

class ReportGenerator:
    """
    Depends on Storage and PriorityEngine via __init__ (Dependency Injection).
    Does not instantiate storage internally → testable with mock.
    Accesses only: done, deadline, subject from Homework (minimal coupling).
    """

    def __init__(self, storage: Storage, engine: PriorityEngine):
        self._storage = storage
        self._engine  = engine

    def generate_report(self, entries: List[Homework]) -> ReportData:
        total   = len(entries)
        done    = sum(1 for hw in entries if hw.done)
        pending = total - done
        today   = self._engine._today
        overdue = sum(
            1 for hw in entries
            if not hw.done and
               datetime.strptime(hw.deadline, "%Y-%m-%d").date() < today
        )
        rate = round((done / total) * 100) if total else 0

        # subject stats
        subj_map: Dict[str, SubjectStats] = {}
        for hw in entries:
            if hw.subject not in subj_map:
                subj_map[hw.subject] = SubjectStats(hw.subject, 0, 0)
            subj_map[hw.subject].total += 1
            if hw.done:
                subj_map[hw.subject].done += 1
        subject_stats = sorted(subj_map.values(), key=lambda s: s.name)

        # upcoming = nearest 5 pending
        upcoming = sorted(
            [hw for hw in entries if not hw.done],
            key=lambda hw: hw.deadline
        )[:5]

        return ReportData(total, done, pending, overdue, rate, subject_stats, upcoming)


# ══════════════════════════════════════════════════════════════════════
#  CONSOLE RENDERER  (Display Layer — separated from logic)
# ══════════════════════════════════════════════════════════════════════

class ConsoleRenderer:
    """Renders homework cards and reports to stdout. Pure display — no logic."""

    def __init__(self, engine: PriorityEngine):
        self._engine = engine

    # ── Header ──────────────────────────────────────────────────────
    def print_header(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print()
        print(colored("╔══════════════════════════════════════════════════════════════════╗", C.MAGENTA, C.BOLD))
        print(colored("║  ◈  STUDYDESK  —  HOMEWORK MANAGEMENT APP                       ║", C.MAGENTA, C.BOLD))
        print(colored("║     Sorsogon State University · Bulan Campus                    ║", C.GREY))
        print(colored("╚══════════════════════════════════════════════════════════════════╝", C.MAGENTA, C.BOLD))
        print()

    # ── Task list ───────────────────────────────────────────────────
    def print_task_list(self, entries: List[Homework]) -> None:
        if not entries:
            print(colored("  No homework entries found. Press [A] to add one.", C.GREY))
            return

        sorted_entries = sorted(
            entries,
            key=lambda hw: self._engine.get_priority(hw).order()
        )

        for i, hw in enumerate(sorted_entries, start=1):
            priority = self._engine.get_priority(hw)
            dlabel   = self._engine.days_label(hw)
            status   = colored("✓", C.GREEN) if hw.done else colored("○", C.GREY)
            title_color = C.GREY if hw.done else C.WHITE + C.BOLD

            print(f"  {colored(str(i).rjust(2), C.GREY)}.  {status}  {priority.label()}  {colored(hw.title, title_color)}")
            print(f"          {colored('Subject:', C.GREY)} {colored(hw.subject, C.CYAN)}   "
                  f"{colored('Due:', C.GREY)} {colored(hw.deadline, C.WHITE)}   {dlabel}")

            if hw.description:
                print(f"          {colored(hw.description[:60] + ('…' if len(hw.description)>60 else ''), C.DIM)}")

            if hw.subtasks:
                done_count = sum(1 for s in hw.subtasks if s.done)
                print(f"          {colored(f'Subtasks: {done_count}/{len(hw.subtasks)} done', C.GREY)}", end="")
                st_texts = [colored(('✓ ' if s.done else '○ ') + s.text, C.GREEN if s.done else C.GREY)
                            for s in hw.subtasks[:3]]
                print("  →  " + "  |  ".join(st_texts) + ("  …" if len(hw.subtasks) > 3 else ""))

            print(f"          {colored('ID: ' + hw.id, C.GREY)}")
            print()

    # ── Report ──────────────────────────────────────────────────────
    def print_report(self, report: ReportData, engine: PriorityEngine) -> None:
        print(colored("  ═══  ACADEMIC PROGRESS REPORT  ═══\n", C.MAGENTA, C.BOLD))

        # Summary
        print(f"  {'Total Tasks':<20} {colored(str(report.total), C.WHITE, C.BOLD)}")
        print(f"  {'Completed':<20} {colored(str(report.done),    C.GREEN, C.BOLD)}")
        print(f"  {'Pending':<20}   {colored(str(report.pending), C.YELLOW, C.BOLD)}")
        print(f"  {'Overdue':<20}   {colored(str(report.overdue), C.RED, C.BOLD)}")
        print()

        # Completion rate bar
        BAR_WIDTH = 40
        filled = int(BAR_WIDTH * report.rate / 100) if report.total else 0
        bar    = colored("█" * filled, C.GREEN) + colored("░" * (BAR_WIDTH - filled), C.GREY)
        print(f"  Overall Completion  [{bar}]  {colored(str(report.rate) + '%', C.WHITE, C.BOLD)}")
        print()

        # Subject stats
        if report.subject_stats:
            print(colored("  Subject-wise Progress:", C.CYAN, C.BOLD))
            print(line())
            for sub in report.subject_stats:
                sb   = int(30 * sub.pct / 100)
                sbar = colored("█" * sb, C.CYAN) + colored("░" * (30 - sb), C.GREY)
                print(f"  {sub.name:<22}  [{sbar}]  {colored(str(sub.done)+'/'+str(sub.total), C.WHITE)}  ({sub.pct}%)")
            print()

        # Upcoming deadlines
        if report.upcoming:
            print(colored("  Upcoming Deadlines (nearest 5):", C.YELLOW, C.BOLD))
            print(line())
            for hw in report.upcoming:
                p     = engine.get_priority(hw)
                dleft = engine.days_label(hw)
                print(f"  {p.label()}  {colored(hw.title, C.WHITE)}  ·  {colored(hw.subject, C.CYAN)}  ·  {hw.deadline}  {dleft}")
            print()

        if report.total == 0:
            print(colored("  No homework data yet. Add tasks to see your report.", C.GREY))


# ══════════════════════════════════════════════════════════════════════
#  INPUT HELPERS
# ══════════════════════════════════════════════════════════════════════

def prompt(label: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    value = input(colored(f"  {label}{hint}: ", C.CYAN)).strip()
    return value if value else default

def prompt_menu(options: List[str]) -> str:
    for opt in options:
        print(colored(f"    {opt}", C.WHITE))
    return input(colored("  Choice: ", C.CYAN)).strip().upper()

def pause() -> None:
    input(colored("\n  Press Enter to continue…", C.GREY))


# ══════════════════════════════════════════════════════════════════════
#  ADD / EDIT HOMEWORK FORM  (Feature 1 — inline validation)
# ══════════════════════════════════════════════════════════════════════

def homework_form(existing: Homework = None) -> Optional[Homework]:
    """
    Collects homework fields with inline validation.
    Red error messages appear per field; the loop re-prompts until valid.
    Returns a Homework object or None if the user cancels.
    """
    print()
    action = "EDIT HOMEWORK" if existing else "ADD NEW HOMEWORK"
    print(colored(f"  ─── {action} ───", C.MAGENTA, C.BOLD))
    print(colored("  (Leave field blank + Enter to cancel)\n", C.GREY))

    # ── TITLE ────────────────────────────────────────────────────────
    while True:
        title = prompt("Title", existing.title if existing else "")
        if title == "" and existing is None:
            print(colored("  Cancelled.", C.GREY)); return None
        errs = Validation.validate_homework(title, "placeholder", "2099-01-01")
        if "title" in errs:
            Validation.show_error("Title", errs["title"])
        else:
            break

    # ── SUBJECT ──────────────────────────────────────────────────────
    while True:
        subject = prompt("Subject", existing.subject if existing else "")
        if subject == "" and existing is None:
            print(colored("  Cancelled.", C.GREY)); return None
        errs = Validation.validate_homework("ok", subject, "2099-01-01")
        if "subject" in errs:
            Validation.show_error("Subject", errs["subject"])
        else:
            break

    # ── DEADLINE ─────────────────────────────────────────────────────
    while True:
        deadline = prompt("Deadline (YYYY-MM-DD)", existing.deadline if existing else "")
        if deadline == "" and existing is None:
            print(colored("  Cancelled.", C.GREY)); return None
        errs = Validation.validate_homework("ok", "ok", deadline)
        if "deadline" in errs:
            Validation.show_error("Deadline", errs["deadline"])
        else:
            break

    # ── DESCRIPTION (optional) ────────────────────────────────────────
    description = prompt("Description (optional)", existing.description if existing else "")

    # ── SUBTASKS ─────────────────────────────────────────────────────
    subtask_texts: List[str] = []
    if existing:
        subtask_texts = [s.text for s in existing.subtasks]

    print(colored("  Subtasks — type one per line, blank line to finish:", C.GREY))
    if subtask_texts:
        for t in subtask_texts:
            print(colored(f"    (existing) {t}", C.DIM))
        keep = input(colored("  Keep existing subtasks? [Y/n]: ", C.CYAN)).strip().lower()
        if keep == "n":
            subtask_texts = []

    while True:
        st = input(colored("    + Subtask (or blank to finish): ", C.GREY)).strip()
        if not st:
            break
        subtask_texts.append(st)

    # ── BUILD OBJECT ─────────────────────────────────────────────────
    if existing:
        existing.save(title, subject, deadline, description)
        # rebuild subtasks
        existing._subtasks = [Subtask.create(t) for t in subtask_texts]
        return existing
    else:
        return Homework.create(title, subject, deadline, description, subtask_texts)


# ══════════════════════════════════════════════════════════════════════
#  SUBTASK MANAGEMENT SCREEN
# ══════════════════════════════════════════════════════════════════════

def manage_subtasks(hw: Homework, storage: Storage, entries: List[Homework]) -> None:
    while True:
        print()
        print(colored(f"  Subtasks for: {hw.title}", C.WHITE, C.BOLD))
        print(line())
        if not hw.subtasks:
            print(colored("  No subtasks.", C.GREY))
        else:
            for i, st in enumerate(hw.subtasks, 1):
                mark = colored("✓", C.GREEN) if st.done else colored("○", C.GREY)
                print(f"    {i}. {mark}  {colored(st.text, C.GREEN if st.done else C.WHITE)}")
        print()
        choice = prompt_menu([
            "[T] Toggle subtask done/undone",
            "[A] Add subtask",
            "[D] Delete subtask",
            "[B] Back",
        ])
        if choice == "T":
            idx_s = input(colored("  Subtask number: ", C.CYAN)).strip()
            if idx_s.isdigit():
                idx = int(idx_s) - 1
                if 0 <= idx < len(hw.subtasks):
                    hw.subtasks[idx].toggle()
                    storage.save_homework(entries)
        elif choice == "A":
            text = prompt("Subtask text")
            if text:
                hw.add_subtask(text)
                storage.save_homework(entries)
        elif choice == "D":
            idx_s = input(colored("  Subtask number to delete: ", C.CYAN)).strip()
            if idx_s.isdigit():
                hw.delete_subtask(int(idx_s) - 1)
                storage.save_homework(entries)
        elif choice == "B":
            break


# ══════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION  (Composition Root)
# ══════════════════════════════════════════════════════════════════════

class HomeworkApp:
    """
    Composition root: constructs all concrete objects and injects dependencies.
    No module creates its own dependencies — satisfies DI requirement.
    """

    def __init__(self):
        self._storage  = FileStorage("homework_data.json")
        self._engine   = PriorityEngine()
        self._renderer = ConsoleRenderer(self._engine)
        self._report_gen = ReportGenerator(self._storage, self._engine)
        self._entries: List[Homework] = []

    # ── Bootstrap ────────────────────────────────────────────────────
    def run(self) -> None:
        self._entries = self._storage.load_homework()
        while True:
            self._main_menu()

    # ── Menus ────────────────────────────────────────────────────────
    def _main_menu(self) -> None:
        self._renderer.print_header()
        self._renderer.print_task_list(self._entries)
        print(line())
        choice = prompt_menu([
            "[A] Add Homework",
            "[E] Edit Homework",
            "[M] Mark Done / Undone",
            "[S] Manage Subtasks",
            "[D] Delete Homework",
            "[R] View Report",
            "[F] Filter by Priority",
            "[Q] Quit",
        ])

        if   choice == "A": self._add_homework()
        elif choice == "E": self._edit_homework()
        elif choice == "M": self._toggle_done()
        elif choice == "S": self._subtask_menu()
        elif choice == "D": self._delete_homework()
        elif choice == "R": self._view_report()
        elif choice == "F": self._filter_view()
        elif choice == "Q": self._quit()

    # ── Feature 1 – Add ─────────────────────────────────────────────
    def _add_homework(self) -> None:
        hw = homework_form()
        if hw:
            self._entries.append(hw)
            self._storage.save_homework(self._entries)
            print(colored("\n  ✓ Homework saved successfully!", C.GREEN, C.BOLD))
        pause()

    # ── Feature 1 – Edit ─────────────────────────────────────────────
    def _edit_homework(self) -> None:
        hw = self._select_homework("Edit")
        if hw:
            homework_form(existing=hw)
            self._storage.save_homework(self._entries)
            print(colored("\n  ✓ Homework updated.", C.GREEN, C.BOLD))
        pause()

    # ── Feature 2 – Toggle done ───────────────────────────────────────
    def _toggle_done(self) -> None:
        hw = self._select_homework("Mark Done/Undone")
        if hw:
            if hw.done:
                hw.mark_pending()
                print(colored(f"\n  ○ '{hw.title}' marked as PENDING.", C.YELLOW))
            else:
                hw.mark_done()
                print(colored(f"\n  ✓ '{hw.title}' marked as DONE.", C.GREEN, C.BOLD))
            self._storage.save_homework(self._entries)
        pause()

    # ── Subtasks ──────────────────────────────────────────────────────
    def _subtask_menu(self) -> None:
        hw = self._select_homework("Manage Subtasks")
        if hw:
            manage_subtasks(hw, self._storage, self._entries)

    # ── Delete (two-tap confirmation) ─────────────────────────────────
    def _delete_homework(self) -> None:
        hw = self._select_homework("Delete")
        if hw:
            print(colored(f"\n  ⚠  Delete '{hw.title}'? This cannot be undone.", C.RED))
            confirm = input(colored("  Type DELETE to confirm: ", C.RED)).strip()
            if confirm == "DELETE":
                self._entries = self._storage.delete_homework(hw.id, self._entries)
                print(colored("  ✓ Homework deleted.", C.GREEN))
            else:
                print(colored("  Cancelled.", C.GREY))
        pause()

    # ── Feature 3 – Report ───────────────────────────────────────────
    def _view_report(self) -> None:
        self._renderer.print_header()
        report = self._report_gen.generate_report(self._entries)
        self._renderer.print_report(report, self._engine)
        pause()

    # ── Filter view ───────────────────────────────────────────────────
    def _filter_view(self) -> None:
        self._renderer.print_header()
        print(colored("  Filter by Priority Level:\n", C.MAGENTA, C.BOLD))
        choice = prompt_menu([
            "[1] CRITICAL",
            "[2] HIGH",
            "[3] MEDIUM",
            "[4] LOW",
            "[5] DONE",
            "[B] Back",
        ])
        level_map = {
            "1": PriorityLevel.CRITICAL,
            "2": PriorityLevel.HIGH,
            "3": PriorityLevel.MEDIUM,
            "4": PriorityLevel.LOW,
            "5": PriorityLevel.DONE,
        }
        if choice in level_map:
            target = level_map[choice]
            filtered = [hw for hw in self._entries if self._engine.get_priority(hw) == target]
            self._renderer.print_header()
            print(colored(f"  Showing: {target.value}\n", C.MAGENTA, C.BOLD))
            self._renderer.print_task_list(filtered)
            pause()

    # ── Helper: pick homework by number ───────────────────────────────
    def _select_homework(self, action: str) -> Optional[Homework]:
        if not self._entries:
            print(colored("  No homework entries to select.", C.GREY))
            pause()
            return None
        sorted_entries = sorted(
            self._entries,
            key=lambda hw: self._engine.get_priority(hw).order()
        )
        print()
        for i, hw in enumerate(sorted_entries, 1):
            p = self._engine.get_priority(hw)
            print(f"  {str(i).rjust(2)}.  {p.label()}  {colored(hw.title, C.WHITE)}  ·  {colored(hw.subject, C.GREY)}")
        print()
        idx_s = input(colored(f"  Select number to {action} (0 to cancel): ", C.CYAN)).strip()
        if idx_s.isdigit():
            idx = int(idx_s) - 1
            if 0 <= idx < len(sorted_entries):
                # return reference from original list
                sel_id = sorted_entries[idx].id
                return next((hw for hw in self._entries if hw.id == sel_id), None)
        print(colored("  Invalid selection.", C.GREY))
        return None

    # ── Quit ──────────────────────────────────────────────────────────
    def _quit(self) -> None:
        self._storage.save_homework(self._entries)
        print(colored("\n  Data saved. Goodbye!\n", C.GREEN))
        raise SystemExit(0)


# ══════════════════════════════════════════════════════════════════════
#  UNIT TESTS  (pytest-compatible — run: python -m pytest homework_manager.py -v)
# ══════════════════════════════════════════════════════════════════════

def _make_hw(days_from_today: int, done: bool = False) -> Homework:
    """Helper: create a homework due N days from today."""
    target = date.today()
    from datetime import timedelta
    due = target + timedelta(days=days_from_today)
    hw = Homework.create("Test HW", "Math", due.strftime("%Y-%m-%d"), "desc")
    if done:
        hw.mark_done()
    return hw

# ── PriorityEngine tests ─────────────────────────────────────────────

def test_priority_done():
    engine = PriorityEngine()
    hw = _make_hw(5, done=True)
    assert engine.get_priority(hw) == PriorityLevel.DONE

def test_priority_overdue():
    engine = PriorityEngine()
    hw = _make_hw(-1)
    assert engine.get_priority(hw) == PriorityLevel.CRITICAL

def test_priority_due_today():
    engine = PriorityEngine()
    hw = _make_hw(0)
    assert engine.get_priority(hw) == PriorityLevel.CRITICAL

def test_priority_high():
    engine = PriorityEngine()
    hw = _make_hw(3)
    assert engine.get_priority(hw) == PriorityLevel.HIGH

def test_priority_medium():
    engine = PriorityEngine()
    hw = _make_hw(7)
    assert engine.get_priority(hw) == PriorityLevel.MEDIUM

def test_priority_low():
    engine = PriorityEngine()
    hw = _make_hw(8)
    assert engine.get_priority(hw) == PriorityLevel.LOW

# ── Validation tests ─────────────────────────────────────────────────

def test_validation_all_empty():
    errs = Validation.validate_homework("", "", "")
    assert "title"    in errs
    assert "subject"  in errs
    assert "deadline" in errs

def test_validation_bad_date():
    errs = Validation.validate_homework("Lab Report", "Math", "31-12-2025")
    assert "deadline" in errs

def test_validation_valid():
    errs = Validation.validate_homework("Lab Report", "Math", "2099-12-31")
    assert errs == {}

def test_validation_short_title():
    errs = Validation.validate_homework("AB", "Math", "2099-01-01")
    assert "title" in errs

# ── Homework entity tests ────────────────────────────────────────────

def test_homework_mark_done():
    hw = _make_hw(5)
    assert hw.done is False
    hw.mark_done()
    assert hw.done is True
    assert hw.completed_at is not None

def test_homework_mark_pending():
    hw = _make_hw(5, done=True)
    hw.mark_pending()
    assert hw.done is False
    assert hw.completed_at is None

def test_subtask_toggle():
    hw = Homework.create("T", "S", "2099-01-01", subtasks=["Step 1"])
    st = hw.subtasks[0]
    assert st.done is False
    st.toggle()
    assert st.done is True
    st.toggle()
    assert st.done is False

# ── Report generator tests ────────────────────────────────────────────

def test_report_empty():
    storage = FileStorage.__new__(FileStorage)   # skip __init__
    engine  = PriorityEngine()
    rg      = ReportGenerator(storage, engine)
    report  = rg.generate_report([])
    assert report.total == 0
    assert report.rate  == 0

def test_report_mixed():
    storage = FileStorage.__new__(FileStorage)
    engine  = PriorityEngine()
    rg      = ReportGenerator(storage, engine)
    entries = [_make_hw(5), _make_hw(5, done=True)]
    report  = rg.generate_report(entries)
    assert report.total   == 2
    assert report.done    == 1
    assert report.pending == 1
    assert report.rate    == 50

def test_report_all_done():
    storage = FileStorage.__new__(FileStorage)
    engine  = PriorityEngine()
    rg      = ReportGenerator(storage, engine)
    entries = [_make_hw(5, done=True), _make_hw(10, done=True)]
    report  = rg.generate_report(entries)
    assert report.rate == 100
    assert report.pending == 0


# ══════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = HomeworkApp()
    app.run()
