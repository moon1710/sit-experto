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

    #=== MODO SÍNTOMAS ===#
    
    # Etiqueta de instrucción para síntomas
    ttk.Label(
        sintomas_frame, 
        text="Seleccione los síntomas del paciente:", 
        font=subtitulo_font,
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    ).pack(pady=10)
    
    # Frame para contener los checkbuttons de síntomas
    sintomas_check_frame = tk.Frame(sintomas_frame, bg=COLOR_FRAME, bd=1, relief=tk.GROOVE)
    sintomas_check_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # Variables para los checkbuttons
    sintomas_vars = {}
    
    # Crear dos columnas para los síntomas
    col1 = tk.Frame(sintomas_check_frame, bg=COLOR_FRAME)
    col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    col2 = tk.Frame(sintomas_check_frame, bg=COLOR_FRAME)
    col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Distribuir síntomas en dos columnas
    for i, sintoma in enumerate(todos_sintomas):
        var = tk.BooleanVar(value=False)
        sintomas_vars[sintoma] = var
        
        # Decidir en qué columna colocar el checkbox
        parent_frame = col1 if i < len(todos_sintomas) / 2 else col2
        
        sintoma_text = sintoma.replace("_", " ").capitalize()
        cb = ttk.Checkbutton(
            parent_frame, 
            text=sintoma_text,
            variable=var,
            onvalue=True,
            offvalue=False
        )
        cb.pack(anchor="w", pady=2)
    
    # Frame para resultado por síntomas
    resultado_sintomas_frame = tk.Frame(sintomas_frame, bg=COLOR_FRAME, bd=1, relief=tk.GROOVE)
    resultado_sintomas_frame.pack(fill=tk.X, padx=20, pady=10)
    
    diagnostico_sintomas_label = ttk.Label(
        resultado_sintomas_frame, 
        text="Diagnóstico: ", 
        font=texto_normal,
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    )
    diagnostico_sintomas_label.pack(anchor="w", padx=10, pady=5)
    
    # Botón para obtener diagnóstico por síntomas
    def on_diagnosticar_sintomas():
        # Obtener síntomas seleccionados
        seleccionados = [s for s, var in sintomas_vars.items() if var.get()]
        
        if not seleccionados:
            messagebox.showwarning("Atención", "Por favor, seleccione al menos un síntoma.")
            return
        
        # Mostrar diagnóstico
        resultado = diagnosticar_por_sintomas(seleccionados)
        diagnostico_sintomas_label.config(text=f"Diagnóstico: {resultado}")
    
    boton_sintomas_frame = tk.Frame(sintomas_frame, bg=COLOR_FRAME)
    boton_sintomas_frame.pack(pady=10)
    
    ttk.Button(
        boton_sintomas_frame, 
        text="Obtener Diagnóstico", 
        command=on_diagnosticar_sintomas,
        style="Accent.TButton"
    ).pack(pady=5)import tkinter as tk
from tkinter import ttk, messagebox, font
from tkinter.font import Font

# Base de conocimientos: síntomas por persona
sintomas = {
    "lulu": ["fiebre", "dolor_de_garganta", "tos"],
    "pablo": ["fiebre", "dolor_muscular", "dolor_de_cabeza"],
    "lupita": ["estornudos", "congestion_nasal", "ojos_llorosos"],
    "ciro": ["dolor_de_cabeza", "sensibilidad_a_la_luz"]
}

# Lista de todos los síntomas posibles
todos_sintomas = sorted(list(set(
    sintoma for lista_sintomas in sintomas.values() 
    for sintoma in lista_sintomas
)))

# Mapeo de enfermedades a síntomas
enfermedades = {
    "Gripe": ["fiebre", "dolor_muscular", "dolor_de_cabeza"],
    "Resfriado": ["estornudos", "congestion_nasal", "ojos_llorosos"],
    "Faringitis": ["fiebre", "dolor_de_garganta", "tos"],
    "Migraña": ["dolor_de_cabeza", "sensibilidad_a_la_luz"]
}

# Reglas del sistema experto para diagnosticar a partir de persona
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

# Diagnosticar a partir de un conjunto de síntomas
def diagnosticar_por_sintomas(sintomas_seleccionados):
    if not sintomas_seleccionados:
        return "Sin síntomas seleccionados"
    
    s = set(sintomas_seleccionados)
    
    # Comprueba coincidencias exactas primero
    for enfermedad, sintomas_req in enfermedades.items():
        if set(sintomas_req) == s:
            return enfermedad
            
    # Si no hay coincidencia exacta, busca la mejor coincidencia
    max_coincidencia = 0
    mejor_diagnostico = "Sin diagnóstico claro"
    
    for enfermedad, sintomas_req in enfermedades.items():
        req_set = set(sintomas_req)
        coincidencias = len(s.intersection(req_set))
        cobertura = coincidencias / len(req_set) if req_set else 0
        
        if coincidencias > 0 and cobertura > max_coincidencia:
            max_coincidencia = cobertura
            mejor_diagnostico = enfermedad if cobertura >= 0.7 else f"Posible {enfermedad} ({int(cobertura*100)}%)"
    
    return mejor_diagnostico

# Función para mostrar los síntomas
def mostrar_sintomas(persona):
    if persona in sintomas:
        sintomas_persona = ", ".join([s.replace("_", " ").capitalize() for s in sintomas[persona]])
        return sintomas_persona
    return "No hay síntomas registrados"

# Obtener síntomas por enfermedad
def obtener_sintomas_enfermedad(enfermedad):
    if enfermedad in enfermedades:
        return ", ".join([s.replace("_", " ").capitalize() for s in enfermedades[enfermedad]])
    return "No hay síntomas registrados para esta enfermedad"

# Colores para la interfaz
COLOR_FONDO = "#f0f8ff"  # Azul claro
COLOR_FRAME = "#e6f2ff"  # Azul más claro
COLOR_BOTON = "#4682b4"  # Azul acero
COLOR_TEXTO = "#2c3e50"  # Azul oscuro
COLOR_ACTIVO = "#3498db"  # Azul brillante

# Interfaz gráfica
def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Sistema Experto - Diagnóstico Médico")
    ventana.geometry("550x600")
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
        text="Hecho por: Nombre 1, Nombre 2", 
        font=texto_normal, 
        background=COLOR_FRAME, 
        foreground=COLOR_TEXTO
    ).pack(pady=5)
    
    # Línea separadora
    sep = ttk.Separator(main_frame, orient="horizontal")
    sep.pack(fill=tk.X, padx=20, pady=10)
    
    # Toggle para cambiar entre modos
    modo_var = tk.StringVar(value="paciente")
    
    # Frame para el toggle
    toggle_frame = tk.Frame(main_frame, bg=COLOR_FRAME)
    toggle_frame.pack(fill=tk.X, padx=20, pady=5)
    
    # Label para modo
    ttk.Label(
        toggle_frame,
        text="Modo de diagnóstico:",
        font=texto_normal,
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    ).pack(side=tk.LEFT, padx=5)
    
    # Estilo para botones de toggle
    style = ttk.Style()
    style.configure("Toggle.TButton", font=texto_normal)
    style.configure("Active.Toggle.TButton", foreground=COLOR_ACTIVO, font=(None, 10, "bold"))
    
    # Frames para cada modo (se mostrarán/ocultarán según selección)
    paciente_frame = tk.Frame(main_frame, bg=COLOR_FRAME)
    sintomas_frame = tk.Frame(main_frame, bg=COLOR_FRAME)
    
    def cambiar_modo(nuevo_modo):
        modo_var.set(nuevo_modo)
        
        # Actualizar apariencia de botones
        if nuevo_modo == "paciente":
            btn_paciente.configure(style="Active.Toggle.TButton")
            btn_sintomas.configure(style="Toggle.TButton")
            paciente_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            sintomas_frame.pack_forget()
        else:
            btn_sintomas.configure(style="Active.Toggle.TButton")
            btn_paciente.configure(style="Toggle.TButton")
            sintomas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            paciente_frame.pack_forget()
    
    # Botones de toggle
    btn_paciente = ttk.Button(
        toggle_frame, 
        text="Por Paciente", 
        style="Active.Toggle.TButton", 
        command=lambda: cambiar_modo("paciente")
    )
    btn_paciente.pack(side=tk.LEFT, padx=5)
    
    btn_sintomas = ttk.Button(
        toggle_frame, 
        text="Por Síntomas", 
        style="Toggle.TButton", 
        command=lambda: cambiar_modo("sintomas")
    )
    btn_sintomas.pack(side=tk.LEFT, padx=5)
    
    # Inicialmente mostrar el modo paciente
    paciente_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    #=== MODO PACIENTE ===#
    
    # Etiqueta de instrucción
    ttk.Label(
        paciente_frame, 
        text="Seleccione una persona para diagnóstico:", 
        font=subtitulo_font,
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    ).pack(pady=10)
    
    # Frame para el combobox
    select_frame = tk.Frame(paciente_frame, bg=COLOR_FRAME)
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
    
    # Frame para mostrar síntomas del paciente
    sintomas_paciente_frame = tk.Frame(paciente_frame, bg=COLOR_FRAME, bd=1, relief=tk.GROOVE)
    sintomas_paciente_frame.pack(fill=tk.X, padx=20, pady=10)
    
    sintomas_label = ttk.Label(
        sintomas_paciente_frame, 
        text="Síntomas: ", 
        font=texto_normal,
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    )
    sintomas_label.pack(anchor="w", padx=10, pady=5)
    
    # Frame para resultado paciente
    resultado_paciente_frame = tk.Frame(paciente_frame, bg=COLOR_FRAME, bd=1, relief=tk.GROOVE)
    resultado_paciente_frame.pack(fill=tk.X, padx=20, pady=10)
    
    diagnostico_label = ttk.Label(
        resultado_paciente_frame, 
        text="Diagnóstico: ", 
        font=texto_normal,
        background=COLOR_FRAME,
        foreground=COLOR_TEXTO
    )
    diagnostico_label.pack(anchor="w", padx=10, pady=5)
    
    # Estilo de los botones
    style.configure("Accent.TButton", font=texto_normal)
    
    # Función al pulsar el botón
    def on_diagnosticar_paciente():
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
    
    # Botón para obtener diagnóstico de paciente
    boton_paciente_frame = tk.Frame(paciente_frame, bg=COLOR_FRAME)
    boton_paciente_frame.pack(pady=10)
    
    ttk.Button(
        boton_paciente_frame, 
        text="Diagnosticar", 
        command=on_diagnosticar_paciente,
        style="Accent.TButton"
    ).pack(pady=5)
    
    # Función para actualizar al seleccionar paciente
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