def format_single_lab_result(data: dict) -> str:
    """Formatea un resultado de laboratorio individual"""
    
    response = (
        f"RESULTADOS DE LABORATORIO\n"
        f"========================\n\n"
        f"Orden ID: {data.get('orden_id')}\n"
        f"Paciente: {data.get('nombre_paciente')}\n"
        f"Cédula: {data.get('cedula')}\n"
        f"Fecha de orden: {data.get('fecha_orden').strftime('%d/%m/%Y')}\n"
        f"Fecha de resultado: {data.get('fecha_resultado').strftime('%d/%m/%Y')}\n"
        f"Estado: {data.get('estado')}\n"
        f"Tipo: {data.get('tipo_examen')}\n"
        f"Medico solicitante: {data.get('medico_solicitante')}\n\n"
    )
    
    # Agregar examenes individuales
    response += "EXAMENES:\n"
    response += "-" * 80 + "\n"
    
    for examen in data.get('examenes', []):
        estado = examen.get('estado_resultado', 'Normal')
        alerta = ""
        
        if estado == "Alto":
            alerta = " [ALTO]"
        elif estado == "Bajo":
            alerta = " [BAJO]"
        elif estado == "Critico":
            alerta = " [CRITICO - REQUIERE ATENCION]"
        
        response += (
            f"\n{examen.get('nombre_examen')}{alerta}\n"
            f"  Resultado: {examen.get('resultado_valor')} {examen.get('unidad', '')}\n"
            f"  Rango referencia: {examen.get('valor_referencia_min')} - {examen.get('valor_referencia_max')} {examen.get('unidad', '')}\n"
            f"  Metodo: {examen.get('metodo', 'N/A')}\n"
        )
    
    # Agregar observaciones si existen
    if data.get('observaciones'):
        response += f"\n\nObservaciones:\n{data.get('observaciones')}\n"
    
    response += "\n" + "=" * 80 + "\n"
    response += "Nota: Estos resultados deben ser interpretados por su medico tratante.\n"
    
    return response


def format_multiple_lab_results(ordenes: list) -> str:
    """Formatea multiples resultados de laboratorio"""
    
    response = (
        f"Se encontraron {len(ordenes)} ordenes de laboratorio:\n"
        f"{'=' * 80}\n\n"
    )
    
    for i, orden in enumerate(ordenes, 1):
        estado_icon = "✓" if orden.get('estado') == "Disponible" else "⏳"
        
        response += (
            f"{i}. {estado_icon} Orden: {orden.get('orden_id')}\n"
            f"   Fecha: {orden.get('fecha_orden').strftime('%d/%m/%Y')}\n"
            f"   Tipo: {orden.get('tipo_examen')}\n"
            f"   Estado: {orden.get('estado')}\n"
            f"   Examenes: {len(orden.get('examenes', []))} pruebas\n\n"
        )
    
    response += (
        "\nPara ver el detalle completo de una orden especifica, "
        "proporciona el ID de la orden que deseas consultar.\n"
    )
    
    return response