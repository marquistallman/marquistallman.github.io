import os, json, shutil, re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_FILE  = os.path.join(BASE_DIR, "src", "data", "portfolio.json")
CSS_FILE   = os.path.join(BASE_DIR, "src", "index.css")
IMG_FOLDER = os.path.join(BASE_DIR, "public", "img")

# ── helpers ──────────────────────────────────────────────────────────────────

def load_data():
    if not os.path.exists(DATA_FILE):
        messagebox.showerror("Error", f"File not found:\n{DATA_FILE}")
        return None
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    messagebox.showinfo("Saved", "Changes saved successfully.")

def handle_image(path):
    src = path.strip('"').strip("'")
    if not src or not os.path.exists(src):
        messagebox.showwarning("Warning", f"Image not found:\n{src}")
        return None
    os.makedirs(IMG_FOLDER, exist_ok=True)
    fname = os.path.basename(src)
    try:
        shutil.copy(src, os.path.join(IMG_FOLDER, fname))
        return f"img/{fname}"
    except Exception as e:
        messagebox.showerror("Error", f"Could not copy image:\n{e}")
        return None

def list_to_str(lst):   return ", ".join(lst)
def str_to_list(s):     return [x.strip() for x in s.split(",") if x.strip()]
def text_to_list(s):    return [x.strip() for x in s.splitlines() if x.strip()]

# ── projects ─────────────────────────────────────────────────────────────────

def manage_projects(data):
    root = tk.Tk(); root.title("Gestionar Proyectos"); root.geometry("720x620")
    tk.Label(root, text="Proyectos", font=("Arial", 16, "bold")).pack(pady=8)
    projects = data["projects"]
    lb = tk.Listbox(root, font=("Arial", 11)); lb.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh():
        lb.delete(0, tk.END)
        for p in projects: lb.insert(tk.END, p.get("title", ""))

    def open_form(proj=None):
        w = tk.Toplevel(); w.title("Proyecto"); w.geometry("660x660")
        fields_def = [
            ("Titulo",        "title",    "entry"),
            ("Tagline",       "tagline",  "entry"),
            ("Imagen (ruta)", "image",    "entry"),
            ("Repo URL",      "repo",     "entry"),
            ("Demo URL",      "demo",     "entry"),
            ("Stack (comas)", "stack",    "entry"),
        ]
        entries = {}
        for lbl, key, kind in fields_def:
            tk.Label(w, text=f"{lbl}:").pack(anchor="w", padx=10)
            e = tk.Entry(w, width=70)
            val = proj.get(key, "") if proj else ""
            if isinstance(val, list): val = list_to_str(val)
            e.insert(0, val)
            e.pack(padx=10, pady=2)
            entries[key] = e

        for lbl, key, h in [("Problema", "problem", 4), ("Solucion", "solution", 4), ("Decisiones clave (una por linea)", "keyDecisions", 4)]:
            tk.Label(w, text=f"{lbl}:").pack(anchor="w", padx=10)
            t = tk.Text(w, height=h, width=70)
            val = proj.get(key, "") if proj else ""
            if isinstance(val, list): val = "\n".join(val)
            t.insert("1.0", val)
            t.pack(padx=10, pady=2)
            entries[key] = t

        def save():
            title = entries["title"].get().strip()
            if not title: messagebox.showerror("Error", "Titulo obligatorio."); return
            img_input = entries["image"].get().strip()
            img_src = img_input
            if img_input and not img_input.startswith("img/") and os.path.exists(img_input):
                copied = handle_image(img_input)
                if copied: img_src = copied
            entry = {
                "id":           proj["id"] if proj else (max((p["id"] for p in projects), default=0) + 1),
                "title":        title,
                "tagline":      entries["tagline"].get().strip(),
                "problem":      entries["problem"].get("1.0", tk.END).strip(),
                "solution":     entries["solution"].get("1.0", tk.END).strip(),
                "stack":        str_to_list(entries["stack"].get()),
                "keyDecisions": text_to_list(entries["keyDecisions"].get("1.0", tk.END)),
                "image":        img_src,
                "repo":         entries["repo"].get().strip(),
                "demo":         entries["demo"].get().strip(),
            }
            if proj:
                idx = next(i for i, p in enumerate(projects) if p["id"] == proj["id"])
                projects[idx] = entry
            else:
                projects.append(entry)
            save_data(data); refresh(); w.destroy()

        tk.Button(w, text="Guardar", command=save, bg="#58A6FF", fg="black").pack(pady=6)
        tk.Button(w, text="Cancelar", command=w.destroy).pack()

    def add():   open_form()
    def edit():
        sel = lb.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona un proyecto"); return
        open_form(projects[sel[0]])
    def delete():
        sel = lb.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona un proyecto"); return
        if messagebox.askyesno("Confirmar", "Borrar proyecto?"):
            projects.pop(sel[0]); save_data(data); refresh()

    refresh()
    bf = tk.Frame(root); bf.pack(pady=6)
    tk.Button(bf, text="Agregar", command=add).pack(side=tk.LEFT, padx=4)
    tk.Button(bf, text="Editar",  command=edit).pack(side=tk.LEFT, padx=4)
    tk.Button(bf, text="Borrar",  command=delete).pack(side=tk.LEFT, padx=4)
    tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=6)
    root.mainloop()

# ── experiments ──────────────────────────────────────────────────────────────

def manage_experiments(data):
    root = tk.Tk(); root.title("Experimentos / Lab"); root.geometry("680x540")
    tk.Label(root, text="Experimentos", font=("Arial", 16, "bold")).pack(pady=8)
    experiments = data.setdefault("experiments", [])
    lb = tk.Listbox(root, font=("Arial", 11)); lb.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh():
        lb.delete(0, tk.END)
        for e in experiments: lb.insert(tk.END, f"[{e.get('status','')}] {e.get('title','')}")

    STATUSES = ["in-progress", "exploring", "paused"]

    def open_form(exp=None):
        w = tk.Toplevel(); w.title("Experimento"); w.geometry("620x400")
        tk.Label(w, text="Titulo:").pack(anchor="w", padx=10)
        title_e = tk.Entry(w, width=70); title_e.insert(0, exp.get("title","") if exp else ""); title_e.pack(padx=10, pady=2)
        tk.Label(w, text="Descripcion:").pack(anchor="w", padx=10)
        desc_t = tk.Text(w, height=4, width=70); desc_t.insert("1.0", exp.get("description","") if exp else ""); desc_t.pack(padx=10, pady=2)
        tk.Label(w, text="Status:").pack(anchor="w", padx=10)
        status_var = tk.StringVar(value=exp.get("status", "exploring") if exp else "exploring")
        tk.OptionMenu(w, status_var, *STATUSES).pack(padx=10, pady=2, anchor="w")
        tk.Label(w, text="Stack (comas):").pack(anchor="w", padx=10)
        stack_e = tk.Entry(w, width=70); stack_e.insert(0, list_to_str(exp.get("stack",[]) if exp else [])); stack_e.pack(padx=10, pady=2)

        def save():
            title = title_e.get().strip()
            if not title: messagebox.showerror("Error", "Titulo obligatorio."); return
            entry = {
                "id":          exp["id"] if exp else (max((e["id"] for e in experiments), default=0) + 1),
                "title":       title,
                "description": desc_t.get("1.0", tk.END).strip(),
                "status":      status_var.get(),
                "stack":       str_to_list(stack_e.get()),
            }
            if exp:
                idx = next(i for i, e in enumerate(experiments) if e["id"] == exp["id"])
                experiments[idx] = entry
            else:
                experiments.append(entry)
            save_data(data); refresh(); w.destroy()

        tk.Button(w, text="Guardar", command=save, bg="#39D353", fg="black").pack(pady=6)
        tk.Button(w, text="Cancelar", command=w.destroy).pack()

    def add():   open_form()
    def edit():
        sel = lb.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona un experimento"); return
        open_form(experiments[sel[0]])
    def delete():
        sel = lb.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona un experimento"); return
        if messagebox.askyesno("Confirmar", "Borrar?"):
            experiments.pop(sel[0]); save_data(data); refresh()

    refresh()
    bf = tk.Frame(root); bf.pack(pady=6)
    tk.Button(bf, text="Agregar", command=add).pack(side=tk.LEFT, padx=4)
    tk.Button(bf, text="Editar",  command=edit).pack(side=tk.LEFT, padx=4)
    tk.Button(bf, text="Borrar",  command=delete).pack(side=tk.LEFT, padx=4)
    tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=6)
    root.mainloop()

# ── general / hero / header ───────────────────────────────────────────────────

def manage_general(data):
    root = tk.Tk(); root.title("Editar Textos Generales"); root.geometry("640x580")
    tk.Label(root, text="Textos Generales", font=("Arial", 16, "bold")).pack(pady=8)
    h = data["header"]; hero = data["hero"]; about = data["about"]
    simple_fields = [
        ("Nombre (Header)",     h,    "name"),
        ("Role / Subtitle",     h,    "role"),
        ("Avatar (img/...)",    h,    "avatar"),
        ("Hero Headline",       hero, "headline"),
        ("Hero Subheadline",    hero, "subheadline"),
        ("Hero Stack (comas)",  hero, "stack"),
        ("GitHub URL",          hero, "githubUrl"),
        ("Email",               hero, "email"),
    ]
    entries = []
    for lbl, obj, key in simple_fields:
        tk.Label(root, text=f"{lbl}:").pack(anchor="w", padx=10)
        e = tk.Entry(root, width=70)
        val = obj.get(key, "")
        if isinstance(val, list): val = list_to_str(val)
        e.insert(0, val)
        e.pack(padx=10, pady=2)
        entries.append((obj, key, e, isinstance(obj.get(key,""), list)))

    tk.Label(root, text="Bio (About):").pack(anchor="w", padx=10)
    bio_t = tk.Text(root, height=4, width=70)
    bio_t.insert("1.0", about.get("bio",""))
    bio_t.pack(padx=10, pady=2)

    tk.Label(root, text="Intereses (comas):").pack(anchor="w", padx=10)
    interests_e = tk.Entry(root, width=70)
    interests_e.insert(0, list_to_str(about.get("interests",[])))
    interests_e.pack(padx=10, pady=2)

    def save():
        for obj, key, e, is_list in entries:
            obj[key] = str_to_list(e.get()) if is_list else e.get().strip()
        about["bio"]       = bio_t.get("1.0", tk.END).strip()
        about["interests"] = str_to_list(interests_e.get())
        save_data(data); root.destroy()

    tk.Button(root, text="Guardar", command=save, bg="#58A6FF", fg="black").pack(pady=10)
    tk.Button(root, text="Cancelar", command=root.destroy).pack()
    root.mainloop()

# ── skills ────────────────────────────────────────────────────────────────────

def manage_skills(data):
    root = tk.Tk(); root.title("Gestionar Skills"); root.geometry("580x300")
    tk.Label(root, text="Skills por Categoria", font=("Arial", 16, "bold")).pack(pady=8)
    skills = data.setdefault("skills", {"backend":[], "systems":[], "tools":[]})
    CATS = [("Backend",          "backend"),
            ("Systems & DevOps", "systems"),
            ("Tools & Misc",     "tools")]
    entries = []
    for lbl, key in CATS:
        tk.Label(root, text=f"{lbl} (comas):").pack(anchor="w", padx=10)
        e = tk.Entry(root, width=72)
        e.insert(0, list_to_str(skills.get(key,[])))
        e.pack(padx=10, pady=3)
        entries.append((key, e))

    def save():
        for key, e in entries:
            skills[key] = str_to_list(e.get())
        save_data(data); root.destroy()

    tk.Button(root, text="Guardar", command=save, bg="#39D353", fg="black").pack(pady=10)
    tk.Button(root, text="Cancelar", command=root.destroy).pack()
    root.mainloop()

# ── contact ───────────────────────────────────────────────────────────────────

def manage_contact(data):
    root = tk.Tk(); root.title("Gestionar Contacto"); root.geometry("640x420")
    tk.Label(root, text="Contacto", font=("Arial", 16, "bold")).pack(pady=8)
    contacts = data["contact"]
    lb = tk.Listbox(root, font=("Arial", 11)); lb.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh():
        lb.delete(0, tk.END)
        for c in contacts: lb.insert(tk.END, f"{c.get('label','')}  ->  {c.get('href','')}")

    ICONS = ["email","github","discord","linkedin","twitter"]

    def open_form(c=None):
        w = tk.Toplevel(); w.title("Contacto"); w.geometry("500x260")
        tk.Label(w, text="Etiqueta visible:").pack(anchor="w", padx=10)
        label_e = tk.Entry(w, width=60); label_e.insert(0, c.get("label","") if c else ""); label_e.pack(padx=10, pady=2)
        tk.Label(w, text="Enlace (URL o mailto:):").pack(anchor="w", padx=10)
        href_e  = tk.Entry(w, width=60); href_e.insert(0,  c.get("href", "") if c else ""); href_e.pack(padx=10, pady=2)
        tk.Label(w, text="Icono (email/github/discord/linkedin/twitter):").pack(anchor="w", padx=10)
        icon_e  = tk.Entry(w, width=60); icon_e.insert(0,  c.get("icon", "") if c else ""); icon_e.pack(padx=10, pady=2)

        def save():
            label = label_e.get().strip()
            if not label: messagebox.showerror("Error", "Etiqueta obligatoria."); return
            entry = {"label": label, "href": href_e.get().strip(), "icon": icon_e.get().strip()}
            if c:
                idx = contacts.index(c); contacts[idx] = entry
            else:
                contacts.append(entry)
            save_data(data); refresh(); w.destroy()

        tk.Button(w, text="Guardar", command=save).pack(pady=6)
        tk.Button(w, text="Cancelar", command=w.destroy).pack()

    def add():   open_form()
    def edit():
        sel = lb.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona un item"); return
        open_form(contacts[sel[0]])
    def delete():
        sel = lb.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona un item"); return
        if messagebox.askyesno("Confirmar", "Borrar?"):
            contacts.pop(sel[0]); save_data(data); refresh()

    refresh()
    bf = tk.Frame(root); bf.pack(pady=6)
    tk.Button(bf, text="Agregar", command=add).pack(side=tk.LEFT, padx=4)
    tk.Button(bf, text="Editar",  command=edit).pack(side=tk.LEFT, padx=4)
    tk.Button(bf, text="Borrar",  command=delete).pack(side=tk.LEFT, padx=4)
    tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=6)
    root.mainloop()

# ── colors ────────────────────────────────────────────────────────────────────

def manage_colors():
    root = tk.Tk(); root.title("Gestionar Colores"); root.geometry("520x540")
    if not os.path.exists(CSS_FILE): messagebox.showerror("Error", f"Not found: {CSS_FILE}"); root.destroy(); return
    with open(CSS_FILE, encoding="utf-8") as f: css = f.read()
    original = dict(re.findall(r"--(\w+):\s*(#[\da-fA-F]{6}|rgba?\([^)]+\))", css))
    current  = dict(original)
    tk.Label(root, text="Colores CSS (--variables)", font=("Arial", 14, "bold")).pack(pady=8)
    for var, val in original.items():
        fr = tk.Frame(root); fr.pack(fill=tk.X, padx=16, pady=3)
        tk.Label(fr, text=f"--{var}:", width=14, anchor="w").pack(side=tk.LEFT)
        lbl = tk.Label(fr, text=val, width=24, anchor="w"); lbl.pack(side=tk.LEFT, padx=4)
        def pick(v=var, lb=lbl, cur=val):
            init = cur if cur.startswith("#") else "#58A6FF"
            chosen = colorchooser.askcolor(color=init)
            if chosen[1]: current[v] = chosen[1]; lb.config(text=chosen[1])
        tk.Button(fr, text="Cambiar", command=pick).pack(side=tk.LEFT)

    def save():
        updated = css
        for v, new in current.items():
            if new != original.get(v):
                updated = re.sub(f"--{v}:\\s*{re.escape(original[v])}", f"--{v}: {new}", updated)
        with open(CSS_FILE, "w", encoding="utf-8") as f: f.write(updated)
        messagebox.showinfo("Saved", "Palette updated. Reload browser.")
        root.destroy()

    tk.Button(root, text="Guardar Cambios", command=save, bg="#58A6FF", fg="black", font=("Arial", 12, "bold")).pack(pady=16)
    tk.Button(root, text="Cancelar", command=root.destroy).pack()
    root.mainloop()

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    root = tk.Tk(); root.title("PORTFOLIO MANAGER v3"); root.geometry("400x460")
    tk.Label(root, text="PORTFOLIO MANAGER v3", font=("Arial", 17, "bold")).pack(pady=18)

    def run(fn, needs_data=True):
        if needs_data:
            d = load_data()
            if d: fn(d)
        else:
            fn()

    buttons = [
        ("Gestionar Proyectos",     lambda: run(manage_projects)),
        ("Gestionar Experimentos",  lambda: run(manage_experiments)),
        ("Editar Textos Generales", lambda: run(manage_general)),
        ("Gestionar Skills",        lambda: run(manage_skills)),
        ("Gestionar Contacto",      lambda: run(manage_contact)),
        ("Gestionar Colores",       lambda: run(manage_colors, needs_data=False)),
    ]
    for txt, cmd in buttons:
        tk.Button(root, text=txt, width=34, height=2, command=cmd).pack(pady=4)

    tk.Button(root, text="Salir", width=14, command=root.quit).pack(pady=14)
    root.mainloop()

if __name__ == "__main__":
    main()
