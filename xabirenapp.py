import streamlit as st
import json
import random

# Configurar la página
st.set_page_config(
    page_title="Xabirenapp",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        padding: 12px;
        font-size: 16px;
        border-radius: 8px;
        border: 2px solid #3498db;
        background-color: #3498db;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        border-color: #2980b9;
    }
    .correct {
        background-color: #2ecc71;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .incorrect {
        background-color: #e74c3c;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .question-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .stats-box {
        background-color: #ecf0f1;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .header-title {
        color: #2c3e50;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar preguntas
@st.cache_data
def cargar_preguntas():
    with open('preguntas.json', 'r', encoding='utf-8') as f:
        datos = json.load(f)
    return datos['preguntas']

preguntas = cargar_preguntas()

# Inicializar sesión
if 'pregunta_actual' not in st.session_state:
    st.session_state.pregunta_actual = 0
    st.session_state.aciertos = 0
    st.session_state.errores = 0
    st.session_state.respuestas = []
    st.session_state.mostrar_resultado = False
    st.session_state.respuesta_seleccionada = None
    st.session_state.preguntas_orden = list(range(len(preguntas)))
    random.shuffle(st.session_state.preguntas_orden)

# Encabezado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="header-title">🎓 Xabirenapp</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #7f8c8d; font-size: 1.1em;">Examen Test Interactivo</p>', unsafe_allow_html=True)

# Barra lateral con estadísticas
with st.sidebar:
    st.markdown("### 📊 Estadísticas")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Aciertos", st.session_state.aciertos, delta=None)
    with col2:
        st.metric("❌ Errores", st.session_state.errores, delta=None)
    
    total_respondidas = st.session_state.aciertos + st.session_state.errores
    if total_respondidas > 0:
        porcentaje = (st.session_state.aciertos / total_respondidas) * 100
        st.metric("📈 Porcentaje", f"{porcentaje:.1f}%", delta=None)
    
    st.markdown("---")
    st.markdown(f"### Pregunta {st.session_state.pregunta_actual + 1} de {len(preguntas)}")
    
    # Barra de progreso
    progreso = (st.session_state.pregunta_actual) / len(preguntas)
    st.progress(progreso)
    
    st.markdown("---")
    
    if st.button("🔄 Reiniciar Examen", use_container_width=True):
        st.session_state.pregunta_actual = 0
        st.session_state.aciertos = 0
        st.session_state.errores = 0
        st.session_state.respuestas = []
        st.session_state.mostrar_resultado = False
        st.session_state.respuesta_seleccionada = None
        st.session_state.preguntas_orden = list(range(len(preguntas)))
        random.shuffle(st.session_state.preguntas_orden)
        st.rerun()

# Contenido principal
if st.session_state.pregunta_actual < len(preguntas):
    idx_pregunta = st.session_state.preguntas_orden[st.session_state.pregunta_actual]
    pregunta = preguntas[idx_pregunta]
    
    # Mostrar pregunta
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown(f"### 📝 {pregunta['enunciado']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mostrar opciones
    st.markdown("### Selecciona una opción:")
    
    opciones = ['A', 'B', 'C', 'D']
    cols = st.columns(2)
    
    for i, opcion in enumerate(opciones):
        col = cols[i % 2]
        with col:
            if st.button(
                f"**{opcion}** - {pregunta['opciones'][opcion]}",
                key=f"btn_{opcion}_{st.session_state.pregunta_actual}",
                use_container_width=True
            ):
                st.session_state.respuesta_seleccionada = opcion
                st.session_state.mostrar_resultado = True
                st.rerun()
    
    # Mostrar resultado si se seleccionó una opción
    if st.session_state.mostrar_resultado and st.session_state.respuesta_seleccionada:
        respuesta_correcta = pregunta['respuesta_correcta']
        es_correcta = st.session_state.respuesta_seleccionada == respuesta_correcta
        
        if es_correcta:
            st.markdown(
                f'<div class="correct">✅ ¡CORRECTO! Has acertado.</div>',
                unsafe_allow_html=True
            )
            if st.session_state.pregunta_actual not in [r[0] for r in st.session_state.respuestas]:
                st.session_state.aciertos += 1
        else:
            st.markdown(
                f'<div class="incorrect">❌ INCORRECTO. La respuesta correcta es: <strong>{respuesta_correcta}</strong></div>',
                unsafe_allow_html=True
            )
            if st.session_state.pregunta_actual not in [r[0] for r in st.session_state.respuestas]:
                st.session_state.errores += 1
        
        # Mostrar razonamiento
        st.markdown("### 💡 Explicación:")
        st.info(pregunta['razonamiento'])
        
        # Guardar respuesta
        st.session_state.respuestas.append((st.session_state.pregunta_actual, st.session_state.respuesta_seleccionada))
        
        # Botón para siguiente pregunta
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("➡️ Siguiente Pregunta", use_container_width=True):
                st.session_state.pregunta_actual += 1
                st.session_state.mostrar_resultado = False
                st.session_state.respuesta_seleccionada = None
                st.rerun()
        
        with col2:
            if st.button("⏭️ Saltar Pregunta", use_container_width=True):
                st.session_state.pregunta_actual += 1
                st.session_state.mostrar_resultado = False
                st.session_state.respuesta_seleccionada = None
                st.rerun()

else:
    # Examen completado
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown("# 🎉 ¡Examen Completado!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Resultados finales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("✅ Aciertos", st.session_state.aciertos)
    
    with col2:
        st.metric("❌ Errores", st.session_state.errores)
    
    with col3:
        porcentaje_final = (st.session_state.aciertos / len(preguntas)) * 100
        st.metric("📊 Calificación", f"{porcentaje_final:.1f}%")
    
    st.markdown("---")
    
    # Evaluación
    if porcentaje_final >= 90:
        st.success("🏆 ¡Excelente! Has dominado el tema.")
    elif porcentaje_final >= 70:
        st.info("👍 ¡Buen trabajo! Tienes una buena comprensión del tema.")
    elif porcentaje_final >= 50:
        st.warning("📚 Necesitas repasar algunos conceptos.")
    else:
        st.error("❌ Te recomendamos estudiar más antes de intentar de nuevo.")
    
    # Botón para reiniciar
    if st.button("🔄 Hacer Examen de Nuevo", use_container_width=True):
        st.session_state.pregunta_actual = 0
        st.session_state.aciertos = 0
        st.session_state.errores = 0
        st.session_state.respuestas = []
        st.session_state.mostrar_resultado = False
        st.session_state.respuesta_seleccionada = None
        st.session_state.preguntas_orden = list(range(len(preguntas)))
        random.shuffle(st.session_state.preguntas_orden)
        st.rerun()

