#!/usr/bin/python
import smtplib, ssl ,time ,os, sys, re, datetime
#Options
refreshTime = 5 # in seconds
LANGUAGE= "es"
#List of websites where consult external IP
weblist=(   "https://api.ipify.org",
            "https://ifconfig.me",
            "https://https://ident.me",
            "https://checkip.amazonaws.co"
            "http://bot.whatismyipaddress.com",
            "http://icanhazip.com",
            "http://ipinfo.io/ip",
            "http://ident.me",
            "http://ipecho.net/plain",
            "http://whatismyip.akamai.com",
            "http://tnx.nl/ip",
            "http://myip.dnsomatic.com",
        )

#Language Traslations
notifications={
    "es":{
    "TEXT_name":"Español",
    "TEXT_alert":"Alerta.",
    "TEXT_port" :"Puerto",
    "TEXT_servermail":"Email del servidor",
    "TEXT_password":"Contraseña",
    "TEXT_serveraddres":"Dirección del servidor",
    "TEXT_reciver_mail":"Email de Notificación",
    "INFO_ip_changed":"Cambio de IP.",
    "INFO_start_service":"Servicio FKYUISP inicializado.",
    "INFO_initi_config":"No se ha encontrado configuración previa.Se procederá a la configuración:",
    "INFO_exit":"Servicio finalizado por el usuario.",
    "INFO_waiting":"Analizando por si cambia la ip. Te mantendré informado.",
    "INFO_actual_ip":"La ip publica actual es %s devuelta por %s.",
    "INSERT_port":"Introduce el puerto del servidor de correo:",
    "INSERT_servermail":"Introduce del correo del servidor:",
    "INSERT_password":"Introduce la contraseña del servidor:",
    "INSERT_serveraddress":"Introduce la dirección del servidor:",
    "INSERT_recivermail":"Introduce el correo donde recibir las notificaciones:",
    "INSERT_use_conf":"Desea usar esta configuración: [y/n]",
    "INSERT_save_conf":"Desea guardar la configuración: [y/n]",
    "ERROR_lang" : "Error de lenguaje - Lenguaje no soportado.\nLista de lenguajes:",
    "ERROR_previus_config":"No existe configuración guardada.",
    "ERROR_port":"El puerto introducido no es un número o no esta en el rango 0-65535.",
    "ERROR_mail":"El mail introducido no es válido.",
    "SMTP_error_login":"Error de autentificación, el usuario o la contraseña no son correctos.",
    "SMTP_error_send":"Error al enviar el correo.",
    "SMTP_login_sucesfull":"La autentificación de %s es correcta.",
    "SMTP_sender_refused":"El envío ha sido rechazado. Reintentando.",
    "SMTP_notification_send":"Notificación ha sido enviada a %s.",
    "ERROR_connection":"No se obtuvo respuesta. Revise la conexión a internet. Se reintentara conexión en "+str(refreshTime)+"s",
    "INFO_screen_conf":"""La configuración actual del servidor SMTP:
    Puerto: %i
    Correo del servidor: %s
    Dirección del servidor: %s
    Correo de notificación: %s""",
    "INFO_actual_conf":"""La configuración actual del servidor SMTP:
                        -Puerto: %i
                        -Correo del servidor: %s
                        -Dirección del servidor: %s
                        -Correo de notificación: %s""",
    "INFO_help":"""
    \x1b[1mFKYUISP\x1b[0m
    Script que avisa por correo del cambio de ip pública de tu PC. Ante las
    políticas abusivas de las ISP por el cobro de una IP estática y la
    posibilidad de que ante un cambio de IP no se pueda acceder a un PC
    a traves de Internet.

    \x1b[1mOpciones\x1b[0m      \x1b[1mDescripción\x1b[0m
    \x1b[1m-r\x1b[0m            Inicia el servicio de notificación de cambio de ip.
    \x1b[1m-v [lang]\x1b[0m     Muestra el log en la terminal. Permite la entrada para un cambio de idioma.
    \x1b[1m-c\x1b[0m            Muestra la configuración SMTP guardada. IMPIDE EL INICIO DEL SERVICIO.
    \x1b[1m-n\x1b[0m            Fuerza una configuración nueva.
    \x1b[1m-l [ruta]\x1b[0m     Guarda un log. Ruta opcional.

    Para el cambio de Idioma usar '-v código_de_idioma' Ej: -v es | Para el español.
    Idiomas disponibles:
    """
    },
    "en":{
    "TEXT_name": "English",
    "TEXT_alert": "Alert.",
    "TEXT_port" : "Port.",
    "TEXT_servermail": "Server email",
    "TEXT_password": "Password",
    "TEXT_serveraddres": "Server address",
    "TEXT_reciver_mail": "Email Notification",
    "INFO_ip_changed": "IP change.",
    "INFO_start_service": "FKYUISP service initialized.",
    "INFO_initi_config": "No previous configuration found. Configuration will proceed:",
    "INFO_exit": "Service terminated by user.",
    "INFO_waiting": "Analyzing in case the ip changes. I will keep you informed.",
    "INFO_actual_ip": "The current public ip is %s returned by %s.",
    "INSERT_port": "Enter mail server port:",
    "INSERT_servermail": "Enter server's mail:",
    "INSERT_password": "Enter server password:",
    "INSERT_serveraddress": "Enter server address:",
    "INSERT_recivermail": "Enter the mail where to receive the notifications:",
    "INSERT_use_conf": "You wish to use this configuration: [y/n]",
    "INSERT_save_conf": "You wish to save the configuration: [y/n]",
    "ERROR_lang" : "Language error - Language not supported. Language list:",
    "ERROR_previus_config": "No saved configuration.",
    "ERROR_port": "The port entered is not a number or is not in the range 0-65535.",
    "ERROR_mail": "The mail entered is not valid.",
    "SMTP_error_login": "Authentication error, user or password are not correct.",
    "SMTP_error_send": "Error when sending the mail.",
    "SMTP_login_sucesfull": "Authentication of %s is correct.",
    "SMTP_sender_refused": "Sending has been rejected. Retrying.",
    "SMTP_notification_send": "Notification has been sent to %s.",
    "ERROR_connection": "No response obtained. Check internet connection. Connection will be reattempted at "+str(refreshTime)+"s.",
    "INFO_screen_conf":"""The current SMTP server configuration
    Port: %i
    Server's mail: %s
    Server address: %s
    Notification mail: %s""",
    "INFO_actual_conf":"""The current SMTP server settings:
                        -Port: %i
                        -Server mail: %s
                        -Server address: %s
                        -Notification mail: %s""",
    "INFO_help":"""
    \x1b [1mFKYUISP\x1b [0m
    Script that notifies by mail the change of public ip of your PC. Before the
    abusive ISP policies for charging for a static IP and
    possibility that a change of IP will make a PC inaccessible
    through the Internet.

    \x1b [1mOptions\x1b [0m \x1b [1mDescription\x1b [0m
    \x1b [1m-r\x1b [0m Starts IP change notification service.
    \x1b[1m-v [lang]\x1b[0m Shows the log on the terminal. Allows input for a language change.
    \x1b [1m-c\x1b [0m Displays saved SMTP settings. PREVENTS THE START OF SERVICE.
    \x1b [1m-n\x1b [0m Forces a new configuration.
    \x1b[1m-l [path]\x1b[0m Saves a log. Optional path.

    To change the language use '-v language_code'.
    Available languages:
    """
    }
}

#Debug Options------------------------------------------------------------------
VERBOSE = False
RUN=False
FORCE_CONFIG=False
LOG=False
SHOW_CFG= False
args = len(sys.argv)
if args <= 1:
    print(notifications[LANGUAGE]["INFO_help"])
    for lang in notifications:
        print("   ",lang,"- "+notifications[lang]["TEXT_name"])
    print("\n")
else:
    for index, arg in enumerate(sys.argv):
        if arg == "-r":
            RUN= True

        if arg == "-n":
            FORCE_CONFIG=True

        if arg == "-l":
            LOG = True
            try:
                if sys.argv[index+1]:
                    if re.match("^/[^%S]*", sys.argv[index+1]):
                        log_path = sys.argv[index+1]+"/"
                    else:
                        log_path = ""
            except IndexError:
                log_path = ""

        if arg == "-v":
            VERBOSE = True
            try:
                if notifications[sys.argv[index+1]]:
                    LANGUAGE = sys.argv[index+1]
            except IndexError:
                LANGUAGE=LANGUAGE

            except KeyError:
                if sys.argv[index+1][0:1]!="-":
                    print(notifications[LANGUAGE]["ERROR_lang"])
                    for lang in notifications:
                        print(lang,"- "+notifications[lang]["TEXT_name"])
                    RUN= False

        if arg == "-c":
            RUN= False
            SHOW_CFG= True

def showConfig():
    try:
        d = {}
        with open("mail.cfg","r") as cfg:
            for line in cfg:
                (key, val) = line.split()
                d[key] = val

            print(notifications[LANGUAGE]["INFO_screen_conf"]%(int(d['port']),d['servermail'],d['serveraddres'],d['reciver_mail']))

    except:
        print(notifications[LANGUAGE]["ERROR_previus_config"])


def getDate():
    now = datetime.datetime.now()
    return ("%02i:%02i:%02i - %02i/%02i/%i")%(now.hour, now.minute, now.second, now.day ,  now.month,now.year)

def INFO_output(text):
    if VERBOSE == True:
        print(getDate(),":",text)
    if LOG == True:
        with open(log_path+"log_fkyuisp.txt","a") as file:
            file.write(getDate()+" : "+text+"\n")

def ERROR_output(text):
    print(getDate(),":",text)
    if LOG == True:
        with open(log_path+"log_fkyuisp.txt","a") as file:
            file.write(getDate()+" : "+text+"\n")

#END OF Debug Options-----------------------------------------------------------
def existConfig(LANGUAGE):
    try:
        d = {}
        with open("mail.cfg","r") as cfg:
            for line in cfg:
                (key, val) = line.split()
                d[key] = val
        return int(d['port']),d['servermail'],d['password'],d['serveraddres'],d['servermail'],d['reciver_mail']

    except:
        print(notifications[LANGUAGE]["INFO_initi_config"])
        return createConfig(LANGUAGE)

def createConfig(LANGUAGE):
    #ServerMail Options
    while True:
        while True:
            try:
                port = int(input(notifications[LANGUAGE]["INSERT_port"]+"\n"))
                if port > 0 and port < 65536:
                    break
                else:
                    print(notifications[LANGUAGE]["ERROR_port"])
            except ValueError:
                print(notifications[LANGUAGE]["ERROR_port"])

        while True:
            servermail = input(notifications[LANGUAGE]["INSERT_servermail"]+"\n")
            if not re.match("[^@]+@[^@]+\.[^@]+", servermail):
                print(notifications[LANGUAGE]["ERROR_mail"])
            else:
                break

        password = input(notifications[LANGUAGE]["INSERT_password"]+"\n")
        serverAddress = input(notifications[LANGUAGE]["INSERT_serveraddress"]+"\n")
        #Your Mail where you recive notification
        sender_email = servermail

        while True:
            reciver_mail = input(notifications[LANGUAGE]["INSERT_recivermail"]+"\n")
            if not re.match("[^@]+@[^@]+\.[^@]+", servermail):
                print(notifications[LANGUAGE]["ERROR_mail"])
            else:
                break


        print( notifications[LANGUAGE]["INFO_screen_conf"]% (port, servermail, serverAddress, reciver_mail))
        if input(notifications[LANGUAGE]["INSERT_use_conf"]+"\n") == "y":
            break

    if input(notifications[LANGUAGE]["INSERT_save_conf"]+"\n") == "y":
        with open("mail.cfg","w") as file:
            conf="port %i\nservermail %s\npassword %s\nserveraddres %s\nreciver_mail %s"%(port, servermail, password, serverAddress, reciver_mail)
            file.write(conf)


    return port,servermail,password,serverAddress,sender_email,reciver_mail

def findip():
    for web in weblist:
        command='wget -qO- ' + web
        ip=os.popen(command).read()
        if ip != "":
            return  True , ip , web
    return False , "" , ""

def sendMail(serverAddress,password,port,servermail,reciver_mail,fr,subject,message):
    text="""Subject:%s\nFrom:%s\n


    %s
    """ % (fr,subject,message)
    while True:
        try:
            with smtplib.SMTP(serverAddress, port) as server:
                server.starttls()
                try:
                    server.login(servermail, password)
                    INFO_output(notifications[LANGUAGE]["SMTP_login_sucesfull"] % servermail)
                except smtplib.SMTPAuthenticationError:
                    ERROR_output(notifications[LANGUAGE]["SMTP_error_login"])
                    port,servermail,password,serverAddress,sender_email,reciver_mail = createConfig(LANGUAGE)
                try:
                    server.sendmail(servermail, reciver_mail,text)
                    INFO_output(notifications[LANGUAGE]["SMTP_notification_send"] % reciver_mail)
                    server.quit()
                    break
                except smtplib.SMTPSenderRefused:
                    ERROR_output(notifications[LANGUAGE]["SMTP_sender_refused"])
        except:
            ERROR_output(notifications[LANGUAGE]["SMTP_error_send"])
            port,servermail,password,serverAddress,sender_email,reciver_mail = createConfig(LANGUAGE)

def main():
    if FORCE_CONFIG:
        port,servermail,password,serverAddress,sender_email,reciver_mail = createConfig(LANGUAGE)
    else:
        port,servermail,password,serverAddress,sender_email,reciver_mail = existConfig(LANGUAGE)

    INFO_output(notifications[LANGUAGE]["INFO_start_service"])
    INFO_output(notifications[LANGUAGE]["INFO_actual_conf"]%(port,servermail,serverAddress,reciver_mail))
    actualIP = ""
    while True:
        connection,ip,web = findip()
        if connection == True:
            if actualIP != ip:
                actualIP = ip
                INFO_output(notifications[LANGUAGE]["INFO_actual_ip"]%(str(actualIP), web))
                sendMail(serverAddress,password,port,sender_email, reciver_mail,
                        notifications[LANGUAGE]["INFO_ip_changed"],
                        "fkyuISP",str(actualIP))
                INFO_output(notifications[LANGUAGE]["INFO_waiting"])

        else:
            actualIP = ""
            INFO_output(notifications[LANGUAGE]["ERROR_connection"])
        time.sleep(refreshTime)

if SHOW_CFG:
    showConfig()

if RUN:
    try:
        main()
    except KeyboardInterrupt:
        INFO_output(notifications[LANGUAGE]["INFO_exit"])
