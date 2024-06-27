from django.shortcuts import render, redirect
from django.http import HttpResponse
from scripts.manejo_archivos import scan_archivo


import sys
print(sys.path)


def scan(request):
    if request.method == "GET":
        texto = scan_archivo()
        return HttpResponse(texto)

