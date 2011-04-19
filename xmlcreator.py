#!python
# -*- coding: utf8 -*-

from xml.dom.minidom import Document
from biaozhu import rootElement, topElement

def createelem(xmldoc, text, value):
		elem = xmldoc.createElement(value)
		elem.appendChild(xmldoc.createTextNode(text))
		return elem

def createtop(xmldoc, tuples, id):
	top = xmldoc.createElement(topElement)
	for text, value in tuples:
		top.appendChild(createelem(xmldoc, text, value))
	top.setAttribute('id', id)
	return top

def xmlinit():
	xmldoc = Document()
	xmldoc.appendChild(xmldoc.createElement(rootElement))
	return xmldoc

if __name__ == '__main__':
	tuples = [('place', u'广州'), ('rank', u'一等')]
	xmldoc = xmlinit()
	print createtop(xmldoc, tuples).toprettyxml()

