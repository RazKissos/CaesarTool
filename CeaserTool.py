import argparse
import os.path as path


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
    parser.add_argument(
        "--file",
        default=None,
        type=str,
        help="The text file path to be operated on in calculation.",
        dest="path",
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
    if args.path and args.string:
        raise ValueError(
            "Both string and text file path were given, please specify only one!"
        )
    if not args.path and not args.string:
        raise ValueError(
            "Neither a string nor a text file path were specified, please select one!"
        )
    if args.path and not path.exists(args.path):
        raise FileNotFoundError(
            f"Could not find specified file to be operated on.\nFile Path:{args.path}"
        )
    if not args.path.endswith(".txt"):
        raise ValueError("Cannot operate on a non `.txt` file!")

    return args


LETTERS = [chr(ascii_val) for ascii_val in range(97, 123)]


def calc_letter(letter: str, letters: list, offset: int):
    if letter not in letters:  # Check if letter is not valid.
        raise ValueError(f"Letter {letter} not in letters to use!")
    elif len(letter) != 1:  # Check if string size is not 1.
        raise ValueError("Variable `letter` is a string with size greater than 1!")
    else:
        ascii_val = ord(letter) + offset  # Calculate ciphered value.
        # If value is bigger than top ascii value or lower than bottom ascii value, recalculate.
        while any((ascii_val > ord("z"), ascii_val < ord("a"))):
            if ascii_val > ord("z"):
                ascii_val -= 26
            elif ascii_val < ord("a"):
                ascii_val += 26

        return chr(ascii_val)  # Return the calculated character.


def decrypt(text: str, offset: int):
    if offset > 0:  # Check if offset is valid.
        raise ValueError("Decipher offset cannot be positive!")
    output = ""
    for character in text:  # Modify each character accordingly.
        if (
            character not in LETTERS
        ):  # If character is not in the valid letters list then ignore.
            output = output + character
            continue
        output = output + calc_letter(character, LETTERS, offset)
    return output  # Return decrypted output.


def encrypt(text: str, offset: int):
    if offset < 0:  # Check if offset is valid.
        raise ValueError("Encryption offset cannot be negative!")
    output = ""
    for character in text:  # Modify each character accordingly.
        if (
            character not in LETTERS
        ):  # If character is not in the valid letters list then ignore.
            output = output + character
            continue
        output = output + calc_letter(character, LETTERS, offset)
    return output  # Return encrypted output.


def main():
    try:
        args = read_arguments()  # Read arguments
    except Exception as e:
        print(f"ERROR: {e}")
        exit()
    offset = args.offset
    text = str()

    # Select desired text to operate on.
    if args.path is not None:
        with open(args.path, "r") as f:
            text = f.read()
    else:
        text = args.string

    if args.decrypt:  # Perform selected task.
        if offset > 0:
            offset = -offset
        try:
            print(decrypt(text.lower(), offset))
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            exit()
    elif args.encrypt:
        try:
            print(encrypt(text.lower(), offset))
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            exit()


if __name__ == "__main__":
    main()
