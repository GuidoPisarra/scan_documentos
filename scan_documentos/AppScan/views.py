from django.shortcuts import render, redirect
from django.http import HttpResponse
from scripts.manejo_archivos import *


import sys
print(sys.path)


def scan(request):
    if request.method == "GET":
        texto = unificar_datos(r'C:\Users\guidi\OneDrive\Escritorio\scan_documentos\scan_documentos\media\A.pdf')
        return HttpResponse(texto)

