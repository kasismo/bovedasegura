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
if 'logs_backend' not in st.session_state: 
    st.session_state['logs_backend'] = []

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
# --- PANTALLA 2: CIBERSEGURIDAD ---
# ==========================================
elif pantalla_actual == "🛡️ Clínica de Ciberseguridad":
    st.title("🛡️ Clínica de Ciberseguridad B2B")
    st.markdown("### Prevención de Fuerza Bruta y Análisis Bcrypt")

    st.info("**ℹ️ ARQUITECTURA DE DEFENSA EN DOS CAPAS:**\n1. **Perímetro (Frontend):** Rate Limiting corta los ataques de fuerza bruta al 5to intento fallido.\n2. **Núcleo (Backend):** Si un atacante roba la base de datos, el costo computacional de Bcrypt satura su CPU antes de que pueda descifrar los hashes.")
    st.divider()

    col_izq, espaciador, col_der = st.columns([1, 0.1, 1.5])

    # --- FRONTEND (LOGIN) ---
    with col_izq:
        st.subheader("🖥️ Frontend (Login)")
        with st.container(border=True):
            st.markdown("Intenta ingresar con credenciales incorrectas para disparar el escudo perimetral.")
            
            email_input = st.text_input("Correo Electrónico", value="gerente@industriasfaku.com")
            pass_input = st.text_input("Contraseña", type="password")
            
            c_btn1, c_btn2 = st.columns([1, 1])
            btn_login = c_btn1.button("ACCEDER", type="primary", use_container_width=True)
            btn_bot = c_btn2.button("🤖 Simular Bot (x5)", use_container_width=True)
            
            st.caption("*(Tip: La contraseña real es `admin123`)*")

            if btn_login or btn_bot:
                intentos_a_procesar = 5 if btn_bot else 1
                clave_a_probar = "bot_password" if btn_bot else pass_input
                
                usuario = st.session_state['db_usuarios'].get(email_input)
                
                if not usuario:
                    st.error("Usuario no encontrado.")
                    agregar_log(f"⚠️ Fallo: Correo inexistente ({email_input})")
                else:
                    for _ in range(intentos_a_procesar):
                        ahora = datetime.now()
                        
                        if usuario['bloqueado_hasta'] and ahora < usuario['bloqueado_hasta']:
                            st.error(f"❌ Cuenta bloqueada por seguridad. Vuelva a intentar en 4 horas.")
                            agregar_log(f"🛑 RECHAZADO: Cuenta {email_input} bloqueada. CPU salvada.")
                            break
                        else:
                            agregar_log(f"🔍 Evaluando credenciales para {email_input}...")
                            start_time = time.time()
                            es_valido = bcrypt.checkpw(clave_a_probar.encode('utf-8'), usuario['hash'])
                            tiempo_ms = (time.time() - start_time) * 1000
                            
                            if es_valido:
                                st.success("✅ ¡Acceso Concedido!")
                                usuario['intentos_fallidos'] = 0
                                agregar_log(f"✅ ÉXITO: Sesión iniciada. Costo CPU: {tiempo_ms:.2f} ms")
                                break
                            else:
                                if not btn_bot: st.error("❌ Contraseña incorrecta.")
                                usuario['intentos_fallidos'] += 1
                                agregar_log(f"❌ ERROR: Intento {usuario['intentos_fallidos']}/5. Costo CPU: {tiempo_ms:.2f} ms")
                                
                                if usuario['intentos_fallidos'] >= 5:
                                    usuario['bloqueado_hasta'] = ahora + timedelta(hours=4)
                                    agregar_log(f"🚨 ALERTA: Límite superado. Cuenta bloqueada por 4hs.")
                                    if btn_bot: st.error("❌ Cuenta bloqueada por seguridad. Vuelva a intentar en 4 horas.")

    # --- BACKEND (CONSOLA) ---
    with col_der:
        modo_vista = st.radio("📡 Selector de Vista Backend:", ["Console Logs (Trafico Vivo)", "Simulador de Ataque (Base de Datos Robada)"], horizontal=True)
        st.write("")
        
        if modo_vista == "Console Logs (Trafico Vivo)":
            with st.container(border=True):
                st.markdown("**Terminal de Monitoreo & Estado de DB**")
                datos_usuario = st.session_state['db_usuarios'].get("gerente@industriasfaku.com")
                estado_bloqueo = "ACTIVA" if not datos_usuario['bloqueado_hasta'] or datetime.now() > datos_usuario['bloqueado_hasta'] else "BLOQUEADA (4hs)"
                
                st.code(f"[DATABASE STATUS]\nUsuario: gerente@industriasfaku.com\nIntentos Fallidos: {datos_usuario['intentos_fallidos']} / 5\nEstado: {estado_bloqueo}", language="bash")
                
                log_text = "\n".join(st.session_state['logs_backend'])
                st.code(log_text if log_text else "Esperando tráfico entrante en el puerto 443...", language="log")
                
            if st.button("🔄 Purgar Logs y Desbloquear Cuenta"):
                st.session_state['db_usuarios']["gerente@industriasfaku.com"].update({'intentos_fallidos': 0, 'bloqueado_hasta': None})
                st.session_state['logs_backend'] = []
                st.rerun()

        elif modo_vista == "Simulador de Ataque (Base de Datos Robada)":
            with st.container(border=True):
                st.markdown("**⚠️ Entorno de Estrés Criptográfico**")
                st.write("¿Qué pasa si un atacante evade el login y descarga la base de datos SQL completa? Intentará inyectar un diccionario
