import tkinter as tk
from tkinter import ttk, messagebox

# Base de conocimientos: síntomas por persona (no usado en modo inverso)
sintomas = {
    "lulu": ["fiebre", "dolor_de_garganta", "tos"],
    "pablo": ["fiebre", "dolor_muscular", "dolor_de_cabeza"],
    "lupita": ["estornudos", "congestion_nasal", "ojos_llorosos"],
    "ciro": ["dolor_de_cabeza", "sensibilidad_a_la_luz"]
}

# Reglas (enfermedad → síntomas)
enfermedades = {
    "Gripe": {"fiebre", "dolor_muscular", "dolor_de_cabeza"},
    "Resfriado": {"estornudos", "congestion_nasal", "ojos_llorosos"},
    "Faringitis": {"fiebre", "dolor_de_garganta", "tos"},
    "Migraña": {"dolor_de_cabeza", "sensibilidad_a_la_luz"}
}

def diagnosticar_por_sintomas(seleccionados):
    for enf, req in enfermedades.items():
        if req.issubset(seleccionados):
            return enf
    return "Sin diagnóstico claro"

def mostrar_sintomas_de(enf):
    req = enfermedades.get(enf, set())
    if not req:
        messagebox.showwarning("Atención", "Seleccione una enfermedad válida.")
    else:
        lista = "\n".join(f"- {s.replace('_', ' ')}" for s in req)
        messagebox.showinfo("Síntomas", f"Sintomas de {enf}:\n\n{lista}")

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Sistema Experto de Diagnóstico. Hecho por: Nombre 1")
    ventana.geometry("500x400")
    ventana.resizable(False, False)

    style = ttk.Style(ventana)
    style.theme_use('clam')
    style.configure('TFrame', background='#f0f4f7')
    style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), background='#f0f4f7')
    style.configure('TLabel', background='#f0f4f7', font=('Arial', 11))
    style.configure('TButton', font=('Arial', 11, 'bold'))
    style.configure('TRadiobutton', background='#f0f4f7', font=('Arial', 11))

    cont = ttk.Frame(ventana, padding=20, style='TFrame')
    cont.pack(fill='both', expand=True)

    # Encabezado
    ttk.Label(cont, text="Sistema Experto Médico", style='Header.TLabel').pack(pady=(0, 15))

    # Modo: seleccionar enfermedad / ingresar síntomas
    modo_var = tk.StringVar(value='modo_enf')
    modos = ttk.Frame(cont, style='TFrame')
    modos.pack(fill='x', pady=5)
    ttk.Radiobutton(modos, text="Buscar síntomas de enfermedad", variable=modo_var, value='modo_enf', command=lambda: switch_mode()).pack(side='left', padx=5)
    ttk.Radiobutton(modos, text="Diagnosticar por síntomas", variable=modo_var, value='modo_sint', command=lambda: switch_mode()).pack(side='left', padx=5)

    # --- Frame para modo 1: síntomas de enfermedad ---
    frame_enf = ttk.Frame(cont, style='TFrame')
    ttk.Label(frame_enf, text="Seleccione una enfermedad:").pack(anchor='w', pady=(10,0))
    enf_combo = ttk.Combobox(frame_enf, values=list(enfermedades.keys()), state="readonly", font=('Arial', 11))
    enf_combo.pack(fill='x', pady=5)
    enf_combo.current(0)
    ttk.Button(frame_enf, text="Mostrar síntomas", command=lambda: mostrar_sintomas_de(enf_combo.get())).pack(pady=10)

    # --- Frame para modo 2: diagnosticar por síntomas ---
    frame_sint = ttk.Frame(cont, style='TFrame')
    ttk.Label(frame_sint, text="Seleccione los síntomas presentes:").pack(anchor='w', pady=(10,0))
    # Crear checklist dinámico
    symptom_vars = {}
    for s in sorted({s for req in enfermedades.values() for s in req}):
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame_sint, text=s.replace('_', ' '), variable=var)
        chk.pack(anchor='w')
        symptom_vars[s] = var
    ttk.Button(frame_sint, text="Diagnosticar", command=lambda: messagebox.showinfo(
        "Resultado",
        f"Enfermedad: {diagnosticar_por_sintomas({k for k,v in symptom_vars.items() if v.get()})}"
    )).pack(pady=10)

    # Función para mostrar/ocultar frames
    def switch_mode():
        frame_enf.pack_forget()
        frame_sint.pack_forget()
        if modo_var.get() == 'modo_enf':
            frame_enf.pack(fill='x', pady=20)
        else:
            frame_sint.pack(fill='x', pady=20)

    # Iniciar en modo enfermedad
    switch_mode()

    # Créditos
    ttk.Label(cont, text="© 2025 Nombre 1", font=('Arial', 9), foreground='#666').pack(side='bottom', anchor='e')

    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()
