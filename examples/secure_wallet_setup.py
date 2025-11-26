import getpass
from blurtpy import Blurt
from blurtpy.wallet import Wallet
from blurtpy.exceptions import WalletExists

def setup_wallet():
    """
    Script interactivo para configurar un wallet seguro y añadir claves.
    """
    print("=== Configuración de Wallet Seguro de Blurtpy ===")
    print("Este script creará un archivo de base de datos local cifrado para guardar tus claves.")
    
    b = Blurt()
    
    # 1. Crear Wallet si no existe
    if b.wallet.created():
        print("\n¡Ya existe un wallet creado!")
        print("Si quieres borrarlo y empezar de cero, borra el archivo 'blurtpy.sqlite' o usa b.wallet.wipe(True)")
    else:
        print("\nVamos a crear un nuevo wallet.")
        password = getpass.getpass("Elige una contraseña maestra para el wallet: ")
        confirm = getpass.getpass("Confirma la contraseña: ")
        
        if password != confirm:
            print("Error: Las contraseñas no coinciden.")
            return
            
        try:
            b.wallet.create(password)
            print("Wallet creado exitosamente.")
        except WalletExists:
            print("El wallet ya existía.")

    # 2. Desbloquear Wallet
    if b.wallet.locked():
        password = getpass.getpass("\nIntroduce la contraseña del wallet para desbloquearlo: ")
        try:
            b.wallet.unlock(password)
            print("Wallet desbloqueado.")
        except Exception as e:
            print(f"Error al desbloquear: {e}")
            return

    # 3. Añadir Claves
    while True:
        print("\n--- Gestión de Claves ---")
        print("1. Añadir una clave privada (WIF)")
        print("2. Listar claves públicas guardadas")
        print("3. Salir")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            wif = getpass.getpass("Introduce la clave privada (WIF) (comienza por 5...): ")
            try:
                b.wallet.addPrivateKey(wif)
                print("¡Clave añadida correctamente!")
                
                # Intentar identificar a qué cuenta pertenece
                pub = b.wallet.publickey_from_wif(wif)
                account = b.wallet.getAccountFromPublicKey(pub)
                if account:
                    print(f"Esta clave pertenece a la cuenta: {account}")
                else:
                    print("No se pudo identificar la cuenta asociada (¿estás conectado a internet?)")
                    
            except Exception as e:
                print(f"Error al añadir clave: {e}")
                
        elif opcion == "2":
            keys = b.wallet.getPublicKeys()
            print(f"\nHay {len(keys)} claves guardadas:")
            for k in keys:
                print(f"- {k}")
                
        elif opcion == "3":
            break

if __name__ == "__main__":
    setup_wallet()
