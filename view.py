import tkinter as tk
import tkinter.filedialog
import sys
import os
from PIL import Image, ImageTk

"""
#ボタンがクリックされたら実行
def button_click():
    input_value = input_box.get()
    messagebox.showinfo("クリックイベント",input_value + "が入力されました。")
"""

ICON = "./picture/icon.ico"
BACKGROUND = "./picture/bg.png"
BACKGROUND_TOP = "./picture/bg_top.png"
BACKGROUND_DRAG = "./picture/bg_top_drag.png"
BUTTON_HOME = "./picture/home_button.png"
BUTTON_SELECT = "./picture/select_button.png"

imgs = []

file_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

def change_page(page):
    page.tkraise()


class Frame(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('PriLog')
        self.geometry("960x540")
        self.resizable(width=False, height=False)
        self.iconbitmap(default=ICON)

        # ---------------------MAIN画面の設定---------------------
        self.main_frame = tk.Frame()
        self.main_frame.grid(row=0, column=0, sticky=tk.W)
        # 背景を設定(layer:0)
        bg_image = Image.open(BACKGROUND_TOP)
        img = ImageTk.PhotoImage(bg_image)
        imgs.append(img)
        self.bg = tk.Label(self.main_frame, image=img, bd=0)
        self.bg.pack(fill="x")

        # ヘッダーを設定 (layer:1)
        self.header = tk.Label(self.main_frame)
        self.header["bg"] = "#272727"
        self.header["font"] = ("", 18)
        self.header["width"] = 960
        self.header["height"] = 0
        self.header.place(x=0, y=0)

        # Homeボタンを設定 (layer:2)
        home_image = Image.open(BUTTON_HOME)
        img = ImageTk.PhotoImage(home_image)
        imgs.append(img)
        self.header_bt_home_1 = tk.Label(self.main_frame, image=img, width=95, height=26, bg="#272727")
        self.header_bt_home_1.bind("<Leave>", self.bt_home_nm)
        self.header_bt_home_1.bind("<Enter>", self.bt_home_select)
        self.header_bt_home_1.bind("<ButtonRelease-1>", self.bt_change_to_select)
        self.header_bt_home_1.place(x=0, y=0)

        # 入力フォームを設定 (layer:3)
        self.text_box = tk.Entry(self.main_frame, width=38, fg="#a0a0a0", bg="#FFFFFF", bd=6, font=("Arial", 12), relief="flat")
        self.text_box.place(x=267, y=278)

        # SELECTボタンを設定 (layer:4)
        select_image = Image.open(BUTTON_SELECT)
        img = ImageTk.PhotoImage(select_image)
        imgs.append(img)
        self.bt_select = tk.Label(self.main_frame, image=img, width=70, height=32, bd=0)
        self.bt_select.bind("<Leave>", self.bt_select_nm)
        self.bt_select.bind("<Enter>", self.bt_select_nm_select)
        self.bt_select.bind("<ButtonRelease-1>", self.bt_select_push)
        self.bt_select.place(x=623, y=278)

        # ---------------------選択画面の設定---------------------
        self.select = tk.Frame()
        self.select.grid(row=0, column=0, sticky=tk.W)
        # 背景を設定(layer:0)
        bg_image = Image.open(BACKGROUND_DRAG)
        img = ImageTk.PhotoImage(bg_image)
        imgs.append(img)
        self.bg = tk.Label(self.select, image=img, bd=0)
        self.bg.pack(fill="x")

        # ヘッダーを設定 (layer:1)
        self.header = tk.Label(self.select)
        self.header["bg"] = "#272727"
        self.header["font"] = ("", 18)
        self.header["width"] = 960
        self.header["height"] = 0
        self.header.place(x=0, y=0)

        # Homeボタンを設定 (layer:2)
        home_image = Image.open(BUTTON_HOME)
        img = ImageTk.PhotoImage(home_image)
        imgs.append(img)
        self.header_bt_home_2 = tk.Label(self.select, image=img, width=95, height=26, bg="#272727")
        self.header_bt_home_2.bind("<Leave>", self.bt_home_nm)
        self.header_bt_home_2.bind("<Enter>", self.bt_home_select)
        self.header_bt_home_2.bind("<ButtonRelease-1>", self.bt_change_to_home)
        self.header_bt_home_2.place(x=0, y=0)

        """
        # 入力フォームを設定 (layer:3)
        home_image = Image.open(FORM_BG)
        img = ImageTk.PhotoImage(home_image)
        imgs.append(img)
        self.form_bg = tk.Label(self.select, image=img, width=95, height=26)
        self.form_bg.place(x=150, y=250)
        """

        self.main_frame.tkraise()

    # Homeボタン用イベント (layer:2)
    def bt_home_nm(self, event):
        self.header_bt_home_1.configure(bg="#272727", cursor="arrow")
        self.header_bt_home_2.configure(bg="#272727", cursor="arrow")

    def bt_home_select(self, event):
        self.header_bt_home_1.configure(bg="#585858", cursor="hand2")
        self.header_bt_home_2.configure(bg="#585858", cursor="hand2")

    def bt_change_to_select(self, event):
        self.select.tkraise()

    def bt_change_to_home(self, event):
        self.main_frame.tkraise()
        self.text_box.delete(0, tk.END)

    # SELECTボタン用イベント (layer:4)
    def bt_select_nm(self, event):
        self.bt_select.configure(cursor="arrow")

    def bt_select_nm_select(self, event):
        self.bt_select.configure(cursor="hand2")

    def bt_select_push(self, event):
        global file_dir

        file_type = [("", ".mp4")]
        initial_dir = file_dir
        file = tkinter.filedialog.askopenfilename(filetypes=file_type, initialdir=initial_dir)

        if file != "":
            file_dir = os.path.dirname(file)
            self.text_box.delete(0, tk.END)
            self.text_box.insert(tk.END, file)


if __name__ == "__main__":
    f = Frame()
    f.mainloop()
