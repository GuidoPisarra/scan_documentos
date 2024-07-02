from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from scripts.manejo_archivos import *
from django.views.decorators.http import require_GET

import sys
print(sys.path)

@require_GET
def scan(request):
    try:
        pdf_path = r'C:\Users\guidi\OneDrive\Escritorio\scan_documentos\scan_documentos\media\A.pdf'
        datos_unificados = unificar_datos(pdf_path)
        
        # Verificar los datos antes de retornar
        print(datos_unificados)
        
        # Convertir los datos a JSON
        datos_json = json.dumps(datos_unificados, indent=4)
        return JsonResponse(datos_unificados, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

