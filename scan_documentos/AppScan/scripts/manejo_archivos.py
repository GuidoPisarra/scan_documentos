import pdfplumber
import re
import json
import fitz 
# pyzbar para decodificar códigos QR
from pyzbar.pyzbar import decode  
 # Para manipular imágenes
from PIL import Image 
# Para manejar bytes
import io  
import base64
from groq import Groq

def scan_archivo ():
    return "This function scans the user's input and returns the result."


def extract_factura_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    client = Groq(
        api_key="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",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Responde con un JSON que contenga los siguente campos: importe_neto_gravado, iva_27, importe_neto_no_gravado, iva_21, iva_10_5, iva_5, iva_2_5, iva_0, subtotal, importe_otros_tributos, importe_total. Obteniendo informacion del texto: " + text,
            }
        ],
        model="llama3-8b-8192",
    )

    #print(chat_completion.choices[0].message.content)

    # Expresiones regulares para extraer los campos específicos
    importe_neto_gravado_regex = re.compile(r'Importe Neto Gravado:\s*\$ ([\d.,]+)')
    iva_27_regex = re.compile(r'IVA 27%:\s*\$ ([\d.,]+)')
    iva_21_regex = re.compile(r'IVA 21%:\s*\$ ([\d.,]+)')
    iva_105_regex = re.compile(r'IVA 10.5%:\s*\$ ([\d.,]+)')
    iva_5_regex = re.compile(r'IVA 5%:\s*\$ ([\d.,]+)')
    iva_25_regex = re.compile(r'IVA 2.5%:\s*\$ ([\d.,]+)')
    importe_otros_tributos_regex = re.compile(r'Importe Otros Tributos:\s*\$ ([\d.,]+)')
    importe_total_regex = re.compile(r'Importe Total:\s*\$ ([\d.,]+)')
    cae_numero_regex = re.compile(r'CAE N°:\s*([\d]+)')
    vencimiento_cae_regex = re.compile(r'Fecha de Vto. de CAE:\s*([\d\/]+)')

    # Nuevas expresiones regulares para los campos adicionales
    punto_venta_regex = re.compile(r'Punto de Venta:\s*([\d]+)')
    comp_numero_regex = re.compile(r'Comp\. Nro:\s*([\d]+)')
    fecha_emision_regex = re.compile(r'Fecha de Emisión:\s*([\d\/]+)')
    cuit_regex = re.compile(r'CUIT:\s*([\d]+)')
    ingresos_brutos_regex = re.compile(r'Ingresos Brutos:\s*([\d]+)')
    inicio_actividades_regex = re.compile(r'Fecha de Inicio de Actividades:\s*([\d\/]+)')
    periodo_facturado_desde_regex = re.compile(r'Período Facturado Desde:\s*([\d\/]+)')
    periodo_facturado_hasta_regex = re.compile(r'Hasta:\s*([\d\/]+)')
    razon_social_regex = re.compile(r'Razón Social:\s*(.{0,30})')
    domicilio_comercial_regex = re.compile(r'Domicilio Comercial:\s*(.{0,40})')
    condicion_iva_regex = re.compile(r'Condición frente al IVA:\s*(.{0,25})')
    vencimiento_pago_regex = re.compile(r'Fecha de Vto. para el pago:\s*([\d\/]+)')
    cbu_emisor_regex = re.compile(r'CBU del Emisor:\s*([\d]+)')
    alias_cbu_regex = re.compile(r'Alias CBU:\s*(.*)')

    factura_data = {
        "data": {
            "factura": {
                "copia": None,
                "tipo": None,
                "domicilio_comercial": domicilio_comercial_regex.search(text).group(1) if domicilio_comercial_regex.search(text) else None,
                "condicion_frente_iva": condicion_iva_regex.search(text).group(1) if condicion_iva_regex.search(text) else None,
                "punto_venta": punto_venta_regex.search(text).group(1) if punto_venta_regex.search(text) else None,
                "comprobante_numero": comp_numero_regex.search(text).group(1) if comp_numero_regex.search(text) else None,
                "fecha_emision": fecha_emision_regex.search(text).group(1) if fecha_emision_regex.search(text) else None,
                "cuit": cuit_regex.search(text).group(1) if cuit_regex.search(text) else None,
                "ingresos_brutos": ingresos_brutos_regex.search(text).group(1) if ingresos_brutos_regex.search(text) else None,
                "fecha_inicio_actividades": inicio_actividades_regex.search(text).group(1) if inicio_actividades_regex.search(text) else None,
                "periodo_facturado_desde": periodo_facturado_desde_regex.search(text).group(1) if periodo_facturado_desde_regex.search(text) else None,
                "periodo_facturado_hasta": periodo_facturado_hasta_regex.search(text).group(1) if periodo_facturado_hasta_regex.search(text) else None,
                "fecha_vencimiento_pago": vencimiento_pago_regex.search(text).group(1) if vencimiento_pago_regex.search(text) else None,
                "CBU_emisor": cbu_emisor_regex.search(text).group(1) if cbu_emisor_regex.search(text) else None,
                "alias_CBU": alias_cbu_regex.search(text).group(1) if alias_cbu_regex.search(text) else None
            },
            "detalle": {
                "cuit": cuit_regex.search(text).group(1) if cuit_regex.search(text) else None,
                "apellido_nombre_razon_social": razon_social_regex.search(text).group(1) if razon_social_regex.search(text) else None,
                "condicion_frente_iva": condicion_iva_regex.search(text).group(1) if condicion_iva_regex.search(text) else None,
                "domicilio_comercial": domicilio_comercial_regex.search(text).group(1) if domicilio_comercial_regex.search(text) else None,
                "condicion_venta": None,
                "opcion_transferencia": None,
                "detalle_negocio": None
            },
            "totales": {
                "importe_neto_gravado": importe_neto_gravado_regex.search(text).group(1) if importe_neto_gravado_regex.search(text) else None,
                "importe_neto_no_gravado": None,
                "iva_27": iva_27_regex.search(text).group(1) if iva_27_regex.search(text) else None,
                "iva_21": iva_21_regex.search(text).group(1) if iva_21_regex.search(text) else None,
                "iva_10_5": iva_105_regex.search(text).group(1) if iva_105_regex.search(text) else None,
                "iva_5": iva_5_regex.search(text).group(1) if iva_5_regex.search(text) else None,
                "iva_2_5": iva_25_regex.search(text).group(1) if iva_25_regex.search(text) else None,
                "iva_0": None,
                "subtotal": None,
                "importe_otros_tributos": importe_otros_tributos_regex.search(text).group(1) if importe_otros_tributos_regex.search(text) else None,
                "importe_total": importe_total_regex.search(text).group(1) if importe_total_regex.search(text) else None,
                "perRet_impuesto_ganancias": None,
                "perRet_iva": None,
                "perRet_ingresos_brutos": None,
                "impuestos_internos": None,
                "impuestos_municipales": None
            },
            "footer": {
                "cae_numero": cae_numero_regex.search(text).group(1) if cae_numero_regex.search(text) else None,
                "vencimiento_cae": vencimiento_cae_regex.search(text).group(1) if vencimiento_cae_regex.search(text) else None
            }
        }
    }

    return factura_data

def extract_qr_from_pdf(pdf_path):
    # Abrir el documento PDF con PyMuPDF
    document = fitz.open(pdf_path)
    
    qr_codes = []  # Lista para almacenar los códigos QR encontrados
    
    # Solo procesar la primera página del documento
    page_num = 0
    page = document.load_page(page_num)
    
    # Extraer todas las imágenes de la página
    images = page.get_images(full=True)
    
    # Iterar sobre las imágenes extraídas
    for img_info in images:
        xref = img_info[0]  # Referencia cruzada de la imagen
        base_image = document.extract_image(xref)
        image_bytes = base_image["image"]
        
        # Convertir los bytes a un objeto de tipo Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Decodificar el código QR usando pyzbar
        qr_codes_found = decode(image)
        
        # Agregar los datos del código QR encontrado a la lista
        for qr_code in qr_codes_found:
            qr_data = qr_code.data.decode('utf-8')
            qr_codes.append(qr_data)

    return qr_codes

def unificar_datos(pdf_path):
    factura_data = extract_factura_data(pdf_path)
    qr_codes = extract_qr_from_pdf(pdf_path)
    
    qr_data_decoded = None
    
    if qr_codes:
        for qr_code in qr_codes:
            # Obtener el parámetro codificado desde la URL
            parametro_base64 = qr_code.split('?p=')[1]
            
            # Decodificar el parámetro base64
            parametro_decodificado = base64.b64decode(parametro_base64).decode('utf-8')
            
            # Convertir a JSON
            qr_data_decoded = json.loads(parametro_decodificado)
            

            # Fusionar los datos del QR con los datos de la factura
            factura_data['data']['factura']['fecha_emision'] = qr_data_decoded.get('fecha')
            factura_data['data']['factura']['cuit'] = qr_data_decoded.get('cuit')
            factura_data['data']['factura']['punto_venta'] = qr_data_decoded.get('ptoVta')
            factura_data['data']['factura']['tipo'] = qr_data_decoded.get('tipoCmp')
            factura_data['data']['factura']['comprobante_numero'] = qr_data_decoded.get('nroCmp')
            factura_data['data']['totales']['importe_total'] = qr_data_decoded.get('importe')
            factura_data['data']['footer']['cae_numero'] = qr_data_decoded.get('codAut')

            print(qr_data_decoded)
            # Agregar los datos decodificados del QR a los datos de la factura
            #factura_data['data']['qr'] = qr_data_decoded

    return factura_data

# Ejemplo de uso
if __name__ == "__main__":
    pdf_path = "A.pdf"  # Ruta al archivo PDF que deseas analizar
    datos_unificados = unificar_datos(pdf_path)
    
    # Convertir a JSON
    datos_json = json.dumps(datos_unificados, indent=4)
    print(datos_json)