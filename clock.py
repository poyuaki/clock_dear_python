import tkinter
from datetime import datetime
import time
import os
import sys

default_window = {
  "width": 800,
  "height": 200
}
id_time = "" # 時間のテキストのid
id_date = "" # 日付のテキストのid

time_text = { # 時間テキストの位置
  "width": 0,
  "height": 0
}

date_text = { # 日付テキストの位置
  "width": 0,
  "height": 0
}

button_text = {
  "width": 0,
  "height": 0
}
is_tikutaku = True

def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
    return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath("."), relative_path)

root = tkinter.Tk()
root.title("Clock")
root.geometry(str(default_window["width"]) + "x" + str(default_window["height"])) # ウインドウサイズ
root.minsize(width=370, height=150) # 最小ウインドウサイズ

c = tkinter.Canvas( # テキストを描くキャンバスを生成
  root,
  width = default_window["width"],
  height = default_window["height"],
  background = '#000000'
)
c.pack(anchor='center',expand=1, fill = tkinter.BOTH) # ウインドウサイズをリサイズ

# サイズを変更した時の処理(生成時も)
def change_size(event):
  w = c.winfo_width() # ウインドウの幅
  h = c.winfo_height() # ウインドウの高さ
  time_text["width"] = w / 2
  time_text["height"] = h / 2 + 20
  date_text["width"] = time_text["width"]
  date_text["height"] = time_text["height"] - 70
  button_text["width"] = time_text["width"] / 2
  button_text["height"] = time_text["height"] - 20
  c.coords(id_time, time_text["width"], time_text["height"]) # テキストの変更
  c.coords(id_date, date_text["width"], date_text["height"]) # テキストの変更

root.bind('<Configure>', change_size) # 関数のバインド(連携)

# 実は、ウインドウを閉じるときどうしてもエラーを出すので、tryで隠します

try:
  while True:
    now = datetime.now() # 現在時間の取得
    time_s = '{0:0>2d}:{1:0>2d}:{2:0>2d}'.format(now.hour, now.minute, now.second)
    date_s = '{0:0>4d}/{1:0>2d}/{2:0>2d}'.format(now.year, now.month, now.day)
    id_time_color = '#bbbbbb'
    if now.hour < 6 or now.hour > 17: # もしも夜ならば->ダークモード
      c.configure(bg='#000000')
    else:
      c.configure(bg='#ffffff')
      id_time_color = 'black'
    id_time = c.create_text(
      time_text["width"],
      time_text["height"],
      text = time_s,
      font = ('DJB Get Digital', 80),
      fill = id_time_color,
      tag="time_text"
    )
    id_date = c.create_text(
      date_text["width"],
      date_text["height"],
      text = date_s,
      font = ('DJB Get Digital', 40),
      fill = 'red',
      tag="date_text"
    )
    c.update()
    time.sleep(0.1)
    c.delete("time_text")
    c.delete("date_text")
  root.mainloop()
except:
  pass