import os
import sys
import time


class Cat:
    def __init__(self, name="Mırmır", kiss_symbol="💋", heart_symbol="❤"):
        self.name = name
        self.kiss_symbol = kiss_symbol
        self.heart_symbol = heart_symbol

    def _clear_terminal(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def blow_kiss(self, target="sahip"):
        frames = [
            f"{self.name}: Miauu! {self.kiss_symbol}",
            f"{self.name}: {self.kiss_symbol}   {self.heart_symbol}",
            f"{self.name}:  {self.kiss_symbol}  {self.heart_symbol}",
            f"{self.name}:   {self.kiss_symbol} {self.heart_symbol}",
            f"{self.name}:    {self.kiss_symbol}{self.heart_symbol}",
            f"{self.name}:     {self.heart_symbol} -> {target}",
            f"{target}: \"Ay! Teşekkürler {self.name}!\"",
        ]

        for frame in frames:
            self._clear_terminal()
            print(frame)
            time.sleep(0.4)


def main():
    name = "Mırmır"
    target = "sahip"

    if len(sys.argv) > 1:
        name = sys.argv[1]
    if len(sys.argv) > 2:
        target = sys.argv[2]

    cat = Cat(name=name)
    cat.blow_kiss(target=target)


if __name__ == "__main__":
    main()

