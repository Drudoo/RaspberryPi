### NOTES
#
# http://icalendar.readthedocs.io/en/latest/install.html
# https://github.com/picklepete/pyicloud
#
#
#
#

import sys
import imaplib
import getpass
import email
import email.header
from datetime import datetime, timedelta, date
import time
import ast
from pytz import timezone
import pytz 

from pyicloud import PyiCloudService

from tkinter import *
from tkinter import font


config = [line.rstrip('\n') for line in open('config.txt')]

to_do = []


EMAIL_ACCOUNT = config[0]
EMAIL_PASSWORD = config[1]
EMAIL_FOLDER = config[2]
FOLDER_TO_DO = config[3]
FOLDER_DONE = config[4]
EMAIL_IMAP = config[5]

M = imaplib.IMAP4_SSL(EMAIL_IMAP)

def emailLogin(M):
	try:
		rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
	except imaplib.IMAP4.error:
		print ("LOGIN FAILED!!! ")
		#sys.exit(1)
		return 

	print (rv, data)

def process_mailbox(M):
	rv, data = M.search(None,"UNSEEN")
	if rv != 'OK':
		print ("No messages found!")
		return

	for num in data[0].split():
		rv, data = M.fetch(num, '(RFC822)')
		if rv != 'OK':
			print ("ERROR getting message", num)
			return
		msg = email.message_from_bytes(data[0][1])
		decode = email.header.decode_header(msg['Subject'])[0]
		#subject = unicode(decode[0])
		#print 'Subject %s: %s' % (num, subject)
		#print 'Message' 

		subject = decode[0].split()

		if subject[0] != 'Delete':
			mov,data=M.uid('STORE',num,'+FLAGS','(\Seen)')
			M.copy(num,FOLDER_TO_DO)
		#print("Moving message " + msg["Subject"] + " to " + FOLDER_TO_DO)
		#result = M.store(num, '-FLAGS', FOLDER_TO_DO)
		##result = m.store(emailid, '+FLAGS', '\\Deleted')
		#mov, data = M.uid('STORE', num , '+FLAGS', '(\Deleted)')
		#M.expunge()



		# print 'Raw Date:', msg['Date']
		# # Now convert to local date-time
		# date_tuple = email.utils.parsedate_tz(msg['Date'])
		# if date_tuple:
		#     local_date = datetime.datetime.fromtimestamp(
		#         email.utils.mktime_tz(date_tuple))
		#     print "Local Date:", \
		#         local_date.strftime("%a, %d %b %Y %H:%M:%S")

def moveToTrash(M):
	M.select(EMAIL_FOLDER)
	rv,data=M.search(None,'ALL')
	if rv != 'OK':
		print ("No messages in", EMAIL_FOLDER)
		return
	for num in data[0].split():
		rv, data = M.fetch(num, '(RFC822)')
		if rv != 'OK':
			print ("ERROR getting message", num)
			return
		msg = email.message_from_bytes(data[0][1])
		decode = email.header.decode_header(msg['Subject'])[0]
		deleteNum = decode[0].split()

		if deleteNum[0] == 'Delete':
			print ("---Starting to delete message---")

			print ("Should delete msg", num, "with subject",decode[0])
			typ, response = M.fetch(num, '(FLAGS)')
			print ('Flags before:', response)
			M.copy(num,FOLDER_DONE)
			print ('Change Flag')
			M.store(num, '+FLAGS', r'(\Deleted)')
			typ, response = M.fetch(num, '(FLAGS)')
			print ('Flags after:', response)
			typ, response = M.expunge()
			print ('Expunged:', response)

			print ("---Delete finished---")

def moveToDone(M):
	M.select(EMAIL_FOLDER)
	rv,data=M.search(None,'ALL')
	if rv != 'OK':
		print ("No messages in", FOLDER_TO_DO)
		return
	for num in data[0].split():
		rv, data = M.fetch(num, '(RFC822)')
		if rv != 'OK':
			print ("ERROR getting message", num)
			return
		msg = email.message_from_bytes(data[0][1])
		decode = email.header.decode_header(msg['Subject'])[0]
		deleteNum = decode[0].split()

		if deleteNum[0] == 'Delete':

			print ("---Starting to delete message---")

			print ("Should delete msg", deleteNum[1])
			print ("Selecting", FOLDER_TO_DO)
			M.select(FOLDER_TO_DO)
			print ('Matching messages:', deleteNum[1])
			typ, response = M.fetch(deleteNum[1], '(FLAGS)')
			print ('Flags before:', response)
			M.copy(deleteNum[1],FOLDER_DONE)
			print ('Change Flag')
			M.store(deleteNum[1], '+FLAGS', r'(\Deleted)')
			typ, response = M.fetch(deleteNum[1], '(FLAGS)')
			print ('Flags after:', response)
			typ, response = M.expunge()
			print ('Expunged:', response)

			print ("---Delete finished---")

def getToDoList(M):
	M.select(FOLDER_TO_DO)
	rv, data = M.search(None,'ALL')
	count = 1
	#reset to do array
	if rv != 'OK':
		print ("No messages in", FOLDER_TO_DO)
		return
	for num in data[0].split():
		rv, data = M.fetch(num, '(RFC822)')
		if rv != 'OK':
			print ("ERROR getting message", num)
			return
		msg = email.message_from_bytes(data[0][1])
		decode = email.header.decode_header(msg['Subject'])[0]
		subject = str(decode[0])
		to_do_item = "%d: %s" % (count, subject)
		to_do.append(to_do_item)
		count=count+1
		#for part in msg.walk():
		#    # each part is a either non-multipart, or another multipart message
		#    # that contains further parts... Message is organized like a tree
		#	if part.get_content_type() == 'text/plain':
		#		payload = part.get_payload()
		#		payload = payload.rstrip()
		#		payload = payload.translate(None, '=C2=A0')
		#		to_do.append(payload)
				#print payload

def emailWorkFlow(M):
	rv, mailboxes = M.list()
	if rv == 'OK':
		print ("Mailboxes:")
		print (mailboxes)

	rv, data = M.select(EMAIL_FOLDER)
	if rv == 'OK':
		print ("Processing mailbox...", end="")
		process_mailbox(M)
		print ("Done")
		print ("Move to...", end="")
		moveToDone(M)
		print ("Done")
		print ("Move to...", end="")
		moveToTrash(M)
		print ("Trash")
		print ("Get To Do List...", end="")
		getToDoList(M)
		print ("Done")
		M.close()
	else:
		print ("ERROR: Unable to open mailbox ", rv)

	print (M.logout())

	print 
	if to_do:
		print ("Printing To Do list: ")
		for lines in range(len(to_do)):
			print (lines+1,":",to_do[lines])
	else: 
		print ("No new messages")

def calendarWorkFlow():
	iApi = PyiCloudService(config[6], config[7])
	from_dt = datetime(2016,10,1)
	#to_dt = date.today()
	to_dt = datetime(2016,10,10)
	events = iApi.calendar.events(from_dt, to_dt)

	print (len(events))

	for event in range(len(events)):
		for key, value in events[event].items():
			#eventTitle = ""
			#eventStartDate = ""
			#eventEndDate = ""
			if key=='title':
				print (key, ":",value)
				#eventTitle = value
			if key=='startDate':
				print (convertValueToDate(value[0:6]),convertValueToTime(value[0:6]))
			#if key=='endDate':
				#eventEndDate = convertValueToDate(value[0:6]),convertValueToTime(value[0:6])
			#print eventTitle , eventStartDate, eventEndDate

def convertValueToTime(value):
	values = "/".join(str(x) for x in value)
	first, rest = values[0:8], values[8:]
	fullyear = datetime.strptime(first,"%Y%m%d")
	restofdate = datetime.strptime(rest,"/%Y/%m/%d/%H/%M")

	return restofdate.time()

def convertValueToDate(value):
	values = "/".join(str(x) for x in value)
	first, rest = values[0:8], values[8:]
	fullyear = datetime.strptime(first,"%Y%m%d")

	return fullyear.date()

#emailLogin(M)
#emailWorkFlow(M)

#calendarWorkFlow()

def callback(number):
	print ("button", number)

def updateListBox(to_do,listbox):
	for item in to_do:
		listbox.insert(END,item)

def refreshToDo(M,listbox):
	M = imaplib.IMAP4_SSL(EMAIL_IMAP)
	global to_do
	to_do = []
	emailLogin(M)
	emailWorkFlow(M)
	listbox.delete(1, END)
	updateListBox(to_do,listbox)
	listbox.update_idletasks()

root = Tk()

root.title("rpiKiosk")


clockFont = font.Font(family='Helvetica', size=124, weight='normal')
todaysFont = font.Font(family='Helvetica', size=48, weight='normal')
todoFont = font.Font(family='Helvetica', size=18, weight='normal')


w,h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.configure(background='black')

listboxWidth = 30;
listboxHeight = 20;

listbox=Listbox(root,fg="white", bg="black",bd=0,font=todoFont,height=len(to_do),highlightthickness=0)

listbox.insert(END,"To Do List:")
updateListBox(to_do,listbox)

root.bind("<Escape>", lambda e: e.widget.quit())

def pitt():
	global timePitt1;
	# timePitt2 = time.strftime('%H:%M')
	timePitt2 = datetime.now(pytz.timezone('Etc/GMT-6')).astimezone().strftime('%H:%M')

	global time1
	# get the current local time from the PC
	time2 = time.strftime('%H:%M')
	# print (time2)
	# if time string has changed, update it
	if time2 != time1:
		time1 = time2
		# clock.config(text=time2)


	if timePitt2 != timePitt1:
		timePitt1 = timePitt2
		clockPitt.config(text=(time2,timePitt2))

	clockPitt.after(1000,pitt)

time1 = ''
timePitt1 = ''

# clock = Label(root, font=clockFont, bg='black', fg='white')
clockPitt = Label(root, font=clockFont, bg='black', fg='white')

pitt()

root.grid_columnconfigure(0,weight=1)

# clock.grid(row=0,column=0,columnspan=w)
clockPitt.grid(row=0,column=0,columnspan=w)

Label(root,text="Todays Agenda:",font=todaysFont,bg='black',fg='white').grid(row=1,column=0,columnspan=1,sticky='w')
listbox.grid(row=1,column=1,sticky=N)
listbox.place(anchor=SE,x=w,y=h)

#print(listbox.winfo_width())
#print(listbox['width'])


# Entry(root).grid(row=3,column=0,columnspan=1)
# Entry(root).grid(row=3,column=1,columnspan=1)
# Entry(root).grid(row=3,column=2,columnspan=1)
# Entry(root).grid(row=3,column=3,columnspan=1)
# Entry(root).grid(row=3,column=4,columnspan=1)
# Entry(root).grid(row=3,column=5,columnspan=1)
# Entry(root).grid(row=3,column=6,columnspan=1)
# Entry(root).grid(row=3,column=7,columnspan=1)
# Entry(root).grid(row=3,column=8,columnspan=1)
# Entry(root).grid(row=3,column=9,columnspan=1)


#listbox.pack(expand=1,fill=Y,anchor = SE,side=RIGHT)
Button(text="Refresh To Do",   command=lambda: refreshToDo(M,listbox)).grid(row=1,column=1)
#Button(text="two",   command=lambda: callback(2)).pack()
#Button(text="three", command=lambda: callback(3)).pack()




root.mainloop()
