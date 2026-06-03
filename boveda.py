import streamlit as st
import pandas as pd
import numpy as np
import time
import bcrypt
from datetime import datetime, timedelta

# ==========================================
# --- CONFIGURACIÓN Y ESTADOS GLOBALES ---
# ==========================================
st.set_page_config(page_title="Sandbox Técnico | Facundo Eliggi", page_icon="👨‍💻", layout="wide")

# Estados para la Clínica de Ciberseguridad
if 'db_usuarios' not in st.session_state:
    salt = bcrypt.gensalt(rounds=12) 
    hash_guardado = bcrypt.hashpw(b"admin123", salt)
    st.session_state['db_usuarios'] = {
        "gerente@industriasfaku.com": {"hash": hash_guardado, "intentos_fallidos": 0, "bloqueado_hasta": None}
    }
if 'logs_backend' not in st.session_state: st.session_state['logs_backend'] = []

def agregar_log(mensaje):
    hora = datetime.now().strftime("%H:%M:%S")
    st.session_state['logs_backend'].insert(0, f"[{hora}] {mensaje}")

# Función pesada cacheada para la Clínica de Datos
@st.cache_data
def generar_base_datos_masiva():
    jefes = pd.DataFrame({
        'id_jefe': [1, 2, 3, 4, 5],
        'nombre_jefe': ['Bruce Wayne (CEO)', 'Clark Kent', 'Diana Prince', 'Barry Allen', 'Arthur Curry'],
        'region': ['Global', 'Norte', 'Sur', 'Este', 'Oeste']
    })
    np.random.seed(42) 
    empleados = pd.DataFrame({
        'id_empleado': range(1000, 51000),
        'salario': np.random.randint(500, 5000, size=50000),
        'id_jefe': np.random.choice([1, 2, 3, 4, 5], size=50000) 
    })
    return jefes, empleados

# ==========================================
# --- SIDEBAR Y NAVEGACIÓN ---
# ==========================================
st.sidebar.title("👨‍💻 Sandbox Técnico")
st.sidebar.caption("Portafolio de Arquitectura Backend - Facundo Eliggi")
st.sidebar.divider()

pantalla_actual = st.sidebar.radio(
    "Módulos de Demostración",
    ["🏠 Inicio y Contexto", "🛡️ Clínica de Ciberseguridad", "🗄️ Clínica de Datos Relacionales"]
)

st.sidebar.divider()
st.sidebar.info("Este entorno está diseñado para demostrar habilidades en optimización de algoritmos, ciberseguridad y manejo de bases de datos masivas.")

# ==========================================
# --- PANTALLA 1: INICIO ---
# ==========================================
if pantalla_actual == "🏠 Inicio y Contexto":
    st.title("Bienvenido al Entorno de Pruebas")
    st.markdown("""
    ### ¿Qué es este Sandbox?
    A diferencia de un proyecto tradicional, este espacio es una **clínica a cielo abierto**. Aquí expongo la lógica de backend, los tiempos de ejecución y las consultas a bases de datos directamente en la interfaz.
    
    Selecciona un módulo en el menú lateral para evaluar demostraciones en vivo de:
    * **Defensa Algorítmica:** Rate limiting y mitigación de ataques DoS sobre protocolos de hashing (Bcrypt).
    * **Big Data y Álgebra Relacional:** Resolución de problemas de integridad referencial en datasets masivos (50k+ registros) con tiempos de ejecución submilisegundo usando Python (Pandas) y lógica SQL.
    """)
    st.success("👈 Selecciona una clínica en el menú lateral para comenzar.")

# ==========================================
# --- PANTALLA 2: CIBERSEGURIDAD (MODO WIREFRAME) ---
# ==========================================
elif pantalla_actual == "🛡️ Clínica de Ciberseguridad":
    st.title("🛡️ Clínica de Ciberseguridad B2B")
    st.markdown("### Prevención de Fuerza Bruta y Análisis Bcrypt")

    st.info("**ℹ️ ESCENARIO DE AMENAZA:** Bcrypt es intencionalmente costoso para la CPU. Esta demostración ilustra gráficamente por qué un ataque de diccionario fracasa contra un Work Factor alto, saturando los recursos del atacante antes que los del servidor.")
    st.divider()

    # Layout exacto de tu diagrama
    col_izq, espaciador, col_der = st.columns([1, 0.1, 1.5])

    # ------------------------------------------
    # CAJA IZQUIERDA: LOGIN TRADICIONAL
    # ------------------------------------------
    with col_izq:
        st.subheader("🖥️ Frontend (Login)")
        with st.container(border=True):
            st.markdown("<br>", unsafe_allow_html=True)
            email_input = st.text_input("Correo Electrónico", value="gerente@industriasfaku.com")
            pass_input = st.text_input("Contraseña", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            btn_login = st.button("ACCEDER", type="primary", use_container_width=True)
            
            if btn_login:
                st.toast("Intento de acceso enviado al backend...", icon="🚀")

    # ------------------------------------------
    # CAJA DERECHA: CONSOLA Y SIMULADOR
    # ------------------------------------------
    with col_der:
        # Switcher Back-Front
        modo_vista = st.radio("📡 Selector de Vista:", ["Console Logs (Trafico Vivo)", "Simulador de Ataque (Hacking)"], horizontal=True)
        
        st.write("") # Espaciador
        
        # VISTA 1: LOGS DE TRÁFICO VIVO
        if modo_vista == "Console Logs (Trafico Vivo)":
            with st.container(border=True):
                st.markdown("**Terminal de Monitoreo**")
                
                # Simulamos la lista de 10-15 que se desplaza hacia abajo
                logs_falsos = [
                    "[14:05:22] CONEXIÓN ENTRANTE - IP: 192.168.1.45",
                    "[14:05:23] AUTH REQUEST - gerente@industriasfaku.com",
                    "[14:05:23] BCRYPT VALIDATION... SUCCESS",
                    "[14:12:01] CONEXIÓN ENTRANTE - IP: 10.0.0.8",
                    "[14:12:05] AUTH REQUEST - admin@industriasfaku.com",
                    "[14:12:06] BCRYPT VALIDATION... FAILED (Bad Password)",
                    "[14:18:44] SYSTEM CHECK - OK"
                ]
                st.code("\n".join(logs_falsos), language="bash")
                st.caption("Los logs más antiguos se purgan automáticamente para ahorrar memoria RAM.")

        # VISTA 2: EL SIMULADOR DE ATAQUE
        elif modo_vista == "Simulador de Ataque (Hacking)":
            with st.container(border=True):
                st.markdown("**⚠️ Entorno de Estrés de Base de Datos**")
                st.write("Inyectar diccionario de 10,000 contraseñas contra los hashes de la base de datos.")
                
                if st.button("🔥 EJECUTAR ATAQUE DE DICCIONARIO (Fuerza Bruta)", type="primary"):
                    
                    # 1. Empiezan a verse las contraseñas largas
                    st.code("""
[TARGET ACQUIRED] Extrayendo Hashes de la DB...
Hash 1: $2b$12$N9qx1y7g9T8...
Hash 2: $2b$12$x8aL2pQ1m4...
Hash 3: $2b$12$L9zT5bY6n2...
[INJECTING PAYLOAD] Testeando diccionario rockyou.txt
                    """, language="bash")
                    
                    # 2. Barra de procesamiento intentando hackear la primera
                    progreso = st.progress(0)
                    estado_ataque = st.empty()
                    
                    # Simulamos que el atacante se queda trabado en la primera iteración
                    for i in range(1, 35):
                        progreso.progress(i)
                        estado_ataque.caption(f"Calculando combinaciones... {i}% (Hash 1 de 10,000)")
                        time.sleep(0.05)
                    
                    # 3. Fracaso y explicación matemática
                    progreso.empty()
                    estado_ataque.error("🛑 ATAQUE FALLIDO: Sobrecarga de CPU en el cliente (Timeout)")
                    
                    st.divider()
                    st.markdown("### 🧮 ¿Por qué fracasó el ataque?")
                    st.write("Bcrypt no es solo un hash, es una **función de derivación de claves con coste adaptable**.")
                    
                    # Usamos LaTeX puro para demostrar el peso matemático de la encriptación
                    st.latex(r"Coste Computacional = 2^{\text{Work Factor}}")
                    
                    st.write("El servidor está configurado con un `Work Factor = 12`. Esto obliga a la CPU del atacante a procesar el algoritmo EksBlowfish exactamente:")
                    
                    st.latex(r"2^{12} = 4096 \text{ iteraciones por cada intento}")
                    
                    st.write("Para probar un diccionario básico de **10 millones de contraseñas** contra un solo usuario, un clúster de servidores tardaría meses. La barrera criptográfica hace que el coste económico del ataque sea infinitamente superior al valor de los datos.")
