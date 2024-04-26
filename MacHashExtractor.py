import plistlib
import sys
import argparse
import binascii

def format_hex(hex_str, chunk_size=256):
    return '\n'.join([hex_str[i:i+chunk_size] for i in range(0, len(hex_str), chunk_size)])

def main(input_file, output_file):
    with open(input_file, 'rb') as f:
        plist_data = plistlib.load(f)

    # Extracting and formatting data
    entropy_bytes = plist_data['SALTED-SHA512-PBKDF2']['entropy']
    hex_entropy = binascii.hexlify(entropy_bytes).decode('utf-8').strip()
    formatted_entropy = format_hex(hex_entropy)

    iterations = plist_data['SALTED-SHA512-PBKDF2']['iterations']
    salt = plist_data['SALTED-SHA512-PBKDF2']['salt']

    # Prepare output string
    output_str = "$ml$" + str(iterations) + "$" + binascii.hexlify(salt).decode('utf-8') + "$" + formatted_entropy + "\n"

    # Write to output file
    with open(output_file, 'w') as out:
        out.write(output_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts plist file to a specific format.")
    parser.add_argument("-i", "--input", help="Input plist file", required=True)
    parser.add_argument("-o", "--output", help="Output file", required=True)
    args = parser.parse_args()

    main(args.input, args.output)
