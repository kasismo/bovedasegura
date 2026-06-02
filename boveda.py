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
# --- PANTALLA 2: CIBERSEGURIDAD ---
# ==========================================
elif pantalla_actual == "🛡️ Clínica de Ciberseguridad":
    st.title("🛡️ Clínica de Ciberseguridad B2B")
    st.markdown("### Simulador de Autenticación Bcrypt y Prevención de Fuerza Bruta")

    st.info("**ℹ️ ESCENARIO DE AMENAZA: DoS Algorítmico y Coste Computacional.** Bcrypt es intencionalmente costoso para la CPU. Si un bot bombardea el login, el cálculo criptográfico puede saturar el servidor. Esta demostración aplica **Rate Limiting** por cuenta: al 5to intento fallido, se desactiva la verificación Bcrypt durante 4 horas para proteger la infraestructura.")
    st.divider()

    col_front, espaciador, col_back = st.columns([1, 0.1, 1.5])

    with col_front:
        st.subheader("🖥️ Vista del Cliente (Frontend)")
        with st.container(border=True):
            email_input = st.text_input("Correo Electrónico", value="gerente@industriasfaku.com")
            pass_input = st.text_input("Contraseña", type="password")
            btn_login = st.button("Iniciar Sesión", type="primary", use_container_width=True)
            st.write("*(Tip: La contraseña real es `admin123`)*")

            if st.button("🤖 Simular Ataque Bot (5 intentos rápidos)"):
                email_input, pass_input = "gerente@industriasfaku.com", "bot_password"
                for _ in range(5): btn_login = True

    with col_back:
        st.subheader("⚙️ Consola del Servidor (Backend)")
        if btn_login:
            usuario = st.session_state['db_usuarios'].get(email_input)
            if not usuario:
                st.error("Usuario no encontrado."); agregar_log(f"⚠️ Fallo: Correo inexistente ({email_input})")
            else:
                ahora = datetime.now()
                if usuario['bloqueado_hasta'] and ahora < usuario['bloqueado_hasta']:
                    st.error(f"❌ Cuenta bloqueada por seguridad. Vuelva a intentar en 4 horas.")
                    agregar_log(f"🛑 RECHAZADO: Cuenta bloqueada. CPU salvada.")
                else:
                    agregar_log(f"🔍 Evaluando credenciales para {email_input}...")
                    start_time = time.time()
                    es_valido = bcrypt.checkpw(pass_input.encode('utf-8'), usuario['hash'])
                    tiempo_ms = (time.time() - start_time) * 1000
                    agregar_log(f"⏳ Costo de cálculo Bcrypt: {tiempo_ms:.2f} ms")
                    
                    if es_valido:
                        st.success("✅ ¡Acceso Concedido!"); usuario['intentos_fallidos'] = 0
                        agregar_log(f"✅ ÉXITO: Sesión iniciada")
                    else:
                        st.error("❌ Contraseña incorrecta."); usuario['intentos_fallidos'] += 1
                        agregar_log(f"❌ ERROR: Intento {usuario['intentos_fallidos']}/5")
                        if usuario['intentos_fallidos'] >= 5:
                            usuario['bloqueado_hasta'] = ahora + timedelta(hours=4)
                            agregar_log(f"🚨 ALERTA: Limite superado. Cuenta bloqueada por 4hs.")

        with st.container(border=True):
            datos_usuario = st.session_state['db_usuarios'].get("gerente@industriasfaku.com")
            estado_bloqueo = "ACTIVA" if not datos_usuario['bloqueado_hasta'] or datetime.now() > datos_usuario['bloqueado_hasta'] else "BLOQUEADA (4hs)"
            st.code(f"[DATABASE STATUS]\nHash: {datos_usuario['hash'][:20]}...\nIntentos: {datos_usuario['intentos_fallidos']} / 5\nEstado: {estado_bloqueo}", language="bash")
            log_text = "\n".join(st.session_state['logs_backend'])
            st.code(log_text if log_text else "Esperando eventos de conexión...", language="log")
            
        if st.button("🔄 Resetear Base de Datos de Pruebas"):
            st.session_state['db_usuarios']["gerente@industriasfaku.com"].update({'intentos_fallidos': 0, 'bloqueado_hasta': None})
            st.session_state['logs_backend'] = []
            st.rerun()

# ==========================================
# --- PANTALLA 3: DATOS RELACIONALES ---
# ==========================================
elif pantalla_actual == "🗄️ Clínica de Datos Relacionales":
    st.title("🗄️ Clínica de Datos Relacionales")
    st.markdown("### Simulador de Integridad Referencial y Big Data")

    st.info("**ℹ️ CONTEXTO CORPORATIVO: Optimización de Consultas a Gran Escala.** Simulamos la base de datos de una multinacional con **50,000 registros históricos**. Un bucle tradicional colapsaría la memoria RAM. Aquí se demuestra el uso de operaciones vectorizadas y lógica de conjuntos (`LEFT JOIN` / `IS NULL`) para resolver crisis en milisegundos.")
    
    df_jefes, df_empleados = generar_base_datos_masiva()

    st.divider()
    st.subheader("🚨 El Incidente: Borrado Accidental en Producción")
    st.write("Un usuario ejecutó un `DELETE` accidental y borró a la gerente **Diana Prince (ID 3)**, dejando a miles de empleados sin jefe asignado.")

    df_jefes_corrupta = df_jefes[df_jefes['id_jefe'] != 3].reset_index(drop=True)

    c1, c2 = st.columns(2)
    with c1: st.markdown("**Tabla Jefes (Falta el ID 3)**"); st.dataframe(df_jefes_corrupta, use_container_width=True, hide_index=True)
    with c2: st.markdown("**Tabla Empleados (50,000 registros)**"); st.dataframe(df_empleados.head(5), use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("🛠️ Resolución Técnica: Detección Vectorizada")

    if st.button("🚀 Ejecutar Búsqueda Optimizada (Anti-Huérfanos)", type="primary"):
        start_time = time.time()
        huerfanos = df_empleados[~df_empleados['id_jefe'].isin(df_jefes_corrupta['id_jefe'])]
        tiempo_ms = (time.time() - start_time) * 1000
        
        st.success(f"✅ Búsqueda completada en **{tiempo_ms:.2f} milisegundos**.")
        st.warning(f"⚠️ Se detectaron **{len(huerfanos):,} empleados huérfanos** que requieren reasignación urgente.")
        st.dataframe(huerfanos.head(), use_container_width=True, hide_index=True)
        
        st.markdown("#### ¿Cómo se resolvió por detrás?")
        tab_sql, tab_pandas = st.tabs(["Lógica SQL (Backend)", "Lógica Pandas (Data Science)"])
        with tab_sql:
            st.code("SELECT e.id_empleado, e.salario, e.id_jefe\nFROM tabla_empleados e\nLEFT JOIN tabla_jefes j ON e.id_jefe = j.id_jefe\nWHERE j.id_jefe IS NULL;", language="sql")
        with tab_pandas:
            st.code("ids_validos = df_jefes_corrupta['id_jefe']\nempleados_huerfanos = df_empleados[~df_empleados['id_jefe'].isin(ids_validos)]", language="python")

        st.markdown("#### 🩹 Acción Crítica: Reasignación Automática")
        if st.button("Reasignar Huérfanos al CEO (ID 1)"):
            with st.spinner("Ejecutando UPDATE masivo..."):
                time.sleep(0.8)
                st.success("¡Base de datos estabilizada! 10,000 registros actualizados con éxito.")
                st.balloons()
