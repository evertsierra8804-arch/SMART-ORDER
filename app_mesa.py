import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de lujo
st.set_page_config(page_title="SmartOrder Elite", layout="wide")

# --- ESTILO DE DISEÑADOR JEFE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap');
    
    .main { background-color: #0e1117; }
    h1, h2 { font-family: 'Playfair Display', serif; color: #D4AF37; }
    p, div { font-family: 'Montserrat', sans-serif; color: #e0e0e0; }
    
    /* Tarjetas de platos */
    .plato-card {
        background-color: #1a1c23;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .plato-card:hover { border-color: #D4AF37; }
    
    /* Botón Dorado */
    div.stButton > button {
        background-color: transparent;
        border: 1px solid #D4AF37;
        color: #D4AF37;
        width: 100%;
        border-radius: 5px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    div.stButton > button:hover {
        background-color: #D4AF37;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DEL CARRITO ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

def agregar_al_carrito(plato, precio):
    st.session_state.carrito.append({"plato": plato, "precio": precio})

# --- INTERFAZ ---
st.markdown("<h1>🛎️ SmartOrder <span style='font-size:20px; opacity:0.5;'>TABLE SERVICE</span></h1>", unsafe_allow_html=True)

col_menu, col_orden = st.columns([2, 1])

with col_menu:
    st.markdown("## Menú Gourmet")
    menu_df = pd.read_csv("menu.csv")
    
    for index, row in menu_df.iterrows():
        with st.container():
            st.markdown(f"""
                <div class="plato-card">
                    <h3 style="color:#D4AF37; margin:0;">{row['plato']}</h3>
                    <p style="font-size:14px; opacity:0.7;">{row['descripcion']}</p>
                    <p style="font-weight:bold;">${row['precio']:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Añadir {row['plato']}", key=f"btn_{index}"):
                agregar_al_carrito(row['plato'], row['precio'])
                st.toast(f"{row['plato']} añadido!")

with col_orden:
    st.markdown("## Tu Pedido")
    if not st.session_state.carrito:
        st.write("El carrito está vacío.")
    else:
        total = 0
        for item in st.session_state.carrito:
            st.write(f"• {item['plato']} - ${item['precio']:.2f}")
            total += item['precio']
        
        st.divider()
        st.markdown(f"### TOTAL: ${total:.2f}")
        
        mesa = st.selectbox("Número de Mesa:", [1, 2, 3, 4, 5])
        
        if st.button("🚀 ENVIAR A COCINA"):
            # Aquí simulamos el envío. En el siguiente paso lo conectaremos a la pantalla de cocina
            pedido_final = {
                "mesa": mesa,
                "items": [i['plato'] for i in st.session_state.carrito],
                "hora": datetime.now().strftime("%H:%M:%S")
            }
            st.success("¡Pedido enviado! La cocina ha recibido tu orden.")
            st.session_state.carrito = [] # Limpiar carrito