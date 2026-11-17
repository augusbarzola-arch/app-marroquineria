import re

with open("2_Guion_Hablado.md", "r", encoding="utf-8") as f:
    text = f.read()

# Replace placeholders
text = text.replace("[Nombre 1]", "Augusto Barzola")
text = text.replace("[Nombre 2]", "Lucas Duarte")
text = text.replace("[INT. 1:]", "🎤 [AUGUSTO BARZOLA]:")
text = text.replace("[INT. 2:]", "🎤 [LUCAS DUARTE]:")
text = text.replace("INT. 1 -> Integrante 1 habla", "Augusto Barzola -> Base de Datos, DER, Triggers, Optimización")
text = text.replace("INT. 2 -> Integrante 2 habla", "Lucas Duarte -> Arquitectura, UI/UX, IA asistida, Conclusiones")

with open("2_Guion_Hablado.md", "w", encoding="utf-8") as f:
    f.write(text)

print("2_Guion_Hablado.md updated with real names!")
