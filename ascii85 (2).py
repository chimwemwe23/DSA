import sys


def encode_ascii85(string):
    hex_str = ''
    result = ''

    for s in string:
        hex_str += format(ord(s), '02x')
    index = 0
    while index < len(hex_str):
        padding = max(((index + 8) - len(hex_str)) / 2, 0)
        if padding != 0:
            encode_block = hex_str[index:] + '00' * int(padding)
        else:
            encode_block = hex_str[index:index + 8]
        if encode_block != '0' * 8 or padding != 0:
            encode_block_int = int(encode_block, 16) / (85 ** padding)
            encode_result = ' '
            for _ in range(5 - int(padding)):
                encode_block_int, remainder = divmod(encode_block_int, 85)
                encode_result = chr(int(remainder) + 33) + encode_result

            result += encode_result
        else:
            result += 'z'

        index += 8

    return result


def decode_ascii85(encoded_string):
    result = " "
    ill_char = ['\n', ' ', '\0', '\t']
    for c in ill_char:
        encoded_string = encoded_string.replace(c, '')
    encoded_string = encoded_string[2:-2]

    index = 0

    while index < len(encoded_string):
        if encoded_string[index] == 'z':
            result += '\0' * 4
            index += 1

        else:
            padding = max(index + 5 - len(encoded_string), 0)
            encoded_block = encoded_string[index:index + 5] if padding == 0 else encoded_string[index:] + 'u' * padding
            encoded_int = 0
            for i, c in enumerate(encoded_block[::-1]):
                encoded_int += (ord(c) - 33) * (85 ** i)
            encoded_byte = format(encoded_int, '08x')

            if padding > 0:
                encoded_byte = encoded_byte[:-padding * 2]
            index += 5
        result += ''.join([chr(int(encoded_byte[i:i + 2], 16)) for i in range(0, len(encoded_byte), 2)])

    return result


def main():
    global output
    if len(sys.argv) < 2 or sys.agrv[1] not in ['-e', '-d']:
        print("Usage: python ascii85 -e|-d")
        sys.exit(1)

    mode = sys.argv[1]
    input_data = sys.stdin.read()

    if mode == '-e':
        output = encode_ascii85(input_data)

    elif mode == '-d':
        output = decode_ascii85(input_data)

    sys.stdout.write(output)


if __name__ == "__main__":
    main()


