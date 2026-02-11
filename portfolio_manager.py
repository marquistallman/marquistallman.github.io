import os
import shutil
import sys
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from bs4 import BeautifulSoup

# --- CONSTANTS AND SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, "index.html")
IMG_FOLDER = os.path.join(BASE_DIR, "img")
CSS_FILE = os.path.join(BASE_DIR, "style.css")

# --- CORE HELPER FUNCTIONS ---

def load_soup():
    """Loads and parses the index.html file."""
    if not os.path.exists(HTML_FILE):
        messagebox.showerror("Error", f"❌ No se encuentra el archivo principal:\n{HTML_FILE}")
        return None
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def save_soup(soup):
    """Saves the BeautifulSoup object back to the HTML file."""
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    messagebox.showinfo("✅ Éxito", "Cambios guardados exitosamente.")

def handle_image(img_path_input):
    """Copies an image to the project's img folder and returns its relative path."""
    src_path = img_path_input.strip('"').strip("'")
    if not src_path:
        return None

    if not os.path.exists(src_path):
        messagebox.showwarning("Aviso", f"⚠️ Imagen no encontrada:\n{src_path}")
        return None

    filename = os.path.basename(src_path)
    dest_path = os.path.join(IMG_FOLDER, filename)

    if not os.path.exists(IMG_FOLDER):
        os.makedirs(IMG_FOLDER)

    try:
        shutil.copy(src_path, dest_path)
        return f"img/{filename}"
    except Exception as e:
        messagebox.showerror("Error", f"Error al copiar la imagen:\n{e}")
        return None

# --- GESTIÓN DE PROYECTOS ---

def add_project(soup, container, parent_window=None):
    """Add a new project with GUI dialog."""
    form = tk.Toplevel()
    form.title("Agregar Nuevo Proyecto")
    form.geometry("600x500")
    
    # Title
    tk.Label(form, text="Título:").pack()
    title_entry = tk.Entry(form, width=50)
    title_entry.pack(padx=10, pady=5)
    
    # Description
    tk.Label(form, text="Descripción:").pack()
    desc_entry = tk.Entry(form, width=50)
    desc_entry.pack(padx=10, pady=5)
    
    # Tags
    tk.Label(form, text="Tags:").pack()
    tags_entry = tk.Entry(form, width=50)
    tags_entry.pack(padx=10, pady=5)
    
    # Image
    tk.Label(form, text="Ruta Imagen:").pack()
    img_entry = tk.Entry(form, width=50)
    img_entry.pack(padx=10, pady=5)
    
    # Repo
    tk.Label(form, text="Link Repo:").pack()
    repo_entry = tk.Entry(form, width=50)
    repo_entry.pack(padx=10, pady=5)
    
    # Demo
    tk.Label(form, text="Link Demo:").pack()
    demo_entry = tk.Entry(form, width=50)
    demo_entry.pack(padx=10, pady=5)
    
    def save_project():
        title = title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "El título es obligatorio.")
            return
        
        desc = desc_entry.get().strip()
        tags = tags_entry.get().strip()
        img_path = img_entry.get().strip()
        repo = repo_entry.get().strip()
        demo = demo_entry.get().strip()
        
        img_src = handle_image(img_path) if img_path else "https://via.placeholder.com/300"
        
        article = soup.new_tag("article", attrs={"class": "card"})
        
        img = soup.new_tag("img", src=img_src, alt=title, attrs={"class": "card-img"})
        article.append(img)
        
        body = soup.new_tag("div", attrs={"class": "card-body"})
        h4 = soup.new_tag("h4")
        h4.string = title
        body.append(h4)
        
        p = soup.new_tag("p")
        p.string = desc
        body.append(p)
        
        ptags = soup.new_tag("p", attrs={"class": "muted small"})
        ptags.string = tags
        body.append(ptags)
        
        actions = soup.new_tag("div", attrs={"class": "card-actions"})
        if repo:
            a = soup.new_tag("a", href=repo, target="_blank")
            a.string = "Repo"
            actions.append(a)
        if demo:
            a = soup.new_tag("a", href=demo, target="_blank")
            a.string = "Demo"
            actions.append(a)
        
        body.append(actions)
        article.append(body)
        container.append(article)
        save_soup(soup)
        messagebox.showinfo("✅", "Proyecto agregado.")
        form.destroy()
    
    tk.Button(form, text="Guardar", command=save_project).pack(pady=5)
    tk.Button(form, text="Cancelar", command=form.destroy).pack(pady=5)

def edit_project(soup, project, parent_window=None):
    """Edit an existing project."""
    form = tk.Toplevel()
    form.title("Editar Proyecto")
    form.geometry("600x500")
    
    h4 = project.find("h4")
    curr_title = h4.get_text(strip=True) if h4 else ""
    
    p_desc = project.find("p")
    curr_desc = p_desc.get_text(strip=True) if p_desc else ""
    
    p_tags = project.find("p", class_="muted")
    curr_tags = p_tags.get_text(strip=True) if p_tags else ""
    
    img = project.find("img")
    curr_img = img['src'] if img else ""
    
    actions = project.find("div", class_="card-actions")
    links = actions.find_all("a") if actions else []
    curr_repo = links[0]['href'] if len(links) > 0 else ""
    curr_demo = links[1]['href'] if len(links) > 1 else ""
    
    tk.Label(form, text="Título:").pack()
    title_entry = tk.Entry(form, width=50)
    title_entry.insert(0, curr_title)
    title_entry.pack(padx=10, pady=5)
    
    tk.Label(form, text="Descripción:").pack()
    desc_entry = tk.Entry(form, width=50)
    desc_entry.insert(0, curr_desc)
    desc_entry.pack(padx=10, pady=5)
    
    tk.Label(form, text="Tags:").pack()
    tags_entry = tk.Entry(form, width=50)
    tags_entry.insert(0, curr_tags)
    tags_entry.pack(padx=10, pady=5)
    
    tk.Label(form, text="Link Repo:").pack()
    repo_entry = tk.Entry(form, width=50)
    repo_entry.insert(0, curr_repo)
    repo_entry.pack(padx=10, pady=5)
    
    tk.Label(form, text="Link Demo:").pack()
    demo_entry = tk.Entry(form, width=50)
    demo_entry.insert(0, curr_demo)
    demo_entry.pack(padx=10, pady=5)
    
    tk.Label(form, text=f"Imagen actual: {curr_img}").pack()
    
    tk.Label(form, text="Nueva Imagen (Enter para mantener):").pack()
    img_entry = tk.Entry(form, width=50)
    img_entry.pack(padx=10, pady=5)
    
    def save_edit():
        new_title = title_entry.get().strip()
        new_desc = desc_entry.get().strip()
        new_tags = tags_entry.get().strip()
        new_repo = repo_entry.get().strip()
        new_demo = demo_entry.get().strip()
        new_img_path = img_entry.get().strip()
        
        if h4: h4.string = new_title
        if p_desc: p_desc.string = new_desc
        if p_tags: p_tags.string = new_tags
        
        if new_img_path:
            processed = handle_image(new_img_path)
            if processed and img: img['src'] = processed
        
        if actions:
            actions.clear()
            if new_repo:
                a = soup.new_tag("a", href=new_repo, target="_blank")
                a.string = "Repo"
                actions.append(a)
            if new_demo:
                a = soup.new_tag("a", href=new_demo, target="_blank")
                a.string = "Demo"
                actions.append(a)
        
        save_soup(soup)
        messagebox.showinfo("✅", "Proyecto actualizado.")
        form.destroy()
    
    tk.Button(form, text="Guardar", command=save_edit).pack(pady=5)
    tk.Button(form, text="Cancelar", command=form.destroy).pack(pady=5)

def manage_projects(soup):
    """Manage projects with GUI."""
    root = tk.Tk()
    root.title("Gestionar Proyectos")
    root.geometry("700x600")
    
    tk.Label(root, text="Gestionar Proyectos", font=("Arial", 16)).pack(pady=10)
    
    container = soup.find(id="projects-list")
    if not container:
        messagebox.showerror("Error", "No se encontró el contenedor #projects-list")
        root.destroy()
        return
    
    # Listbox
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    listbox = tk.Listbox(frame)
    listbox.pack(fill=tk.BOTH, expand=True)
    
    def refresh_list():
        listbox.delete(0, tk.END)
        projects = container.find_all("article", class_="card")
        for p in projects:
            t = p.find("h4").get_text(strip=True) if p.find("h4") else "Sin título"
            listbox.insert(tk.END, t)
    
    refresh_list()
    
    def add():
        add_project(soup, container, root)
        refresh_list()
    
    def edit():
        sel = listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un proyecto")
            return
        idx = sel[0]
        projects = container.find_all("article", class_="card")
        edit_project(soup, projects[idx], root)
        refresh_list()
    
    def delete():
        sel = listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un proyecto")
            return
        if messagebox.askyesno("Confirmar", "¿Borrar proyecto?"):
            idx = sel[0]
            projects = container.find_all("article", class_="card")
            projects[idx].decompose()
            save_soup(soup)
            refresh_list()
    
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Agregar", command=add).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Editar", command=edit).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Borrar", command=delete).pack(side=tk.LEFT, padx=5)
    tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=10)
    
    root.mainloop()

# --- GESTIÓN GENERAL ---

def manage_general(soup):
    """Edit general website texts."""
    root = tk.Tk()
    root.title("Editar Textos Generales")
    root.geometry("600x500")
    
    tk.Label(root, text="Editar Textos Generales", font=("Arial", 16)).pack(pady=10)
    
    h1 = soup.select_one(".brand h1")
    sub = soup.select_one(".brand .muted")
    hero_h2 = soup.select_one(".hero h2")
    about_p = soup.select_one(".about-card p")
    
    tk.Label(root, text="Nombre (Header):").pack()
    h1_entry = tk.Entry(root, width=50)
    h1_entry.insert(0, h1.get_text(strip=True) if h1 else "")
    h1_entry.pack(pady=5)
    
    tk.Label(root, text="Subtítulo:").pack()
    sub_entry = tk.Entry(root, width=50)
    sub_entry.insert(0, sub.get_text(strip=True) if sub else "")
    sub_entry.pack(pady=5)
    
    tk.Label(root, text="Título Hero:").pack()
    hero_entry = tk.Entry(root, width=50)
    hero_entry.insert(0, hero_h2.get_text(strip=True) if hero_h2 else "")
    hero_entry.pack(pady=5)
    
    tk.Label(root, text="Sobre mí (Texto):").pack()
    about_text = tk.Text(root, height=6, width=50)
    about_text.insert(1.0, about_p.get_text(strip=True) if about_p else "")
    about_text.pack(pady=5)
    
    def save():
        if h1: h1.string = h1_entry.get().strip()
        if sub: sub.string = sub_entry.get().strip()
        if hero_h2: hero_h2.string = hero_entry.get().strip()
        if about_p: about_p.string = about_text.get(1.0, tk.END).strip()
        save_soup(soup)
        root.destroy()
    
    tk.Button(root, text="Guardar", command=save).pack(pady=10)
    tk.Button(root, text="Cancelar", command=root.destroy).pack()
    
    root.mainloop()

# --- GESTIÓN SKILLS ---

def manage_skills(soup):
    """Manage skills with GUI."""
    root = tk.Tk()
    root.title("Gestionar Skills")
    root.geometry("600x500")
    
    tk.Label(root, text="Gestionar Skills", font=("Arial", 16)).pack(pady=10)
    
    container = soup.select_one(".chips")
    if not container:
        messagebox.showerror("Error", "No se encontró el contenedor .chips")
        root.destroy()
        return
    
    # Listbox
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    listbox = tk.Listbox(frame)
    listbox.pack(fill=tk.BOTH, expand=True)
    
    def refresh_list():
        listbox.delete(0, tk.END)
        skills = container.find_all("span", class_="chip")
        for s in skills:
            listbox.insert(tk.END, s.get_text(strip=True))
    
    refresh_list()
    
    def add():
        name = simpledialog.askstring("Nueva Skill", "Nombre de la skill:")
        if name:
            desc = simpledialog.askstring("Nueva Skill", "Descripción:")
            img_path = filedialog.askopenfilename(title="Selecciona imagen")
            
            processed_img = handle_image(img_path) if img_path else "https://via.placeholder.com/320x180"
            
            span = soup.new_tag("span", attrs={
                "class": "chip",
                "data-img": processed_img,
                "data-desc": desc or "",
                "title": name
            })
            span.string = name
            container.append(span)
            save_soup(soup)
            refresh_list()
    
    def edit():
        sel = listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona una skill")
            return
        idx = sel[0]
        skills = container.find_all("span", class_="chip")
        chip = skills[idx]
        
        new_name = simpledialog.askstring("Editar", "Nombre:", initialvalue=chip.get_text(strip=True))
        if new_name:
            new_desc = simpledialog.askstring("Editar", "Descripción:", initialvalue=chip.get('data-desc', ''))
            chip.string = new_name
            chip['title'] = new_name
            chip['data-desc'] = new_desc or ""
            save_soup(soup)
            refresh_list()
    
    def delete():
        sel = listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona una skill")
            return
        if messagebox.askyesno("Confirmar", "¿Borrar skill?"):
            idx = sel[0]
            skills = container.find_all("span", class_="chip")
            skills[idx].decompose()
            save_soup(soup)
            refresh_list()
    
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Agregar", command=add).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Editar", command=edit).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Borrar", command=delete).pack(side=tk.LEFT, padx=5)
    tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=10)
    
    root.mainloop()

# --- GESTIÓN CONTACTO ---

def manage_contact(soup):
    """Manage contact links with GUI."""
    root = tk.Tk()
    root.title("Gestionar Contacto")
    root.geometry("600x400")
    
    tk.Label(root, text="Gestionar Contacto", font=("Arial", 16)).pack(pady=10)
    
    cards = soup.select("#contact .contact-card")
    if not cards:
        messagebox.showerror("Error", "No se encontraron links de contacto")
        root.destroy()
        return
    
    # Listbox
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    listbox = tk.Listbox(frame)
    listbox.pack(fill=tk.BOTH, expand=True)
    
    def refresh_list():
        listbox.delete(0, tk.END)
        for c in cards:
            text = c.get_text(strip=True)
            href = c.get('href', '')
            listbox.insert(tk.END, f"{text} -> {href}")
    
    refresh_list()
    
    def edit():
        sel = listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un contacto")
            return
        idx = sel[0]
        card = cards[idx]
        
        curr_text = card.get_text(strip=True)
        curr_href = card.get('href', '')
        
        new_text = simpledialog.askstring("Editar", "Texto visible:", initialvalue=curr_text)
        if new_text:
            new_href = simpledialog.askstring("Editar", "Enlace:", initialvalue=curr_href)
            if new_href:
                card.string = new_text
                card['href'] = new_href
                save_soup(soup)
                cards = soup.select("#contact .contact-card")
                refresh_list()
    
    tk.Button(root, text="Editar", command=edit).pack(pady=10)
    tk.Button(root, text="Cerrar", command=root.destroy).pack()
    
    root.mainloop()

# --- GESTIÓN COLORES ---

def manage_colors():
    """Manage website color palette."""
    root = tk.Tk()
    root.title("Gestionar Colores")
    root.geometry("500x600")
    
    if not os.path.exists(CSS_FILE):
        messagebox.showerror("Error", f"No se encuentra {CSS_FILE}")
        root.destroy()
        return
    
    # Read current CSS
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css_content = f.read()
    
    # Extract color variables
    colors = {}
    color_pattern = r'--(\w+):\s*(#[\da-fA-F]{6}|rgba?\([^)]+\))'
    matches = re.findall(color_pattern, css_content)
    
    for var_name, color_val in matches:
        colors[var_name] = color_val
    
    tk.Label(root, text="Gestionar Colores", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="Haz clic en un color para editarlo:", font=("Arial", 10)).pack(pady=5)
    
    color_entries = {}
    
    def create_color_button(var_name, current_color):
        frame = tk.Frame(root)
        frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(frame, text=f"--{var_name}:", width=15, anchor="w").pack(side=tk.LEFT)
        tk.Label(frame, text=current_color, width=20, anchor="w").pack(side=tk.LEFT, padx=10)
        
        def pick_color():
            # Para RGBA, usar aproximación
            if 'rgba' in current_color:
                initial_color = "#6dd3ff"  # Fallback a azul
            else:
                initial_color = current_color
            
            color = colorchooser.askcolor(color=initial_color)
            if color[1]:  # Si el usuario seleccionó un color
                color_entries[var_name] = color[1]
                color_label.config(text=color[1])
        
        color_label = tk.Label(frame, text=current_color, width=10)
        color_label.pack(side=tk.LEFT)
        
        tk.Button(frame, text="Cambiar", command=pick_color).pack(side=tk.LEFT, padx=5)
        color_entries[var_name] = current_color
    
    for var_name, color_val in colors.items():
        create_color_button(var_name, color_val)
    
    def save_colors():
        # Reemplazar colores en el CSS
        updated_css = css_content
        
        for var_name, new_color in color_entries.items():
            if new_color != colors.get(var_name):
                old_pattern = f"--{var_name}:\\s*{re.escape(colors[var_name])}"
                updated_css = re.sub(old_pattern, f"--{var_name}: {new_color}", updated_css)
        
        # Guardar cambios
        with open(CSS_FILE, "w", encoding="utf-8") as f:
            f.write(updated_css)
        
        messagebox.showinfo("✅ Éxito", "Paleta de colores actualizada.\n\nRecarga el navegador para ver los cambios.")
        root.destroy()
    
    tk.Button(root, text="Guardar Cambios", command=save_colors, bg="#6dd3ff", fg="black", font=("Arial", 12, "bold")).pack(pady=20)
    tk.Button(root, text="Cancelar", command=root.destroy).pack(pady=5)
    
    root.mainloop()

# --- MAIN APPLICATION ---

def main():
    """Main application window."""
    root = tk.Tk()
    root.title("PORTFOLIO MANAGER v2 🛠️")
    root.geometry("400x500")
    
    tk.Label(root, text="PORTFOLIO MANAGER v2 🛠️", font=("Arial", 20, "bold")).pack(pady=20)
    
    def btn_projects():
        soup = load_soup()
        if soup:
            manage_projects(soup)
    
    def btn_general():
        soup = load_soup()
        if soup:
            manage_general(soup)
    
    def btn_skills():
        soup = load_soup()
        if soup:
            manage_skills(soup)
    
    def btn_contact():
        soup = load_soup()
        if soup:
            manage_contact(soup)
    
    def btn_colors():
        manage_colors()
    
    tk.Button(root, text="Gestionar Proyectos", width=30, height=2, command=btn_projects).pack(pady=10)
    tk.Button(root, text="Editar Textos Generales", width=30, height=2, command=btn_general).pack(pady=10)
    tk.Button(root, text="Gestionar Skills", width=30, height=2, command=btn_skills).pack(pady=10)
    tk.Button(root, text="Gestionar Contacto", width=30, height=2, command=btn_contact).pack(pady=10)
    tk.Button(root, text="Gestionar Colores 🎨", width=30, height=2, command=btn_colors, bg="#6dd3ff", fg="black", font=("Arial", 10, "bold")).pack(pady=10)
    tk.Button(root, text="Salir", width=15, height=1, command=root.quit).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()