import tkinter as tk
from PIL import Image, ImageTk

"""
#ボタンがクリックされたら実行
def button_click():
    input_value = input_box.get()
    messagebox.showinfo("クリックイベント",input_value + "が入力されました。")
"""

ICON = "./picture/icon.ico"
BACKGROUND = "./picture/bg.png"
BACKGROUND_BLACK = "./picture/bg_black.png"
BUTTON_HOME = "./picture/home_button.png"
FORM_BG = "./picture/form_bg.png"

imgs = []


def change_page(page):
    page.tkraise()


class Frame(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('PriLog')
        self.master.geometry("960x540")
        self.master.resizable(width=False, height=False)
        self.master.iconbitmap(default=ICON)

        # 背景を設定(layer:0)
        bg_image = Image.open(BACKGROUND)
        img = ImageTk.PhotoImage(bg_image)
        imgs.append(img)
        self.bg = tk.Label(self, image=img)
        self.bg.pack(fill="x")

        # ヘッダーを設定 (layer:1)
        self.header = tk.Label(self)
        self.header["bg"] = "#272727"
        self.header["font"] = ("", 18)
        self.header["width"] = 960
        self.header["height"] = 0
        self.header.place(x=0, y=0)

        # Homeボタンを設定 (layer:2)
        home_image = Image.open(BUTTON_HOME)
        img = ImageTk.PhotoImage(home_image)
        imgs.append(img)
        self.header_bt_home = tk.Label(self, image=img, width=95, height=26, bg="#272727")
        self.header_bt_home.bind("<Leave>", self.bt_home_nm)
        self.header_bt_home.bind("<Enter>", self.bt_home_select)
        self.header_bt_home.place(x=0, y=0)

        # 入力フォームを設定 (layer:3)
        home_image = Image.open(FORM_BG)
        img = ImageTk.PhotoImage(home_image)
        imgs.append(img)
        self.form_bg = tk.Label(self, image=img, width=95, height=26)
        self.form_bg.place(x=150, y=250)

    # Homeボタン用イベント (layer:2)
    def bt_home_nm(self, event):
        self.header_bt_home.configure(bg="#272727", cursor="arrow")

    def bt_home_select(self, event):
        self.header_bt_home.configure(bg="#585858", cursor="hand2")


if __name__ == "__main__":
    f = Frame()
    f.pack()
    f.mainloop()
