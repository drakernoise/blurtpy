#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba SEGURO para verificar compatibilidad de wallets
NO modifica la wallet real, solo hace pruebas de lectura
"""
import os
import sys
import shutil
import tempfile
import sqlite3
from pathlib import Path

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def find_wallet():
    """Encuentra la ubicación de la wallet de blurtpy"""
    from appdirs import user_data_dir
    wallet_dir = user_data_dir('blurtpy', 'blurtpy')
    wallet_file = os.path.join(wallet_dir, 'blurtpy.sqlite')
    return wallet_file if os.path.exists(wallet_file) else None

def analyze_wallet_structure(wallet_path):
    """Analiza la estructura de la wallet SIN modificarla"""
    print_header("ANÁLISIS DE ESTRUCTURA DE WALLET")
    
    if not os.path.exists(wallet_path):
        print_error(f"Wallet no encontrada: {wallet_path}")
        return None
    
    print_success(f"Wallet encontrada: {wallet_path}")
    print(f"   Tamaño: {os.path.getsize(wallet_path)} bytes")
    
    # Conectar en modo solo lectura
    conn = sqlite3.connect(f"file:{wallet_path}?mode=ro", uri=True)
    cursor = conn.cursor()
    
    # Ver tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n   Tablas encontradas: {len(tables)}")
    
    info = {}
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   - {table_name}: {count} registros")
        
        # Ver estructura de la tabla
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        info[table_name] = {
            'count': count,
            'columns': [col[1] for col in columns]
        }
    
    conn.close()
    return info

def check_encryption_method(wallet_path):
    """Detecta qué método de cifrado se está usando"""
    print_header("DETECCIÓN DE MÉTODO DE CIFRADO")
    
    conn = sqlite3.connect(f"file:{wallet_path}?mode=ro", uri=True)
    cursor = conn.cursor()
    
    # Buscar configuración de master password
    try:
        cursor.execute("SELECT key, value FROM config WHERE key='encrypted_master_password'")
        result = cursor.fetchone()
        
        if result:
            print_success("Master password cifrado encontrado")
            encrypted_value = result[1]
            
            # El formato es: checksum$encrypted_data
            if '$' in encrypted_value:
                checksum, encrypted = encrypted_value.split('$', 1)
                print(f"   Checksum: {checksum} (primeros 4 chars de SHA256)")
                print(f"   Datos cifrados (primeros 20 chars): {encrypted[:20]}...")
                print_warning("   Método actual: AES-256-CBC con clave derivada de SHA256")
                return 'sha256-aes'
            else:
                print_warning("   Formato desconocido")
                return 'unknown'
        else:
            print_warning("No hay master password configurado (wallet vacía?)")
            return None
            
    except sqlite3.Error as e:
        print_error(f"Error al leer configuración: {e}")
        return None
    finally:
        conn.close()

def test_decrypt_with_backup(wallet_path):
    """Prueba de descifrado con backup temporal"""
    print_header("PRUEBA DE COMPATIBILIDAD (MODO SEGURO)")
    
    # Crear copia temporal
    temp_dir = tempfile.mkdtemp(prefix='blurtpy_test_')
    temp_wallet = os.path.join(temp_dir, 'test_wallet.sqlite')
    
    try:
        shutil.copy2(wallet_path, temp_wallet)
        print_success(f"Copia de seguridad creada en: {temp_dir}")
        
        # Intentar abrir con blurtpy
        print("\n   Intentando abrir wallet con blurtpy...")
        
        try:
            from blurtpy import Blurt
            from blurtstorage import SqliteConfigurationStore
            
            # Crear instancia con la copia temporal
            config = SqliteConfigurationStore(data_dir=temp_dir, appname='test_wallet')
            
            # Verificar si tiene configuración
            if 'encrypted_master_password' in config:
                print_success("   Wallet puede abrirse correctamente")
                print_warning("   Requiere password para desbloquear")
                return True
            else:
                print_warning("   Wallet está vacía o no inicializada")
                return True
                
        except Exception as e:
            print_error(f"   Error al abrir wallet: {e}")
            return False
            
    finally:
        # Limpiar
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"\n   Copia temporal eliminada")

def main():
    print_header("TEST DE COMPATIBILIDAD DE WALLET BLURTPY")
    print(f"Fecha: 2026-02-04")
    print(f"Propósito: Verificar impacto de cambios en cifrado")
    print(f"{YELLOW}MODO SEGURO: No modifica la wallet original{RESET}")
    
    # 1. Buscar wallet
    wallet_path = find_wallet()
    
    if not wallet_path:
        print_warning("\nNo se encontró wallet de blurtpy")
        print("   Esto significa que:")
        print("   - No hay usuarios con wallets existentes en este sistema")
        print("   - Es SEGURO cambiar el algoritmo de cifrado")
        return 0
    
    # 2. Analizar estructura
    info = analyze_wallet_structure(wallet_path)
    
    if not info:
        return 1
    
    # 3. Detectar método de cifrado
    encryption_method = check_encryption_method(wallet_path)
    
    # 4. Prueba de compatibilidad
    compatible = test_decrypt_with_backup(wallet_path)
    
    # Resumen final
    print_header("RESUMEN Y RECOMENDACIONES")
    
    if encryption_method == 'sha256-aes':
        print_warning("HALLAZGO:")
        print("   - La wallet usa cifrado SHA256+AES (método heredado de Beem)")
        print("   - CodeQL marca esto como inseguro para 2026")
        print("\nOPCIONES:")
        print("   A) Mantener compatibilidad: Solo agregar comentarios")
        print("   B) Migración suave: Crear nueva clase, mantener la antigua")
        print("   C) Romper compatibilidad: Cambiar a scrypt (usuarios pierden acceso)")
        print(f"\n{RED}RECOMENDACIÓN: Opción A o B para no afectar usuarios{RESET}")
        
    elif encryption_method is None:
        print_success("HALLAZGO:")
        print("   - Wallet sin master password configurado")
        print("   - Es SEGURO implementar nuevo cifrado")
        print(f"\n{GREEN}RECOMENDACIÓN: Implementar scrypt desde ahora{RESET}")
    
    print("\nPara más detalles, revisa el código en:")
    print("   - blurtgraphenebase/aes.py (línea 22)")
    print("   - blurtstorage/masterpassword.py (uso del cifrado)")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Prueba cancelada por usuario{RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{RED}Error inesperado: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
