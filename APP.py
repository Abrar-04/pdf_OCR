import os
from pytesseract import Output
import pytesseract
import cv2
import os
from pathlib import Path
#from PIL import Image
import PIL.Image
from pdf2image import convert_from_path
import pytesseract
from pytesseract import Output
import pytesseract
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = 'C:/Users/DELL/Documents/Tesseract-OCR/Tesseract.exe'
popplerPath=r'C:\Users\DELL\Documents\poppler\poppler-0.68.0\bin'
image_counter=0
pages_dir=Path('pages')

root=Tk()
root.title("OCR on PDF ")
root.geometry("500x250") 
root.resizable(0,0)
root.configure(bg='black')

def open_pdf():
	#global my_pdf
	global root

	root.filename=filedialog.askopenfilename(initialdir='D:/',title = "Select a PDF", filetypes = (("all files", "*.*"),("Text files", "*.txt*")))
	my_label=Label(root,text=root.filename).pack()
	images=convert_from_path(root.filename,500,poppler_path=popplerPath)
	for i,image in enumerate(images):
		fname='page_'+str(i)+'.png'
		image.save(pages_dir/f'{fname}',"PNG")
	f=open('Out/output.txt',"a")
	input_dir = r'pages/'
	fx = []
	tx = []  
	for root, dirs, filenames in os.walk(input_dir):
		for filename in filenames:
			try:
				print(filename)
				fx.append(filename)
				img = PIL.Image.open(input_dir+ filename)
				text = pytesseract.image_to_string(img, lang = 'eng')
				tx.append(text)
				print(text)
				print('-='*20)
			except:
				continue
			f.write(text)
			f.write('-='*20)
			f.write('\n')

		f.close()
		
	save_dir=Path('Out')

	def localise_all_images(folder):
		images = []
		for filename in os.listdir(folder):
			imgs = cv2.imread(os.path.join(folder,filename))
			if imgs is not None:
				images.append(imgs)
				img=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
				gray=cv2.cvtColor(imgs,cv2.COLOR_BGR2GRAY)
				gray,img_bin=cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
				gray = cv2.bitwise_not(img_bin)
				kernel = np.ones((2, 1), np.uint8)
				img = cv2.erode(gray, kernel, iterations=1)
				img = cv2.dilate(img, kernel, iterations=1)
				results=pytesseract.image_to_data(img,output_type=Output.DICT)
				print(results)
				for i in range(0, len(results["text"])):
					x = results["left"][i]
					y = results["top"][i]
					w = results["width"][i]
					h = results["height"][i]
					text = results["text"][i]
					conf = int(float(results["conf"][i]))

					if conf > 00.00 :
						print("Confidence: {}".format(conf))
						print("Text: {}".format(text))
						print("")
						text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
						cv2.rectangle(imgs, (x, y), (x + w, y + h), (0, 255, 0), 5)
						cv2.putText(imgs, text, (x,y), cv2.FONT_HERSHEY_SIMPLEX,4, (0, 0, 255),9)
				cv2.imwrite(os.path.join(save_dir,f'{filename}'),imgs)
	
		return images

	
	localise_all_images(pages_dir)

	messagebox.showinfo(title='OCR',message='Check Output folder')
			

my_btn=Button(root,text='Browse:',command=open_pdf,height=5,width=15,font=('Comic Sans MS',25,'bold'),bg='DarkOrchid3',fg='Yellow').pack()
root.mainloop()		




















