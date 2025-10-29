import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os

SENDER_EMAIL = "sharma69vijay@gmail.com"
SENDER_APP_PASSWORD = "bnhv nvhx rfcl dlse"

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x580")
        self.root.minsize(480, 500)
        self.root.iconbitmap("qr.ico")

        tk.Label(root, text="Enter Child Details", font=("Arial", 16)).pack(pady=10)

        self.name = tk.Entry(root, width=40)
        tk.Label(root, text="Name:").pack()
        self.name.pack(pady=5)

        self.school = tk.Entry(root, width=40)
        tk.Label(root, text="School:").pack()
        self.school.pack(pady=5)

        self.grade = tk.Entry(root, width=40)
        tk.Label(root, text="Class / Grade:").pack()
        self.grade.pack(pady=5)

        self.roll = tk.Entry(root, width=40)
        tk.Label(root, text="Roll No.:").pack()
        self.roll.pack(pady=5)

        self.contact = tk.Entry(root, width=40)
        tk.Label(root, text="Parent Contact:").pack()
        self.contact.pack(pady=5)

        self.address = tk.Entry(root, width=40)
        tk.Label(root, text="Address:").pack()
        self.address.pack(pady=5)

        tk.Label(root, text="Recipient Gmail:").pack()
        self.recipient_email = tk.Entry(root, width=40)
        self.recipient_email.pack(pady=5)

        tk.Button(root, text="Generate QR", command=self.generate_qr, bg="green", fg="white").pack(pady=5)
        tk.Button(root, text="Download QR", command=self.download_qr, bg="blue", fg="white").pack(pady=5)
        tk.Button(root, text="Send Email", command=self.email_qr, bg="orange", fg="white").pack(pady=5)

        self.qr_image = None
        self.last_saved_path = None

    def generate_qr(self):
        data = (
            f"Name: {self.name.get()}\n"
            f"School: {self.school.get()}\n"
            f"Class: {self.grade.get()}\n"
            f"Roll No.: {self.roll.get()}\n"
            f"Parent Contact: {self.contact.get()}\n"
            f"Address: {self.address.get()}"
        )

        if self.name.get() == "":
            messagebox.showerror("Error", "Please enter at least the name.")
            return

        self.qr_image = qrcode.make(data)
        messagebox.showinfo("Success", "QR Code Generated!")

    def download_qr(self):
        if self.qr_image is None:
            messagebox.showerror("Error", "Generate QR first.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if path:
            self.qr_image.save(path)
            self.last_saved_path = path
            messagebox.showinfo("Saved", "QR Code saved!")

    def email_qr(self):
        if self.qr_image is None:
            messagebox.showerror("Error", "Generate QR first.")
            return

        recipient = self.recipient_email.get().strip()
        if not recipient:
            messagebox.showerror("Error", "Please enter a recipient Gmail.")
            return

        if not self.last_saved_path:
            temp_path = os.path.join(os.getcwd(), "temp_qr.png")
            self.qr_image.save(temp_path)
            self.last_saved_path = temp_path

        msg = MIMEMultipart()
        msg["Subject"] = "Child QR Code"
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient

        with open(self.last_saved_path, "rb") as f:
            img_data = f.read()
        msg.attach(MIMEImage(img_data, name=os.path.basename(self.last_saved_path)))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
                server.send_message(msg)
            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email.\n\n{e}")

root = tk.Tk()
app = QRApp(root)
root.mainloop()
