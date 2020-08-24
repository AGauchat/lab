def tobits(s, bitmens):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])

    if bitmens != '2':
        result[len(result)-1] = int(bitmens)

    return result
