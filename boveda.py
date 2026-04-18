import streamlit as st
import math
import time
import random
import string
import hashlib
import bcrypt # NUEVA LIBRERÍA REAL

st.set_page_config(page_title="La Bóveda - Criptografía", page_icon="🔐", layout="wide")
st.title("🔐 La Bóveda: Simulador de Entropía y Hashing")
st.markdown("Auditoría de seguridad en tiempo real. Descubre cómo se protegen los datos a nivel de servidor.")
st.divider()

# --- FUNCIONES MATEMÁTICAS (LA CIENCIA) ---
def calcular_espacio_claves(password):
    """Calcula la Entropía: El valor de K (Keyspace) basado en los caracteres usados."""
    k = 0
    if any(c.islower() for c in password): k += 26
    if any(c.isupper() for c in password): k += 26
    if any(c.isdigit() for c in password): k += 10
    if any(c in string.punctuation for c in password): k += 32
    return k if k > 0 else 1

def formatear_tiempo(segundos):
    if segundos < 1: return "Milisegundos (Instantáneo)"
    if segundos < 60: return f"{int(segundos)} segundos"
    if segundos < 3600: return f"{int(segundos/60)} minutos"
    if segundos < 86400: return f"{int(segundos/3600)} horas"
    if segundos < 31536000: return f"{int(segundos/86400)} días"
    años = segundos / 31536000
    if años > 1000: return f"+1,000 años (Inhackeable)"
    return f"{int(años):,} años"

# --- NUEVO: FUNCIÓN CRIPTOGRÁFICA REAL ---
def generar_hash_real(password_plana, algoritmo):
    """Genera el hash utilizando las librerías matemáticas reales de Python."""
    password_bytes = password_plana.encode('utf-8')
    
    if "MD5" in algoritmo:
        return hashlib.md5(password_bytes).hexdigest()
    else:
        # Bcrypt REAL: Generamos un Salt aleatorio y hasheamos con un "Work Factor" de 12
        salt = bcrypt.gensalt(rounds=12)
        hash_seguro = bcrypt.hashpw(password_bytes, salt)
        # Decodificamos a string solo para poder mostrarlo en la pantalla
        return hash_seguro.decode('utf-8')

# --- PANEL DE CONTROL ---
st.sidebar.header("🎯 Parámetros del Ataque")
password_objetivo = st.sidebar.text_input("Ingresa una contraseña de prueba:", type="password", value="Admin123")
algoritmo = st.sidebar.selectbox("Motor de Hashing:", ["MD5 (Obsoleto/Rápido)", "Bcrypt (Estándar/Lento)"])
iniciar_ataque = st.sidebar.button("Simular Ataque de Fuerza Bruta", type="primary")

# Tasas de Hash realistas para una GPU de gama alta (ej. RTX 4090)
velocidad_hash = 100000000000 if "MD5" in algoritmo else 100000 

if password_objetivo:
    # 1. LA CIENCIA EN TIEMPO REAL
    L = len(password_objetivo)
    K = calcular_espacio_claves(password_objetivo)
    combinaciones = K ** L
    tiempo_estimado_seg = combinaciones / velocidad_hash
    
    # Obtenemos el Hash verdadero llamando a nuestra función
    hash_real_bd = generar_hash_real(password_objetivo, algoritmo)
    
    col_show, col_ciencia = st.columns(2)
    
    with col_ciencia:
        st.subheader("🧮 Matemáticas del Servidor")
        
        m1, m2 = st.columns(2)
        m1.metric("Longitud (L)", f"{L}", help="Cantidad de caracteres en la contraseña.")
        m2.metric("Alfabeto (K)", f"{K}", help="26=Minúsculas, 52=Mayús+Minús, 62=+Números, 94=+Símbolos")
        
        st.metric("Combinaciones Totales (K^L)", f"{combinaciones:,}", help="Es el número total de intentos que el hacker tendría que hacer en el peor de los casos.")
        st.metric("Poder del Hacker (Tasa de Hash)", f"{velocidad_hash:,} H/s", help="Cuántas contraseñas por segundo puede probar una tarjeta gráfica moderna.")
        
        st.info(f"⏳ **Tiempo Teórico de Ruptura:** {formatear_tiempo(tiempo_estimado_seg)}")

    with col_show:
        st.subheader("💻 Terminal del Atacante")
        terminal_visual = st.empty() 
        
        st.caption(f"Registro en la Base de Datos:\n`{hash_real_bd}`")

        if iniciar_ataque:
            # IMPORTANTE: Simulamos visualmente el ataque porque hacer un bucle for REAL 
            # probando Bcrypt congelaría el servidor de Streamlit (¡lo que prueba su efectividad!)
            ciclos_animacion = 20 if tiempo_estimado_seg > 2 else int(tiempo_estimado_seg * 10)
            
            for _ in range(max(5, ciclos_animacion)): 
                intento_falso = ''.join(random.choices(string.ascii_letters + string.digits, k=L))
                hash_falso = hashlib.md5(intento_falso.encode()).hexdigest()[:20]
                terminal_visual.code(f"Atacando... Probando: {intento_falso}\nGenerando Hash: {hash_falso}...", language="bash")
                time.sleep(0.05)
            
            if tiempo_estimado_seg < 3:
                terminal_visual.error(f"❌ ¡BÓVEDA VULNERADA!\nContraseña descubierta: {password_objetivo}\nTiempo real: {formatear_tiempo(tiempo_estimado_seg)}")
            else:
                terminal_visual.success(f"✅ DEFENSA EXITOSA.\nEl ataque por fuerza bruta es matemáticamente inviable.\nTomaría {formatear_tiempo(tiempo_estimado_seg)}.")
        else:
            terminal_visual.code("Esperando orden de ejecución...\nSistema en reposo.", language="bash")