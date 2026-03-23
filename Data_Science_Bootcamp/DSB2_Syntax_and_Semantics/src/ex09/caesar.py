def caesar_ciph(text, shift, mode='encode'):
    result = []
    if mode == 'decode':
        shift = -shift
    for ch in text:
        if ch.islower():
            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        elif ch.isupper():
            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(ch)
    return ''.join(result)

def encoder_decoder():
    import sys

    if len(sys.argv) != 4:
        raise Exception("Incorrect number of arguments provided. Correct usage: python3 caesar.py encode/decode <text> <shift>")
    
    dec_or_enc = sys.argv[1]
    text = sys.argv[2]
    shift = int(sys.argv[3])

    if any(ord(ch) > 127 for ch in text):
        raise Exception("The script does not support your language yet")

    if dec_or_enc == 'encode':
        result = caesar_ciph(text, shift, mode='encode')
    elif dec_or_enc == 'decode':
        result = caesar_ciph(text, shift, mode='decode')
    print(result)

if __name__ == "__main__":
    encoder_decoder()
