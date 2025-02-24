# Określ nazwę pliku txt
file_name: str = "./unformatted.txt"

found_words = []

coins = open("coins.txt", "w", encoding="utf-8")
coins.write("(")


try:
    with open(file_name, "r") as file:
        for line_number, line in enumerate(file, 1):
            if line.startswith(
                (
                    "a",
                    "A",
                    "b",
                    "B",
                    "c",
                    "C",
                    "d",
                    "D",
                    "e",
                    "E",
                    "f",
                    "F",
                    "g",
                    "G",
                    "h",
                    "H",
                    "i",
                    "I",
                    "j",
                    "J",
                    "k",
                    "K",
                    "l",
                    "L",
                    "m",
                    "M",
                    "n",
                    "N",
                    "o",
                    "O",
                    "p",
                    "P",
                    "q",
                    "Q",
                    "r",
                    "R",
                    "s",
                    "S",
                    "t",
                    "T",
                    "u",
                    "U",
                    "v",
                    "V",
                    "w",
                    "W",
                    "x",
                    "X",
                    "y",
                    "Y",
                    "z",
                    "Z",
                )
            ):
                if not line.isupper():
                    if not (line in found_words):
                        coin = line.lower()
                        coin = coin.replace(" ", "-")
                        coin = coin.replace("\n", "")
                        print("writing: ", coin)
                        found_words.append(line)
                        coin = f"'{coin}',"
                        print(coin)
                        coins.write(coin)
    coins.write(")")

except FileNotFoundError:
    print(f"File '{file_name}' does not exist.")
except Exception as e:
    print(f"Error occured: {e}")
