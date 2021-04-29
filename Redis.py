import redis

subscribers = []
accounts = redis.Redis(host='localhost', port=6379, db=0)
fook = True

# Generar subscribers de los que ya existan
if accounts.exists("counter"):
    c = int(accounts.get("counter").decode("utf8"))
    for x in range(c):
        # print(x)
        subscribers.append(redis.Redis(host='localhost', port=6379, db=0))
        # Registrar el usuario
else:
    print("new")
    accounts.set("counter", 1)
    subscribers.append(redis.Redis(host='localhost', port=6379, db=0))
    ponce = {"username": "admin", "password": "pwdsars", "index": 0}
    accounts.hmset("admin", ponce)
    accounts.rpush("listSuscribers", "admin")

def gfg():
    global fook
    print("Showing Timeline\n")
    fook = False

def iniciarSesion(user, passW):
    global fook
    if user == accounts.hget(user, "username").decode("utf8") and passW == accounts.hget(user, "password").decode(
            "utf8"):
        print("The information is correct")
        tweet = ""

        print("Que quieres hacer? 1)Twittear 2)Suscibirse a un canal 3)Ver timeline 4)Cerrar Sesion")
        eleccion = int(input())
        p = subscribers[int(accounts.hget(user, "index").decode("utf8"))].pubsub()
        p.subscribe([user])
        if not accounts.exists(user+"_listSuscribers"):
            accounts.lpush(user+"_listSuscribers", user)
        while eleccion != 4:
            if eleccion == 1:
                # Subir nuevo tweet (publish en tu channel)
                print("En que estas pensando?")
                tweet = input()
                #subscribers[int(accounts.hget(user, "index").decode("utf8"))].publish(user, tweet)
                accounts.lpush(user + accounts.hget(user, "index").decode("utf8"), tweet)
                print("Tweet posted")
            elif eleccion == 2:
                counter = 0
                print("A cual te quieres suscribir? ")
                for subs in accounts.lrange("listSuscribers", 0, -1):
                    counter += 1
                    print(str(counter) + ") " + subs.decode("utf8"))
                print("(Elige el numero)")
                elec = int(input())
                p.subscribe([accounts.lindex("listSuscribers", elec - 1).decode("utf8")])
                accounts.rpush(user + "_listSuscribers", accounts.lindex("listSuscribers", elec - 1).decode("utf8"))
                print("Te has suscrito a: " + accounts.lindex("listSuscribers", elec - 1).decode("utf8"))

                # Seguir a otro usuario (subscribe a un channel de otro usuario)

            elif eleccion == 3:
                for subs in accounts.lrange(user + "_listSuscribers", 0, -1):
                    print("Tweets from user: "+ subs.decode("utf8"))
                    tweets = accounts.llen(subs.decode("utf8") + accounts.hget(subs, "index").decode("utf8"))
                    for tweet in range(tweets):
                        print(accounts.lindex(subs.decode("utf8") + accounts.hget(subs, "index").decode("utf8"), tweet).decode("utf8"))
                    #ver timeLine (Imprimir la obtencion de = subscriber[index].get_Message()['data'])
            print("Que quieres hacer? 1)Twittear 2)Suscibirse a un canal 3)Ver timeline 4)Salir")
            eleccion = int(input())
    else:
        print("Information is NOOOOT correct")


user = ""
passW = ""
accion = -1

print("Quieres registrarte (1) o iniciar Sesion(2): o Salir(3) ")
accion = int(input())
while accion != 3:
    if accion == 1:
        print("Nombre de usario:")
        user = input()
        print("Contraseña:")
        passW = input()
        temp = {"username": user, "password": passW, "index": len(subscribers)}
        
        accounts.hmset(user, temp)
        accounts.incr("counter")

        accounts.rpush("listSuscribers", user)
        subscribers.append(redis.Redis(host='localhost', port=6379, db=0))

        iniciarSesion(user, passW)
        # TODO crear un nuevo canal en el momento que se crear
    elif accion == 2:
        print("nombre de usuario:")
        user = input()
        print("Nueva contraseña:")
        passW = input()

        iniciarSesion(user, passW)
    print("Quieres registrarte (1) o iniciar Sesion(2): o Salir(3) ")
    accion = int(input())
