import tkinter as tk
from tkinter import ttk, messagebox, font
from tkinter.font import Font

# Base de conocimientos: síntomas por persona
sintomas = {
    "lulu": ["fiebre", "dolor_de_garganta", "tos"],
    "pablo": ["fiebre", "dolor_muscular", "dolor_de_cabeza"],
    "lupita": ["estornudos", "congestion_nasal", "ojos_llorosos"],
    "ciro": ["dolor_de_cabeza", "sensibilidad_a_la_luz"]
}

# Reglas del sistema experto
def diagnosticar(persona):
    s = set(sintomas.get(persona, []))
    if {"fiebre", "dolor_muscular", "dolor_de_cabeza"}.issubset(s):
        return "Gripe"
    elif {"estornudos", "congestion_nasal", "ojos_llorosos"}.issubset(s):
        return "Resfriado"
    elif {"fiebre", "dolor_de_garganta", "tos"}.issubset(s):
        return "Faringitis"
    elif {"dolor_de_cabeza", "sensibilidad_a_la_luz"}.issubset(s):
        return "Migraña"
    else:
        return "Sin diagnóstico claro"

# Función para mostrar los síntomas
def mostrar_sintomas(persona):
    if persona in sintomas:
        sintomas_persona = ", ".join([s.replace("_", " ").capitalize() for s in sintomas[persona]])
        return sintomas_persona
    return "No hay síntomas registrados"

# Colores para la interfaz
COLOR_FONDO = "#f0f8ff"  # Azul claro
COLOR_FRAME = "#e6f2ff"  # Azul más claro
COLOR_BOTON = "#4682b4"  # Azul acero
COLOR_TEXTO = "#2c3e50"  # Azul oscuro

# Interfaz gráfica
def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Sistema Experto - Diagnóstico Médico")
    ventana.geometry("500x400")
    ventana.configure(bg=COLOR_FONDO)
    
    # Fuentes personalizadas
    titulo_font = Font(family="Arial", size=16, weight="bold")
    subtitulo_font = Font(family="Arial", size=12, weight="bold")
    texto_normal = Font(family="Arial", size=10)
    
    # Frame principal con borde
    main_frame = tk.Frame(ventana, bg=COLOR_FRAME, bd=2, relief=tk.GROOVE)
    main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    # Título y créditos
    titulo_frame = tk.Frame(main_frame, bg=COLOR_FRAME)
    titulo_frame.pack(fill=tk.X, padx=10, pady=10)
    
    ttk.Label(
        titulo_frame, 
        text="Sistema Experto de Diagnóstico", 
        font=titulo_font, 
        background=COLOR_FRAME, 
        foreground=COLOR_TEXTO
    ).pack()
    
    ttk.Label(
        titulo_frame, 
        text="Hecho por: Lady, Lupita, Mon, Martín, Luis A", 
        font=texto_normal, 
        background=COLOR_FRAME, 
        foreground=COLOR_TEXTO
    ).pack(pady=5)
    
    # Línea separadora
    sep = ttk.Separator(main_frame, orient="horizontal")
    sep.pack(fill=tk.X, padx=20, pady=10)
    
    # Frame de contenido
    content_frame = tk.Frame(main_frame, bg=COLOR_FRAME)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Etiqueta de instrucción
    ttk.Label(
        content_frame, 
        text="Seleccione una persona para diagnóstico:", 
        font=subtitulo_font,
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    ).pack(pady=10)
    
    # Frame para el combobox y botón
    select_frame = tk.Frame(content_frame, bg=COLOR_FRAME)
    select_frame.pack(pady=10)
    
    # Combobox de selección
    personas = list(sintomas.keys())
    seleccion = tk.StringVar()
    
    ttk.Label(
        select_frame, 
        text="Paciente:", 
        font=texto_normal,
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    ).pack(side=tk.LEFT, padx=5)
    
    combo = ttk.Combobox(
        select_frame, 
        textvariable=seleccion, 
        values=[p.capitalize() for p in personas], 
        state="readonly", 
        font=texto_normal,
        width=15
    )
    combo.pack(side=tk.LEFT, padx=5)
    
    # Frame para mostrar síntomas
    sintomas_frame = tk.Frame(content_frame, bg=COLOR_FRAME, bd=1, relief=tk.GROOVE)
    sintomas_frame.pack(fill=tk.X, padx=20, pady=10)
    
    sintomas_label = ttk.Label(
        sintomas_frame, 
        text="Síntomas: ", 
        font=texto_normal,
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    )
    sintomas_label.pack(anchor="w", padx=10, pady=5)
    
    # Frame para resultado
    resultado_frame = tk.Frame(content_frame, bg=COLOR_FRAME, bd=1, relief=tk.GROOVE)
    resultado_frame.pack(fill=tk.X, padx=20, pady=10)
    
    diagnostico_label = ttk.Label(
        resultado_frame, 
        text="Diagnóstico: ", 
        font=texto_normal,
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    )
    diagnostico_label.pack(anchor="w", padx=10, pady=5)
    
    # Estilo de los botones
    style = ttk.Style()
    style.configure("Accent.TButton", font=texto_normal)
    
    # Función al pulsar el botón
    def on_diagnosticar():
        persona = seleccion.get().lower()
        if not persona:
            messagebox.showwarning("Atención", "Por favor, seleccione una persona.")
            return
        
        # Mostrar síntomas
        sintomas_texto = mostrar_sintomas(persona)
        sintomas_label.config(text=f"Síntomas: {sintomas_texto}")
        
        # Mostrar diagnóstico
        resultado = diagnosticar(persona)
        diagnostico_label.config(text=f"Diagnóstico: {resultado}")
    
    # Botón para obtener diagnóstico
    boton_frame = tk.Frame(content_frame, bg=COLOR_FRAME)
    boton_frame.pack(pady=10)
    
    ttk.Button(
        boton_frame, 
        text="Diagnosticar", 
        command=on_diagnosticar,
        style="Accent.TButton"
    ).pack(pady=5)
    
    # Función para actualizar al seleccionar
    def on_seleccion(event):
        persona = seleccion.get().lower()
        if persona:
            sintomas_texto = mostrar_sintomas(persona)
            sintomas_label.config(text=f"Síntomas: {sintomas_texto}")
            diagnostico_label.config(text="Diagnóstico: ")
    
    combo.bind("<<ComboboxSelected>>", on_seleccion)
    
    # Footer
    footer_frame = tk.Frame(main_frame, bg=COLOR_FRAME)
    footer_frame.pack(fill=tk.X, padx=10, pady=5)
    
    ttk.Label(
        footer_frame, 
        text="© 2025 - Sistema Experto de Diagnóstico Médico", 
        font=("Arial", 8),
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    ).pack()
    
    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()