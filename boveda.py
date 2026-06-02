import streamlit as st
import pandas as pd
import numpy as np
import time

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Clínica de Datos | Facundo Eliggi", page_icon="🗄️", layout="wide")

# ==========================================
# GENERADOR DE "BIG DATA" FALSOS (MOCK DATA)
# ==========================================
@st.cache_data
def generar_base_datos_masiva():
    """Simula una base de datos de una multinacional con 50,000 registros"""
    # 1. Tabla de Gerentes (Intacta)
    jefes = pd.DataFrame({
        'id_jefe': [1, 2, 3, 4, 5],
        'nombre_jefe': ['Bruce Wayne (CEO)', 'Clark Kent', 'Diana Prince', 'Barry Allen', 'Arthur Curry'],
        'region': ['Global', 'Norte', 'Sur', 'Este', 'Oeste']
    })
    
    # 2. Tabla de Empleados (50,000 registros)
    np.random.seed(42) # Para que siempre genere los mismos datos
    empleados = pd.DataFrame({
        'id_empleado': range(1000, 51000),
        'salario': np.random.randint(500, 5000, size=50000),
        'id_jefe': np.random.choice([1, 2, 3, 4, 5], size=50000) # Asignados aleatoriamente
    })
    
    return jefes, empleados

# ==========================================
# INTERFAZ Y STORYTELLING TÉCNICO
# ==========================================
st.title("🗄️ Clínica de Datos Relacionales")
st.markdown("### Simulador de Integridad Referencial y Big Data")

# El panel de contexto para el reclutador
st.info("""
**ℹ️ CONTEXTO CORPORATIVO: Optimización de Consultas a Gran Escala** En una PYME, encontrar inconsistencias toma segundos revisando un Excel. En este escenario, 
simulamos la base de datos de una multinacional con **50,000 registros históricos**.  
Un bucle `for` tradicional colapsaría la memoria RAM y tardaría minutos. Aquí se demuestra el uso de 
operaciones vectorizadas y lógica de conjuntos (`LEFT JOIN` / `IS NULL`) para resolver crisis en milisegundos.
""")

# Cargamos los datos
df_jefes, df_empleados = generar_base_datos_masiva()

# ==========================================
# EL DESASTRE CORPORATIVO (Simulamos el error)
# ==========================================
st.divider()
st.subheader("🚨 El Incidente: Borrado Accidental en Producción")
st.write("Un usuario de RRHH ejecutó un `DELETE` accidental y borró a la gerente **Diana Prince (ID 3)** de la tabla de Jefes, pero olvidó reasignar a su equipo.")

# Simulamos que la base de datos de jefes ya no tiene al ID 3
df_jefes_corrupta = df_jefes[df_jefes['id_jefe'] != 3].reset_index(drop=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("**Tabla Jefes (Actualizada - Falta el ID 3)**")
    st.dataframe(df_jefes_corrupta, use_container_width=True, hide_index=True)
with c2:
    st.markdown("**Tabla Empleados (50,000 registros - Muestra de 5)**")
    st.dataframe(df_empleados.head(5), use_container_width=True, hide_index=True)

# ==========================================
# LA SOLUCIÓN TÉCNICA (Tu momento de brillar)
# ==========================================
st.divider()
st.subheader("🛠️ Resolución Técnica: Detección Vectorizada")

if st.button("🚀 Ejecutar Búsqueda Optimizada (Anti-Huérfanos)", type="primary"):
    
    start_time = time.time()
    
    # --- LA LÓGICA DE BACKEND (PANDAS/SQL) ---
    # Buscamos qué empleados tienen un ID de jefe que ya no existe en la tabla de jefes
    huerfanos = df_empleados[~df_empleados['id_jefe'].isin(df_jefes_corrupta['id_jefe'])]
    
    end_time = time.time()
    tiempo_ms = (end_time - start_time) * 1000
    
    # --- RESULTADOS VISUALES ---
    st.success(f"✅ Búsqueda completada en **{tiempo_ms:.2f} milisegundos**.")
    
    st.warning(f"⚠️ Se detectaron **{len(huerfanos):,} empleados huérfanos** que requieren reasignación urgente.")
    st.dataframe(huerfanos.head(), use_container_width=True, hide_index=True)
    
    # --- MOSTRAR EL CÓDIGO AL RECLUTADOR ---
    st.markdown("#### ¿Cómo se resolvió por detrás?")
    st.write("En lugar de iterar fila por fila, el motor utiliza operaciones de álgebra relacional en memoria:")
    
    tab_sql, tab_pandas = st.tabs(["Lógica SQL (Backend)", "Lógica Pandas (Data Science)"])
    
    with tab_sql:
        st.code("""
        -- Equivalente en PostgreSQL para detectar integridad rota:
        SELECT e.id_empleado, e.salario, e.id_jefe
        FROM tabla_empleados e
        LEFT JOIN tabla_jefes j ON e.id_jefe = j.id_jefe
        WHERE j.id_jefe IS NULL;
        """, language="sql")
        
    with tab_pandas:
        st.code("""
        # Equivalente ejecutado en Python usando memoria vectorizada:
        ids_validos = df_jefes_corrupta['id_jefe']
        empleados_huerfanos = df_empleados[~df_empleados['id_jefe'].isin(ids_validos)]
        """, language="python")

    # --- REPARACIÓN FINAL ---
    st.markdown("#### 🩹 Acción Crítica: Reasignación Automática")
    if st.button("Reasignar Huérfanos al CEO (ID 1)"):
        with st.spinner("Ejecutando UPDATE masivo..."):
            time.sleep(0.8) # Pausa dramática para simular latencia de red
            df_reparado = df_empleados.copy()
            df_reparado.loc[~df_reparado['id_jefe'].isin(df_jefes_corrupta['id_jefe']), 'id_jefe'] = 1
            
            st.success("¡Base de datos estabilizada! 10,000 registros actualizados con éxito.")
            st.balloons()
