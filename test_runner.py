import sys
import os

# Log all output
log_file = os.path.join(os.path.dirname(__file__), "error.log")

try:
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("Iniciando test...\n")
        f.flush()
        
        # Test 1: Import BeautifulSoup
        f.write("Test 1: Importar BeautifulSoup\n")
        from bs4 import BeautifulSoup
        f.write("✓ BeautifulSoup OK\n")
        f.flush()
        
        # Test 2: Import PySimpleGUI
        f.write("Test 2: Importar PySimpleGUI\n")
        import PySimpleGUI as sg
        f.write("✓ PySimpleGUI OK\n")
        f.flush()
        
        # Test 3: Call main
        f.write("Test 3: Importar portfolio_manager\n")
        import portfolio_manager
        f.write("✓ portfolio_manager OK\n")
        f.flush()
        
        f.write("Test 4: Llamar main()\n")
        portfolio_manager.main()
        f.write("✓ main() ejecutado\n")
        
except Exception as e:
    with open(log_file, "a", encoding="utf-8") as f:
        import traceback
        f.write(f"❌ ERROR: {e}\n")
        f.write(traceback.format_exc())
