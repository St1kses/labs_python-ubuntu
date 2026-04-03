import sys
def decrypt(cipher_text: str) -> str:
    result = []
    i = 0
    n = len(cipher_text)
    while i < n:
        ch = cipher_text[i]
        if ch != ".":
            result.append(ch)
            i += 1
            continue
        if i + 1 < n and cipher_text[i + 1] == ".":
            if result:
                result.pop()
            i += 2
        else:
            i += 1
    return "".join(result)
if __name__ == "__main__":
    encrypted = sys.stdin.read().rstrip("\n")
    print(decrypt(encrypted))
