import os
import time
import webbrowser
from rich.console import Console
from rich.text import Text

# Secret key to unlock the surprise
SECRET_KEY = "663688"

# YouTube song link
YOUTUBE_URL = "https://astrasoftwares.github.io/Heart/"

# Lyrics to display
lyrics = [
    "🎵 You are the reason I smile every day...",
    "🎶 Every heartbeat sings your name...",
    "💖 Forever and always, my love! 💖"
]

console = Console()

def show_lyrics():
    for line in lyrics:
        text = Text(line, style="bold magenta")
        console.print(text)
        time.sleep(3)

def main():
    console.print("\n[bold blue]Welcome to My Wish 💖[/bold blue]\n")
    user_key = input("Enter the secret key to unlock your wish: ")

    if user_key == SECRET_KEY:
        console.print("\n[green]Access granted! Enjoy your surprise 💖[/green]\n")
        webbrowser.open(YOUTUBE_URL)
        time.sleep(2)
        show_lyrics()
        console.print("\n[bold red]💘 Forever and always! 💘[/bold red]\n")
    else:
        console.print("\n[red]Incorrect key! Try again later. 💔[/red]\n")

if __name__ == "__main__":
    main()