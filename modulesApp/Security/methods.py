from random import randint
import re
from .models import User
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None

def change_password(request, password):
    usuario = request.user
    usuario.set_password(password)
    update_session_auth_hash(request, usuario)
    usuario.fecha_ult_cambio = datetime.today()
    usuario.intentos_fallidos = 0
    usuario.save(update_fields=['password','fecha_ult_cambio','intentos_fallidos'])

def get_Random_Code(lenght, onlyNumber = False, onlyMayus = True):
    code = ""
    try:
        for x in range(lenght):
            if onlyNumber:
                code += str(randint(0,9))
            else:
                tipo = 0
                if onlyMayus:
                    tipo = randint(0,1)
                else:
                    tipo = randint(0,2)
                    
                if tipo == 0:#letra mayuscula
                    code += str(chr(randint(65,90)))
                elif tipo == 1:
                    code += str(randint(0,9))
                elif tipo == 2:
                    code += str(chr(randint(97,122)))
    except Exception as e:
        code = "error no generate code "+e.__str__()
    return code
