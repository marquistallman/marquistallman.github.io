import os
import shutil
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Error: Necesitas instalar 'beautifulsoup4'. Ejecuta: pip install beautifulsoup4")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, "index.html")
IMG_FOLDER = os.path.join(BASE_DIR, "img")

def load_soup():
    if not os.path.exists(HTML_FILE):
        print(f"❌ No se encuentra {HTML_FILE}")
        return None
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def save_soup(soup):
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    print("💾 Cambios guardados exitosamente.")

def input_default(prompt, default):
    """Pide input al usuario mostrando el valor actual por defecto."""
    d_str = default if default else ""
    val = input(f"{prompt} [{d_str}]: ").strip()
    return val if val else d_str

def handle_image(img_path_input):
    src_path = img_path_input.strip('"').strip("'")
    if not src_path: return None

    if not os.path.exists(src_path):
        print(f"⚠️ Imagen no encontrada: {src_path}")
        return None

    filename = os.path.basename(src_path)
    dest_path = os.path.join(IMG_FOLDER, filename)

    if not os.path.exists(IMG_FOLDER): os.makedirs(IMG_FOLDER)

    try:
        shutil.copy(src_path, dest_path)
        print(f"✅ Imagen copiada: {filename}")
        return f"img/{filename}"
    except Exception as e:
        print(f"Error copiando: {e}")
        return None

# --- GESTIÓN DE PROYECTOS ---

def manage_projects(soup):
    while True:
        print("\n--- 📂 GESTIONAR PROYECTOS ---")
        container = soup.find(id="projects-list")
        if not container:
            print("❌ No se encontró el contenedor #projects-list en el HTML.")
            return

        projects = container.find_all("article", class_="card")
        for i, p in enumerate(projects):
            t = p.find("h4").get_text(strip=True) if p.find("h4") else "Sin título"
            print(f"{i+1}. {t}")
        
        print("\nA. Agregar Nuevo Proyecto")
        print("B. Volver al Menú Principal")
        
        sel = input("\nElige una opción o el número de proyecto a editar: ").strip().upper()
        if sel == 'B': return
        if sel == 'A':
            add_project(soup, container)
            continue
            
        try:
            idx = int(sel) - 1
            if 0 <= idx < len(projects):
                edit_project(soup, projects[idx])
            else:
                print("Número inválido.")
        except ValueError:
            pass

def add_project(soup, container):
    print("\n--- NUEVO PROYECTO ---")
    title = input("Título: ")
    desc = input("Descripción: ")
    tags = input("Tags (ej: Python, AI): ")
    img_path = input("Ruta imagen: ")
    repo = input("Link Repo: ")
    demo = input("Link Demo (Enter para omitir): ")
    
    img_src = handle_image(img_path) or "https://via.placeholder.com/300"
    
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

def edit_project(soup, project):
    print("\n--- EDITAR PROYECTO ---")
    print("1. Modificar datos")
    print("2. Borrar proyecto")
    print("3. Cancelar")
    op = input("Opción: ")
    
    if op == "2":
        if input("¿Seguro? (s/n): ").lower() == 's':
            project.decompose()
            save_soup(soup)
        return

    if op == "1":
        # Obtener valores actuales
        h4 = project.find("h4")
        curr_title = h4.get_text(strip=True) if h4 else ""
        
        p_desc = project.find("p") # Primer párrafo es descripción
        curr_desc = p_desc.get_text(strip=True) if p_desc else ""
        
        p_tags = project.find("p", class_="muted")
        curr_tags = p_tags.get_text(strip=True) if p_tags else ""
        
        img = project.find("img")
        curr_img = img['src'] if img else ""
        
        actions = project.find("div", class_="card-actions")
        links = actions.find_all("a") if actions else []
        curr_repo = links[0]['href'] if len(links) > 0 else ""
        curr_demo = links[1]['href'] if len(links) > 1 else ""

        # Pedir nuevos valores
        new_title = input_default("Título", curr_title)
        new_desc = input_default("Descripción", curr_desc)
        new_tags = input_default("Tags", curr_tags)
        
        print(f"Imagen actual: {curr_img}")
        new_img_path = input("Nueva imagen (Enter para mantener): ")
        
        new_repo = input_default("Link Repo", curr_repo)
        new_demo = input_default("Link Demo", curr_demo)
        
        # Aplicar cambios
        if h4: h4.string = new_title
        if p_desc: p_desc.string = new_desc
        if p_tags: p_tags.string = new_tags
        
        if new_img_path:
            processed = handle_image(new_img_path)
            if processed and img: img['src'] = processed
            
        # Reconstruir botones
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

# --- GESTIÓN GENERAL ---

def manage_general(soup):
    print("\n--- 📝 EDITAR TEXTOS GENERALES ---")
    
    # 1. Header
    h1 = soup.select_one(".brand h1")
    if h1: h1.string = input_default("Nombre (Header)", h1.get_text(strip=True))
    
    sub = soup.select_one(".brand .muted")
    if sub: sub.string = input_default("Subtítulo", sub.get_text(strip=True))
        
    # 2. Hero
    hero_h2 = soup.select_one(".hero h2")
    if hero_h2: hero_h2.string = input_default("Título Hero", hero_h2.get_text(strip=True))
    
    # 3. About
    about_p = soup.select_one(".about-card p")
    if about_p: about_p.string = input_default("Sobre mí (Texto)", about_p.get_text(strip=True))
        
    save_soup(soup)

def manage_skills(soup):
    while True:
        print("\n--- ⚡ SKILLS ---")
        container = soup.select_one(".chips")
        if not container: return
        
        chips = container.find_all("span", class_="chip")
        for i, c in enumerate(chips):
            print(f"{i+1}. {c.get_text(strip=True)}")
            
        print("\nA. Agregar Skill")
        print("B. Volver")
        
        sel = input("Opción: ").strip().upper()
        if sel == 'B': return
        if sel == 'A':
            name = input("Nombre Skill: ")
            desc = input("Descripción: ")
            img = input("Ruta imagen icono: ")
            processed_img = handle_image(img) or "https://via.placeholder.com/320x180"
            
            span = soup.new_tag("span", attrs={
                "class": "chip",
                "data-img": processed_img,
                "data-desc": desc,
                "title": name
            })
            span.string = name
            container.append(span)
            save_soup(soup)
            continue
            
        try:
            idx = int(sel) - 1
            if 0 <= idx < len(chips):
                c = chips[idx]
                print(f"\nEditando: {c.get_text(strip=True)}")
                if input("¿Borrar? (s/n): ").lower() == 's':
                    c.decompose()
                else:
                    new_name = input_default("Nombre", c.get_text(strip=True))
                    new_desc = input_default("Desc", c.get('data-desc', ''))
                    new_img = input("Nueva imagen (Enter omitir): ")
                    
                    c.string = new_name
                    c['title'] = new_name
                    c['data-desc'] = new_desc
                    if new_img:
                        p = handle_image(new_img)
                        if p: c['data-img'] = p
                save_soup(soup)
        except ValueError: pass

def manage_contact(soup):
    print("\n--- 📧 CONTACTO ---")
    cards = soup.select("#contact .contact-card")
    for i, c in enumerate(cards):
        print(f"{i+1}. {c.get_text(strip=True)} -> {c['href']}")
    
    sel = input("\nNúmero para editar (Enter volver): ")
    if not sel: return
    
    try:
        idx = int(sel) - 1
        if 0 <= idx < len(cards):
            c = cards[idx]
            c.string = input_default("Texto visible", c.get_text(strip=True))
            c['href'] = input_default("Enlace (mailto: o https://)", c['href'])
            save_soup(soup)
    except: pass

def main():
    while True:
        soup = load_soup()
        if not soup: break
        
        print("\n" + "="*30)
        print("   PORTFOLIO MANAGER v2 🛠️")
        print("="*30)
        print("1. Gestionar Proyectos (Agregar/Editar/Borrar)")
        print("2. Editar Textos (Nombre, Bio, Hero)")
        print("3. Gestionar Skills")
        print("4. Gestionar Contacto")
        print("5. Salir")
        
        op = input("\nOpción: ")
        
        if op == "1": manage_projects(soup)
        elif op == "2": manage_general(soup)
        elif op == "3": manage_skills(soup)
        elif op == "4": manage_contact(soup)
        elif op == "5": break
        else: print("Opción no válida")

if __name__ == "__main__":
    main()