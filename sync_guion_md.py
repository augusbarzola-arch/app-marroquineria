with open("generate_academic_docx.py", "r", encoding="utf-8") as f:
    code = f.read()

# Extraer el array de slides_academic
start_str = "slides_academic = ["
end_str = "    for num, title, speaker, timing, text in slides_academic:"
start = code.find(start_str)
end = code.find(end_str)
slides_code = code[start:end]

exec(slides_code)

md_out = """# 🎙️ GUION HABLADO OFICIAL — DEFENSA DE BASES DE DATOS (50% / 50%)
### Sistema de Gestión Comercial para Marroquinería
**Disertantes:** Augusto Barzola & Lucas Duarte  
**Duración total estimada:** 12 - 14 minutos (~6.5 minutos cada uno)  
**Tono:** Académico formal, riguroso, seguro y enfocado en SGBD

---

## 📊 TABLA DE DISTRIBUCIÓN EQUITATIVA (50% / 50%)

| Bloque | Disertante | Diapositivas | Ejes Conceptuales de Base de Datos | Tiempo |
|---|---|---|---|---|
| **PRIMERA MITAD** | **Augusto Barzola** | **Slides 1 a 7** (7 diapositivas) | • Contexto de Negocio y Dominio de Datos<br>• Agenda de Exposición Académica<br>• Justificación del Motor Relacional (ACID)<br>• Arquitectura de Acceso a Datos y Capas Transaccionales<br>• Modelo de Datos — DER (13 tablas relacionales)<br>• Teoría de Normalización (1FN, 2FN, 3FN)<br>• Triggers en PL/pgSQL y Reglas de Negocio en Motor | **~6.5 min** |
| **SEGUNDA MITAD** | **Lucas Duarte** | **Slides 8 a 13** (6 diapositivas) | • Integridad Referencial: FK Compuesta en Devolución<br>• Consultas Complejas y Álgebra Relacional (Push-Down)<br>• Fundamentación Técnica: SQL Directo vs ORM (ACID)<br>• Interfaz de Acceso a Datos como Cliente Transaccional<br>• Metodología de Diseño y Rol Asistencial de la IA<br>• Conclusiones Académicas y Preguntas de Cátedra | **~6.5 min** |

---
"""

for num, title, speaker, timing, text in slides_academic:
    md_out += f"\n## DIAPOSITIVA {num}: {title}\n"
    md_out += f"- **Disertante:** {speaker}\n"
    md_out += f"- **Tiempo sugerido:** {timing}\n\n"
    md_out += f"> \"{text.replace(chr(10), chr(10) + '> ')}\"\n\n---\n"

with open("2_Guion_Hablado.md", "w", encoding="utf-8") as f:
    f.write(md_out)

print("2_Guion_Hablado.md synchronized successfully with academic docx!")
