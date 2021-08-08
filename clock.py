import tkinter
from datetime import datetime
import time
import pygame.mixer
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

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

is_audio = True

path = os.getcwd()

root = tkinter.Tk()
root.title("Clock")
root.geometry(str(default_window["width"]) + "x" + str(default_window["height"])) # ウインドウサイズ
root.minsize(width=500, height=174) # 最小ウインドウサイズ

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
  button_text["height"] = time_te["height"] - 20
  c.coords(id_time, time_text["width"], time_text["height"]) # テキストの変更
  c.coords(id_date, date_text["width"], date_text["height"]) # テキストの変更

root.bind('<Configure>', change_size) # 関数のバインド(連携)

# チックタックの音声において、空白のところをなくす
clock_sound = AudioSegment.from_file(path + "/time/clock_oto.mp3", "mp3")
clock_chunks = split_on_silence(clock_sound, min_silence_len=300, silence_thresh=-40, keep_silence=30)
for i, clock_chunk in enumerate(clock_chunks):
  clock_chunk.export("./time/clock_sound_without.mp3", format="mp3")

# 音声を生成
def start_sound(hour):
  outputSound = 0
  hour_solo = hour # 一の位の数を取得(ただし、10と20はそのまま)
  if hour > 10 and hour < 20: # もしも組み合わせ用の10を使う場合
    outputSound += AudioSegment.from_file(path + "/time/time_10_kumiawase.mp3", "mp3")
    hour_solo = hour - 10
  elif hour > 20: # もしも組み合わせ用の20を使う場合
    outputSound += AudioSegment.from_file(path + "/time/time_20_kumiawase.mp3", "mp3")
    hour_solo = hour - 20
  outputSound += AudioSegment.from_file(path + "/time/time_" + str(hour_solo) + ".mp3", "mp3") + AudioSegment.from_file(path + "/time/ji.mp3", "mp3")
  # 無音となっているところをカットする
  chunks = split_on_silence(outputSound, min_silence_len=300, silence_thresh=-40, keep_silence=30)
  outputWithoutSilence = 0 # 無音をカットした音声を格納
  for i, chunk in enumerate(chunks):
    outputWithoutSilence += chunk #　無音をカットした音声を代入
  # 人間味を帯びせるため、少々倍速
  outputWithoutSilence = outputWithoutSilence.speedup(playback_speed=1.2, crossfade=0)
  outputWithoutSilence.export(path + "/time/output.mp3", format="mp3") # 出力
  pygame.mixer.init() #初期化
  pygame.mixer.music.load(path + '/time/output.mp3') #読み込み
  pygame.mixer.music.play()

# チックタック鳴らすやつ
def start_clock_sound():
  pygame.mixer.init() #初期化
  pygame.mixer.music.load(path + '/time/clock_sound_without.mp3') #読み込み
  pygame.mixer.music.play()

def btn_click():
  global is_audio
  value = is_audio
  is_audio = not value

# 実は、ウインドウを閉じるときどうしてもエラーを出すので、tryで隠します

temp_second = -1

btn = tkinter.Button(
  root,
  text=' Audio',
  font = ('DJB Get Digital', 30),
  width=10,
  anchor="center",
  relief=tkinter.RAISED,
  cursor="hand2",
  command = btn_click
)
btn.place(x=0,y=0)
try:
  while True:
    now = datetime.now() # 現在時間の取得
    time_s = '{0:0>2d}:{1:0>2d}:{2:0>2d}'.format(now.hour, now.minute, now.second)
    date_s = '{0:0>4d}/{1:0>2d}/{2:0>2d}'.format(now.year, now.month, now.day)
    if temp_second == -1:
      temp_second = now.second
    id_time_color = '#bbbbbb'
    if now.hour < 6 or now.hour > 17 and False: # もしも夜ならば->ダークモード
      c.configure(bg='#000000')
    else:
      c.configure(bg='#ffffff')
      id_time_color = 'black'
    id_time = c.create_text(
      time_text["width"],
      time_text["height"],
      text = time_s,
      font = ('DJB Get Digital', 100),
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
    if now.second == 0 and now.minute == 0 and is_audio:
      start_sound(now.hour)
    if now.second != temp_second and is_audio:
      start_clock_sound()
      temp_second = now.second
  root.mainloop()
except:
  pass