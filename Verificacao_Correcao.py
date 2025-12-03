# A)
def merge_sorted(a, b):
    """Retorna lista que é a fusão ordenada de duas listas já ordenadas (crescente)."""
    i = j = 0
    res = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i]); i += 1
        else:
            res.append(b[j]); j += 1
    # copia o restante
    if i < len(a):
        res.extend(a[i:])
    if j < len(b):
        res.extend(b[j:])
    return res

# teste
if __name__ == "__main__":
    v1 = [1,2,5,7]
    v2 = [0,3,4,6,8]
    print(merge_sorted(v1, v2))  # -> [0,1,2,3,4,5,6,7,8]







# B)
def is_palindrome_number_num(num: int) -> bool:
    if num < 0:
        return False  # decisão: números negativos não são palíndromos (por causa do '-')
    original = num
    inv = 0
    while num > 0:
        d = num % 10
        inv = inv*10 + d
        num //= 10
    return inv == original

def is_palindrome_number_str(num: int) -> bool:
    s = str(abs(num))  # opcional: tratar negativos como inválidos ou usar abs
    return s == s[::-1]

if __name__ == "__main__":
    for x in [121, 12321, -121, 10, 0]:
        print(x, is_palindrome_number_num(x), is_palindrome_number_str(x))
