"""Secret Scroll Caesar Cipher.

A small educational desktop application for encrypting and decrypting text
with the classical Caesar cipher.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from caesar_cipher import decrypt, encrypt


APP_NAME = "Secret Scroll Caesar Cipher"


class SecretScrollApp:
    """Tkinter interface for the Caesar cipher functions."""

    BG = "#17152B"
    PANEL = "#24203D"
    INPUT_BG = "#302B4F"
    TEXT = "#F7F6FB"
    MUTED = "#B8B3CA"
    ACCENT = "#7C6FF0"
    ACCENT_HOVER = "#9186F5"
    BORDER = "#4B4569"
    SUCCESS = "#74C69D"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("900x650")
        self.root.minsize(720, 560)
        self.root.configure(bg=self.BG)

        self.shift_var = tk.StringVar(value="3")
        self.status_var = tk.StringVar(value="Ready")

        self._configure_styles()
        self._build_interface()
        self.root.bind("<Control-Return>", lambda _event: self._process("encrypt"))

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.TFrame", background=self.BG)
        style.configure("Panel.TFrame", background=self.PANEL)
        style.configure(
            "Accent.TButton",
            background=self.ACCENT,
            foreground="white",
            borderwidth=0,
            focusthickness=3,
            focuscolor=self.ACCENT,
            font=("Arial", 11, "bold"),
            padding=(18, 11),
        )
        style.map("Accent.TButton", background=[("active", self.ACCENT_HOVER)])
        style.configure(
            "Secondary.TButton",
            background=self.INPUT_BG,
            foreground=self.TEXT,
            bordercolor=self.BORDER,
            font=("Arial", 11, "bold"),
            padding=(18, 11),
        )
        style.map("Secondary.TButton", background=[("active", self.BORDER)])
        style.configure(
            "Shift.TSpinbox",
            fieldbackground=self.INPUT_BG,
            foreground=self.TEXT,
            arrowcolor=self.TEXT,
            bordercolor=self.BORDER,
            insertcolor=self.TEXT,
            padding=8,
        )

    def _build_interface(self) -> None:
        container = ttk.Frame(self.root, style="App.TFrame", padding=(40, 32))
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="SECRET SCROLL",
            bg=self.BG,
            fg=self.ACCENT_HOVER,
            font=("Arial", 11, "bold"),
        ).pack(anchor="w")
        tk.Label(
            container,
            text="Caesar Cipher",
            bg=self.BG,
            fg=self.TEXT,
            font=("Arial", 30, "bold"),
        ).pack(anchor="w", pady=(4, 4))
        tk.Label(
            container,
            text="Encrypt or decrypt a message by rotating each letter through the alphabet.",
            bg=self.BG,
            fg=self.MUTED,
            font=("Arial", 11),
        ).pack(anchor="w", pady=(0, 24))

        panel = ttk.Frame(container, style="Panel.TFrame", padding=24)
        panel.pack(fill="both", expand=True)

        controls = ttk.Frame(panel, style="Panel.TFrame")
        controls.pack(fill="x", pady=(0, 14))

        tk.Label(
            controls,
            text="Shift value",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Arial", 11, "bold"),
        ).pack(side="left")

        shift_box = ttk.Spinbox(
            controls,
            from_=-9999,
            to=9999,
            textvariable=self.shift_var,
            width=8,
            justify="center",
            style="Shift.TSpinbox",
            font=("Arial", 11),
        )
        shift_box.pack(side="left", padx=(12, 0))

        tk.Label(
            controls,
            text="Letters wrap automatically every 26 positions.",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Arial", 10),
        ).pack(side="left", padx=(16, 0))

        tk.Label(
            panel,
            text="Message",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Arial", 11, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        self.message_text = tk.Text(
            panel,
            height=7,
            wrap="word",
            bg=self.INPUT_BG,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            selectbackground=self.ACCENT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.ACCENT,
            padx=14,
            pady=12,
            font=("Arial", 12),
        )
        self.message_text.pack(fill="both", expand=True)
        self.message_text.focus_set()

        actions = ttk.Frame(panel, style="Panel.TFrame")
        actions.pack(fill="x", pady=14)
        ttk.Button(
            actions,
            text="Encrypt",
            command=lambda: self._process("encrypt"),
            style="Accent.TButton",
        ).pack(side="left")
        ttk.Button(
            actions,
            text="Decrypt",
            command=lambda: self._process("decrypt"),
            style="Secondary.TButton",
        ).pack(side="left", padx=10)
        ttk.Button(
            actions,
            text="Clear",
            command=self._clear,
            style="Secondary.TButton",
        ).pack(side="left")

        tk.Label(
            panel,
            text="Result",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Arial", 11, "bold"),
        ).pack(anchor="w", pady=(2, 8))

        self.result_text = tk.Text(
            panel,
            height=7,
            wrap="word",
            state="disabled",
            bg=self.INPUT_BG,
            fg=self.TEXT,
            selectbackground=self.ACCENT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.BORDER,
            padx=14,
            pady=12,
            font=("Arial", 12),
        )
        self.result_text.pack(fill="both", expand=True)

        footer = ttk.Frame(panel, style="Panel.TFrame")
        footer.pack(fill="x", pady=(12, 0))
        tk.Label(
            footer,
            textvariable=self.status_var,
            bg=self.PANEL,
            fg=self.SUCCESS,
            font=("Arial", 10, "bold"),
        ).pack(side="left")
        ttk.Button(
            footer,
            text="Copy result",
            command=self._copy_result,
            style="Secondary.TButton",
        ).pack(side="right")

    def _get_shift(self) -> int | None:
        try:
            return int(self.shift_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid shift", "Enter a whole number for the shift value.")
            self.status_var.set("Invalid shift value")
            return None

    def _process(self, operation: str) -> None:
        shift = self._get_shift()
        if shift is None:
            return

        message = self.message_text.get("1.0", "end-1c")
        if not message:
            messagebox.showinfo("Message required", "Enter a message before continuing.")
            self.status_var.set("Waiting for a message")
            return

        result = encrypt(message, shift) if operation == "encrypt" else decrypt(message, shift)
        self._set_result(result)
        self.status_var.set(f"Message {operation}ed with shift {shift % 26}")

    def _set_result(self, text: str) -> None:
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", text)
        self.result_text.configure(state="disabled")

    def _copy_result(self) -> None:
        result = self.result_text.get("1.0", "end-1c")
        if not result:
            messagebox.showinfo("Nothing to copy", "Create an encrypted or decrypted result first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.status_var.set("Result copied to clipboard")

    def _clear(self) -> None:
        self.message_text.delete("1.0", "end")
        self._set_result("")
        self.status_var.set("Ready")
        self.message_text.focus_set()


def main() -> None:
    root = tk.Tk()
    SecretScrollApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
