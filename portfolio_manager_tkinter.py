import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup

# --- CONSTANTS AND SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, "index.html")
IMG_FOLDER = os.path.join(BASE_DIR, "img")

# --- CORE HELPER FUNCTIONS ---

def load_soup():
    """Loads and parses the index.html file."""
    if not os.path.exists(HTML_FILE):
        messagebox.showerror("Error", f"No se encuentra el archivo principal:\n{HTML_FILE}")
        return None
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def save_soup(soup):
    """Saves the BeautifulSoup object back to the HTML file."""
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

# --- MAIN APPLICATION ---
def main():
    """Main application window."""
    root = tk.Tk()
    root.title("PORTFOLIO MANAGER v2 🛠️")
    root.geometry("400x500")
    
    # Title
    title = tk.Label(root, text="PORTFOLIO MANAGER v2 🛠️", font=("Helvetica", 20))
    title.pack(pady=20)
    
    # Buttons
    btn_projects = tk.Button(root, text="Gestionar Proyectos", width=30, height=2,
                           command=lambda: messagebox.showinfo("Info", "Funcionalidad no implementada"))
    btn_projects.pack(pady=10)
    
    btn_general = tk.Button(root, text="Editar Textos Generales", width=30, height=2,
                          command=lambda: messagebox.showinfo("Info", "Funcionalidad no implementada"))
    btn_general.pack(pady=10)
    
    btn_skills = tk.Button(root, text="Gestionar Skills", width=30, height=2,
                         command=lambda: messagebox.showinfo("Info", "Funcionalidad no implementada"))
    btn_skills.pack(pady=10)
    
    btn_contact = tk.Button(root, text="Gestionar Contacto", width=30, height=2,
                          command=lambda: messagebox.showinfo("Info", "Funcionalidad no implementada"))
    btn_contact.pack(pady=10)
    
    btn_exit = tk.Button(root, text="Salir", width=15, height=1, command=root.quit)
    btn_exit.pack(pady=20)
    
    # Test that HTML file exists
    soup = load_soup()
    if soup:
        messagebox.showinfo("✅ Éxito", "Archivo HTML cargado correctamente")
    
    root.mainloop()

if __name__ == "__main__":
    main()
