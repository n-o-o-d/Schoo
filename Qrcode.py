import qrcode
import tkinter as tk
from tkinter import filedialog

class QRCODEGEN:
    def __init__(self, master):
        self.master = master
        master.title("QRCODE GEN")

        self.label = tk.Label(master, text="ENTER URL: ")
        self.label.pack()
        self.entry = tk.Entry(master, width = 50)
        self.entry.pack()

        self.generate = tk.Button(master, text = "Create QR Code", command = self.generate_qr_code)
        self.generate.pack()
        self.saveButton = tk.Button(master, text = "Save file", command = self.save_qr_code, state = tk.DISABLED)
        self.saveButton.pack()

        self.qr_code = None

    def generate_qr_code(self):
        data = self.entry.get()
        if data:
            self.qr_code = qrcode.make(data)
            self.saveButton.config(state=tk.NORMAL)
        else:
            self.qr_code = None
            self.saveButton.config(state=tk.DISABLED)

    def save_qr_code(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.qr_code.save(file_path)
            
root = tk.Tk()
qrcode_generator = QRCODEGEN(root)
root.mainloop()
