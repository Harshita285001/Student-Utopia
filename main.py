# Importing required Modules
from tkinter import *
from tkinter.messagebox import showinfo
import speech_recognition as sr
import os
import requests,webbrowser
from bs4 import BeautifulSoup
from keras.models import load_model
from time import sleep
from keras_preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
from textutil import *

mainwindow= Tk()
mainwindow.title('Students-Utopia')
mainwindow.geometry('500x500')
mainwindow.resizable(0, 0)
mainwindow.configure(bg='lightblue')

# Speech-to-Text Module
def recordvoice():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio=r.listen(source)
            try:    
                text = r.recognize_google(audio,language="en-IN")
            except:
                pass
            return text

def SpeechToText():
    speechtotextwindow = Toplevel(mainwindow)
    speechtotextwindow.title('Speech-to-Text Converter')
    speechtotextwindow.geometry("500x500")
    speechtotextwindow.configure(bg='pink')

    st = Label(speechtotextwindow, text='Speech-to-Text', font=("Times", 20, "bold"), bg='IndianRed')
    st.place(x=160, y=30)

    text = Text(speechtotextwindow, font=12, height=3, width=30)
    text.place(x=110, y=150)
    
    recordbutton = Button(speechtotextwindow, text='Record', bg='Sienna', command=lambda: text.insert(END, recordvoice()))
    recordbutton.place(x=230, y=100)

title = Label(mainwindow, text="STUDENTS-UTOPIA", font=("Times", 30, "bold"))
title.place(x=62, y=50)

speechtotextbutton = Button(mainwindow, text='Speech-To-Text Conversion', font=('Times New Roman', 16), bg='brown', command=SpeechToText)
speechtotextbutton.place(x=125, y=150)

# Search Module
def searchgui():
    struct = Toplevel(mainwindow)
    struct.title('My Search Engine')
    struct.geometry("500x500")
    struct.configure(bg='teal')
    st = Label(struct, text='Search Engine', font=("Times", 20, "bold"), bg="teal", fg="white")
    st.place(x=170, y=30)
    label=Label(struct,text="Enter here to search",bg="teal",fg="white",font=("Times",15,"bold"))
    label.place(x=168,y=100)
    enter=Entry(struct,font=("Times",10,"bold"),textvar=text,width=30,bd=2,bg="white")
    enter.place(x=150,y=130)
    button=Button(struct,text="Search",font=("Times",10,"bold"),width=30,bd=2,command=search)
    button.place(x=149,y=170)

text=StringVar()
def search():
     data=requests.get('https://www.google.com/search?q='+text.get())
     soup=BeautifulSoup(data.content,"html.parser")
     result=soup.select(".kCrYT a")
     for link in result[:1]:
         searching=link.get("href")
         searching=searching[7:]
         searching=searching.split("&")
         webbrowser.open(searching[0])

searchbutton = Button(mainwindow, text='Search Anything', font=('Times New Roman', 16), bg='green', command=searchgui)
searchbutton.place(x=175, y=200)

# Face Emotion Detection

def emotiongui():
    face_classifier = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
    classifier =load_model(r'model.h5')

    emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

    cap = cv2.VideoCapture(0)



    while True:
        _, frame = cap.read()
        labels = []
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)

                prediction = classifier.predict(roi)[0]
                label=emotion_labels[prediction.argmax()]
                label_position = (x,y)
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            else:
                cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imshow('Emotion Detector',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

emobutton = Button(mainwindow, text='Face Emotion', font=('Times New Roman', 16), bg='blue', command=emotiongui)
emobutton.place(x=183, y=250)

# Text Summary Module

def summarygui():
    root = Toplevel(mainwindow)
    root.title("Text Summarizer")
    top_frame = Frame(root)
    Label(top_frame,text='Size of summary in % :').pack(side=LEFT)
    edit = Entry(top_frame)
    edit.pack(side=LEFT, fill=BOTH, expand=1)
    edit.focus_set()
    butt = Button(top_frame, text='Summarize')
    butt.pack(side=RIGHT)
    top_frame.pack(side=TOP)


    center_frame = Frame(root)
    Label(center_frame,text='Put some text here ...').pack(side=TOP)
    center_frame.pack(side=TOP)
    original = Text(center_frame)
    original.insert('1.0','''''')
    original.pack(side=TOP)

    summary = Text(center_frame)
    summary.insert('1.0','''''')
    summary.pack(side=BOTTOM)


    def summarize():
        if edit.get()=='' :
            percentage = 1
        else :
            percentage = int(edit.get())

        orig_text = original.get('1.0','end')
        result = rate_sentences(orig_text, percentage)


        summary.delete('1.0','end')
        summary.insert('1.0',str(result))

    butt.config(command=summarize)
    root.mainloop()

summarybutton = Button(mainwindow, text='Text Summary', font=('Times New Roman', 16), bg='yellow', command=summarygui)
summarybutton.place(x=181, y=300)

mainwindow.update()
mainwindow.mainloop()