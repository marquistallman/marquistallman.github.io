import os
import json
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser

# --- CONSTANTS ---
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "src", "data", "portfolio.json")
CSS_FILE  = os.path.join(BASE_DIR, "src", "index.css")
IMG_FOLDER = os.path.join(BASE_DIR, "public", "img")

# --- HELPERS ---

def load_data():
    if not os.path.exists(DATA_FILE):
        messagebox.showerror("Error", f"No se encuentra:\n{DATA_FILE}")
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    messagebox.showinfo("Exito", "Cambios guardados.")

def handle_image(img_path_input):
    src = img_path_input.strip('"').strip("'")
    if not src or not os.path.exists(src):
        messagebox.showwarning("Aviso", f"Imagen no encontrada:\n{src}")
        return None
    os.makedirs(IMG_FOLDER, exist_ok=True)
    filename = os.path.basename(src)
    dest = os.path.join(IMG_FOLDER, filename)
    try:
        shutil.copy(src, dest)
        return f"img/{filename}"
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo copiar la imagen:\n{e}")
        return None

# --- PROJECTS ---

def manage_projects(data):
    root = tk.Tk()
    root.title("Gestionar Proyectos")
    root.geometry("700x600")
    tk.Label(root, text="Gestionar Proyectos", font=("Arial", 16)).pack(pady=10)
    projects = data["projects"]
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    listbox = tk.Listbox(frame)
    listbox.pack(fill=tk.BOTH, expand=True)

    def refresh():
        listbox.delete(0, tk.END)
        for p in projects:
            listbox.insert(tk.END, p.get("title", "Sin titulo"))

    def open_form(project=None):
        form = tk.Toplevel()
        form.title("Proyecto")
        form.geometry("600x520")
        fields = [
            ("Titulo",       "title",       ""),
            ("Descripcion",  "description", ""),
            ("Tags",         "tags",        ""),
            ("Ruta Imagen",  "image",       ""),
            ("Link Repo",    "repo",        ""),
            ("Link Demo",    "demo",        ""),
        ]
        entries = {}
        for label, key, default in fields:
            tk.Label(form, text=f"{label}:").pack()
            e = tk.Entry(form, width=60)
            e.insert(0, project.get(key, default) if project else default)
            e.pack(padx=10, pady=3)
            entries[key] = e

        def save():
            title = entries["title"].get().strip()
            if not title:
                messagebox.showerror("Error", "El titulo es obligatorio.")
                return
            img_input = entries["image"].get().strip()
            img_src = img_input
            if img_input and not img_input.startswith("img/") and os.path.exists(img_input):
                copied = handle_image(img_input)
                if copied:
                    img_src = copied
            entry = {
                "id":          project["id"] if project else (max((p["id"] for p in projects), default=0) + 1),
                "title":       title,
                "description": entries["description"].get().strip(),
                "tags":        entries["tags"].get().strip(),
                "image":       img_src,
                "repo":        entries["repo"].get().strip(),
                "demo":        entries["demo"].get().strip(),
            }
            if project:
                idx = next(i for i, p in enumerate(projects) if p["id"] == project["id"])
                projects[idx] = entry
            else:
                projects.append(entry)
            save_data(data)
            refresh()
            form.destroy()

        tk.Button(form, text="Guardar",  command=save).pack(pady=5)
        tk.Button(form, text="Cancelar", command=form.destroy).pack()

    def add():   open_form()
    def edit():
        sel = listbox.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona un proyecto"); return
        open_form(projects[sel[0]])
    def delete():
        sel = listbox.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona un proyecto"); return
        if messagebox.askyesno("Confirmar", "Borrar proyecto?"):
            projects.pop(sel[0]); save_data(data); refresh()

    refresh()
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Agregar", command=add).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Editar",  command=edit).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Borrar",  command=delete).pack(side=tk.LEFT, padx=5)
    tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=10)
    root.mainloop()

# --- GENERAL ---

def manage_general(data):
    root = tk.Tk()
    root.title("Editar Textos Generales")
    root.geometry("600x520")
    tk.Label(root, text="Editar Textos Generales", font=("Arial", 16)).pack(pady=10)
    h = data["header"]; hero = data["hero"]; about = data["about"]
    fields = [
        ("Nombre (Header)",  h,     "name"),
        ("Subtitulo",        h,     "subtitle"),
        ("Avatar (img/...)", h,     "avatar"),
        ("Titulo Hero",      hero,  "title"),
        ("GitHub URL",       hero,  "githubUrl"),
        ("Email",            hero,  "email"),
        ("Imagen Hero",      hero,  "image"),
    ]
    entries = []
    for label, obj, key in fields:
        tk.Label(root, text=f"{label}:").pack()
        e = tk.Entry(root, width=60)
        e.insert(0, obj.get(key, ""))
        e.pack(padx=10, pady=3)
        entries.append((obj, key, e))
    tk.Label(root, text="Sobre mi:").pack()
    about_text = tk.Text(root, height=5, width=60)
    about_text.insert(1.0, about.get("bio", ""))
    about_text.pack(padx=10, pady=3)
    def save():
        for obj, key, e in entries: obj[key] = e.get().strip()
        about["bio"] = about_text.get(1.0, tk.END).strip()
        save_data(data); root.destroy()
    tk.Button(root, text="Guardar",  command=save).pack(pady=10)
    tk.Button(root, text="Cancelar", command=root.destroy).pack()
    root.mainloop()

# --- SKILLS ---

def manage_skills(data):
    root = tk.Tk()
    root.title("Gestionar Skills")
    root.geometry("600x500")
    tk.Label(root, text="Gestionar Skills", font=("Arial", 16)).pack(pady=10)
    skills = data["skills"]
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    listbox = tk.Listbox(frame)
    listbox.pack(fill=tk.BOTH, expand=True)

    def refresh():
        listbox.delete(0, tk.END)
        for s in skills: listbox.insert(tk.END, s.get("name", ""))

    def add():
        name = simpledialog.askstring("Nueva Skill", "Nombre:"); 
        if not name: return
        desc = simpledialog.askstring("Nueva Skill", "Descripcion:") or ""
        img_path = filedialog.askopenfilename(title="Selecciona imagen")
        img_src = handle_image(img_path) if img_path else ""
        skills.append({"name": name, "desc": desc, "img": img_src or ""})
        save_data(data); refresh()

    def edit():
        sel = listbox.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona una skill"); return
        s = skills[sel[0]]
        new_name = simpledialog.askstring("Editar", "Nombre:", initialvalue=s.get("name", ""))
        if not new_name: return
        new_desc = simpledialog.askstring("Editar", "Descripcion:", initialvalue=s.get("desc", "")) or ""
        if messagebox.askyesno("Imagen", "Cambiar imagen?"):
            img_path = filedialog.askopenfilename(title="Selecciona imagen")
            if img_path:
                copied = handle_image(img_path)
                if copied: s["img"] = copied
        s["name"] = new_name; s["desc"] = new_desc
        save_data(data); refresh()

    def delete():
        sel = listbox.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona una skill"); return
        if messagebox.askyesno("Confirmar", "Borrar skill?"):
            skills.pop(sel[0]); save_data(data); refresh()

    refresh()
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Agregar", command=add).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Editar",  command=edit).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Borrar",  command=delete).pack(side=tk.LEFT, padx=5)
    tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=10)
    root.mainloop()

# --- CONTACT ---

def manage_contact(data):
    root = tk.Tk()
    root.title("Gestionar Contacto")
    root.geometry("600x400")
    tk.Label(root, text="Gestionar Contacto", font=("Arial", 16)).pack(pady=10)
    contacts = data["contact"]
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    listbox = tk.Listbox(frame)
    listbox.pack(fill=tk.BOTH, expand=True)

    def refresh():
        listbox.delete(0, tk.END)
        for c in contacts: listbox.insert(tk.END, f"{c.get('label','')}  ->  {c.get('href','')}")

    def edit():
        sel = listbox.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona un contacto"); return
        c = contacts[sel[0]]
        new_label = simpledialog.askstring("Editar", "Texto visible:", initialvalue=c.get("label", ""))
        if not new_label: return
        new_href = simpledialog.askstring("Editar", "Enlace:", initialvalue=c.get("href", "")) or ""
        c["label"] = new_label; c["href"] = new_href
        save_data(data); refresh()

    def add():
        label = simpledialog.askstring("Nuevo Contacto", "Texto visible:")
        if not label: return
        href = simpledialog.askstring("Nuevo Contacto", "Enlace:") or ""
        contacts.append({"label": label, "href": href}); save_data(data); refresh()

    def delete():
        sel = listbox.curselection()
        if not sel: messagebox.showerror("Error", "Selecciona un contacto"); return
        if messagebox.askyesno("Confirmar", "Borrar?"):
            contacts.pop(sel[0]); save_data(data); refresh()

    refresh()
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Agregar", command=add).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Editar",  command=edit).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Borrar",  command=delete).pack(side=tk.LEFT, padx=5)
    tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=10)
    root.mainloop()

# --- COLORS ---

def manage_colors():
    root = tk.Tk()
    root.title("Gestionar Colores")
    root.geometry("500x580")
    if not os.path.exists(CSS_FILE):
        messagebox.showerror("Error", f"No se encuentra {CSS_FILE}"); root.destroy(); return
    with open(CSS_FILE, "r", encoding="utf-8") as f: css_content = f.read()
    color_pattern = r"--(\w+):\s*(#[\da-fA-F]{6}|rgba?\([^)]+\))"
    original_colors = dict(re.findall(color_pattern, css_content))
    color_entries = dict(original_colors)
    tk.Label(root, text="Gestionar Colores", font=("Arial", 16)).pack(pady=10)
    for var_name, color_val in original_colors.items():
        frame = tk.Frame(root)
        frame.pack(fill=tk.X, padx=20, pady=4)
        tk.Label(frame, text=f"--{var_name}:", width=16, anchor="w").pack(side=tk.LEFT)
        label = tk.Label(frame, text=color_val, width=22, anchor="w")
        label.pack(side=tk.LEFT, padx=5)
        def pick(v=var_name, lbl=label, cur=color_val):
            initial = cur if cur.startswith("#") else "#6dd3ff"
            chosen = colorchooser.askcolor(color=initial)
            if chosen[1]: color_entries[v] = chosen[1]; lbl.config(text=chosen[1])
        tk.Button(frame, text="Cambiar", command=pick).pack(side=tk.LEFT)

    def save():
        updated = css_content
        for var_name, new_color in color_entries.items():
            if new_color != original_colors.get(var_name):
                updated = re.sub(
                    f"--{var_name}:\\s*{re.escape(original_colors[var_name])}",
                    f"--{var_name}: {new_color}", updated)
        with open(CSS_FILE, "w", encoding="utf-8") as f: f.write(updated)
        messagebox.showinfo("Exito", "Paleta actualizada. Recarga el navegador.")
        root.destroy()

    tk.Button(root, text="Guardar Cambios", command=save,
              bg="#6dd3ff", fg="black", font=("Arial", 12, "bold")).pack(pady=20)
    tk.Button(root, text="Cancelar", command=root.destroy).pack()
    root.mainloop()

# --- MAIN ---

def main():
    root = tk.Tk()
    root.title("PORTFOLIO MANAGER v3")
    root.geometry("400x480")
    tk.Label(root, text="PORTFOLIO MANAGER v3", font=("Arial", 18, "bold")).pack(pady=20)

    def run(fn, uses_data=True):
        if uses_data:
            d = load_data()
            if d: fn(d)
        else:
            fn()

    for text, cmd in [
        ("Gestionar Proyectos",     lambda: run(manage_projects)),
        ("Editar Textos Generales", lambda: run(manage_general)),
        ("Gestionar Skills",        lambda: run(manage_skills)),
        ("Gestionar Contacto",      lambda: run(manage_contact)),
        ("Gestionar Colores",       lambda: run(manage_colors, uses_data=False)),
    ]:
        tk.Button(root, text=text, width=32, height=2, command=cmd).pack(pady=6)

    tk.Button(root, text="Salir", width=15, command=root.quit).pack(pady=16)
    root.mainloop()

if __name__ == "__main__":
    main()
