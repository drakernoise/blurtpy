import getpass
from blurtpy import Blurt
from blurtpy.account import Account
from blurtpy.comment import Comment
from blurtpy.discussions import Query, Discussions_by_created
from blurtpy.wallet import Wallet

# Configuración
USUARIO = "tu_usuario"
NODO = ["https://rpc.blurt.world"]

# Inicializar Blurt sin claves hardcodeadas
# Se usará el wallet local (blurtpy.sqlite)
b = Blurt(node=NODO)

# Desbloquear Wallet
if b.wallet.created():
    if b.wallet.locked():
        pwd = getpass.getpass(f"Introduce contraseña del wallet para operar como {USUARIO}: ")
        try:
            b.wallet.unlock(pwd)
            print("Wallet desbloqueado.")
        except Exception as e:
            print(f"Error al desbloquear: {e}")
            exit()
else:
    print("No se encontró un wallet creado. Ejecuta 'examples/secure_wallet_setup.py' primero.")
    exit()

def comentar_post(identifier, body, title=""):
    """Comenta en un post existente."""
    print(f"Comentando en {identifier}...")
    try:
        c = Comment(identifier, blockchain_instance=b)
        c.reply(body, title=title, author=USUARIO)
        print("Comentario publicado con éxito.")
    except Exception as e:
        print(f"Error al comentar: {e}")

def analizar_comentarios(identifier):
    """Cuenta comentarios y lista autores."""
    print(f"Analizando comentarios de {identifier}...")
    try:
        c = Comment(identifier, blockchain_instance=b)
        replies = c.get_replies()
        print(f"Total de comentarios directos: {len(replies)}")
        
        autores = set()
        for reply in replies:
            autores.add(reply['author'])
        
        print(f"Autores únicos: {', '.join(autores)}")
        return replies
    except Exception as e:
        print(f"Error al analizar comentarios: {e}")
        return []

def votar_comentarios(replies, peso=100):
    """Vota una lista de comentarios."""
    print(f"Votando {len(replies)} comentarios con peso {peso}%...")
    for reply in replies:
        try:
            print(f"Votando a {reply['author']}...")
            reply.vote(peso, account=USUARIO)
            print("Voto enviado.")
        except Exception as e:
            print(f"Error al votar a {reply['author']}: {e}")

def ultimo_post_usuario(usuario):
    """Encuentra el último post de un usuario."""
    print(f"Buscando último post de {usuario}...")
    try:
        acc = Account(usuario, blockchain_instance=b)
        # get_blog devuelve una lista de entradas del blog
        blog = acc.get_blog(limit=1)
        if blog:
            last_post = blog[0]
            print(f"Último post: {last_post['title']} ({last_post['permlink']})")
            return last_post
        else:
            print("El usuario no tiene posts.")
            return None
    except Exception as e:
        print(f"Error al buscar post: {e}")
        return None

def buscar_posts_recientes(tag, horas=24):
    """Busca posts recientes por tag."""
    print(f"Buscando posts en tag '{tag}' de las últimas {horas} horas...")
    try:
        q = Query(limit=20, tag=tag)
        posts = Discussions_by_created(q, blockchain_instance=b)
        
        limit_date = datetime.utcnow() - timedelta(hours=horas)
        
        count = 0
        for post in posts:
            post_date = post['created'] # Esto ya debería ser un objeto datetime si se parsea bien, o string
            # Asegurar formato fecha si es string (depende de la versión de la librería, beem solía devolver datetime)
            if isinstance(post_date, str):
                post_date = datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S")
            
            if post_date > limit_date:
                print(f"- {post['created']}: {post['title']} por {post['author']}")
                count += 1
            else:
                # Como Discussions_by_created está ordenado por fecha, si pasamos el límite podemos parar
                break
        print(f"Encontrados {count} posts recientes.")
    except Exception as e:
        print(f"Error en búsqueda: {e}")

if __name__ == "__main__":
    # EJEMPLOS DE USO (Descomenta para probar)
    
    # 1. Encontrar último post de un usuario
    # post = ultimo_post_usuario("tekraze")
    
    # 2. Comentar en ese post (¡CUIDADO! Esto publica en la blockchain real)
    # if post:
    #    identificador = f"@{post['author']}/{post['permlink']}"
    #    comentar_post(identificador, "¡Hola! Este es un comentario de prueba desde blurtpy.")
    
    # 3. Analizar comentarios
    # if post:
    #    identificador = f"@{post['author']}/{post['permlink']}"
    #    comentarios = analizar_comentarios(identificador)
       
    # 4. Votar comentarios (¡CUIDADO! Esto gasta Voting Power)
    #    votar_comentarios(comentarios, peso=10) # 10%
    
    # 5. Buscar posts recientes
    buscar_posts_recientes("blurt", horas=24)
