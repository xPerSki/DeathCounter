from customtkinter import *
import threading
import time
import keyboard
import utils
import detect
import pygame


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

        self.death_counter_increment = utils.get_setting("death_counter_increment")
        self.death_counter_decrement = utils.get_setting("death_counter_decrement")
        self._reload_hotkeys()
        self.font = ("Consolas", 16)

        self.title("p e r s k i _ _")
        self.geometry("400x210")
        self.resizable(False, False)
        self.iconbitmap("stuff/twitch.ico")
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
        self.detection_thread = None
        self.detection_running = False
        self.sleep_after_death = float(utils.get_setting("sleep_after_death"))
        self.sleep_interval = float(utils.get_setting("sleep_interval"))
        self.sleep_after_error = float(utils.get_setting("sleep_after_error"))
        self.death_sound_effect = utils.get_setting("death_sound_effect")
        if self.death_sound_effect:
            pygame.mixer.init()
            pygame.mixer.music.load(self.death_sound_effect)

        self.auto_detect_box = CTkCheckBox(self, text="Auto detect death", font=self.font, command=self._flip_toggle)
        self.auto_detect_box.configure(
            fg_color="#4c1d99",
            hover_color="#5a1f9c",
            border_color="white",
            border_width=2,
        )
        self.auto_detect_box.grid(row=3, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="nsew")

    def _flip_toggle(self):
        if self.auto_detect_box.get():

            self.start_detection()
        else:
            self.stop_detection()

    def start_detection(self):
        if self.detection_thread and self.detection_thread.is_alive():
            return

        self.detection_running = True
        self.detection_thread = threading.Thread(target=self._detection_loop)
        self.detection_thread.start()

    def stop_detection(self):
        self.detection_running = False
        if self.detection_thread:
            self.detection_thread.join(timeout=1)

    def _detection_loop(self):
        death_screen = utils.get_setting("death_screen")
        while self.detection_running:
            try:
                if detect.detect_death_screen(death_screen):
                    utils.death_count(True)
                    print("Death detected!")
                    if self.death_sound_effect:
                        pygame.mixer.music.play()
                    time.sleep(self.sleep_after_death)  # sleep after death
                else:
                    time.sleep(self.sleep_interval)  # sleep interval
            except Exception as e:
                print(f"Error during detection: {e}")
                time.sleep(self.sleep_after_error)

    def create_bind_window(self, bind):
        dialog = CTkInputDialog(title="Bind Key", text="Press a key to bind:")

        key = dialog.get_input()
        if key is None or key == "" or len(key) > 1 or not key.isprintable():
            return

        self.change_bind(bind, key)

    def change_bind(self, bind, key):
        utils.save_setting(bind, key.upper())
        self.reload_binds()

    def reload_binds(self):
        self.death_counter_increment = utils.get_setting("death_counter_increment")
        self.death_counter_decrement = utils.get_setting("death_counter_decrement")
        self.increment_label.configure(text=f"+1 bound to '{self.death_counter_increment}'")
        self.decrement_label.configure(text=f"-1 bound to '{self.death_counter_decrement}'")
        self._reload_hotkeys()

    def _reload_hotkeys(self):
        death_counter_increment = self.death_counter_increment
        death_counter_decrement = self.death_counter_decrement
        if keyboard._hotkeys:
            keyboard.unhook_all_hotkeys()
        keyboard.add_hotkey(death_counter_increment, utils.death_count, args=(True,))
        keyboard.add_hotkey(death_counter_decrement, utils.death_count, args=(False,))

    def destroy(self):
        self.stop_detection()
        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
