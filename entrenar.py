from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

print("--- Iniciando proceso de entrenamiento ---")

# 1. CARGAR LA MATERIA PRIMA
try:
    df = pd.read_csv('correos.csv', encoding='utf-8')
    print("✅ Archivo 'correos.csv' cargado con éxito.")
except FileNotFoundError:
    print("❌ Error: No se encontró 'correos.csv'. Ejecuta primero el script para generar los datos.")
    exit()

# 2. SEPARAR CARACTERÍSTICAS (X) E ETIQUETA (y)
X = df['texto']  # El texto del correo
y = df['spam']   # El resultado (1 o 0)

# 3. DIVIDIR EN TRAINING SET (75%) Y TEST SET (25%)
X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 4. EXTRAER CARACTERÍSTICAS (NLP: Traducir texto a números)
vectorizador = CountVectorizer()
X_entrenamiento_num = vectorizador.fit_transform(X_entrenamiento)
X_prueba_num = vectorizador.transform(X_prueba)

# 5 Y 7. ENTRENAR EL MODELO + AJUSTE DE HIPERPARÁMETROS
# Usamos GridSearchCV para buscar automáticamente si funciona mejor con 50, 100 o 150 árboles
print("Buscando la mejor configuración del algoritmo...")
parametros = {'n_estimators': [50, 100, 150]}

optimizador = GridSearchCV(RandomForestClassifier(random_state=42), parametros, cv=3)
optimizador.fit(X_entrenamiento_num, y_entrenamiento)

# Nos quedamos con el mejor modelo ganador
modelo_optimizado = optimizador.best_estimator_
print(f"Mejor configuración encontrada: {optimizador.best_params_}")

# 6. MEDIR LA MÉTRICA DE PRECISIÓN (Examen sorpresa)
predicciones = modelo_optimizado.predict(X_prueba_num)
precision = accuracy_score(y_prueba, predicciones)
print(f"🎯 Porcentaje de aciertos de la IA (Accuracy): {precision * 100:.1f}%")

# 8. GUARDAR EL MODELO ENTRENADO CON JOBLIB
joblib.dump(modelo_optimizado, 'modelo_spam.joblib', compress=3)
joblib.dump(vectorizador, 'vectorizador.joblib', compress=3)

print("💾 ¡Archivos 'modelo_spam.joblib' y 'vectorizador.joblib' generados con éxito!")
print("--- Proceso finalizado ---")
