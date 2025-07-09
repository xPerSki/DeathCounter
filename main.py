from customtkinter import *
from time import sleep
import keyboard
import utils
import detect


class CustomButton(CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            corner_radius=7,
            border_width=2,
            border_color="white",
            fg_color="#4c1d99",
            hover_color="#5a1f9c"
        )


class App(CTk):
    def __init__(self):
        super().__init__()

        self.death_counter_increment = utils.get_action_bind("death_counter_increment")
        self.death_counter_decrement = utils.get_action_bind("death_counter_decrement")
        self.font = ("Consolas", 16)

        self.title("p e r s k i _ _")
        self.geometry("400x210")
        self.resizable(False, False)
        self.iconbitmap("twitch.ico")
        self._set_appearance_mode("dark")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # title
        self.label = CTkLabel(self, text="Death Counter", font=self.font)
        self.label.grid(row=0, column=0, columnspan=2, sticky="", pady=10)

        # +1
        self.increment_label = CTkLabel(self, text=f"+1 bound to '{self.death_counter_increment}'", font=self.font)
        self.increment_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.increment_button = CustomButton(self,
                                             text="bind",
                                             command=lambda: self.create_bind_window("death_counter_increment"))
        self.increment_button.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        # -1
        self.decrement_label = CTkLabel(self, text=f"-1 bound to '{self.death_counter_decrement}'", font=self.font)
        self.decrement_label.grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.decrement_button = CustomButton(self,
                                             text="bind",
                                             command=lambda: self.create_bind_window("death_counter_decrement"))
        self.decrement_button.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # auto detect death
        self.auto_detect_box = CTkCheckBox(self, text="Auto detect death", font=self.font, command=self._flip_toggle)
        self.auto_detect_box.configure(
            fg_color="#4c1d99",
            hover_color="#5a1f9c",
            border_color="white",
            border_width=2,
        )
        self.auto_detect_box.grid(row=3, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="nsew")
        self.auto_detect_tooltip = CTkLabel(self, text="*To turn off, restart the app", font=("Consolas", 12))
        self.auto_detect_tooltip.grid(row=4, column=0, padx=10)

    def _flip_toggle(self):
        self.auto_detect_box.configure(state="off")
        death_screen = utils.get_action_bind("death_screen_image")
        while True:
            if detect.detect_death_screen(death_screen):
                utils.death_count(True)
                print("Death detected!")
                sleep(0.77)

    def create_bind_window(self, bind):
        dialog = CTkInputDialog(title="Bind Key", text="Press a key to bind:")

        key = dialog.get_input()
        if key is None or key == "" or len(key) > 1 or not key.isprintable():
            return

        self.change_bind(bind, key)

    def change_bind(self, bind, key):
        utils.save_action_bind(bind, key.upper())
        self.reload_binds()

    def reload_binds(self):
        self.death_counter_increment = utils.get_action_bind("death_counter_increment")
        self.death_counter_decrement = utils.get_action_bind("death_counter_decrement")
        self.increment_label.configure(text=f"+1 bound to '{self.death_counter_increment}'")
        self.decrement_label.configure(text=f"-1 bound to '{self.death_counter_decrement}'")


class KeyBinds:
    def __init__(self):
        self.death_counter_increment = utils.get_action_bind("death_counter_increment")
        self.death_counter_decrement = utils.get_action_bind("death_counter_decrement")

        keyboard.add_hotkey(self.death_counter_increment, utils.death_count, args=(True,))
        keyboard.add_hotkey(self.death_counter_decrement, utils.death_count, args=(False,))


if __name__ == "__main__":
    app = App()
    key_binds = KeyBinds()
    app.mainloop()
