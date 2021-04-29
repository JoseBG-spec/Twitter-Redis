import redis

subscribers = []
accounts = redis.Redis(host='localhost', port=6379, db=0)


# Generar subscribers de los que ya existan
if accounts.exists("counter"):
    c = int(accounts.get("counter").decode("utf8"))
    for x in range(c):
        subscribers.append(redis.Redis(host='localhost', port=6379, db=0))
        # Registrar el usuario
else:
    accounts.set("counter", 1)
    subscribers.append(redis.Redis(host='localhost', port=6379, db=0))
    ponce = {"username": "admin", "password": "pwdsars", "index": 0}
    accounts.hmset("admin", ponce)
    accounts.rpush("listSuscribers", "admin")


def iniciarSesion(user, passW):
    if user == accounts.hget(user, "username").decode("utf8") and passW == accounts.hget(user, "password").decode(
            "utf8"):
        print("La informacion es correcta")
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
                accounts.lpush(user + accounts.hget(user, "index").decode("utf8"), tweet)
                print("Tweet publicado")
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
                    print("Tweets del usuario: "+ subs.decode("utf8"))
                    tweets = accounts.llen(subs.decode("utf8") + accounts.hget(subs, "index").decode("utf8"))
                    for tweet in range(tweets):
                        print(accounts.lindex(subs.decode("utf8") + accounts.hget(subs, "index").decode("utf8"), tweet).decode("utf8"))
            print("Que quieres hacer? 1)Twittear 2)Suscibirse a un canal 3)Ver timeline 4)Salir")
            eleccion = int(input())
    else:
        print("La informacion es incorrecta")


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
        if not accounts.exists(user):
          accounts.hmset(user, temp)
          accounts.incr("counter")
          accounts.rpush("listSuscribers", user)
          subscribers.append(redis.Redis(host='localhost', port=6379, db=0))
          iniciarSesion(user, passW)
        else:
          print("Ya existe el usuario")
        # TODO crear un nuevo canal en el momento que se crear
    elif accion == 2:
        print("Nombre de usuario:")
        user = input()
        print("Contraseña:")
        passW = input()

        iniciarSesion(user, passW)
    print("Quieres registrarte (1) o iniciar Sesion(2): o Salir(3) ")
    accion = int(input())