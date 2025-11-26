import logging
import time
from blurtpy import Blurt
from blurtpy.account import Account
from blurtpy.amount import Amount

# Configuración
# REEMPLAZA ESTAS VARIABLES CON TUS DATOS
WIF_ACTIVE = "TU_CLAVE_PRIVADA_ACTIVA" # Necesaria para transferencias
USUARIO = "tu_usuario"
NODO = ["https://rpc.blurt.world"]

# Inicializar Blurt
b = Blurt(node=NODO, keys=[WIF_ACTIVE])

def power_up(cantidad, usuario_destino=None):
    """Convierte BLURT líquido a Blurt Power (Vesting)."""
    print(f"Haciendo Power Up de {cantidad} BLURT...")
    try:
        acc = Account(USUARIO, blockchain_instance=b)
        # Si usuario_destino es None, se hace power up a la propia cuenta
        acc.transfer_to_vesting(cantidad, to=usuario_destino)
        print("Power Up realizado con éxito.")
    except Exception as e:
        print(f"Error en Power Up: {e}")

def delegar_bp(cantidad_vests, usuario_destino):
    """Delega Blurt Power a otro usuario."""
    print(f"Delegando {cantidad_vests} VESTS a {usuario_destino}...")
    try:
        acc = Account(USUARIO, blockchain_instance=b)
        acc.delegate_vesting_shares(usuario_destino, cantidad_vests)
        print("Delegación realizada con éxito.")
    except Exception as e:
        print(f"Error en Delegación: {e}")

def transferencia_multiple(lista_destinatarios, cantidad, asset="BLURT", memo=""):
    """Envía la misma cantidad a múltiples usuarios."""
    print(f"Iniciando transferencia múltiple a {len(lista_destinatarios)} usuarios...")
    acc = Account(USUARIO, blockchain_instance=b)
    
    for destinatario in lista_destinatarios:
        try:
            print(f"Enviando {cantidad} {asset} a {destinatario}...")
            acc.transfer(destinatario, cantidad, asset, memo)
            print("Enviado.")
        except Exception as e:
            print(f"Error enviando a {destinatario}: {e}")

def transferencia_recurrente(destinatario, cantidad, asset="BLURT", memo="", repeticiones=3, intervalo_segundos=60):
    """Simula una transferencia recurrente (ejecutar script en segundo plano)."""
    print(f"Iniciando transferencia recurrente a {destinatario}: {repeticiones} veces cada {intervalo_segundos}s.")
    acc = Account(USUARIO, blockchain_instance=b)
    
    for i in range(repeticiones):
        try:
            print(f"Ejecución {i+1}/{repeticiones}...")
            acc.transfer(destinatario, cantidad, asset, memo)
            print("Transferencia realizada.")
        except Exception as e:
            print(f"Error en transferencia recurrente: {e}")
        
        if i < repeticiones - 1:
            print(f"Esperando {intervalo_segundos} segundos...")
            time.sleep(intervalo_segundos)

def transferir_a_savings(cantidad, asset="BLURT", memo="Ahorros"):
    """Transfiere fondos a la cuenta de ahorros (Savings)."""
    print(f"Transfiriendo {cantidad} {asset} a Savings...")
    try:
        acc = Account(USUARIO, blockchain_instance=b)
        acc.transfer_to_savings(cantidad, asset, memo)
        print("Transferencia a Savings exitosa.")
    except Exception as e:
        print(f"Error en transferencia a Savings: {e}")

if __name__ == "__main__":
    # EJEMPLOS DE USO (Descomenta para probar)
    
    # 1. Power Up (1 BLURT)
    # power_up(1)
    
    # 2. Delegar BP (1000 VESTS)
    # delegar_bp("1000 VESTS", "tekraze")
    
    # 3. Transferencia Múltiple
    # destinatarios = ["usuario1", "usuario2", "usuario3"]
    # transferencia_multiple(destinatarios, 0.1, "BLURT", "Regalo")
    
    # 4. Transferencia Recurrente (3 veces, cada 10 segundos)
    # transferencia_recurrente("draktest", 0.1, "BLURT", "Pago recurrente", repeticiones=3, intervalo_segundos=10)
    
    # 5. Ahorros
    # transferir_a_savings(1, "BLURT", "Guardando para el futuro")
