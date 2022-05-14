# from AI import BrowserControl
from tkinter import *
from AI.Response import errorresponse
from tkinter import filedialog
from threading import Thread
from AI.SpeakAndListen import *

from AI.Authentication import check, Authentication
from AI import CsvFiles, BrowserControl
import PySimpleGUI as sg
Entries = []




def browsefunc(ent1):
    try:
        Entries.remove(ent1.get().lower())
    except ValueError:
        pass
    finally:
        ent1.delete(0,'end')
        filename = filedialog.askdirectory()
        ent1.insert(END, filename)
        Entries.append(ent1.get().lower())



def Entry_Box(heading, rows=0, restric=0):
	root = Tk()
	root.title(heading)
	root.geometry("590x200")
	Label(root, text="Root Foler"+str(restric+1)).grid(row=rows, column=1, padx="20")
	address = Entry(root)
	address.grid(row = rows, column = 4, ipadx="100",pady="15", ipady="2.5")
	browser = Button(root, font=25, text = "Browse",command = lambda:browsefunc(address))
	browser.grid(row = rows, column = 6, padx="5")
	Button(root,font=25, text= "OK", command=root.destroy).place(relx=0.95,rely=0.95, anchor="se")
	if restric < 2:
		apeendaddress = Button(root, text = "+",command = lambda:Entry_Box(heading,rows+2, restric+1))
		apeendaddress.grid(row = rows, column = 8, padx="5", ipady="2.5")
	return Entries

def get(gender = None, rate = None, get=True, name="" ):
	if connectionStatus():

		layout = [
					[sg.Text('Name', size =(15, 1), visible=get), sg.InputText(name,key='name', visible=get)],
					[sg.Text('E-mail', size =(15, 1)), sg.InputText(key='email')],
					[sg.Text('Password', size=(15, 1)), sg.InputText('', key='password', password_char='-')],
					[sg.Submit()]
				]
		window = sg.Window('Simple data entry window', layout, keep_on_top=True ,no_titlebar=True)
		while True:
			event, values = window.read()
			if not "@" in values['email']:
				values['email'] += "@gmail.com"
			if not "@gmail.com" in values['email']:
				speak("need only gmail mail", gender, rate)
				continue

			val = check(values['email'])

			if val and values['password']:
				if Authentication(values['email'], values['password'], gender, rate):
					break
				else:
					speak(errorresponse["SAError", gender, rate])
			elif not val:
				speak(errorresponse["EmailNV"], gender, rate)
			else:
				speak(errorresponse["IR"], gender, rate)
		window.close()

		return values
	else:
		speak("you don't have a internet connection", gender, rate)
		return False


def two_input(op, name=""):
	layout = [
					[sg.Text('Name', size =(15, 1)), sg.InputText(name,key='name')],
					[sg.Text('Address', size=(15, 1)), sg.InputText(key='address')],
					[sg.Submit()]
				]
	window = sg.Window("",layout, keep_on_top=True ,no_titlebar=True)
	while True:
		event, values = window.read()
		if values['name'] and values['address']:
			if op == "email":
				val = check(values['address'])
				if val:
					break
			else:
				if "+" in values['address']:
					break
			break
		else:
			speak("something is missing")

	window.close()
	return values

# print(two_input("email", name="muhammad khna"))


def multiplechoice(results):
	r = {}
	def cb(event):
		r['name'] = lb.get(lb.curselection()[0])
		root.destroy()
	root = Tk()
	var = StringVar(value=results)
	lb = Listbox(root, listvariable=var, width=30, height=10, borderwidth=4, selectmode='browse', takefocus=True,
				 activestyle='underline', font=('Time New Roman', 14), justify=CENTER)
	lb.grid(padx=20,pady=20)
	lb.bind('<<ListboxSelect>>', cb)
	root.mainloop()
	try:
		return r['name']
	except KeyError:
		return False


