
__all__ = ["trunc_err_detect"]

def trunc_err_detect(a, b):
    return a + b == max(a, b)

