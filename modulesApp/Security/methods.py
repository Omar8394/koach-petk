from random import randint
import hashlib
import re
from .models import User,CodigoVerificacion
from django.contrib.auth import update_session_auth_hash, authenticate
from datetime import datetime, timedelta
from modulesApp.Comunication.methods import create_mail, send_mail
from modulesApp.App.models import ConfTablasConfiguracion

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
    user.fk_status_cuenta = ConfTablasConfiguracion.objects.filter(valor_elemento="user_active")[0]
    user.save()

def intentos_fallidos(user):
    if user.is_active and user.intentos_fallidos < 3:
        user.intentos_fallidos = user.intentos_fallidos + 1
        user.save()
    elif user.is_active and user.intentos_fallidos >= 3:
        user.is_active = False
        user.fk_status_cuenta = ConfTablasConfiguracion.objects.filter(valor_elemento="user_account_blocked")[0]
        user.save()
    elif not user.is_active:
        user.fk_status_cuenta = ConfTablasConfiguracion.objects.filter(valor_elemento="user_account_suspended")[0]
        user.save()
        
        

def get_status_user(cuenta):
    status_user = {} 
    user = is_user_exists(cuenta)
    if user is None:
        status_user['estado'] = "Invalid Account"
        status_user['mensaje'] = "El Usuario o correo proporcionados no estan asociados a ninguna cuenta."
    else:
        status_user['estado'] = str(user.fk_status_cuenta.valor_elemento).\
        replace("user", "").replace("_", " ").lstrip().capitalize()
        status_user['mensaje'] = str(user.fk_status_cuenta.desc_elemento)
    status_user['user'] = user      
    return status_user

def auth_user(cuenta, password):
    status_user = get_status_user(cuenta)
    print("cuenta ",cuenta)
    print(status_user)
    if status_user['estado'] == "Active":
        user_aux = authenticate(username=status_user['user'].username, password=password)
        if user_aux is None:
            intentos_fallidos(status_user['user'])
            status_user['estado'] = "Invalid Credencial"
            status_user['mensaje'] = "Usuario o contraseña invalidos tenga en \
                                        cuenta que podria ser bloqueado si excede el numero maximo de intentos"
        else:
            restablecer_cuenta(status_user['user'])
    return status_user 
                      
            

def is_user_exists(cuenta):
    user = None
    try:
        if es_correo_valido(cuenta):
            user = User.objects.filter(email=cuenta)[0]
        else:
            user = User.objects.filter(username=cuenta)[0]
    except Exception as e:
        pass
    return user

def get_verification_code(user,expirationtime,tipo):
    try:
        x = get_Random_Code(8)
        code = str(x) + user.email
        h = hashlib.sha1(code.encode())
        salt = h.hexdigest()
        activation_key = hashlib.sha1(str(salt + code).encode()).hexdigest()
        key_expires = datetime.today() + timedelta(days=expirationtime)
        CodigoVerificacion.objects.create(activation_key=activation_key, key_expires=key_expires,
                                                        usuario=user, tipo_verificacion=tipo)
        return activation_key
    except Exception as e:
        print("error al generar el codigo de verificacion", e)
        return None
    
def verificarenlace(key_expires):
    formato = "%Y-%m-%d %H:%M:%S"
    return datetime.strftime(key_expires, formato) >= datetime.now().strftime(formato)

def change_password_link(enlace, password):
    enlace.user.set_password(password)
    enlace.save()
    enlace.delete()
    # validar las claves anteriores
    restabler_cuenta(enlace.user)
    
def send_vefication_code_email(user,asunto,contenido,tipo):
    code = get_verification_code(user, 3, tipo)
    if code != None: 
        context = {"titulo": "Validacion de Operaciones",
                                    "content":contenido if contenido else "Hemos generado un codigo de verificacion para que puedas continuar\
                                    con tus operaciones de"+ tipo.desc_elemento + "introduce el siguiente codigo: "+code+" en el formulario\
                                    solicitado: Si no solicitaste este código, puedes hacer caso omiso de este mensaje de correo electrónico.\
                                    Otra persona puede haber escrito tu dirección de correo electrónico por error."}
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
