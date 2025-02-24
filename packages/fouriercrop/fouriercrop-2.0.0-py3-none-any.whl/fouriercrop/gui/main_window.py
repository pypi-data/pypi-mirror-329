"""GUI application."""

import logging
import os
import signal
import subprocess
import threading
import tkinter as tk
import tkinter.messagebox as messagebox
from functools import partial
from pathlib import Path
from tkinter import filedialog
from typing import Callable, Dict, Tuple, Union

import customtkinter
from PIL import Image

from .. import __version__

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme(Path(__file__).resolve().parent / "resources/color.json")
version = f"v{__version__}"


class CustomInputDialog(customtkinter.CTkInputDialog):
    """Customs input dialog with customizable dimensions."""

    def __init__(
        self,
        title: str = "Custom Dialog",
        text: str = "Please input:",
        width: int = 300,
        height: int = 150,
    ) -> None:
        """Initializes."""
        super().__init__(title=title, text=text)
        self.geometry(f"{width}x{height}")


class TextboxHandler(logging.Handler):
    """Customs logging handler to direct log messages to a GUI textbox widget."""

    def __init__(self, textbox: customtkinter.CTkTextbox) -> None:
        """Initializes."""
        super().__init__()
        self.textbox = textbox

    def emit(self, record: logging.LogRecord) -> None:
        """Inserts log messages into the textbox."""
        log_message = self.format(record)
        self.textbox.insert("end", log_message + "\n")
        self.textbox.see("end")


def setup_logging(textbox: customtkinter.CTkTextbox, logger_name: str) -> logging.Logger:
    """Configures a logger to use the TextboxHandler with a specified format."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    textbox_handler = TextboxHandler(textbox)
    formatter = logging.Formatter(
        fmt="%(asctime)s, %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    textbox_handler.setFormatter(formatter)
    logger.addHandler(textbox_handler)
    return logger


class App(customtkinter.CTk):
    """Represents the main application window using customtkinter."""

    def __init__(self, width: int = 1100, height: int = 580, version: str = version) -> None:
        """Initializes."""
        super().__init__()

        self.title(version)
        self.geometry(f"{width}x{height}")

        # Set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Load images with light and dark mode image
        image_path = Path(__file__).resolve().parent / "resources"
        self.logo_image = customtkinter.CTkImage(
            Image.open(image_path / "logo.png"), size=(200, 100)
        )

        # To keep track of the running process
        self.process = None
        self.stop_event = threading.Event()
        self.loggers: Dict[str, logging.Logger] = {}

        # Create frames
        self.build_navigation()
        self.build_execute_panel()

        # Select default frame
        self.select_panel_event("execute_panel")
        self.appearance_mode_menu.set("System")
        self.scaling_optionemenu.set("100%")

    # ================================

    def run_cmd(self, textbox: customtkinter.CTkInputDialog, cmd: str) -> None:
        """Executes command in a separate thread and appends its output to textbox."""
        self.stop_event.clear()  # Reset the stop event

        def append_text(textbox: customtkinter.CTkInputDialog, text: str) -> None:
            """Appends text to the textbox and scrolls to the end."""
            textbox.insert("end", text + "\n")
            textbox.yview_moveto(1)

        def execute() -> None:
            try:
                self.process = subprocess.Popen(  # noqa: S602
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    text=True,
                    preexec_fn=os.setsid,  # type: ignore[attr-defined]
                )

                while True:
                    if self.stop_event.is_set():
                        # Terminate the process group
                        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)  # type: ignore[attr-defined]
                        append_text(textbox, "Command terminated by user.")
                        break

                    # Read output line by line
                    if self.process.stdout is not None:
                        line = self.process.stdout.readline()
                        if not line:  # Break loop when no more output
                            break
                        append_text(textbox, line.strip())

                self.process.wait()  # Wait for process to exit
                if not self.stop_event.is_set():  # Only show finished message if not terminated
                    append_text(
                        textbox,
                        f"Command finished with return code {self.process.returncode}",
                    )
            except Exception as e:  # noqa: BLE001
                append_text(textbox, f"Error: {e!s}")
            finally:
                # Reset buttons after command finishes
                self.process = None

        threading.Thread(target=execute, daemon=True).start()

    def get_label(
        self,
        master: customtkinter,
        text: str,
        row: int,
        column: int,
        pady: Union[int, Tuple] = 5,
    ) -> None:
        """Creates and places a custom label widget in the specified grid location."""
        label = customtkinter.CTkLabel(master, text=text, anchor="e", compound="right")
        label.grid(row=row, column=column, padx=(20, 0), pady=pady, sticky="e")

    def create_control_button(
        self,
        frame: customtkinter.CTkFrame,
        text: str,
        command: Callable,
        size: int = 14,
        weight: str = "normal",
        width: int = 140,
    ) -> customtkinter.CTkButton:
        """Creates a custom button with specified properties."""
        return customtkinter.CTkButton(
            frame,
            text=text,
            command=command,
            font=customtkinter.CTkFont(size=size, weight=weight),
            width=width,
        )

    # ================================

    def build_navigation(self) -> None:
        """Constructs the navigation panel."""

        def create_button(
            master: customtkinter.CTkFrame,
            text: str,
            command: Callable,
            image: customtkinter.CTkImage = None,
        ) -> customtkinter.CTkButton:
            """Creates a custom button with specified properties."""
            return customtkinter.CTkButton(
                master,
                corner_radius=0,
                height=40,
                border_spacing=20,
                text=text,
                font=customtkinter.CTkFont(size=16, weight="bold"),
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                image=image,
                anchor="w",
                command=command,
            )

        buttons_info = [
            ("Execute", "execute_panel"),
        ]
        buttons_num = len(buttons_info)

        navigation_panel = customtkinter.CTkFrame(self, corner_radius=0)
        master = navigation_panel
        master.grid(row=0, column=0, sticky="nsew")
        master.grid_rowconfigure(buttons_num + 1, weight=1)
        padx = 20
        pady = 20

        # LOGO
        logo = customtkinter.CTkLabel(
            master,
            text="",
            image=self.logo_image,
            compound="center",
        )
        logo.grid(row=0, column=0, padx=padx, pady=pady)

        # Buttons
        for idx, (text, panel_name) in enumerate(buttons_info, start=1):
            button = create_button(
                master,
                text=text,
                command=partial(self.select_panel_event, panel_name),
            )
            button.grid(row=idx, column=0, sticky="ew")
            setattr(self, f"{panel_name}_button", button)

        # Adjust frame
        adjust_frame = customtkinter.CTkFrame(master, fg_color="transparent")
        adjust_frame.grid(row=buttons_num + 2, column=0, padx=padx, pady=pady, sticky="nsew")

        ## Appearance Mode
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            adjust_frame,
            width=90,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
            anchor="center",
        )
        self.appearance_mode_menu.grid(row=0, column=0, padx=(0, 10), pady=0)

        ## UI Scaling
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            adjust_frame,
            width=90,
            values=["80%", "100%", "120%", "140%", "160%", "180%", "200%"],
            command=self.change_scaling_event,
            anchor="center",
        )
        self.scaling_optionemenu.grid(row=0, column=1, padx=(10, 0), pady=0)

    def build_execute_panel(self) -> None:
        """Constructs the execute panel."""
        self.execute_var = {}

        self.execute_panel = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        master = self.execute_panel
        master.grid_columnconfigure((0), weight=1)
        master.grid_rowconfigure((1), weight=1)
        # --------------------------------

        control_frame = customtkinter.CTkFrame(master)
        control_frame.grid(row=0, column=1, rowspan=2, padx=0, pady=0, sticky="nsew")
        control_frame.grid_columnconfigure(0, weight=1)

        fc_1 = customtkinter.CTkFrame(control_frame, fg_color="transparent")
        fc_1.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        fc_1.grid_columnconfigure((0, 1, 2), weight=1)
        fc_2 = customtkinter.CTkFrame(control_frame, fg_color="transparent")
        fc_2.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        fc_3 = customtkinter.CTkFrame(control_frame, fg_color="transparent")
        fc_3.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")

        buttons_info = [
            (fc_1, "Clear", self.clear_execute_event, 12, "normal", 20, 0, 0),
            (fc_1, "Stop", self.stop_cmd_event, 12, "normal", 20, 2, 0),
            (fc_2, "Run", self.run_execute_event, 14, "bold", 140, 0, 0),
        ]

        # Buttons
        for frame, text, command, size, weight, width, column, padx in buttons_info:
            button = self.create_control_button(frame, text, command, size, weight, width)
            button.grid(row=0, column=column, padx=padx, pady=0, sticky="nsew")

        self.execute_var["memo"] = tk.StringVar()
        execute_memo_entry = customtkinter.CTkEntry(fc_3, textvariable=self.execute_var["memo"])
        execute_memo_entry.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # --------------------------------

        padx = (10, 20)  # type: ignore[assignment]
        pady = 5

        frame_2 = customtkinter.CTkFrame(master, fg_color="transparent")
        frame_2.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")
        frame_2.grid_columnconfigure(0, weight=1)
        frame_2.grid_rowconfigure(0, weight=1)

        scroll_1 = customtkinter.CTkScrollableFrame(frame_2, label_text=" ")
        scroll_1.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        scroll_1.grid_columnconfigure(1, weight=1)

        infos = [
            (
                "Input path:",
                "input_path",
                customtkinter.CTkButton,
                {
                    "command": self.select_execute_inp_event,
                },
            ),
            (
                "Output path:",
                "output_path",
                customtkinter.CTkButton,
                {
                    "command": self.select_execute_out_event,
                },
            ),
            (
                "Bin factor:",
                "bin_factor",
                customtkinter.CTkComboBox,
                {"values": ["1", "2", "4", "6", "8"]},
            ),
            (
                "Pad mode:",
                "pad_mode",
                customtkinter.CTkComboBox,
                {"values": ["0", "1", "2"]},
            ),
            ("Norm:", "norm_flag", customtkinter.CTkCheckBox, {"text": ""}),
        ]

        for row, (label_text, var_name, widget_class, widget_kwargs) in enumerate(infos):
            self.get_label(
                scroll_1,
                text=label_text,
                row=row,
                column=0,
                pady=(0, pady) if row == 0 else pady,
            )
            if var_name == "norm_flag":
                self.execute_var[var_name] = tk.IntVar()  # type: ignore[assignment]
            else:
                self.execute_var[var_name] = tk.StringVar()

            if widget_class in [
                customtkinter.CTkOptionMenu,
                customtkinter.CTkComboBox,
                customtkinter.CTkCheckBox,
            ]:
                widget = widget_class(
                    scroll_1, variable=self.execute_var[var_name], **widget_kwargs
                )
            else:
                widget = widget_class(
                    scroll_1, textvariable=self.execute_var[var_name], **widget_kwargs
                )

            widget.grid(
                row=row,
                column=1,
                padx=padx,
                pady=(0, pady) if row == 0 else pady,
                sticky="ew",
            )

        # default
        self.execute_var["bin_factor"].set("2")
        self.execute_var["pad_mode"].set("0")

        # create textbox
        self.execute_textbox = customtkinter.CTkTextbox(master, width=200, wrap="word")
        self.execute_textbox.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")  # rowspan=2,
        logger_name = "execute"
        self.loggers[logger_name] = setup_logging(self.execute_textbox, logger_name)

    # ================================

    def stop_cmd_event(self) -> None:
        """Stops a running process."""
        if self.process and self.process.poll() is None:  # Check if the process is running
            self.stop_event.set()  # Signal the thread to stop

    def on_close(self) -> None:
        """Handles the application's close event."""
        if self.process and self.process.poll() is None:
            if messagebox.askyesno("Exit Confirmation", "The program is running. Confirm exit?"):
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)  # type: ignore[attr-defined]
                while True:
                    if self.process.poll() is not None:
                        self.destroy()
                        break
            else:
                pass
        else:
            self.destroy()

    # ================================

    def select_panel_event(self, name: str) -> None:
        """Selects a panel by name and updates the UI accordingly."""
        maps = {
            "execute_panel": (self.execute_panel_button, self.execute_panel),
        }

        # Set button color for selected button and show the corresponding panel
        for panel_name, (button, panel) in maps.items():
            if name == panel_name:
                button.configure(fg_color=("gray75", "gray25"))
                panel.grid(row=0, column=1, sticky="nsew")
            else:
                button.configure(fg_color="transparent")
                panel.grid_forget()

    def change_appearance_mode_event(self, inp: str) -> None:
        """Changes the appearance mode of the application."""
        customtkinter.set_appearance_mode(inp)

    def change_scaling_event(self, inp: str) -> None:
        """Adjusts the widget scaling based on the input percentage string."""
        inp = int(inp.rstrip("%")) / 100  # type: ignore[assignment]
        customtkinter.set_widget_scaling(inp)

    # ================================

    def select_execute_inp_event(self) -> None:
        """Prompts user to select a file path."""
        file_path = filedialog.askopenfilename(
            title="Select File File for Running",
            filetypes=[("MRC Files", "*.mrc"), ("All Files", "*.*")],
        )

        if file_path:
            self.execute_var["input_path"].set(file_path)

    def select_execute_out_event(self) -> None:
        """Prompts user to select a file path and saves output."""
        stem = Path(self.execute_var["input_path"].get()).stem
        bin_factor = self.execute_var["bin_factor"].get()
        bin_factor = "2" if bin_factor in [None, "None", ""] else bin_factor
        name = f"{stem}_bin{bin_factor}"

        file_path = filedialog.asksaveasfilename(
            title="Select Directory for Saving",
            initialfile=name,
            defaultextension=".mrc",
            filetypes=[("MRC Files", "*.mrc"), ("All Files", "*.*")],
        )
        self.execute_var["output_path"].set(file_path)

    def clear_execute_event(self) -> None:
        """Clears the execute_textbox and resets execute_var values."""
        self.execute_textbox.delete("1.0", "end")
        for key, var in self.execute_var.items():
            var.set(0 if key == "norm_flag" else "")  # type: ignore[arg-type]

    def run_execute_event(self) -> None:
        """Executes the shell command."""
        # --norm-flag
        norm_flag = self.execute_var["norm_flag"].get()
        cmd = "fouriercrop " if norm_flag == 0 else "fouriercrop --norm-flag "

        # --input-path
        input_path = self.execute_var["input_path"].get()
        if input_path not in [None, "None", ""]:
            if Path(input_path).exists():
                cmd += f"--input-path {input_path} "

        # --output-path
        output_path = self.execute_var["output_path"].get()
        if output_path not in [None, "None", ""]:
            cmd += f"--output-path {output_path} "

        # --bin-factor
        bin_factor = self.execute_var["bin_factor"].get()
        if bin_factor not in [None, "None", ""]:
            cmd += f"--bin-factor {bin_factor} "

        # --pad-mode
        pad_mode = self.execute_var["pad_mode"].get()
        if pad_mode not in [None, "None", ""]:
            cmd += f"--pad-mode {pad_mode} "

        if "cmd" in self.execute_var["memo"].get():
            self.loggers["execute"].info(cmd)
        else:
            self.loggers["execute"].info(f"Run {cmd}\n\n")
            self.run_cmd(self.execute_textbox, cmd)


def launch_gui() -> None:
    """Initializes and runs the GUI application."""
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()


if __name__ == "__main__":
    launch_gui()
