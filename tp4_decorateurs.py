import time
from functools import wraps, lru_cache

#1
def chronometrer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        print(f"{func.__name__} a pris {time.perf_counter() - start:.2f} s")
        return res
    return wrapper
@chronometrer
def lente(): time.sleep(1)
print("1"); lente()

#2
def majuscules(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@majuscules
def dire_bonjour(): return "bonjour"
print("\n2"); print(dire_bonjour())

#3
def compter_appels(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.appels += 1
        return func(*args, **kwargs)
    wrapper.appels = 0
    return wrapper
@compter_appels
def fonction(x): return x * 2
print("\n3")
for i in [1, 2, 3]: fonction(i)
print("Nombre d'appels :", fonction.appels)

#4
def verifier_positifs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for v in list(args) + list(kwargs.values()):
            if isinstance(v, (int, float)) and v < 0:
                raise ValueError(f"Argument negatif interdit : {v}")
        return func(*args, **kwargs)
    return wrapper
@verifier_positifs
def surface(l, L): return l * L
print("\n4"); print(surface(4, 5))
try: surface(-4, 5)
except ValueError as e: print("Erreur :", e)

#5
def chronometrer_unite(unite="s"):
    def decorateur(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            res = func(*args, **kwargs)
            d = time.perf_counter() - start
            t = f"{d * 1000:.2f} ms" if unite == "ms" else f"{d:.2f} s"
            print(f"{func.__name__} a pris {t}")
            return res
        return wrapper
    return decorateur
@chronometrer_unite("ms")
def courte(): time.sleep(0.2)
print("\n5"); courte()

#6
def memoriser(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache: cache[args] = func(*args)
        return cache[args]
    return wrapper
def fibo(n): return n if n < 2 else fibo(n - 1) + fibo(n - 2)
@memoriser
def fibo_memo(n): return n if n < 2 else fibo_memo(n - 1) + fibo_memo(n - 2)
@lru_cache(maxsize=None)
def fibo_lru(n): return n if n < 2 else fibo_lru(n - 1) + fibo_lru(n - 2)
print("\n6")
print("Sans :", chronometrer(fibo)(25))
print("Memo :", chronometrer(fibo_memo)(30))
print("LRU  :", chronometrer(fibo_lru)(30))

#7
print("\n7")
@chronometrer
@compter_appels
def f1(): return 1
@compter_appels
@chronometrer
def f2(): return 1
f1(); f1()
f2(); f2()
print("f1.appels (chronometrer en haut)  ->", f1.appels) # 0
print("f2.appels (compter_appels en haut) ->", f2.appels) # 2

# 8
class MiniFlask:
    def __init__(self):
        self.routes, self.f404 = {}, None
    def route(self, chemin):
        def deco(func):
            if chemin in self.routes: raise ValueError("Route existante")
            self.routes[chemin] = func
            return func
        return deco
    def erreur_404(self, func):
        self.f404 = func
        return func
    def traiter(self, chemin):
        return self.routes.get(chemin, self.f404 or (lambda: "404"))()

app = MiniFlask()
@app.route("/")
def accueil(): return "Accueil"
@app.route("/contact")
def contact(): return "Contact"
@app.erreur_404
def p404(): return "Page 404 personnalisee"
print("\n8")
print(app.traiter("/"))
print(app.traiter("/inconnue"))