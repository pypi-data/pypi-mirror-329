from os import path, makedirs
import tkinter, tkinter.filedialog, string, json
import ziz_utils

def Caesar(user_input: str, shift: int) -> str:
    """
    Process texts into Caesar Cipher. By default, this only encipher texts, input minus shift if you want to decipher texts.
    
    :type input: str
    :param input: The text you want to process.
    :type shift: int
    :param shift: The text you want to process.
    """
    output = ""
    ALPHABET, ALPHABET_UPPER = [*string.ascii_lowercase], [*string.ascii_uppercase]
    shifted =  ALPHABET[shift % 26:] + ALPHABET[:shift % 26]
    shifted_upper = ALPHABET_UPPER[shift % 26:] + ALPHABET_UPPER[:shift % 26]
    for k in user_input:
        if k in ALPHABET:
            output += shifted[ALPHABET.index(k)]
        elif k in ALPHABET_UPPER:
            output += shifted_upper[ALPHABET_UPPER.index(k)]
        else:
            output += k
    return output

def Vigenere(user_input: str, key: str, decipher_mode: bool = False) -> str:
    """
    Process texts into Vigenere Cipher.

    :type input: str
    :param input: The text you want to process.
    :type key: str
    :param key: A Vigenere Cipher's key. It is practically impossible to crack Vigenere Cipher without this.
    :type decipher_mode: bool
    :param decipher_mode: Choose to decipher instead of encipher. Default is False.
    """
    char_map = {i: char for i, char in enumerate(user_input) if char not in string.ascii_letters}
    user_input = "".join([x for x in user_input if x in string.ascii_letters])
    while len(key) != len(user_input):
        if len(key) > len(user_input):
            key = key[:len(user_input):]
        elif len(key) < len(user_input):
            key = key * 2

    ALPHABET = string.ascii_lowercase
    UPPER_ALPHABET = string.ascii_uppercase
    output = []
    for i, char in enumerate(user_input):
        shift = ALPHABET.index(key[i])

        if char.islower():
            alphabet = ALPHABET
        else:
            alphabet = UPPER_ALPHABET

        if not decipher_mode:
            ciphered = alphabet[(alphabet.index(char) + shift) % len(alphabet)]
        else:
            ciphered = alphabet[(alphabet.index(char) - shift) % len(alphabet)]
        
        output.append(ciphered)
    
    for i, j in char_map.items():
        output.insert(i, j)
    
    return "".join(output)

def main() -> None:
    """
    The main function
    """
    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    config_file_name = "config.json"
    config_folder = path.join(path.expanduser("~"), "caesar_config")
    config_path = path.join(config_folder, config_file_name)

    illegal_chars = [*r'\/:*?"<>|']
    ciphering_schemes = ["Caesar", "Vigenere"]
    def_config = {
        "mode": "Caesar",
        "output_path": "",
        "output_file_name": "output.txt"
    }

    makedirs(config_folder, exist_ok=True)
    ziz_utils.config_manager(def_config, config_folder, config_file_name)

    with open(config_path) as file:
        config = json.load(file)
    
    if config["output_path"] == "":
        output_folder = tkinter.filedialog.askdirectory(title="Choose your output folder (Cancel to quit)")
        if not output_folder:
            return
        with open(config_path, "w") as file:
            config["output_path"] = output_folder
            json.dump(config, file, ensure_ascii = False, indent = 4)
    
    ziz_utils.clear()
    while True:
        mode = 0
        cmd = input("1. Enciphering. \n2. Deciphering. \n3. Settings. \n4. Exit. \nYour input: ").strip()
        ziz_utils.clear()

        if not cmd:
            print("Invalid input: Empty input. \n")
            continue
        elif cmd not in [*"1234"]:
            print("Invalid input: Command does not exist. \n")
            continue
        elif cmd == "4":
            root.destroy()
            exit(0)

        while cmd == "3":
            option = input(f"""1. Choose ciphering scheme.
2. Set output folder.
3. Set output file name.
4. Go back.
5. Reset config to default.
Your input: """).strip()
            ziz_utils.clear()

            match option:
                case "4":
                    break
                case "2":
                    output_folder = tkinter.filedialog.askdirectory(title="Choose your output folder")
                    if output_folder:
                        config["output_folder"] = output_folder
                        ziz_utils.write_config(def_config, config, config_folder, config_file_name)
                        print("Success. \n")
                    else:
                        print("Cancelled. \n")
                case "5":
                    while True:
                        confirm = input("Do you wish to reset the config to default? [Y/N]: ").strip()
                        ziz_utils.clear()

                        if confirm.lower() == "y":
                            config = def_config
                            output_folder = tkinter.filedialog.askdirectory(title="Choose your output folder (Cancel to quit)")
                            if output_folder == "":
                                return
                            
                            config["output_folder"] = output_folder
                            ziz_utils.write_config(def_config, config, config_folder, config_file_name)
                        elif confirm.lower() == "n":
                            break
                        else:
                            print("Invalid input: Option does not exist.\n")
                    continue
                case "1":
                    options = [str(x) for x in range(1, len(ciphering_schemes) + 2)]
                    while True:
                        print(f"Current ciphering scheme: {config["mode"]}.")
                        option = input(f"""{ziz_utils.menu(ciphering_schemes)}
3. Go back.
Your input: """).strip()
                        ziz_utils.clear()

                        if option not in options:
                            print("Invalid input: Option does not exist. \n")
                            continue
                        elif option == "3":
                            break
                        
                        config["mode"] = ciphering_schemes[int(option) - 1]
                        ziz_utils.write_config(def_config, config, config_folder, config_file_name)
                case "3":
                    while True:
                        output_file_name = input("""Type the name of your output file, leave empty to cancel.
(If the name does not contain an extension then the program will automatically add a .txt extension): """).strip()
                        ziz_utils.clear()

                        if not output_file_name:
                            print("Cancelled. \n")
                            break
                        elif any(char in output_file for char in illegal_chars):
                            print("Invalid input: File name contains illegal character(s). \n")
                            continue
                        elif "." not in output_file:
                            output_file += ".txt"
                        elif output_file.endswith("."):
                            output_file += "txt"
                        config["output_file_name"] = output_file_name
                        ziz_utils.write_config(def_config, config, config_folder, config_file_name)
                        print(f'Successful. Output file is now "{output_file_name}". \n')
                case _:
                    print("Invalid input: Option does not exist. \n")

        while cmd != "3":
            mode = input("1. Input from keyboard. \n2. Input from file. \n3. Cancel. \nYour input: ").strip()
            ziz_utils.clear()

            if not mode:
                print("Invalid input: Empty input. \n")
            elif mode not in [*"123"]:
                print("Invalid input: Option does not exist. \n")
            else:
                break
            
        while mode == "1":
            user_input = input("Your input: ").strip()
            ziz_utils.clear()
            temp = ["Shift", "Key"]

            while True:
                match config["mode"]:
                    case "Caesar":
                        shift = input("Shift (Enter / to go back): ").strip()
                        ziz_utils.clear()

                        if shift == "/":
                            break
                        elif not shift:
                            print("Invalid input: Empty input. \n")
                            continue
                        elif ziz_utils.isInt(shift) and shift != "/" and not shift:
                            print("Invalid input: Input has to be an integer. \n")
                            continue
                    case "Vigenere":
                        shift = input("Key (Enter / to go back): ")
                        ziz_utils.clear()

                        if shift == "/":
                            break
                        elif not shift:
                            print("Invalid input: Empty input. \n")
                            continue
                        elif any(char not in string.ascii_letters for char in shift):
                            print("Invalid input: Input cannot contain non-alphabetical character(s). \n")
                            continue
        
                match config["mode"]:
                    case "Caesar":
                        if cmd == "1":
                            content = Caesar(user_input, int(shift))
                        elif cmd == "2":
                            content = Caesar(user_input, -int(shift))
                    case "Vigenere":
                        if cmd == "1":
                            content = Vigenere(user_input, shift)
                        elif cmd == "2":
                            content = Vigenere(user_input, shift, True)
                
                print(f"""Input: {user_input}")
{temp[ciphering_schemes.index(config["mode"])]}: {shift}")
"Result: {content} \n""")
            break

        while mode == "2":
            input_file = tkinter.filedialog.askopenfilename(title="Choose your input file (cancel to go back to main menu)", 
                                                            filetypes=[("All files", "*.*")])
            if not input_file:
                break
            
            while True:
                match config["mode"]:
                    case "Caesar":
                        shift = input("Shift (Enter / to go back): ").strip()
                        ziz_utils.clear()
                        
                        if shift == "/":
                            break
                        elif not shift:
                            print("Invalid input: Empty input. \n")
                            continue
                        elif ziz_utils.isInt(shift) and shift != "/" and not shift:
                            print("Invalid input: Input has to be an integer. \n")
                            continue
                    case "Vigenere":
                        shift = input("Key (Enter / to go back): ")
                        ziz_utils.clear()

                        if shift == "/":
                            break
                        elif not shift:
                            print("Invalid input: Empty input. \n")
                            continue
                        elif any(char not in string.ascii_letters for char in shift):
                            print("Invalid input: Input cannot contain non-alphabetical character(s). \n")
                            continue
                
                with open(input_file) as file:
                    user_input = file.read()

                match config["mode"]:
                    case "Caesar":
                        if cmd == "1":
                            content = Caesar(user_input, int(shift))
                        elif cmd == "2":
                            content = Caesar(user_input, -int(shift))
                    case "Vigenere":
                        if cmd == "1":
                            content = Vigenere(user_input, shift)
                        elif cmd == "2":
                            content = Vigenere(user_input, shift, True)

                with open(path.join(config["output_path"], config["output_file_name"]), "w") as file:
                    file.write(content)
                print(f"Success. Content write to {config["output_path"]}.")
            break

if __name__ == "__main__":
    main()