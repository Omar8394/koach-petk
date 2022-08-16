from random import randint
import hashlib
import re
from .models import User,CodigoVerificacion
from django.contrib.auth import update_session_auth_hash, authenticate
from datetime import datetime
from modulesApp.Comunication.methods import create_mail, send_mail

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

def restablecer_cuenta(user):
    user.is_active = True
    user.intentos_fallidos = 0
    user.save()

def get_status_user(username, password):
    status_user = {}
    fail = False
    user = authenticate(username=username, password=password)
    if user is None:
        fail = True
        user = User.objects.get(username=username)   
        if user.is_active:
            user.intentos_fallidos = user.intentos_fallidos + 1
            user.save()
            status_user['estado'] = "Invalid Credencial"
            status_user['mensaje'] = "Usuario o contraseña invalidos tenga en \
                                            cuenta que podria ser bloqueado si excede el numero maximo de intentos"
    
    if not user.is_active and user.intentos_fallidos < 3:
        status_user['estado'] = "Account Suspended"
        status_user['mensaje'] ="Su cuenta ha sido suspendida para mas informacion contacte al soporte."  
    elif user.intentos_fallidos >= 3:
        user.is_active = False
        status_user['estado'] = "Account Blocked"
        status_user['mensaje'] = "Su cuenta ha sido bloqueada por exceder el numero maximo \
                                    de intentos de inicio de sesion. Intente recuperar su cuenta en la opcion de \
                                        'olvido de contrañsea o cuenta bloqueada'."    
    elif not fail:
        status_user['estado'] = "Active"
        status_user['mensaje'] ="Logueado Correctamente"
        restablecer_cuenta(user)
    status_user['user'] = user          
    return status_user

def get_verification_code(user,expirationtime,tipo):
    try:
        x = get_Random_Code(8)
        code = str(x) + user.email
        h = hashlib.sha1(code.encode())
        salt = h.hexdigest()
        activation_key = hashlib.sha1(str(salt + code).encode()).hexdigest()
        key_expires = datetime.today() + timedelta(days=expirationtime)
        # key_expires = datetime.strptime(key_expires, '%Y-%m-%d %H:%M:%S')
        EnlaceVerificacion.objects.create(activation_key=activation_key, key_expires=key_expires,
                                                        usuario=user,tipo=tipo)
        return activation_key
    except Exception as e:
        print("error al generar el codigo de verificacion")
        return None
    
def send_vefication_code_email(user,asunto,contenido,tipo):
    code = get_verification_code(user, 3, tipo)
    if code != None: 
        context = {"titulo": "Validacion de Operaciones",
                                    "content": "Hemos generado un codigo de verificacion para que puedas continuar\
                                        con tus operaciones de"+ tipo + "introduce el siguiente codigo en el formulario\
                                            solicitado:"}
        send_mail(create_mail(user, asunto,context))
    else:
         print("error al generar el codigo de verificacion de cuenta")
        
    

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
