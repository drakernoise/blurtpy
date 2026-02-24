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
from blurtpy.amount import Amount, ExchangeRate
import json

def test_math_utility():
    node = "https://rpc.beblurt.com"
    print(f"\n--- DEBUG: Conectando a {node} ---")
    stm = Blurt(node)
    
    # 1. ¿Cómo SÍ sirve ExchangeRate? (Matemática local sin RPC)
    print("\n[DEBUG 1] Probando ExchangeRate como herramienta de cálculo local:")
    try:
        # Definir un precio manual: 1 VESTS cuesta 0.001 BLURT (simulado)
        print("Creando ExchangeRate manual: 0.001 BLURT/VESTS...")
        p = ExchangeRate(0.001, base="BLURT", quote="VESTS", blockchain_instance=stm)
        print(f"Objeto ExchangeRate manual: {p}")
        
        monto = Amount("1000.000000 VESTS", blockchain_instance=stm)
        print(f"Multiplicando {monto} * {p}...")
        convertido = monto * p
        print(f"RESULTADO Conversión: {convertido}")
        
        if convertido.symbol == "BLURT" and abs(convertido.amount - 1.0) < 0.0001:
            print("Cálculo matemático de ExchangeRate: OK")
        else:
            print(f"Cálculo matemático de ExchangeRate: Error inesperado (Símbolo: {convertido.symbol}, Cantidad: {convertido.amount})")
            
    except Exception as e:
        print(f"CRASH detectado en cálculo manual de ExchangeRate: {type(e).__name__}: {str(e)}")
        sys.exit(1)

    # 2. Probar división que resulta en ExchangeRate
    print("\n[DEBUG 2] Probando división de Amount que resulta en ExchangeRate:")
    try:
        a1 = Amount("1.000 BLURT", blockchain_instance=stm)
        a2 = Amount("1000.000000 VESTS", blockchain_instance=stm)
        rate = a1 / a2
        print(f"1.000 BLURT / 1000.000000 VESTS = {rate}")
        if isinstance(rate, ExchangeRate):
            print("División de Amount -> ExchangeRate: OK")
        else:
            print(f"Error: Resultado de división no es ExchangeRate, es {type(rate)}")
            sys.exit(1)
    except Exception as e:
        print(f"CRASH detectado en división: {type(e).__name__}: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_math_utility()
