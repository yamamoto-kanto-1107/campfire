from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import app
import os,sys


# ウィンドウを作成
root = Tk()

# ウィンドウサイズを指定
root.geometry("420x340")

# ウィンドウタイトルを指定
root.title('入力フォーム')

frame1 = ttk.Frame(root, padding=(32))
frame1.grid()

# メールアドレス
label1 = ttk.Label(frame1, text='メールアドレス', padding=(5, 2))
label1.grid(row=0, column=0, sticky=E)

# パスワード
label2 = ttk.Label(frame1, text='パスワード', padding=(5, 2))
label2.grid(row=1, column=0, sticky=E)

# CSV出力先
label3 = ttk.Label(frame1, text='CSV出力先', padding=(5, 2))
label3.grid(row=2, column=0, sticky=E)



# 取得企業数
label3 = ttk.Label(frame1, text='取得企業数', padding=(5, 2))
label3.grid(row=3, column=0, sticky=E)

# メールアドレス
mailRow = StringVar()
mailRow_txt = ttk.Entry(
    frame1,
    textvariable=mailRow,
    width=20)
mailRow_txt.grid(row=0, column=1)

# パスワード
passwordRow = StringVar()
passwordRow_txt = ttk.Entry(
    frame1,
    textvariable=passwordRow,
    width=20)
passwordRow_txt.grid(row=1, column=1)

# csv出力先
OutputCSV = StringVar()
OutputCSV_txt = ttk.Entry(
    frame1,
    textvariable=OutputCSV,
    width=20)
OutputCSV_txt.grid(row=2, column=1)

# 取得企業数
getCompanyCount = StringVar()
getCompanyCount_txt = ttk.Entry(
    frame1,
    textvariable=getCompanyCount,
    width=20)
getCompanyCount_txt.grid(row=3, column=1)

def dirdialog_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    OutputCSV.set(iDirPath)

def btn_click():
    # 値の取得
    mail_value = str(mailRow.get())
    pass_value = str(passwordRow.get())
    csv_value = str(OutputCSV.get())
    company_value = int(getCompanyCount.get())

    app.getDataToCampfire(mail_value,pass_value,csv_value,company_value)


IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)
IDirButton.grid(row=2, column=2)


# Button
button1 = ttk.Button(
    frame1, text='開始',
    command=btn_click
)
button1.grid(row=4, column=1)



# ウィンドウ表示継続
root.mainloop()
