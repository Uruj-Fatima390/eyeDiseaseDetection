from tkinter import *
import ctypes,os
from PIL import ImageTk, Image
import tkinter.messagebox as tkMessageBox
from tkinter.filedialog import askopenfilename
import tensorflow as tf
import tensorflow.keras.models as models
from tensorflow.keras.models import load_model
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import  numpy as np
import geocoder
import tkinter.scrolledtext as st

def textwin(textmain):

    win = Tk()
    win.title("Eye Disease Detection")
    win.config(background = '#343434')

    Label(win,text = "Output For Given Image",font = ("Times New Roman", 15),background = '#343434',foreground = "white").grid(column = 0,row = 0)

    text_area = st.ScrolledText(win,width = 30,height = 8,font = ("Times New Roman",15),background = '#343434',foreground = "white")

    text_area.grid(column = 0, pady = 10, padx = 10)

    text_area.insert(INSERT,textmain)

    text_area.configure(state ='disabled')
    win.mainloop()


home = Tk()
home.title("Eye disease detection")

img = Image.open("images/home.png")
img = ImageTk.PhotoImage(img)
panel = Label(home, image=img)
panel.pack(side="top", fill="both", expand="yes")
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
lt = [w, h]
a = str(lt[0]//2-620)
b= str(lt[1]//2-450)
home.geometry("1240x900+"+a+"+"+b)
home.resizable(0,0)
file = ''



def Exit():
    global home
    result = tkMessageBox.askquestion(
        "Eye disease detection", 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        home.destroy()
        exit()
    else:
        tkMessageBox.showinfo(
            'Return', 'You will now return to the main screen')
        
def browse():
    
    global file,l1
    try:
        l1.destroy()
    except:
        pass
    file = askopenfilename(initialdir=os.getcwd(), title="Select Image", filetypes=( ("images", ".png"),("images", ".jpg"),("images", ".jpeg")))


def predict():
    global file,l1
    if file!='' or file!= None:
        model = load_model('./model/resnet glaucoma.h5')
        image = cv2.imread(file)
        img = image
        image = cv2.resize(image,(224,224))
        image = image.reshape(-1,224,224,3)
        pred = model.predict(image)
        print(pred)
        v = pred[0].argmax()
        pred1 = pred[0][0]*100

        model = load_model('./model/resnet cataract.h5')
        pred = model.predict(image)
        print(pred)
        v = pred[0].argmax()
        pred2 = pred[0][0]*100

        if pred2>0.999999:
            pred2-=1
        if pred1>0.999999:
            pred2-=1            
        pred = max([pred1,pred2])
  
        if pred==pred2:
            predt = "Cataract"
        elif pred==pred1:
            predt = "Glucoma"

        #finding doctor based on location
        ip = geocoder.ip("me")
        city = ip.city
        df = pd.read_csv('./data/doctor.csv')
        df = df[df['City']==city]
        df = df[df['Experties']==predt]
        doc = df.to_dict('list')

        #suggesting medicines
        df = pd.read_csv('./data/medicine.csv')
        df = df[df['Use']==predt]
        med = df.to_dict('list')

        #text
        acc = '('+str(round(pred,2))+'%)'
        outtext = "Predicted Output Is: "+predt+acc
        if doc['Name']!=[]:
            outtext+='\n\n\nDoctor Details :\n\n'
            for i in range(len(doc['Name'])):
                outtext+='Name: '+doc['Name'][i]+'\n'
                outtext+='Contact: '+str(doc['Contact'][i])+'\n'

        if med['Name']!=[]:
            outtext+='\n\nMedicinal Details :\n\n'
            for i in range(len(med['Name'])):
                outtext+='Name: '+med['Name'][i]+'\n'
                outtext+='Type: '+med['Type'][i]+'\n'
                outtext+='Description: '+med['Description'][i]+'\n'
                
        
    
        #plotting
        plt.imshow(img,cmap="gray")
        pValue = "Predicted Output Is: {0}".format(predt+acc)
        plt.title(pValue)
        plt.show()
        textwin(outtext)
        
def about():
    about = Toplevel()
    about.title("Eye disease detection")

    img = Image.open("images/about.png")
    img = ImageTk.PhotoImage(img)
    panel = Label(about, image=img)
    panel.pack(side="top", fill="both", expand="yes")
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    lt = [w, h]
    a = str(lt[0]//2-620)
    b= str(lt[1]//2-450)
    about.geometry("1240x900+"+a+"+"+b)
    about.resizable(0,0)
    about.mainloop()
    
photo = Image.open("images/1.png")
img2 = ImageTk.PhotoImage(photo)
b1=Button(home, highlightthickness = 0, bd = 0,activebackground="#343434", image = img2,command=browse)
b1.place(x=0,y=299)

photo = Image.open("images/2.png")
img3 = ImageTk.PhotoImage(photo)
b2=Button(home, highlightthickness = 0, bd = 0,activebackground="#343434", image = img3,command=predict)
b2.place(x=0,y=383)

photo = Image.open("images/3.png")
img4 = ImageTk.PhotoImage(photo)
b3=Button(home, highlightthickness = 0, bd = 0,activebackground="#343434", image = img4,command=about)
b3.place(x=0,y=468)

photo = Image.open("images/4.png")
img5 = ImageTk.PhotoImage(photo)
b4=Button(home, highlightthickness = 0, bd = 0,activebackground="#343434", image = img5,command=Exit)
b4.place(x=0,y=553)

home.mainloop()
