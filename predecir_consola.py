"""
Clasificador de spam desde consola (sin Streamlit).

Requisitos:
  - modelo_spam.joblib
  - vectorizador.joblib
  (generados con: python entrenar.py)

Uso:
  python predecir_consola.py
  python predecir_consola.py "texto del correo aquí"
"""

import sys
from pathlib import Path

import joblib

BASE_DIR = Path(__file__).parent
MODELO_PATH = BASE_DIR / "modelo_spam.joblib"
VECTORIZADOR_PATH = BASE_DIR / "vectorizador.joblib"


def cargar_ia():
    if not MODELO_PATH.exists() or not VECTORIZADOR_PATH.exists():
        print("❌ Faltan 'modelo_spam.joblib' o 'vectorizador.joblib'.")
        print("💡 Ejecutá primero: python entrenar.py")
        sys.exit(1)
    modelo = joblib.load(MODELO_PATH)
    vectorizador = joblib.load(VECTORIZADOR_PATH)
    return modelo, vectorizador


def clasificar(modelo, vectorizador, texto: str) -> str:
    texto = texto.strip()
    if not texto:
        return "⚠️ El texto está vacío."
    texto_num = vectorizador.transform([texto])
    prediccion = modelo.predict(texto_num)[0]
    if prediccion == 1:
        return "🚨 SPAM"
    return "✅ LEGÍTIMO"


def main():
    modelo, vectorizador = cargar_ia()

    # Si pasaste el correo como argumento: python predecir_consola.py "hola..."
    if len(sys.argv) > 1:
        texto = " ".join(sys.argv[1:])
        print(clasificar(modelo, vectorizador, texto))
        return

    # Modo interactivo
    print("Filtro Anti-Spam (consola)")
    print("Escribí un correo y Enter. Vacío + Enter para salir.\n")
    while True:
        try:
            texto = input("Correo> ")
        except (EOFError, KeyboardInterrupt):
            print("\nChau.")
            break
        if not texto.strip():
            print("Chau.")
            break
        print(clasificar(modelo, vectorizador, texto))
        print()


if __name__ == "__main__":
    main()
