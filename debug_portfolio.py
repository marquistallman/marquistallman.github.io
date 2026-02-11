#!/usr/bin/env python3
import traceback
import sys

try:
    print("Iniciando Portfolio Manager...")
    sys.stdout.flush()
    
    import portfolio_manager
    print("✅ Módulo importado correctamente")
    sys.stdout.flush()
    
    print("Llamando a main()...")
    sys.stdout.flush()
    portfolio_manager.main()
    
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}")
    print(f"Mensaje: {e}")
    traceback.print_exc()
    sys.stdout.flush()
