import logging
from blurtpy import Blurt
from blurtpy.account import Account
from blurtpy.graphenebase.account import PasswordKey

# Configuración
# REEMPLAZA ESTAS VARIABLES CON TUS DATOS
# ¡ATENCIÓN! Estas operaciones son críticas y requieren la CLAVE DE PROPIETARIO (OWNER KEY)
# o la CLAVE MAESTRA (MASTER PASSWORD) según la operación.
WIF_OWNER = "TU_CLAVE_PRIVADA_OWNER" 
USUARIO = "tu_usuario"
NODO = ["https://rpc.blurt.world"]

# Inicializar Blurt
b = Blurt(node=NODO, keys=[WIF_OWNER])

def establecer_cuenta_recuperacion(cuenta_recuperacion):
    """Establece la cuenta de recuperación (Recovery Account)."""
    print(f"Estableciendo cuenta de recuperación a: {cuenta_recuperacion}...")
    try:
        acc = Account(USUARIO, blockchain_instance=b)
        # Esta operación tarda 30 días en hacerse efectiva
        acc.change_recovery_account(cuenta_recuperacion)
        print("Solicitud de cambio de cuenta de recuperación enviada (tardará 30 días).")
    except Exception as e:
        print(f"Error al cambiar cuenta de recuperación: {e}")

def cambiar_claves(nueva_contrasena):
    """
    Cambia TODAS las claves de la cuenta (Owner, Active, Posting, Memo)
    derivándolas de una nueva contraseña maestra.
    
    ¡PELIGRO! Si pierdes la nueva contraseña, perderás acceso a tu cuenta para siempre.
    """
    print("¡ATENCIÓN! Estás a punto de cambiar todas las claves de tu cuenta.")
    confirmacion = input("¿Estás seguro? Escribe 'SI' para continuar: ")
    
    if confirmacion != "SI":
        print("Operación cancelada.")
        return

    print("Generando nuevas claves y actualizando cuenta...")
    try:
        acc = Account(USUARIO, blockchain_instance=b)
        # update_account_keys deriva las nuevas claves públicas de la contraseña
        # y envía la transacción de actualización.
        # NO guarda las claves privadas en tu wallet local automáticamente,
        # debes guardarlas tú o actualizar tu wallet.
        acc.update_account_keys(nueva_contrasena)
        
        print("¡Claves actualizadas con éxito!")
        print(f"Tu nueva contraseña maestra es: {nueva_contrasena}")
        print("Generando claves privadas para que las guardes (NO LAS PIERDAS):")
        
        for role in ['owner', 'active', 'posting', 'memo']:
            pk = PasswordKey(USUARIO, nueva_contrasena, role=role)
            priv_key = str(pk.get_private_key())
            pub_key = format(pk.get_public_key(), "BLURT")
            print(f"{role.upper()}:")
            print(f"  Public: {pub_key}")
            print(f"  Private: {priv_key}")
            
    except Exception as e:
        print(f"Error crítico al cambiar claves: {e}")

if __name__ == "__main__":
    # EJEMPLOS DE USO (Descomenta para probar)
    
    # 1. Establecer cuenta de recuperación
    # establecer_cuenta_recuperacion("tekraze")
    
    # 2. Cambiar claves (¡MUCHO CUIDADO!)
    # cambiar_claves("MiNuevaContrasenaSuperSegura123!")
