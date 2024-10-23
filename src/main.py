from gui.main_menu import MainMenu
import tkinter as tk


def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Magic Cube Solver")

    # Initialize the main menu
    main_menu = MainMenu(root)
    main_menu.pack(fill='both', expand=True)

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
