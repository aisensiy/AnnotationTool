#!/usr/bin/python
# -*- coding: utf8 -*-

from Tkinter import *
from tkFileDialog import *
#from config import *
from tkMessageBox import *
from xmlcreator import *
import os
import codecs

configs = open('config.py', 'r').read()
exec(configs)

#entities = [('产地', 'place'), ('品种', 'type'), ('等级', 'rank'), ('其它', 'other')]
def rename(filename, extra):
	(file_path, file_name) = os.path.split(filename)
	(short_name, extension) = os.path.splitext(file_name)
	return os.path.join(file_path, short_name + extra + '.xml')

class FileSelector(Frame):
	def __init__(self, parent=None, **options):
		Frame.__init__(self, parent, **options)
		self.pack()
		Label(self, text='file path').pack(side=LEFT)
		self.filename = StringVar()
		self.ent = Entry(self, state='readonly', width=10, textvariable=self.filename)
		self.ent.pack(side=LEFT, expand=YES, fill=X)
		self.btn = Button(self, text='Choose file', command=self.getfile)
		self.btn.pack(side=RIGHT)
	
	def getfile(self):
		file = askopenfile()
		if file != None: self.filename.set(file.name)
		else: self.filename.set(None)
		self.file = file

	def loadbntaction(self, cmd):
		self.btn.config(command=cmd)

class GoToButton(Frame):
	def __init__(self, parent=None, **options):
		Frame.__init__(self, parent, **options)
		self.pack()
		self.id = IntVar()
		self.ent = Entry(self, width=5, textvariable=self.id)
		self.ent.pack(side=LEFT)
		self.goto = Button(self, text='GOTO', width=8)
		self.goto.pack(side=RIGHT)

class TextArea(Frame):
	def __init__(self, parent=None, **options):
		Frame.__init__(self, parent, **options)
		self.pack()
		self.textarea = Text(self)
		self.textarea.pack(side=TOP)
		self.textarea.config(font=(u'宋体', 12, 'normal'), height = '8')
		self.textblocks = []
		self.current_index = 0
		self.current_prog = StringVar("")
		self.current_id = -1
		self.gotoframe = GoToButton(self)
		self.gotoframe.pack(side=LEFT)
		self.gotoframe.goto.config(command=self.gotoaction)
		self.statusbox = Entry(self, state='readonly', width=12, textvariable=self.current_prog)
		self.statusbox.pack(side=RIGHT)

	def bindselectedaction(self, eventname, cmd):
		self.textarea.bind(eventname, cmd)

	def loadfile(self, file):
		if file == None: return
		self.file2blocks(file)
		self.filltextarea()
		
	def file2blocks(self, file):
		lines = []
		for line in file: lines.append(line.strip().decode(encoding).encode(encoding))
		self.textblocks = []
		sublist = []
		i = 1
		number = int(lines[0].split()[0].split('-')[0])
		sublist.append(lines[0].split()[-1])
		while i < len(lines):
			try:
				temp_num = int(lines[i].split()[0].split('-')[0]) 
				if temp_num == number: sublist.append(lines[i].split()[-1])
				else: 
					self.textblocks.append((number, sublist))
					sublist = [lines[i].split()[-1]]
					number = temp_num
			except:
				pass
			i += 1
			
	def filltextarea(self):
		self.textarea.delete('1.0', END)
		self.textarea.insert('1.0', '\n'.join(self.textblocks[self.current_index][1]))
		self.current_id = self.textblocks[self.current_index][0]
		
	def next(self):
		if self.current_index >= len(self.textblocks) - 1:
			showwarning('Warning', 'At the end of the file now.')
		else:
			self.current_index += 1
			self.filltextarea()
			self.current_prog.set("id:%d|%d/%d" % (self.current_id, self.current_index + 1, len(self.textblocks)))
	
	def gotoaction(self):
		index = -1
		for i in range(len(self.textblocks)):
			if self.gotoframe.id.get() == self.textblocks[i][0]:
				index = i
				break
		if index == -1: showwarning('Warning', 'No id %d in this file' % self.gotoframe.id.get())
		else: 
			self.current_index = index
			self.filltextarea()
			self.current_prog.set("id:%d|%d/%d" % (self.current_id, self.current_index + 1, len(self.textblocks)))
			

#	def showradiobar(self, event):
#		self,showselectedtext()

	def getselected(self):
		try:
			return self.textarea.get(SEL_FIRST, SEL_LAST)
		except: return ""

class Radiobar(Frame):
	def __init__(self, parent=None, picks=[], side=LEFT, anchor=W, command=(lambda: None), disable=True):
		Frame.__init__(self, parent)
		self.var = StringVar()
		self.var.set(None)
		self.rads = []
		for pick in picks:
			rad = Radiobutton(self, text=pick[0], value=pick[1], variable=self.var)
			rad.pack(side=side, anchor=anchor, expand=YES)
			if disable: rad.config(state='disable')
			self.rads.append(rad)

	def state(self):
		return self.var.get()

	def enableradios(self):
		self.var.set(None)
		for rad in self.rads: 
			rad.config(state='normal')
	
	def disableradios(self):
		self.var.set(None)
		for rad in self.rads: rad.config(state='disable')
	
	def bindradio(self, cmd):
		for rad in self.rads: rad.config(command=cmd)

	def select(self, value): self.var.set(value)

class RadioList(Frame):
	def __init__(self, parent=None, side=LEFT, anchor=W, id=-1, **options):
		Frame.__init__(self, parent, **options)
#		Button(self, text='SHOW', command=self.printannotations).pack(side=TOP)
		self.annotations = {'id': id, 'elements': []} 
	
	def addframe(self, text, value):
		fm = Frame(self)
		fm.pack(side=TOP)
		Label(fm, text=text, width=30, justify=RIGHT, relief=SUNKEN).pack(side=LEFT)
		radiobar = Radiobar(fm, entities, disable=False)
		radiobar.pack(side=LEFT)
		radiobar.select(value)
		Button(fm, text=deletetext,
			command=(lambda frame=fm, kv=(text, value): self.removeaction(frame, kv))).pack(side=RIGHT)
		self.annotations['elements'].append((text, radiobar))
	
	def removeaction(self, frame, kv):
		annos = self.totuple(self.annotations['elements'])
		print 'remove debug'
		print annos
		print kv[0], kv[1]
		for i in range(len(annos)):
			if kv[0] == annos[i][0] and kv[1] == annos[i][1]:
				self.annotations['elements'].remove(self.annotations['elements'][i])
				break
		print self.annotations['elements']
		frame.destroy()
	
	def totuple(self, anns):
		return [(text, rb.state()) for text, rb in anns]
	
#	def printannotations(self):
#		for text, radiobar in self.annotations:
#			print text, radiobar.state()
	
#	def persistent(self):

class MainFrame():
	def __init__(self):
		self.root = Tk()
		self.selector = FileSelector(self.root, bd=2)
		self.selector.pack(fill=X, side=TOP)
		self.area = TextArea(self.root, bd=2)
		self.area.pack(side=TOP, fill=X)
		Button(self.root, text='NEXT', command=self.nextaction).pack(side=TOP, fill=X)
		self.radbar = Radiobar(self.root, entities, side=LEFT)
		self.radbar.pack(side=TOP)
		self.radbar.bindradio(self.radioselectaction)
		self.radlist = RadioList(self.root, bd=2)
		self.radlist.pack(side=TOP)
		self.selector.loadbntaction(self.loadfile)
		self.area.bindselectedaction("<ButtonRelease-1>", (lambda event: self.selecttextact()))

		self.annotations = []


	def annotationisnone(self):
		for elem in self.annotations:
			if elem['elements'] is not None and len(elem['elements']) > 0: return False
		return True

	def loadfile(self):
		"""before load a new file, we should persistent the annotation
		xml file if the annotation is not []"""
		self.toxml()
		self.annotations = []
		self.selector.getfile()
		self.area.loadfile(self.selector.file)
		self.reloadradiolist(self.area.current_id)
	
	def radioselectaction(self):
		""" when selected radio button, a new radio list is added"""
		self.radlist.addframe(self.area.getselected(), self.radbar.state())

	def selecttextact(self):
		try:
			self.selecttext = self.area.getselected()
			self.radbar.enableradios()
		except:
			self.radbar.disableradios()
	
	def reloadradiolist(self, id=-1, annotations=[]):
		self.radlist.destroy()
		self.radlist = RadioList(self.root, bd=2, id=id)
		self.radlist.pack(side=TOP)
		for text, value in annotations:
			self.radlist.addframe(text, value)
	
	def nextaction(self):
		self.annotations.append(self.radlist.annotations)
		self.toxml()
		self.area.next()
		self.reloadradiolist(id=self.area.current_id)
		
	def toxml(self):
		if self.annotationisnone(): return
		filename = rename(self.selector.filename.get(), extra)
#		print filename
		file = open(rename(self.selector.filename.get(), extra), 'w')
		xmldoc = xmlinit()
		for elem in self.annotations:
			a = elem['elements']
			if a != []:
				b = self.radlist.totuple(a)
				xmldoc.firstChild.appendChild(createtop(xmldoc, b, str(elem['id'])))
		#open(filename, 'w').write(xmldoc.toprettyxml())
		xmldoc.writexml(codecs.open(filename, 'w', encoding='utf8'), '', '  ', '\n', encoding)
		file.close()

if __name__ == '__main__': 
	MainFrame()
	mainloop()
#	print rename('/asfds/adfasd/adsfasdf/ksdf.xml', '_anno')
