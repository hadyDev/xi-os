import gc

def collect():
    old = gc.mem_free()
    gc.collect()
    new = gc.mem_free()
    diff = new - old
    print("[GRBG] Freed up " + (str(diff)) + " bytes of space")

