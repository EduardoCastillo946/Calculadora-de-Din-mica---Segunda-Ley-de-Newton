import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

def calcular_fuerza_neta(fuerzas_x, fuerzas_y):
    """
    Calcula la fuerza neta en X e Y
    """
    fx_neta = sum(fuerzas_x)
    fy_neta = sum(fuerzas_y)
    return fx_neta, fy_neta

def calcular_magnitud_direccion(fx, fy):
    """
    Calcula la magnitud y dirección de la fuerza resultante
    """
    magnitud = math.sqrt(fx**2 + fy**2)
    if fx == 0 and fy == 0:
        direccion = 0
    else:
        direccion = math.degrees(math.atan2(fy, fx))
    return magnitud, direccion

def calcular_aceleracion(fuerza_neta, masa):
    """
    Calcula la aceleración usando F = ma
    """
    if masa <= 0:
        return None
    return fuerza_neta / masa

def main():
    st.title("⚡ Calculadora de Dinámica - Segunda Ley de Newton")
    st.markdown("---")
    
    # Sidebar para configuración
    st.sidebar.header("⚙️ Configuración")
    
    # Selección del tipo de problema
    tipo_problema = st.sidebar.selectbox(
        "📋 Tipo de problema",
        ["Fuerzas múltiples", "Movimiento en plano inclinado", "Fuerza de fricción"]
    )
    
    # Configuración del gráfico
    mostrar_grafico = st.sidebar.checkbox("📊 Mostrar gráfico", value=True)
    
    if mostrar_grafico:
        color_fuerzas = st.sidebar.color_picker("Color de las fuerzas", "#1f77b4")
        color_resultante = st.sidebar.color_picker("Color de la resultante", "#ff0000")
        escala_vectores = st.sidebar.slider("Escala de vectores", 0.1, 2.0, 1.0, 0.1)
    
    if tipo_problema == "Fuerzas múltiples":
        resolver_fuerzas_multiples(mostrar_grafico, color_fuerzas, color_resultante, escala_vectores)
    elif tipo_problema == "Movimiento en plano inclinado":
        resolver_plano_inclinado(mostrar_grafico, color_fuerzas, color_resultante, escala_vectores)
    else:
        resolver_friccion(mostrar_grafico, color_fuerzas, color_resultante, escala_vectores)

def resolver_fuerzas_multiples(mostrar_grafico, color_fuerzas, color_resultante, escala_vectores):
    st.subheader("🔄 Sistema de Fuerzas Múltiples")
    
    # Parámetros del objeto
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Propiedades del objeto")
        masa = st.number_input("Masa (kg)", value=10.0, min_value=0.1, step=0.1)
    
    with col2:
        st.subheader("🔢 Número de fuerzas")
        num_fuerzas = st.number_input("Cantidad de fuerzas", value=3, min_value=1, max_value=10, step=1)
    
    # Entrada de fuerzas
    st.subheader("💪 Fuerzas aplicadas")
    
    fuerzas_x = []
    fuerzas_y = []
    fuerzas_info = []
    
    for i in range(num_fuerzas):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            magnitud = st.number_input(f"Magnitud F{i+1} (N)", value=10.0, step=0.1, key=f"mag_{i}")
        
        with col2:
            angulo = st.number_input(f"Ángulo F{i+1} (°)", value=0.0, step=1.0, key=f"ang_{i}")
        
        with col3:
            st.write(f"**F{i+1}**: {magnitud:.1f} N")
            st.write(f"**θ{i+1}**: {angulo:.1f}°")
        
        # Convertir a componentes
        fx = magnitud * math.cos(math.radians(angulo))
        fy = magnitud * math.sin(math.radians(angulo))
        
        fuerzas_x.append(fx)
        fuerzas_y.append(fy)
        fuerzas_info.append((magnitud, angulo, fx, fy))
    
    # Calcular resultados
    fx_neta, fy_neta = calcular_fuerza_neta(fuerzas_x, fuerzas_y)
    magnitud_neta, direccion_neta = calcular_magnitud_direccion(fx_neta, fy_neta)
    aceleracion_x = calcular_aceleracion(fx_neta, masa)
    aceleracion_y = calcular_aceleracion(fy_neta, masa)
    aceleracion_neta = math.sqrt(aceleracion_x**2 + aceleracion_y**2)
    
    # Mostrar resultados
    mostrar_resultados_dinamica(fx_neta, fy_neta, magnitud_neta, direccion_neta, 
                               aceleracion_x, aceleracion_y, aceleracion_neta, masa)
    
    # Mostrar gráfico
    if mostrar_grafico:
        graficar_fuerzas_multiples(fuerzas_info, fx_neta, fy_neta, color_fuerzas, 
                                  color_resultante, escala_vectores)

def resolver_plano_inclinado(mostrar_grafico, color_fuerzas, color_resultante, escala_vectores):
    st.subheader("📐 Movimiento en Plano Inclinado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Propiedades del objeto")
        masa = st.number_input("Masa (kg)", value=10.0, min_value=0.1, step=0.1)
        angulo = st.number_input("Ángulo del plano (°)", value=30.0, min_value=0.0, max_value=90.0, step=1.0)
    
    with col2:
        st.subheader("🔧 Coeficientes")
        mu_s = st.number_input("Coeficiente de fricción estática", value=0.3, min_value=0.0, step=0.01)
        mu_k = st.number_input("Coeficiente de fricción cinética", value=0.2, min_value=0.0, step=0.01)
    
    # Constantes
    g = 9.81  # m/s²
    
    # Calcular fuerzas
    peso = masa * g
    peso_paralelo = peso * math.sin(math.radians(angulo))
    peso_perpendicular = peso * math.cos(math.radians(angulo))
    normal = peso_perpendicular
    
    # Fricción máxima estática
    friccion_max_estatica = mu_s * normal
    friccion_cinetica = mu_k * normal
    
    # Determinar tipo de movimiento
    if peso_paralelo <= friccion_max_estatica:
        estado = "Estático"
        friccion_actual = peso_paralelo
        aceleracion = 0
    else:
        estado = "Deslizante"
        friccion_actual = friccion_cinetica
        fuerza_neta = peso_paralelo - friccion_actual
        aceleracion = fuerza_neta / masa
    
    # Mostrar resultados del plano inclinado
    st.markdown("---")
    st.subheader("📊 Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("⚖️ Peso total", f"{peso:.2f} N")
        st.metric("📐 Componente paralela", f"{peso_paralelo:.2f} N")
        st.metric("🔽 Componente perpendicular", f"{peso_perpendicular:.2f} N")
    
    with col2:
        st.metric("🔼 Fuerza normal", f"{normal:.2f} N")
        st.metric("🛑 Fricción máx. estática", f"{friccion_max_estatica:.2f} N")
        st.metric("🏃 Fricción cinética", f"{friccion_cinetica:.2f} N")
    
    with col3:
        st.metric("📍 Estado del objeto", estado)
        st.metric("⚡ Fricción actual", f"{friccion_actual:.2f} N")
        st.metric("🚀 Aceleración", f"{aceleracion:.2f} m/s²")
    
    # Análisis del movimiento
    if estado == "Estático":
        st.success("✅ **El objeto permanece en reposo** - La fricción estática equilibra la componente paralela del peso")
    else:
        st.warning("⚠️ **El objeto se desliza** - La componente paralela del peso supera la fricción máxima estática")
    
    # Mostrar gráfico del plano inclinado
    if mostrar_grafico:
        graficar_plano_inclinado(masa, angulo, peso_paralelo, peso_perpendicular, normal, 
                               friccion_actual, color_fuerzas, color_resultante, escala_vectores)

def resolver_friccion(mostrar_grafico, color_fuerzas, color_resultante, escala_vectores):
    st.subheader("🔄 Problema de Fricción")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Propiedades del objeto")
        masa = st.number_input("Masa (kg)", value=10.0, min_value=0.1, step=0.1)
        fuerza_aplicada = st.number_input("Fuerza aplicada (N)", value=50.0, step=1.0)
        angulo_fuerza = st.number_input("Ángulo de la fuerza (°)", value=0.0, step=1.0)
    
    with col2:
        st.subheader("🔧 Coeficientes de fricción")
        mu_s = st.number_input("Coeficiente estático", value=0.4, min_value=0.0, step=0.01)
        mu_k = st.number_input("Coeficiente cinético", value=0.3, min_value=0.0, step=0.01)
    
    # Constantes
    g = 9.81
    
    # Componentes de la fuerza aplicada
    fx_aplicada = fuerza_aplicada * math.cos(math.radians(angulo_fuerza))
    fy_aplicada = fuerza_aplicada * math.sin(math.radians(angulo_fuerza))
    
    # Fuerzas verticales
    peso = masa * g
    normal = peso - fy_aplicada
    
    # Fricción máxima
    friccion_max = mu_s * normal
    friccion_cinetica = mu_k * normal
    
    # Determinar movimiento
    if fx_aplicada <= friccion_max:
        estado = "Estático"
        friccion_actual = fx_aplicada
        aceleracion = 0
    else:
        estado = "Cinético"
        friccion_actual = friccion_cinetica
        fuerza_neta = fx_aplicada - friccion_actual
        aceleracion = fuerza_neta / masa
    
    # Mostrar resultados
    mostrar_resultados_friccion(peso, normal, fx_aplicada, fy_aplicada, friccion_max, 
                               friccion_actual, estado, aceleracion)
    
    # Mostrar gráfico
    if mostrar_grafico:
        graficar_friccion(masa, fuerza_aplicada, angulo_fuerza, friccion_actual, 
                         color_fuerzas, color_resultante, escala_vectores)

def mostrar_resultados_dinamica(fx_neta, fy_neta, magnitud_neta, direccion_neta, 
                               aceleracion_x, aceleracion_y, aceleracion_neta, masa):
    st.markdown("---")
    st.subheader("📊 Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("➡️ Fuerza neta X", f"{fx_neta:.2f} N")
        st.metric("⬆️ Fuerza neta Y", f"{fy_neta:.2f} N")
    
    with col2:
        st.metric("🔄 Magnitud resultante", f"{magnitud_neta:.2f} N")
        st.metric("📐 Dirección", f"{direccion_neta:.1f}°")
    
    with col3:
        st.metric("🚀 Aceleración neta", f"{aceleracion_neta:.2f} m/s²")
        st.metric("⚖️ Masa", f"{masa:.1f} kg")
    
    # Segunda Ley de Newton
    st.info(f"**Segunda Ley de Newton**: F = ma → {magnitud_neta:.2f} N = {masa:.1f} kg × {aceleracion_neta:.2f} m/s²")

def mostrar_resultados_friccion(peso, normal, fx_aplicada, fy_aplicada, friccion_max, 
                               friccion_actual, estado, aceleracion):
    st.markdown("---")
    st.subheader("📊 Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("⚖️ Peso", f"{peso:.2f} N")
        st.metric("🔼 Fuerza normal", f"{normal:.2f} N")
    
    with col2:
        st.metric("➡️ Fuerza horizontal", f"{fx_aplicada:.2f} N")
        st.metric("⬆️ Fuerza vertical", f"{fy_aplicada:.2f} N")
    
    with col3:
        st.metric("🛑 Fricción máxima", f"{friccion_max:.2f} N")
        st.metric("⚡ Fricción actual", f"{friccion_actual:.2f} N")
    
    # Estado del movimiento
    if estado == "Estático":
        st.success(f"✅ **Objeto en reposo** - Aceleración: {aceleracion:.2f} m/s²")
    else:
        st.warning(f"⚠️ **Objeto en movimiento** - Aceleración: {aceleracion:.2f} m/s²")

def graficar_fuerzas_multiples(fuerzas_info, fx_neta, fy_neta, color_fuerzas, color_resultante, escala):
    st.markdown("---")
    st.subheader("📈 Diagrama de Fuerzas")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Dibujar cada fuerza
    for i, (magnitud, angulo, fx, fy) in enumerate(fuerzas_info):
        ax.arrow(0, 0, fx * escala, fy * escala, head_width=0.3, head_length=0.3, 
                fc=color_fuerzas, ec=color_fuerzas, alpha=0.7, linewidth=2)
        
        # Etiqueta de la fuerza
        label_x = fx * escala * 0.6
        label_y = fy * escala * 0.6
        ax.text(label_x, label_y, f'F{i+1}\n{magnitud:.1f}N', 
                fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Dibujar fuerza resultante
    if fx_neta != 0 or fy_neta != 0:
        ax.arrow(0, 0, fx_neta * escala, fy_neta * escala, head_width=0.4, head_length=0.4, 
                fc=color_resultante, ec=color_resultante, linewidth=3, alpha=0.9)
        
        # Etiqueta de la resultante
        magnitud_neta = math.sqrt(fx_neta**2 + fy_neta**2)
        ax.text(fx_neta * escala * 0.6, fy_neta * escala * 0.6, 
                f'Resultante\n{magnitud_neta:.1f}N', 
                fontsize=12, ha='center', va='center', fontweight='bold', color=color_resultante)
    
    configurar_grafico(ax, "Diagrama de Fuerzas", escala)
    st.pyplot(fig)

def graficar_plano_inclinado(masa, angulo, peso_paralelo, peso_perpendicular, normal, 
                           friccion, color_fuerzas, color_resultante, escala):
    st.markdown("---")
    st.subheader("📈 Diagrama del Plano Inclinado")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Dibujar el plano inclinado
    plano_x = [0, 8, 0, 0]
    plano_y = [0, 8 * math.tan(math.radians(angulo)), 0, 0]
    ax.plot(plano_x, plano_y, 'k-', linewidth=3)
    
    # Posición del objeto en el plano
    obj_x = 4
    obj_y = 4 * math.tan(math.radians(angulo))
    
    # Dibujar objeto
    ax.scatter([obj_x], [obj_y], s=200, c='brown', marker='s', zorder=5)
    
    # Vectores de fuerza (escalados)
    peso_total = masa * 9.81
    escala_local = escala * 0.01
    
    # Peso total (vertical hacia abajo)
    ax.arrow(obj_x, obj_y, 0, -peso_total * escala_local, 
            head_width=0.2, head_length=0.2, fc='blue', ec='blue', linewidth=2)
    ax.text(obj_x - 0.5, obj_y - peso_total * escala_local / 2, 
            f'Peso\n{peso_total:.1f}N', fontsize=10, ha='center', va='center')
    
    # Componente paralela
    dx_paralelo = peso_paralelo * math.cos(math.radians(angulo)) * escala_local
    dy_paralelo = -peso_paralelo * math.sin(math.radians(angulo)) * escala_local
    ax.arrow(obj_x, obj_y, dx_paralelo, dy_paralelo, 
            head_width=0.2, head_length=0.2, fc=color_fuerzas, ec=color_fuerzas, linewidth=2)
    
    # Componente perpendicular
    dx_perp = peso_perpendicular * math.sin(math.radians(angulo)) * escala_local
    dy_perp = peso_perpendicular * math.cos(math.radians(angulo)) * escala_local
    ax.arrow(obj_x, obj_y, dx_perp, -dy_perp, 
            head_width=0.2, head_length=0.2, fc='green', ec='green', linewidth=2)
    
    # Fuerza normal
    ax.arrow(obj_x, obj_y, -dx_perp, dy_perp, 
            head_width=0.2, head_length=0.2, fc='orange', ec='orange', linewidth=2)
    
    # Fricción
    ax.arrow(obj_x, obj_y, -dx_paralelo, -dy_paralelo, 
            head_width=0.2, head_length=0.2, fc=color_resultante, ec=color_resultante, linewidth=2)
    
    # Configurar gráfico
    ax.set_xlim(-1, 10)
    ax.set_ylim(-3, 6)
    ax.set_xlabel('Distancia (m)')
    ax.set_ylabel('Altura (m)')
    ax.set_title(f'Plano Inclinado - Ángulo: {angulo}°')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # Leyenda
    ax.text(1, 4, f'Ángulo: {angulo}°\nMasa: {masa} kg\nPeso paralelo: {peso_paralelo:.1f} N\nFricción: {friccion:.1f} N', 
            fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    
    st.pyplot(fig)

def graficar_friccion(masa, fuerza_aplicada, angulo_fuerza, friccion_actual, 
                     color_fuerzas, color_resultante, escala):
    st.markdown("---")
    st.subheader("📈 Diagrama de Fricción")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Posición del objeto
    obj_x, obj_y = 0, 0
    
    # Dibujar objeto
    ax.scatter([obj_x], [obj_y], s=300, c='brown', marker='s', zorder=5)
    
    # Escalas
    escala_local = escala * 0.1
    
    # Fuerza aplicada
    fx_aplicada = fuerza_aplicada * math.cos(math.radians(angulo_fuerza))
    fy_aplicada = fuerza_aplicada * math.sin(math.radians(angulo_fuerza))
    
    ax.arrow(obj_x, obj_y, fx_aplicada * escala_local, fy_aplicada * escala_local,
            head_width=0.3, head_length=0.3, fc=color_fuerzas, ec=color_fuerzas, linewidth=2)
    ax.text(fx_aplicada * escala_local * 0.6, fy_aplicada * escala_local * 0.6 + 0.5,
            f'Fuerza aplicada\n{fuerza_aplicada:.1f}N', fontsize=10, ha='center', va='center')
    
    # Fricción (opuesta al movimiento)
    ax.arrow(obj_x, obj_y, -friccion_actual * escala_local, 0,
            head_width=0.3, head_length=0.3, fc=color_resultante, ec=color_resultante, linewidth=2)
    ax.text(-friccion_actual * escala_local * 0.6, -0.5,
            f'Fricción\n{friccion_actual:.1f}N', fontsize=10, ha='center', va='center')
    
    # Peso y normal
    peso = masa * 9.81
    ax.arrow(obj_x, obj_y, 0, -peso * escala_local,
            head_width=0.3, head_length=0.3, fc='blue', ec='blue', linewidth=2)
    ax.arrow(obj_x, obj_y, 0, peso * escala_local,
            head_width=0.3, head_length=0.3, fc='green', ec='green', linewidth=2)
    
    configurar_grafico(ax, "Diagrama de Fricción", escala)
    st.pyplot(fig)

def configurar_grafico(ax, titulo, escala):
    ax.set_xlim(-10 * escala, 10 * escala)
    ax.set_ylim(-10 * escala, 10 * escala)
    ax.set_xlabel('Fuerza X (N)')
    ax.set_ylabel('Fuerza Y (N)')
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_aspect('equal')

# Información teórica
def mostrar_informacion_teorica():
    st.markdown("---")
    st.subheader("ℹ️ Información Teórica")
    
    with st.expander("🔬 Leyes de Newton"):
        st.markdown("**Primera Ley (Inercia)**: Un objeto en reposo permanece en reposo, y un objeto en movimiento continúa en movimiento rectilíneo uniforme, a menos que actúe una fuerza neta sobre él.")
        st.markdown("**Segunda Ley**: La aceleración de un objeto es directamente proporcional a la fuerza neta que actúa sobre él e inversamente proporcional a su masa.")
        st.latex(r"\vec{F}_{neta} = m \vec{a}")
        st.markdown("**Tercera Ley**: Para cada acción hay una reacción igual y opuesta.")
    
    with st.expander("⚖️ Equilibrio de Fuerzas"):
        st.markdown("Para que un objeto esté en equilibrio:")
        st.latex(r"\sum F_x = 0 \quad \text{y} \quad \sum F_y = 0")
        st.markdown("Esto significa que la suma de todas las fuerzas en cada dirección debe ser cero.")
    
    with st.expander("🔄 Fricción"):
        st.markdown("**Fricción Estática**: Evita que el objeto comience a moverse")
        st.latex(r"f_s \leq \mu_s N")
        st.markdown("**Fricción Cinética**: Actúa cuando el objeto ya está en movimiento")
        st.latex(r"f_k = \mu_k N")
        st.markdown("Donde μ es el coeficiente de fricción y N es la fuerza normal.")

if __name__ == "__main__":
    main()
    mostrar_informacion_teorica()