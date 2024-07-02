from django import forms
import base64

class ScanFormulario(forms.Form):
    archivo_base64 = forms.CharField(max_length=10000000) 

    def clean_archivo_base64(self):
        data = self.cleaned_data['archivo_base64']
        
        try:
            base64.b64decode(data)
        except (TypeError, ValueError):
            raise forms.ValidationError("El archivo no está correctamente codificado en base64.")
        
        return data