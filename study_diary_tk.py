#!/usr/bin/env python3
"""Study Diary - pixel-style desktop app. Pure Python (Tkinter, standard library).

Run:  python study_diary_tk.py

* Tasks: tick them when done.
* Topics: note what you learned today.
* Revise footer: every DONE task and every topic comes back after 3, 7 and 21 days.
Everything is saved to study_diary.json next to this file (previous version kept as
study_diary.json.bak). The file is compatible with the browser version.
"""
import json
import os
import shutil
import sys
import uuid
from datetime import date, timedelta

try:
    import tkinter as tk
    from tkinter import font as tkfont
except ImportError:
    sys.exit("Tkinter is missing. On Ubuntu/Debian run: sudo apt install python3-tk")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "study_diary.json")
INTERVALS = (3, 7, 21)

# Palette
PAPER, CARD, INK, MUTE = "#f4f7fb", "#ffffff", "#1b2438", "#66728a"
RED, GREEN, GOLD, MINT = "#d64550", "#2e8b6a", "#f2b134", "#5fd0a5"
FOOT, FOOTINK, FOOTMUTE, FOOTRULE = "#1b2438", "#f4f7fb", "#93a0ba", "#33405c"

PIXEL_FONTS = {"Press Start 2P": 0.6, "Silkscreen": 0.9, "Pixelify Sans": 1.0, "VT323": 1.5}
MONO_FONTS = ("Consolas", "Menlo", "DejaVu Sans Mono", "Courier New", "Courier")


# ---------------------------------------------------------------- data
def new_id():
    return uuid.uuid4().hex[:8]


def load():
    data = {"days": {}, "rev": {}}
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            d = json.load(f)
        if isinstance(d, dict) and isinstance(d.get("days"), dict):
            data = d
    except (OSError, ValueError):
        pass
    if not isinstance(data.get("rev"), dict):
        data["rev"] = {}
    for day in data["days"].values():
        day.setdefault("tasks", [])
        day.setdefault("topics", [])
        for t in day["tasks"]:
            t.setdefault("id", new_id())
            t.setdefault("d", False)
        for t in day["topics"]:
            t.setdefault("id", new_id())
    return data


def save(data):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    if os.path.exists(DATA_FILE):
        shutil.copyfile(DATA_FILE, DATA_FILE + ".bak")
    os.replace(tmp, DATA_FILE)


# ---------------------------------------------------------------- pixel art
def px_image(rows, palette, zoom):
    img = tk.PhotoImage(width=len(rows[0]), height=len(rows))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if palette.get(ch):
                img.put(palette[ch], (x, y))
    return img.zoom(zoom, zoom)


TICK = [(2, 4), (3, 5), (4, 6), (5, 5), (6, 4), (7, 3), (2, 5), (3, 6), (4, 7), (5, 6), (6, 5), (7, 4)]


def box_rows(checked):
    g = [["B" if x in (0, 9) or y in (0, 9) else "F" for x in range(10)] for y in range(10)]
    for x, y in ((0, 0), (9, 0), (0, 9), (9, 9)):
        g[y][x] = "."
    if checked:
        for x, y in TICK:
            g[y][x] = "T"
    return ["".join(r) for r in g]


BOOK = [
    "KKKKKKKKKKKK",
    "KRWWWWWWWWWK",
    "KRWBBBBBBBWK",
    "KRWWWWWWWWWK",
    "KRWBBBBBBBWK",
    "KRWWWWWWWWWK",
    "KRWBBBBBWWWK",
    "KRWWWWWWWWWK",
    "KKKKKKKKKKKK",
]


class Scroll(tk.Frame):
    """A frame whose content scrolls vertically (mouse wheel, optional bar)."""

    def __init__(self, master, bg, bar=True):
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        if bar:
            sb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, width=12, relief="flat", bd=0)
            self.canvas.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.win, width=e.width))


class PEntry(tk.Frame):
    """Flat entry with a hard 2px border and a placeholder hint."""

    def __init__(self, master, font, hint, on_enter):
        super().__init__(master, bg=INK, padx=2, pady=2)
        self.hint, self.empty = hint, True
        self.e = tk.Entry(self, font=font, relief="flat", bd=0, highlightthickness=0,
                          bg=CARD, fg=MUTE, insertbackground=INK)
        self.e.pack(fill="x", ipady=6)
        self.e.insert(0, hint)
        self.e.bind("<FocusIn>", self._in)
        self.e.bind("<FocusOut>", self._out)
        self.e.bind("<Return>", lambda ev: on_enter())

    def _in(self, _):
        if self.empty:
            self.e.delete(0, "end")
            self.e.config(fg=INK)
            self.empty = False

    def _out(self, _):
        if not self.e.get().strip():
            self.e.delete(0, "end")
            self.e.insert(0, self.hint)
            self.e.config(fg=MUTE)
            self.empty = True

    def get(self):
        return "" if self.empty else self.e.get().strip()

    def clear(self):
        self.e.delete(0, "end")


# ---------------------------------------------------------------- app
class App(tk.Tk):
    def __init__(self):
        try:  # crisp text on Windows
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
        super().__init__()
        self.title("Study Diary")
        self.geometry("800x900")
        self.minsize(540, 680)
        self.configure(bg=PAPER)
        self.data = load()
        self.cur = date.today()
        self._last_w = 0
        self._after = None
        self.make_fonts()
        self.make_images()
        self.build()
        self.render()
        self.bind("<Configure>", self.on_resize)
        self.bind_all("<MouseWheel>", self.on_wheel)
        self.bind_all("<Button-4>", self.on_wheel)
        self.bind_all("<Button-5>", self.on_wheel)
        self.bind_all("<Control-Left>", lambda e: self.go(-1))
        self.bind_all("<Control-Right>", lambda e: self.go(1))

    # ---- resources
    def make_fonts(self):
        fams = set(tkfont.families())
        pixel = next((f for f in PIXEL_FONTS if f in fams), None)
        fam = pixel or next((f for f in MONO_FONTS if f in fams), "TkFixedFont")
        mult = PIXEL_FONTS.get(pixel, 1.0)

        def mk(size, done=False):
            return tkfont.Font(family=fam, size=max(7, round(size * mult)), weight="bold",
                               overstrike=1 if done else 0)

        self.f = {"title": mk(30), "sub": mk(12), "head": mk(15), "body": mk(12), "done": mk(12, True),
                  "small": mk(10), "btn": mk(11), "foot": mk(11), "foot_done": mk(11, True)}

    def make_images(self):
        page = {"B": INK, "F": CARD, "T": "#ffffff"}
        self.img = {
            "off": px_image(box_rows(False), page, 2),
            "on": px_image(box_rows(True), {**page, "F": GREEN}, 2),
            "foot_off": px_image(box_rows(False), {"B": FOOTINK, "F": FOOT}, 2),
            "foot_on": px_image(box_rows(True), {"B": FOOTINK, "F": MINT, "T": FOOT}, 2),
            "book": px_image(BOOK, {"K": INK, "R": RED, "W": CARD, "B": "#9db4d8"}, 5),
        }

    # ---- widgets
    def button(self, parent, text, cmd, bg=CARD, hover=GOLD):
        outer = tk.Frame(parent, bg=INK)
        lab = tk.Label(outer, text=text, bg=bg, fg=INK, font=self.f["btn"], padx=12, pady=5, cursor="hand2")
        lab.pack(padx=2, pady=(2, 5))  # thicker bottom edge gives a chunky pixel look
        lab.bind("<Enter>", lambda e: lab.config(bg=hover))
        lab.bind("<Leave>", lambda e: lab.config(bg=bg))
        lab.bind("<Button-1>", lambda e: cmd())
        return outer

    def stripe(self, parent):
        c = tk.Canvas(parent, height=8, bg=PAPER, highlightthickness=0, bd=0)

        def draw(e):
            c.delete("all")
            colors = (RED, GOLD, GREEN, INK)
            for i in range(0, e.width // 8 + 1):
                c.create_rectangle(i * 8, 0, i * 8 + 8, 8, fill=colors[i % 4], outline="")

        c.bind("<Configure>", draw)
        return c

    def heading(self, parent, text):
        tk.Label(parent, text=text, bg=CARD, fg=INK, font=self.f["head"]).pack(anchor="w", pady=(12, 0))
        tk.Frame(parent, bg=RED, height=4, width=56).pack(anchor="w", pady=(2, 4))

    # ---- layout
    def build(self):
        top = tk.Frame(self, bg=PAPER, padx=18, pady=14)
        top.pack(side="top", fill="x")

        nav = tk.Frame(top, bg=PAPER)
        nav.pack(fill="x")
        self.button(nav, "<", lambda: self.go(-1)).pack(side="left")
        self.button(nav, ">", lambda: self.go(1)).pack(side="left", padx=8)
        self.button(nav, "Today", self.today, bg=GOLD, hover="#ffd06b").pack(side="left")
        self.button(nav, "Go", self.jump).pack(side="right")
        self.date_e = tk.Entry(nav, width=11, font=self.f["btn"], relief="flat", bg=CARD, fg=INK,
                               highlightthickness=2, highlightbackground=INK, highlightcolor=RED, justify="center")
        self.date_e.pack(side="right", padx=8, ipady=5)
        self.date_e.bind("<Return>", lambda e: self.jump())

        self.warn = tk.Label(top, text="", bg=PAPER, fg=RED, font=self.f["small"], anchor="w")
        self.warn.pack(fill="x", pady=(8, 0))

        head = tk.Frame(top, bg=PAPER)
        head.pack(fill="x", pady=(4, 0))
        tk.Label(head, image=self.img["book"], bg=PAPER).pack(side="left", padx=(0, 14))
        titles = tk.Frame(head, bg=PAPER)
        titles.pack(side="left")
        self.title_l = tk.Label(titles, bg=PAPER, fg=INK, font=self.f["title"], anchor="w")
        self.title_l.pack(anchor="w")
        self.sub_l = tk.Label(titles, bg=PAPER, fg=MUTE, font=self.f["sub"], anchor="w")
        self.sub_l.pack(anchor="w")

        self.stripe(self).pack(side="top", fill="x")

        # footer (fixed height, three columns)
        foot = tk.Frame(self, bg=FOOT, height=270)
        foot.pack(side="bottom", fill="x")
        foot.pack_propagate(False)
        tk.Label(foot, text="Revise", bg=FOOT, fg=FOOTINK, font=self.f["head"]).pack(anchor="w", padx=18, pady=(12, 0))
        tk.Label(foot, text="Done tasks and topics from 3, 7 and 21 days ago. Tick when revised.",
                 bg=FOOT, fg=FOOTMUTE, font=self.f["small"]).pack(anchor="w", padx=18, pady=(0, 6))
        cols = tk.Frame(foot, bg=FOOT)
        cols.pack(fill="both", expand=True, padx=18, pady=(0, 10))
        self.cols = []
        for i in range(3):
            cols.columnconfigure(i, weight=1, uniform="c")
            cf = tk.Frame(cols, bg=FOOT)
            cf.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0))
            cols.rowconfigure(0, weight=1)
            tk.Frame(cf, bg=FOOTRULE, height=3).pack(fill="x")
            lab = tk.Label(cf, bg=FOOT, fg=FOOTINK, font=self.f["btn"], anchor="w")
            lab.pack(fill="x", pady=(4, 0))
            sc = Scroll(cf, FOOT, bar=False)
            sc.pack(fill="both", expand=True)
            self.cols.append((lab, sc))

        # page (scrolls)
        self.body = Scroll(self, PAPER)
        self.body.pack(side="top", fill="both", expand=True)
        outer = tk.Frame(self.body.inner, bg=INK, padx=2, pady=2)
        outer.pack(fill="x", padx=18, pady=12)
        card = tk.Frame(outer, bg=CARD)
        card.pack(fill="both")
        tk.Frame(card, bg=RED, width=8).pack(side="left", fill="y")
        page = tk.Frame(card, bg=CARD, padx=16, pady=6)
        page.pack(side="left", fill="both", expand=True)

        self.heading(page, "Tasks")
        self.prog = tk.Canvas(page, height=14, bg=CARD, highlightthickness=0, bd=0)
        self.prog.pack(fill="x", pady=(0, 6))
        self.tasks_f = tk.Frame(page, bg=CARD)
        self.tasks_f.pack(fill="x")
        row = tk.Frame(page, bg=CARD)
        row.pack(fill="x", pady=(8, 4))
        self.task_in = PEntry(row, self.f["body"], "Add a task", self.add_task)
        self.task_in.pack(side="left", fill="x", expand=True)
        self.button(row, "Add", self.add_task, bg=GOLD, hover="#ffd06b").pack(side="left", padx=(8, 0))

        self.heading(page, "Topics studied today")
        self.topics_f = tk.Frame(page, bg=CARD)
        self.topics_f.pack(fill="x")
        row = tk.Frame(page, bg=CARD)
        row.pack(fill="x", pady=(8, 12))
        self.topic_in = PEntry(row, self.f["body"], "Add a topic you studied", self.add_topic)
        self.topic_in.pack(side="left", fill="x", expand=True)
        self.button(row, "Add", self.add_topic, bg=GOLD, hover="#ffd06b").pack(side="left", padx=(8, 0))

    # ---- data helpers
    def key(self, d=None):
        return (d or self.cur).isoformat()

    def day_view(self, d=None):
        return self.data["days"].get(self.key(d), {"tasks": [], "topics": []})

    def day_edit(self):
        return self.data["days"].setdefault(self.key(), {"tasks": [], "topics": []})

    def revision_items(self, d):
        day = self.day_view(d)
        return [(t["id"], t["t"]) for t in day["tasks"] if t.get("d")] + [(t["id"], t["t"]) for t in day["topics"]]

    def commit(self):
        try:
            save(self.data)
            self.warn.config(text="")
        except OSError as e:
            self.warn.config(text="Could not save: %s" % e)
        self.render()

    # ---- actions
    def go(self, n):
        self.cur += timedelta(days=n)
        self.render()

    def today(self):
        self.cur = date.today()
        self.render()

    def jump(self):
        try:
            self.cur = date.fromisoformat(self.date_e.get().strip())
        except ValueError:
            self.warn.config(text="Use the date format YYYY-MM-DD, for example 2026-10-05.")
            return
        self.warn.config(text="")
        self.render()

    def add_task(self):
        text = self.task_in.get()
        if text:
            self.day_edit()["tasks"].append({"id": new_id(), "t": text, "d": False})
            self.task_in.clear()
            self.commit()

    def add_topic(self):
        text = self.topic_in.get()
        if text:
            self.day_edit()["topics"].append({"id": new_id(), "t": text})
            self.topic_in.clear()
            self.commit()

    def toggle_task(self, t):
        t["d"] = not t.get("d")
        self.commit()

    def remove(self, lst, item):
        lst.remove(item)
        self.commit()

    def toggle_rev(self, key):
        if key in self.data["rev"]:
            del self.data["rev"][key]
        else:
            self.data["rev"][key] = 1
        self.commit()

    # ---- events
    def on_resize(self, e):
        if e.widget is self and e.width != self._last_w:
            self._last_w = e.width
            if self._after:
                self.after_cancel(self._after)
            self._after = self.after(150, self.render)

    def on_wheel(self, e):
        try:
            w = self.winfo_containing(e.x_root, e.y_root)
        except (KeyError, tk.TclError):
            return
        step = -1 if (e.num == 4 or getattr(e, "delta", 0) > 0) else 1
        while w is not None:
            if isinstance(w, Scroll):
                w.canvas.yview_scroll(step * 2, "units")
                return
            w = getattr(w, "master", None)

    # ---- drawing
    def row(self, parent, text, done, bg, fg, mute, imgs, font_ok, font_done, wrap, on_box, on_del=None):
        r = tk.Frame(parent, bg=bg)
        r.pack(fill="x", pady=3)
        box = tk.Label(r, image=imgs[1] if done else imgs[0], bg=bg, cursor="hand2")
        box.pack(side="left", anchor="n", padx=(0, 10), pady=2)
        lab = tk.Label(r, text=text, bg=bg, fg=mute if done else fg, font=font_done if done else font_ok,
                       wraplength=wrap, justify="left", anchor="w", cursor="hand2")
        lab.pack(side="left", fill="x", expand=True)
        for w in (box, lab):
            w.bind("<Button-1>", lambda e: on_box())
        if on_del:
            x = tk.Label(r, text="x", bg=bg, fg=mute, font=self.f["btn"], padx=8, cursor="hand2")
            x.pack(side="right")
            x.bind("<Enter>", lambda e: x.config(fg=RED))
            x.bind("<Leave>", lambda e: x.config(fg=mute))
            x.bind("<Button-1>", lambda e: on_del())

    def note(self, parent, text, bg, fg):
        tk.Label(parent, text=text, bg=bg, fg=fg, font=self.f["small"], anchor="w").pack(fill="x", pady=6)

    def render(self):
        self._after = None
        self.update_idletasks()
        width = max(self.winfo_width(), 540)
        page_wrap = width - 190
        foot_wrap = (width - 36 - 16) // 3 - 44
        keep = [self.body.canvas.yview()[0]] + [sc.canvas.yview()[0] for _, sc in self.cols]

        d = self.day_view()
        self.date_e.delete(0, "end")
        self.date_e.insert(0, self.key())
        self.title_l.config(text=self.cur.strftime("%A"))
        suffix = "  (today)" if self.cur == date.today() else ""
        self.sub_l.config(text="%d %s%s" % (self.cur.day, self.cur.strftime("%B %Y"), suffix))

        for w in self.tasks_f.winfo_children():
            w.destroy()
        for w in self.topics_f.winfo_children():
            w.destroy()
        page_imgs = (self.img["off"], self.img["on"])
        if not d["tasks"]:
            self.note(self.tasks_f, "No tasks yet. Add what you plan to study.", CARD, MUTE)
        for t in d["tasks"]:
            self.row(self.tasks_f, t["t"], t.get("d"), CARD, INK, MUTE, page_imgs, self.f["body"], self.f["done"],
                     page_wrap, lambda t=t: self.toggle_task(t), lambda t=t: self.remove(d["tasks"], t))
        if not d["topics"]:
            self.note(self.topics_f, "Note each topic you learn. It comes back for revision.", CARD, MUTE)
        for t in d["topics"]:
            tk.Frame(self.topics_f, bg=CARD)  # no-op keeps ordering simple
            r = tk.Frame(self.topics_f, bg=CARD)
            r.pack(fill="x", pady=3)
            tk.Frame(r, bg=GOLD, width=10, height=10).pack(side="left", anchor="n", padx=(4, 12), pady=5)
            tk.Label(r, text=t["t"], bg=CARD, fg=INK, font=self.f["body"], wraplength=page_wrap,
                     justify="left", anchor="w").pack(side="left", fill="x", expand=True)
            x = tk.Label(r, text="x", bg=CARD, fg=MUTE, font=self.f["btn"], padx=8, cursor="hand2")
            x.pack(side="right")
            x.bind("<Enter>", lambda e, x=x: x.config(fg=RED))
            x.bind("<Leave>", lambda e, x=x: x.config(fg=MUTE))
            x.bind("<Button-1>", lambda e, t=t: self.remove(d["topics"], t))

        # segmented progress bar
        self.prog.delete("all")
        total = len(d["tasks"])
        done = sum(1 for t in d["tasks"] if t.get("d"))
        if total:
            lit = round(10 * done / total)
            for i in range(10):
                self.prog.create_rectangle(i * 20, 0, i * 20 + 16, 14, outline=INK, width=2,
                                           fill=GREEN if i < lit else CARD)
            self.prog.create_text(212, 7, text="%d of %d done" % (done, total), anchor="w",
                                  font=self.f["small"], fill=MUTE)

        # revise footer
        foot_imgs = (self.img["foot_off"], self.img["foot_on"])
        for (lab, sc), n in zip(self.cols, INTERVALS):
            src = self.cur - timedelta(days=n)
            lab.config(text="%d days ago  (%d %s)" % (n, src.day, src.strftime("%b")))
            for w in sc.inner.winfo_children():
                w.destroy()
            items = self.revision_items(src)
            if not items:
                self.note(sc.inner, "Nothing to revise", FOOT, FOOTMUTE)
            for iid, text in items:
                k = "%s:%d" % (iid, n)
                done_r = k in self.data["rev"]
                self.row(sc.inner, text, done_r, FOOT, FOOTINK, FOOTMUTE, foot_imgs,
                         self.f["foot"], self.f["foot_done"], foot_wrap, lambda k=k: self.toggle_rev(k))

        self.update_idletasks()
        self.body.canvas.yview_moveto(keep[0])
        for (_, sc), y in zip(self.cols, keep[1:]):
            sc.canvas.yview_moveto(y)


if __name__ == "__main__":
    App().mainloop()
