from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'CambiaEstaClavePorUnaSegura'

# Base de conocimientos: pacientes y sus síntomas
patients = {
    "lulu": ["fiebre", "dolor_de_garganta", "tos"],
    "pablo": ["fiebre", "dolor_muscular", "dolor_de_cabeza"],
    "lupita": ["estornudos", "congestion_nasal", "ojos_llorosos"],
    "ciro": ["dolor_de_cabeza", "sensibilidad_a_la_luz"]
}

# Funciones del sistema experto

def diagnosticar(persona):
    s = set(patients.get(persona, []))
    if {"fiebre","dolor_muscular","dolor_de_cabeza"}.issubset(s): return "Gripe"
    if {"estornudos","congestion_nasal","ojos_llorosos"}.issubset(s): return "Resfriado"
    if {"fiebre","dolor_de_garganta","tos"}.issubset(s): return "Faringitis"
    if {"dolor_de_cabeza","sensibilidad_a_la_luz"}.issubset(s): return "Migraña"
    return "Sin diagnóstico claro"

# Usuarios de ejemplo para login
users = {"admin": "pass123", "doctor": "medico456"}

# Decorador de autenticación
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            flash('Por favor, inicia sesión primero.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if users.get(u) == p:
            session['username'] = u
            return redirect(url_for('patients_view'))
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return redirect(url_for('patients_view'))

@app.route('/patients')
@login_required
def patients_view():
    return render_template('patients.html', patients=patients, diagnosticar=diagnosticar)

@app.route('/patients/new', methods=['GET','POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form['name'].lower().strip()
        syms = [s.strip().replace(' ', '_').lower() for s in request.form['symptoms'].split(',') if s.strip()]
        if name and syms:
            patients[name] = syms
            flash(f'Paciente {name.capitalize()} registrado 👍', 'success')
            return redirect(url_for('patients_view'))
        flash('Todos los campos son obligatorios', 'warning')
    return render_template('add_patient.html')

@app.route('/diagnosis', methods=['GET','POST'])
@login_required
def diagnosis():
    results = []
    if request.method == 'POST':
        st = request.form['type']
        q = request.form['query'].lower().replace(' ', '_')
        if st == 'persona' and q in patients:
            results = [(q.capitalize(), ', '.join(patients[q]), diagnosticar(q))]
        elif st == 'diagnostico':
            for p in patients:
                if diagnosticar(p).lower() == q:
                    results.append((p.capitalize(), ', '.join(patients[p]), diagnosticar(p)))
        elif st == 'sintoma':
            for p, syms in patients.items():
                if q in syms:
                    results.append((p.capitalize(), ', '.join(syms), diagnosticar(p)))
    return render_template('diagnosis.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)