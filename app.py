from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps

app = Flask(__name__)
app.secret_key = 'CambiaEstaClavePorUnaSegura'

# ----------------------------
# Base de conocimientos: pacientes y sus síntomas
# ----------------------------
patients = {
    "lulu": ["fiebre", "dolor_de_garganta", "tos"],
    "pablo": ["fiebre", "dolor_muscular", "dolor_de_cabeza"],
    "lupita": ["estornudos", "congestion_nasal", "ojos_llorosos"],
    "ciro": ["dolor_de_cabeza", "sensibilidad_a_la_luz"]
}

# ----------------------------
# Base de conocimientos médicos para recomendaciones
# ----------------------------
medical_knowledge = {
    "Gripe": {
        "recomendaciones": [
            "Mantener reposo en cama",
            "Beber abundantes líquidos",
            "Tomar paracetamol para la fiebre",
            "Evitar lugares concurridos",
            "Consultar médico si empeoran los síntomas"
        ],
        "medicamentos": [
            {"nombre": "Paracetamol", "dosis": "500mg cada 8 horas", "duracion": "3-5 días"},
            {"nombre": "Ibuprofeno", "dosis": "400mg cada 8 horas", "duracion": "3-4 días"},
            {"nombre": "Jarabe para la tos", "dosis": "15ml cada 6 horas", "duracion": "Según necesidad"}
        ],
        "especialistas": ["Médico General", "Medicina Interna"]
    },
    "Resfriado": {
        "recomendaciones": [
            "Descansar lo suficiente",
            "Beber líquidos calientes",
            "Usar humidificador",
            "Evitar cambios bruscos de temperatura",
            "Lavarse las manos frecuentemente"
        ],
        "medicamentos": [
            {"nombre": "Descongestionante nasal", "dosis": "2 gotas cada 8 horas", "duracion": "3-5 días"},
            {"nombre": "Antihistamínico", "dosis": "10mg cada 12 horas", "duracion": "5-7 días"},
            {"nombre": "Vitamina C", "dosis": "1000mg al día", "duracion": "7 días"}
        ],
        "especialistas": ["Médico General", "Otorrinolaringólogo"]
    },
    "Faringitis": {
        "recomendaciones": [
            "Hacer gárgaras con agua tibia y sal",
            "Evitar alimentos irritantes",
            "Mantener la garganta húmeda",
            "No fumar ni exponerse al humo",
            "Descansar la voz"
        ],
        "medicamentos": [
            {"nombre": "Antibiótico", "dosis": "Según prescripción médica", "duracion": "7-10 días"},
            {"nombre": "Analgésico", "dosis": "500mg cada 6 horas", "duracion": "3-5 días"},
            {"nombre": "Antiséptico bucal", "dosis": "Cada 4 horas", "duracion": "5-7 días"}
        ],
        "especialistas": ["Médico General", "Otorrinolaringólogo"]
    },
    "Migraña": {
        "recomendaciones": [
            "Descansar en habitación oscura y silenciosa",
            "Aplicar compresas frías en la frente",
            "Mantener horarios regulares de sueño",
            "Evitar factores desencadenantes",
            "Practicar técnicas de relajación"
        ],
        "medicamentos": [
            {"nombre": "Sumatriptán", "dosis": "50mg al inicio del dolor", "duracion": "Según necesidad"},
            {"nombre": "Ibuprofeno", "dosis": "600mg cada 8 horas", "duracion": "2-3 días"},
            {"nombre": "Relajante muscular", "dosis": "Según prescripción", "duracion": "Según necesidad"}
        ],
        "especialistas": ["Neurólogo", "Médico General"]
    }
}

# ----------------------------
# Médicos cercanos simulados
# ----------------------------
doctors_nearby = [
    {
        "nombre": "Dr. Juan Carlos Mendoza",
        "especialidad": "Médico General",
        "direccion": "Av. Independencia 123, Córdoba, Ver.",
        "telefono": "271-123-4567",
        "rating": 4.8,
        "distancia": "0.5 km",
        "lat": 18.8861,
        "lng": -96.9206
    },
    {
        "nombre": "Dra. María Elena Ruiz",
        "especialidad": "Medicina Interna",
        "direccion": "Calle 5 de Mayo 456, Córdoba, Ver.",
        "telefono": "271-234-5678",
        "rating": 4.9,
        "distancia": "1.2 km",
        "lat": 18.8871,
        "lng": -96.9216
    },
    {
        "nombre": "Dr. Roberto Silva",
        "especialidad": "Otorrinolaringólogo",
        "direccion": "Blvd. Córdoba 789, Córdoba, Ver.",
        "telefono": "271-345-6789",
        "rating": 4.7,
        "distancia": "2.1 km",
        "lat": 18.8881,
        "lng": -96.9226
    },
    {
        "nombre": "Dra. Ana Patricia López",
        "especialidad": "Neurólogo",
        "direccion": "Av. 20 de Noviembre 321, Córdoba, Ver.",
        "telefono": "271-456-7890",
        "rating": 4.6,
        "distancia": "2.8 km",
        "lat": 18.8891,
        "lng": -96.9236
    }
]

# ----------------------------
# Funciones del sistema experto
# ----------------------------
def diagnosticar(persona):
    s = set(patients.get(persona, []))
    if {"fiebre", "dolor_muscular", "dolor_de_cabeza"}.issubset(s):
        return "Gripe"
    if {"estornudos", "congestion_nasal", "ojos_llorosos"}.issubset(s):
        return "Resfriado"
    if {"fiebre", "dolor_de_garganta", "tos"}.issubset(s):
        return "Faringitis"
    if {"dolor_de_cabeza", "sensibilidad_a_la_luz"}.issubset(s):
        return "Migraña"
    return "Sin diagnóstico claro"

def diagnosticar_sintomas(sintomas):
    """Diagnostica basado en una lista de síntomas libres (texto)"""
    s = set([sintoma.lower().replace(' ', '_') for sintoma in sintomas])
    if {"fiebre", "dolor_muscular", "dolor_de_cabeza"}.issubset(s):
        return "Gripe"
    if {"estornudos", "congestion_nasal", "ojos_llorosos"}.issubset(s):
        return "Resfriado"
    if {"fiebre", "dolor_de_garganta", "tos"}.issubset(s):
        return "Faringitis"
    if {"dolor_de_cabeza", "sensibilidad_a_la_luz"}.issubset(s):
        return "Migraña"
    return "Sin diagnóstico claro"

def get_doctors_by_specialty(specialties):
    """Filtra doctors_nearby por lista de especialidades"""
    if not specialties:
        return doctors_nearby
    filtered = []
    for doc in doctors_nearby:
        if any(spec in doc["especialidad"] for spec in specialties):
            filtered.append(doc)
    return filtered if filtered else doctors_nearby

# ----------------------------
# Usuarios de ejemplo para login
# ----------------------------
auth_users = {"admin": "pass123", "doctor": "medico456"}

# ----------------------------
# Decorador de autenticación
# ----------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            flash('Por favor, inicia sesión primero.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ----------------------------
# Rutas de autenticación
# ----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username', '')
        p = request.form.get('password', '')
        if auth_users.get(u) == p:
            session['username'] = u
            return redirect(url_for('patients_view'))
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username')
    return redirect(url_for('login'))

# ----------------------------
# Página de inicio: redirige a /patients
# ----------------------------
@app.route('/')
@login_required
def home():
    return redirect(url_for('patients_view'))

# ----------------------------
# Lista de pacientes + Diagnóstico por paciente
# ----------------------------
@app.route('/patients')
@login_required
def patients_view():
    return render_template('patients.html', patients=patients, diagnosticar=diagnosticar)

# ----------------------------
# Agregar nuevo paciente
# ----------------------------
@app.route('/patients/new', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        # Evitar KeyError usando .get()
        name = request.form.get('name', '').lower().strip()
        syms = [
            s.strip().replace(' ', '_').lower()
            for s in request.form.get('symptoms', '').split(',')
            if s.strip()
        ]
        if name and syms:
            patients[name] = syms
            flash(f'Paciente {name.capitalize()} registrado 👍', 'success')
            return redirect(url_for('patients_view'))
        flash('Todos los campos son obligatorios', 'warning')
    return render_template('add_patient.html')

# ----------------------------
# Búsquedas de diagnóstico (persona, diagnóstico, síntoma)
# ----------------------------
@app.route('/diagnosis', methods=['GET', 'POST'])
@login_required
def diagnosis():
    results = []
    # Datos para dropdowns dinámicos
    diagnoses_set = sorted({ diagnosticar(p) for p in patients })
    symptoms_set = sorted({ s for syms in patients.values() for s in syms })

    if request.method == 'POST':
        st = request.form.get('search_type', '')
        q = request.form.get('query', '').lower().replace(' ', '_')
        if st == 'persona' and q in patients:
            results = [ (q.capitalize(), patients[q], diagnosticar(q)) ]
        elif st == 'diagnostico':
            for p in patients:
                if diagnosticar(p).lower() == q:
                    results.append( (p.capitalize(), patients[p], diagnosticar(p)) )
        elif st == 'sintoma':
            for p, syms in patients.items():
                if q in syms:
                    results.append( (p.capitalize(), patients[p], diagnosticar(p)) )

    return render_template(
        'diagnosis.html',
        results=results,
        patients=patients,
        diagnoses=diagnoses_set,
        symptoms=symptoms_set
    )

# ----------------------------
# Portal de consultas para pacientes (diagnóstico por síntomas libres)
# ----------------------------
@app.route('/patient-portal', methods=['GET', 'POST'])
@login_required
def patient_portal():
    diagnosis_result = None
    recommendations = None
    medications = None
    nearby_doctors = None

    if request.method == 'POST':
        symptoms_input = request.form.get('symptoms', '').strip()
        symptoms_list = [ s.strip() for s in symptoms_input.split(',') if s.strip() ]

        if symptoms_list:
            # Diagnóstico basado en texto libre
            diagnosis_result = diagnosticar_sintomas(symptoms_list)

            # Si existe en medical_knowledge, obtener detalles
            if diagnosis_result in medical_knowledge:
                info = medical_knowledge[diagnosis_result]
                recommendations = info["recomendaciones"]
                medications = info["medicamentos"]
                specialties = info["especialistas"]
                nearby_doctors = get_doctors_by_specialty(specialties)
            else:
                nearby_doctors = doctors_nearby

            flash(f'Diagnóstico preliminar: {diagnosis_result}', 'info')
        else:
            flash('Por favor, ingrese al menos un síntoma', 'warning')

    return render_template(
        'patient_portal.html',
        diagnosis=diagnosis_result,
        recommendations=recommendations,
        medications=medications,
        doctors=nearby_doctors
    )

# ----------------------------
# API: médicos en JSON (filtrado por especialidad opcional)
# ----------------------------
@app.route('/api/doctors')
@login_required
def api_doctors():
    specialty = request.args.get('specialty', '').strip()
    if specialty:
        filtered = get_doctors_by_specialty([specialty])
        return jsonify(filtered)
    return jsonify(doctors_nearby)

# ----------------------------
# Ejecutar servidor
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
