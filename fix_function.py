import sys

with open("iniciarVentaW.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "def validar_licencia_async(root):" in line:
        new_lines.append(line)
        # Add the new body
        new_lines.append('    """Verifica si el programa superó la fecha límite de uso (Async)."""\n')
        new_lines.append('    # ----------------------------------------------------\n')
        new_lines.append('    # 🔥 CONFIGURA TU FECHA DE CADUCIDAD AQUÍ (Año, Mes, Día)\n')
        new_lines.append('    # ----------------------------------------------------\n')
        new_lines.append('    fecha_caducidad = datetime(2027, 2, 19) \n')
        new_lines.append('    \n')
        new_lines.append('    fecha_actual = obtener_fecha_internet()\n')
        new_lines.append('    \n')
        new_lines.append('    # ¿Qué pasa si justo se corta el internet en la estación?\n')
        new_lines.append('    # Usamos la hora local como "salvavidas" temporal para que puedan cerrar la caja igual.\n')
        new_lines.append('    if not fecha_actual:\n')
        new_lines.append('        fecha_actual = datetime.now()\n')
        new_lines.append('        \n')
        new_lines.append('    if fecha_actual > fecha_caducidad:\n')
        new_lines.append('        def mostrar_error_y_salir():\n')
        new_lines.append('            messagebox.showerror(\n')
        new_lines.append('                "Licencia Expirada", \n')
        new_lines.append('                "El período de uso de este sistema ha finalizado.\n"\n')
        new_lines.append('                "Por favor, contacte al administrador o desarrollador para renovar la licencia."\n')
        new_lines.append('            )\n')
        new_lines.append('            root.destroy()\n')
        new_lines.append('            sys.exit() # Cierra el proceso por completo y no deja abrir la app\n')
        new_lines.append('        \n')
        new_lines.append('        root.after(0, mostrar_error_y_salir)\n')
        skip = True
    elif "def main():" in line:
        skip = False
        new_lines.append(line)
    elif skip:
        continue
    else:
        new_lines.append(line)

with open("iniciarVentaW.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Fixed validar_licencia_async body")
