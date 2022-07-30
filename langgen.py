import random
import sys
import json


def main():
    # Get default options from options.json
    with open("options.json", "r") as options_file:
        options = json.load(options_file)
        vowels = options["vowels"]
        consonants = options["consonants"]
        max_vowels = options["max_vowels"]
        max_consonants = options["max_consonants"]
        allow_repeats = options["allow_repeats"]
        total_words = options["total_words"]
        min_length = options["min_length"]
        max_length = options["max_length"]
        switch_chance = options["switch_chance"]
        for option in ["vowels", "consonants"]:
            if not isinstance(options[option], str):
                print("Value of '" + option + "' in options.json is '" + type(options[option]).__name__ + "', expected 'str'")
                exit(1)
        for option in ["max_vowels", "max_consonants", "total_words", "min_length", "max_length", "switch_chance"]:
            if not isinstance(options[option], int):
                print("Value of '" + option + "' in options.json is '" + type(options[option]).__name__ + "', expected 'int'")
                exit(1)
        if not isinstance(allow_repeats, bool):
            print("Value of '" + option + "' in options.json is '" + type(allow_repeats).__name__ + "', expected 'bool'")
            exit(1)

    # Handle command line arguments
    possible_args = ["--help", "-v", "--vowels", "-c", "--consonants", "-V", "--max-vowels", "-C", "--max-consonants", "-r", "--allow-repeats", "-w", "--total-words", "-l", "--max-length", "-s", "--switch-chance"]
    optionless_args = 0
    given_files = []
    for i, arg in enumerate(sys.argv):
        match arg:
            case "--help":
                help()
                exit(0)
            case "-v" | "--vowels":
                vowels = sys.argv[i + 1]
            case "-c" | "--consonants":
                consonants = sys.argv[i + 1]
            case "-V" | "--max-vowels":
                try:
                    max_vowels = int(sys.argv[i + 1])
                except ValueError:
                    print("Expected integer after " + sys.argv[i] + ", got '" + sys.argv[i + 1] + "'.")
                    exit(1)
            case "-C" | "--max-consonants":
                try:
                    max_consonants = int(sys.argv[i + 1])
                except ValueError:
                    print("Expected integer after " + sys.argv[i] + ", got '" + sys.argv[i + 1] + "'.")
                    exit(1)
            case "-r" | "--allow-repeats":
                if sys.argv[i + 1].lower() in ["true", "t", "1"]:
                    allow_repeats = True
                elif sys.argv[i + 1].lower() in ["false", "f", "0"]:
                    allow_repeats = False
                else:
                    print("Expected boolean after " + sys.argv[i] + ", got '" + sys.argv[i + 1] + "'.")
                    exit(1)
            case "-w" | "--total-words":
                try:
                    total_words = int(sys.argv[i + 1])
                except ValueError:
                    print("Expected integer after " + sys.argv[i] + ", got '" + sys.argv[i + 1] + "'.")
                    exit(1)
            case "-l" | "--min-length":
                try:
                    min_length = int(sys.argv[i + 1])
                except ValueError:
                    print("Expected integer after " + sys.argv[i] + ", got '" + sys.argv[i + 1] + "'.")
                    exit(1)
            case "-L" | "--max-length":
                try:
                    max_length = int(sys.argv[i + 1])
                except ValueError:
                    print("Expected integer after " + sys.argv[i] + ", got '" + sys.argv[i + 1] + "'.")
                    exit(1)
            case "-s" | "--switch-chance":
                try:
                    switch_chance = int(sys.argv[i + 1])
                except ValueError:
                    print("Expected integer after " + sys.argv[i] + ", got '" + sys.argv[i + 1] + "'.")
                    exit(1)
            case _:
                if i != 0:
                    if sys.argv[i - 1] not in possible_args:
                        given_files.append(sys.argv[i])
                        optionless_args += 1
                        if optionless_args > 1:
                            print(
                                "Multiple potential filenames were given. This can mean that multiple filenames were provided or an option was mistyped. Arguments in question: '" + given_files[0] + "', '" + given_files[1] + "'")
                            exit(1)

    # Generate words
    text = ""
    for word in range(total_words):
        current_letter = random.choice([vowels, consonants])
        done = False
        vow_count = 0
        con_count = 0
        length = 0
        last_letter = ""
        while not done:
            if current_letter == vowels and len(vowels) > 0 or len(consonants) == 0 and len(vowels) != 0:
                next_letter = random.choice(vowels)
                if not allow_repeats:
                    while next_letter == last_letter:
                        next_letter = random.choice(vowels)
                text += next_letter
                last_letter = next_letter
                vow_count += 1
                length += 1
                if random.randrange(0, 100) < switch_chance or len(vowels) <= 1 and not allow_repeats:
                    current_letter = consonants
            elif current_letter == consonants and len(consonants) > 0 or len(vowels) == 0 and len(consonants) != 0:
                next_letter = random.choice(consonants)
                if not allow_repeats:
                    while next_letter == last_letter:
                        next_letter = random.choice(consonants)
                text += next_letter
                last_letter = next_letter
                con_count += 1
                length += 1
                if random.randrange(0, 100) < switch_chance or len(consonants) <= 1 and not allow_repeats:
                    current_letter = vowels
            else:
                print("No possible letters were given, please provide more letters.")
                exit(1)
            if random.randint(length, max_length) == max_length and length >= min_length:
                text += " "
                last_letter = ""
                done = True
            if vow_count == max_vowels:
                current_letter = consonants
                vow_count = 0
            elif con_count == max_consonants:
                current_letter = vowels
                con_count = 0

    # Output to file if provided, otherwise print to console
    if len(given_files) == 1:
        try:
            with open(given_files[0], "w") as file:
                file.write(text)
                print("Written output to file '" + file.name + "'")
        except OSError:
            print("Failed to write to file '" + file.name + "'")
    else:
        print(text)
        input("\nPress enter to continue...")


def help():
    print("Usage: python3 langgen.py [OPTIONS] [FILE]\n"
          "If a file is provided, program will write to the file, otherwise it will output to the console.\n"
          "\n"
          "-v, --vowels <string>            List of all allowed vowels (default: \"aeiouy\")\n"
          "-c, --consonants <string>        List of all allowed consonants (default: \"bcdfghjklmnpqrstvwxz\")\n"
          "-V, --max-vowels <number>        Maximum amount of allowed vowels in a row (default: 3)\n"
          "-C, --max-consonants <number>    Maximum amount of allowed consonants in a row (default: 3)\n"
          "-r, --allow-repeats <bool>       Whether the same letter can be repeated multiple times in a row (default: true)\n"
          "-w, --total-words <number>       Total amount of words to generate (default: 100)\n"
          "-l, --min-length <number>        Minimum allowed word length (default: 1)\n"
          "-L, --max-length <number>        Maximum allowed word length (default: 10)\n"
          "-s, --switch-chance <number>     Chance of switching between vowel and consonant after every new letter until max, a value of 25 means a 25% chance (default: 50)")


main()
