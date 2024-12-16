from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import app
import os


# ウィンドウを作成
root = Tk()
root.geometry("620x340")
root.title('入力フォーム')

# カラム幅を調整
root.grid_columnconfigure(1, minsize=10)
root.grid_columnconfigure(2, minsize=10)
root.grid_columnconfigure(3, minsize=10)

frame1 = ttk.Frame(root, padding=(32))
frame1.grid()

# CSV出力先
label3 = ttk.Label(frame1, text='CSV出力先', width=10)
label3.grid(row=0, column=0, sticky=E, padx=5, pady=5)

# CSV出力先エントリ
OutputCSV = StringVar()
OutputCSV_txt = ttk.Entry(frame1, textvariable=OutputCSV, width=10)
OutputCSV_txt.grid(row=0, column=1, padx=5, pady=5)

# CSV参照ボタン
def dirdialog_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir=iDir)
    OutputCSV.set(iDirPath)

IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)
IDirButton.grid(row=0, column=3, padx=5, pady=5)

# 取得企業数
radioSelect = StringVar()
radioBtn = ttk.Radiobutton(frame1, text='ページ指定', variable=radioSelect, value='A', width=10)
radioBtn2 = ttk.Radiobutton(frame1, text='全て', variable=radioSelect, value='B', width=10)
radioBtn.grid(row=1, column=0, padx=5, pady=5)
radioBtn2.grid(row=2, column=0, padx=5, pady=5)

# ページ開始エントリ
getCompanyCountStart = StringVar()
getCompanyCountStart_txt = ttk.Entry(frame1, textvariable=getCompanyCountStart, width=10)
getCompanyCountStart_txt.grid(row=1, column=1, padx=5, pady=5)

# セパレーター
separator = ttk.Label(frame1, text='~', anchor=CENTER, width=5)
separator.grid(row=1, column=2, sticky=W+E, padx=5, pady=5)

# ページ終了エントリ
getCompanyCountEnd = StringVar()
getCompanyCountEnd_txt = ttk.Entry(frame1, textvariable=getCompanyCountEnd, width=10)
getCompanyCountEnd_txt.grid(row=1, column=3, padx=5, pady=5)

# 開始ボタン
def btn_click():
    csv_value = str(OutputCSV.get())
    select_value = str(radioSelect.get())

    if select_value == 'A':
        company_start = int(getCompanyCountStart.get())
        company_end = int(getCompanyCountEnd.get())

        # 呼びだし
        app.getDataToCampfire(csv_pass=csv_value,company_start=company_start, company_end=company_end)
    else:
        company_all = True
        app.getDataToCampfire(csv_pass=csv_value, company_all=company_all)



button1 = ttk.Button(frame1, text='開始', command=btn_click)
button1.grid(row=3, column=1, padx=5, pady=10)

# ウィンドウ表示継続
root.mainloop()
