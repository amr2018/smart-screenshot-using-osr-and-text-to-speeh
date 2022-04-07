
import pytesseract
from PIL import Image
from gtts import gTTS
import os
from playsound import playsound

from tkinter import *
from pyautogui import screenshot
from PIL import Image, ImageTk, ImageDraw
from time import sleep
from threading import Thread


root = Tk()
root.geometry('400x100')

lang = StringVar(root)
lang.set("ara")

Label(root, text = 'select text to speeh lang').place(x = 90, y = 20)

langs = OptionMenu(root, lang, 'eng', 'ara')
langs.config(bd = 0)
langs.place(x = 90, y = 45)


def raed_from_image(img):

	"""
	[1] download tesseract from https://github.com/UB-Mannheim/tesseract/wiki
	[2] download ara.traineddata from https://stackoverflow.com/questions/54763731/tesseract-returns-nothing-for-arabic-words-letters 
	and paste it in this path : C:\Program Files\Tesseract-OCR\tessdata [for arabic osr]
	"""
	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

	text = pytesseract.image_to_string(Image.open(img), lang=lang.get())

	myobj = gTTS(text, lang='ar')
	myobj.save('test.mp3')
	playsound('test.mp3')
	os.remove('test.mp3')




def new_win():
	root.wm_state('iconic')
	sleep(1)
	new_win = Toplevel(root)
	new_win.geometry('500x500')


	img = screenshot('x.jpg')
	img = ImageTk.PhotoImage(Image.open('x.jpg'))

	simg = Label(new_win, image = img)
	simg.image = img
	simg.place(x =0, y = 0)

	# 

	new_win.attributes('-fullscreen', True)

	def close(key):
		if key.keycode == 27:
			new_win.destroy()
			exit()

		if key.keycode == 82:
			Thread(target=raed_from_image, args=('test.jpg', )).start()

		print(key)


	new_win.bind('<Key>', close)

	positions = []
	def select_area(pos):
		
		print(pos.state)
		if pos.state == 264:
			positions.append((pos.x, pos.y))
			img = Image.open('x.jpg')
			draw = ImageDraw.Draw(img)
			shape = [positions[0], positions[-1]]
			draw.rectangle(shape, outline ="red")

			imgx = img.crop((positions[0][0] - 1, positions[0][1] - 1, positions[-1][0], positions[-1][1]))
			imgx.save('test.jpg')




			img.save('x-edit.jpg')

			img = ImageTk.PhotoImage(Image.open('x-edit.jpg'))

			simg = Label(new_win, image = img)
			simg.image = img
			simg.place(x =0, y = 0)


		else:
			positions.clear()

			


	new_win.bind('<Motion>', select_area)


screenshot_bt = ImageTk.PhotoImage(Image.open('take-a-photo.png').resize((50, 50)))

bt = Button(root, text = 'new', image = screenshot_bt, bd =0,  command=new_win)
bt.image = screenshot_bt
bt.place(x = 10, y = 20)


root.mainloop()
