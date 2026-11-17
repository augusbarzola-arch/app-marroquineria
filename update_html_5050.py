with open("presentacion.html", "r", encoding="utf-8") as f:
    html = f.read()

# Change slide 4 badge to Augusto
html = html.replace(
    '<span class="badge-role int2"><i class="bi bi-person-fill"></i> Lucas Duarte</span>\n            <h2>Arquitectura del Sistema',
    '<span class="badge-role"><i class="bi bi-person-fill"></i> Augusto Barzola</span>\n            <h2>Arquitectura del Sistema'
)

# Update slide 4 notes panel
old_s4_notes = '<div class="notes-panel int2">\n                <strong>Guion Hablado (Lucas Duarte):</strong> "Gracias [Nombre 1]. El sistema sigue una arquitectura por capas limpia y desacoplada.'
new_s4_notes = '<div class="notes-panel">\n                <strong>Guion Hablado (Augusto Barzola):</strong> "La arquitectura del sistema sigue un modelo por capas limpio y desacoplado:'

html = html.replace(old_s4_notes, new_s4_notes)
# Also in case old had Augusto already
html = html.replace('<strong>Guion Hablado (Lucas Duarte):</strong> "Gracias Augusto.', '<strong>Guion Hablado (Augusto Barzola):</strong> "La arquitectura sigue')

with open("presentacion.html", "w", encoding="utf-8") as f:
    f.write(html)

print("presentacion.html successfully updated!")
