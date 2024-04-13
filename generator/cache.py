import os
import pickle
import hashlib


def get_cache(key: str):
    h = hashlib.sha256(bytes(key, encoding="utf-8"))
    h = h.hexdigest()[:16]

    if not os.path.isdir(os.path.join(os.getcwd(), "cache")):
        os.mkdir(os.path.join(os.getcwd(), "cache"))

    path = os.path.join(os.getcwd(), "cache", f"{str(h)}.pkl")
    if os.path.isfile(path):
        with open(path, "rb") as f:
            return True, pickle.load(f)
    else:
        return False, None


def save_cache(key: str, obj):
    h = hashlib.sha256(bytes(key, encoding="utf-8"))
    h = h.hexdigest()[:16]

    path = os.path.join(os.getcwd(), "cache", f"{str(h)}.pkl")
    with open(path, "wb") as f:
        pickle.dump(obj, f)

    return
