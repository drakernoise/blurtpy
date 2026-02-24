import sys
import os
import logging

# Configurar logging para ver lo que pasa internamente
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("blurtpy")
logger.setLevel(logging.DEBUG)

# Add current directory to path to use local blurtpy
sys.path.append(os.getcwd())

from blurtpy.blurt import Blurt
from blurtpy.price import Price
from blurtpy.amount import Amount
import json

def test_price_utility():
    node = "https://rpc.drakernoise.com"
    print(f"\n--- DEBUG: Conectando a {node} con debug=True ---")
    # Activamos debug=True en la instancia de Blurt
    stm = Blurt(node, debug=True)
    
    # 1. Intentar obtener el historial de feeds (lo que usa Price)
    print("\n[DEBUG 1] Intentando ejecutar stm.get_feed_history(use_stored_data=False):")
    try:
        feed_history = stm.get_feed_history(use_stored_data=False)
        print(f"RESULTADO feed_history: {json.dumps(feed_history, indent=2) if feed_history else 'None'}")
    except Exception as e:
        print(f"CRASH detectado en get_feed_history: {type(e).__name__}: {str(e)}")

    # 2. Intentar obtener el precio mediano (usado para recompensas)
    print("\n[DEBUG 2] Intentando ejecutar stm.get_current_median_history(use_stored_data=False):")
    try:
        median_history = stm.get_current_median_history(use_stored_data=False)
        print(f"RESULTADO median_history: {json.dumps(median_history, indent=2) if median_history else 'None'}")
        if median_history:
            p = Price(median_history, blockchain_instance=stm)
            print(f"Objeto Price creado exitosamente: {p}")
        else:
            print("INFO: No hay datos para crear el objeto Price (se esperaba None en Blurt).")
    except Exception as e:
        print(f"CRASH detectado en get_current_median_history: {type(e).__name__}: {str(e)}")

    # 3. ¿Para qué SÍ sirve Price? (Matemática local sin RPC)
    print("\n[DEBUG 3] Probando Price como herramienta de cálculo local (con activos válidos):")
    try:
        # Definir un precio manual: 1 VESTS cuesta 0.001 BLURT (simulado)
        print("Creando Price manual: 0.001 BLURT/VESTS...")
        p = Price(0.001, base="BLURT", quote="VESTS", blockchain_instance=stm)
        print(f"Objeto Price manual: {p}")
        
        monto = Amount("1000.000000 VESTS", blockchain_instance=stm)
        print(f"Multiplicando {monto} * {p}...")
        convertido = monto * p
        print(f"RESULTADO Conversión: {convertido}")
        
        if convertido.symbol == "BLURT" and abs(convertido.amount - 1.0) < 0.0001:
            print("Cálculo matemático de Price: OK")
        else:
            print(f"Cálculo matemático de Price: Error inesperado (Símbolo: {convertido.symbol}, Cantidad: {convertido.amount})")
            
    except Exception as e:
        print(f"CRASH detectado en cálculo manual de Price: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    test_price_utility()
