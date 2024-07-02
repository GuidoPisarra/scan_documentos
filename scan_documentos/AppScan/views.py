from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from scripts.manejo_archivos import *
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from AppScan.forms import *
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

@csrf_exempt
@require_POST
def scan_archivo(request):
    try:
        data = json.loads(request.body)
        form = ScanFormulario(data)
        if form.is_valid():
            archivo_base64 = form.cleaned_data['archivo_base64']
            archivo_bytes = base64.b64decode(archivo_base64)
            
            # Guardar el archivo en la carpeta de medios
            file_name = 'archivo_recibido.pdf'  # Nombre del archivo
            file_path = default_storage.save(file_name, ContentFile(archivo_bytes))
            file_url = default_storage.url(file_path)
            datos_unificados = unificar_datos(file_path)
            archivo_bytes = base64.b64decode(archivo_base64)
            return JsonResponse({'archivo': datos_unificados}, safe=False)  # Convertir bytes a cadena
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

