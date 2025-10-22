import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import webbrowser
import os

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Child QR Code Generator")
        self.root.geometry("520x550")
        self.root.minsize(480, 500)
        self.root.iconbitmap("qr.ico")

        tk.Label(root, text="Enter Child Details", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        self.entries = {}
        fields = [
            ("Name", "name"),
            ("School", "school"),
            ("Class / Grade", "grade"),
            ("Roll No.", "roll"),
            ("Parent Contact", "contact"),
            ("Address", "address")
        ]

        for i, (label, key) in enumerate(fields):
            tk.Label(form_frame, text=f"{label}:").grid(row=i, column=0, padx=10, pady=6, sticky="e")
            entry = tk.Entry(form_frame, width=35)
            entry.grid(row=i, column=1, padx=5, pady=6, sticky="w")
            self.entries[key] = entry

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Generate QR", command=self.generate_qr, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Download QR", command=self.download_qr, bg="#2196F3", fg="white", width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Email (Gmail)", command=self.email_qr, bg="#FF9800", fg="white", width=15).grid(row=0, column=2, padx=5)

        self.qr_label = tk.Label(root)
        self.qr_label.pack(pady=15, expand=True)

        self.qr_image = None
        self.last_saved_path = None

    def generate_qr(self):
        data = "\n".join([f"{label.title().replace('_', ' ')}: {entry.get()}" for label, entry in self.entries.items()])
        if not self.entries["name"].get():
            messagebox.showerror("Error", "Please enter at least the child's name.")
            return

        qr = qrcode.make(data)
        self.qr_image = qr

        img = qr.resize((240, 240))
        img_tk = ImageTk.PhotoImage(img)
        self.qr_label.config(image=img_tk)
        self.qr_label.image = img_tk

        messagebox.showinfo("Success", "QR Code Generated Successfully!")

    def download_qr(self):
        if self.qr_image is None:
            messagebox.showerror("Error", "Please generate a QR code first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png")])
        if file_path:
            self.qr_image.save(file_path)
            self.last_saved_path = file_path
            messagebox.showinfo("Saved", f"QR Code saved as {file_path}")

    def email_qr(self):
        if self.qr_image is None:
            messagebox.showerror("Error", "Please generate a QR code first.")
            return


        if not self.last_saved_path:
            temp_path = os.path.join(os.getcwd(), "temp_child_qr.png")
            self.qr_image.save(temp_path)
            self.last_saved_path = temp_path

        recipient = self.entries["contact"].get() or ""
        subject = "Child QR Code"
        body = f"The QR code image is saved here:\n{self.last_saved_path}\n\n\nPlease attach it manually before sending."

        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient}&su={subject}&body={body}"
        webbrowser.open(gmail_url)

root = tk.Tk()
app = QRApp(root)
root.mainloop()
