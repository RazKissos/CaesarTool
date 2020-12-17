import argparse


def read_arguments():
    """
    Read the command line arguments.
    Raises:
        ValueError: Both decrypt and encrypt flags were selected.
        ValueError: Neither decrypt not encrypt flags were selected.

    Returns:
        args: the arguments object returned from the argparser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--decrypt",
        action="store_true",
        help="Choose the decrypt option.",
        dest="decrypt",
    )
    parser.add_argument(
        "--encrypt",
        action="store_true",
        help="Choose the encrypt option.",
        dest="encrypt",
    )
    parser.add_argument(
        "--offset",
        default=0,
        type=int,
        help="The offset to be used in calculation.",
        dest="offset",
    )
    parser.add_argument(
        "-s",
        default=None,
        type=str,
        help="The text to be operated on in calculation.",
        dest="string",
    )

    args = parser.parse_args()

    if all((args.encrypt, args.decrypt)):
        raise ValueError(
            "Both decrypt and encrypt have been selected, please select only one!"
        )
    if all((not args.encrypt, not args.decrypt)):
        raise ValueError(
            "Neither decrypt nor encrypt have been selected, please select one!"
        )

    return args


LETTERS = [chr(ascii_val) for ascii_val in range(97, 123)]


def calc_letter(letter: str, letters: list, offset: int):
    if letter not in letters: # Check if letter is not valid.
        raise ValueError(f"Letter {letter} not in letters to use!")
    elif len(letter) != 1: # Check if string size is not 1.
        raise ValueError("Variable `letter` is a string with size greater than 1!")
    else:
        ascii_val = ord(letter) + offset # Calculate ciphered value.
        # If value is bigger than top ascii value or lower than bottom ascii value, recalculate.
        while any((ascii_val > ord("z"), ascii_val < ord("a"))):
            if ascii_val > ord("z"):
                ascii_val -= 26
            elif ascii_val < ord("a"):
                ascii_val += 26
        
        return chr(ascii_val) # Return the calculated character.


def decrypt(text: str, offset: int):
    if offset > 0: # Check if offset is valid.
        raise ValueError("Decipher offset cannot be positive!")
    output = ""
    for character in text: # Modify each character accordingly.
        if character not in LETTERS: # If character is not in the valid letters list then ignore.
            output = output + character
            continue
        output = output + calc_letter(character, LETTERS, offset)
    return output # Return decrypted output.


def encrypt(text: str, offset: int):
    if offset < 0: # Check if offset is valid.
        raise ValueError("Encryption offset cannot be negative!")
    output = ""
    for character in text: # Modify each character accordingly.
        if character not in LETTERS: # If character is not in the valid letters list then ignore.
            output = output + character
            continue
        output = output + calc_letter(character, LETTERS, offset)
    return output # Return encrypted output.


def main():
    args = read_arguments() # Read arguments
    offset = args.offset
    if args.decrypt: # Perform selected task.
        if offset > 0:
            offset = -offset
        try:
            print(decrypt(args.string.lower(), offset))
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            exit()
    elif args.encrypt:
        try:
            print(encrypt(args.string.lower(), offset))
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            exit()


if __name__ == "__main__":
    main()
