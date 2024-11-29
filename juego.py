import streamlit as st
import re
import random

# Listas de palabras
categorias_palabras = {
    "Animales": ["elefante", "jirafa", "leopardo", "pingüino", "delfín"],
    "Países": ["francia", "brasil", "canada", "japon", "mexico"],
    "Programación": ["python", "javascript", "golang", "kotlin", "swift"]
}

def generar_desafio_regex():
    """Genera un desafío de regex basado en las características de las palabras."""
    categoria = random.choice(list(categorias_palabras.keys()))
    palabras = categorias_palabras[categoria]
    palabra_objetivo = random.choice(palabras)
    
    desafios = [
        {
            "descripcion": f"Encuentra una palabra con exactamente {len(palabra_objetivo)} letras",
            "regex": f"^.{{{len(palabra_objetivo)}}}$"
        },
        {
            "descripcion": f"Encuentra una palabra que comience con '{palabra_objetivo[0]}'",
            "regex": f"^{palabra_objetivo[0]}.*"
        },
        {
            "descripcion": f"Encuentra una palabra que termine con '{palabra_objetivo[-1]}'",
            "regex": f".*{palabra_objetivo[-1]}$"
        },
        {
            "descripcion": f"Encuentra una palabra que contenga '{palabra_objetivo[1:-1]}'",
            "regex": f".*{palabra_objetivo[1:-1]}.*"
        }
    ]
    
    desafio = random.choice(desafios)
    return {
        "categoria": categoria,
        "palabras": palabras,
        "palabra_objetivo": palabra_objetivo,
        "desafio": desafio
    }

def verificar_coincidencia_regex(regex, palabras):
    """Verifica cuántas palabras coinciden con la expresión regular dada."""
    coincidencias = [palabra for palabra in palabras if re.match(regex, palabra)]
    return coincidencias

def app():
    st.title("🧩 Juego de Adivinanza de Palabras con Regex")
    
    # Inicializar o recuperar el estado del juego
    if 'juego' not in st.session_state:
        st.session_state.juego = generar_desafio_regex()
        st.session_state.intentos = 0
        st.session_state.resuelto = False
    
    juego = st.session_state.juego
    
    # Mostrar el desafío
    st.write(f"Categoría: {juego['categoria']}")
    st.write(f"Desafío: {juego['desafio']['descripcion']}")
    
    # Entrada del usuario para la expresión regular
    usuario_regex = st.text_input("Ingresa tu patrón de Regex:")
    
    if st.button("Verificar Regex"):
        try:
            coincidencias = verificar_coincidencia_regex(usuario_regex, juego['palabras'])
            
            if juego['palabra_objetivo'] in coincidencias:
                st.success(f"🎉 ¡Felicidades! Encontraste la palabra objetivo: {juego['palabra_objetivo']}")
                st.session_state.resuelto = True
            else:
                st.warning(f"¡No es eso! Coincidencias: {coincidencias}")
            
            st.session_state.intentos += 1
        
        except re.error:
            st.error("¡Expresión regular inválida!")
    
    if st.button("Nuevo Desafío"):
        st.session_state.juego = generar_desafio_regex()
        st.session_state.intentos = 0
        st.session_state.resuelto = False
        st.experimental_rerun()
    
    # Mostrar estadísticas
    st.write(f"Intentos: {st.session_state.intentos}")

if __name__ == "__main__":
    app()
