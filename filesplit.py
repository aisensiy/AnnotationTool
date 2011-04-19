#!python
# -*- coding: utf-8 -*-

import os
import sys

encoding = 'utf-8'
def file2blocks(file):
	lines = []
	for line in file: lines.append(line.strip().decode(encoding).encode('utf-8'))
	textblocks = []
	sublist = []
	i = 1
	number = int(lines[0].split()[0].split('-')[0])
	sublist.append(lines[0])
	while i < len(lines):
		try:
			temp_num = int(lines[i].split()[0].split('-')[0]) 
			if temp_num == number: sublist.append(lines[i])
			else: 
				textblocks.append(sublist)
				sublist = [lines[i]]
				number = temp_num
		except:
			pass
		i += 1
	return textblocks

def splitfiles(filename, number_per_file=500):
	file = open(filename, 'r')
	textblocks = file2blocks(file)
	file.close()
	blocks = ""
	print len(textblocks)
	print len(textblocks)/500
	for i in range(len(textblocks)):
		if i%number_per_file == 0 and i != 0:
			extra = "_" + str(i/number_per_file)
			newfile = open(rename(filename, extra), 'w')
			newfile.write(blocks)
			newfile.close()
			blocks = ""
		blocks += "\n".join(textblocks[i]) + "\n"
	if blocks != "":
		extra = "_" + (str(i/number_per_file + 1))
		newfile = open(rename(filename, extra), 'w')
		newfile.write(blocks)
		newfile.close()

def rename(filename, extra):
	(file_path, file_name) = os.path.split(filename)
	(short_name, extension) = os.path.splitext(file_name)
	return os.path.join(file_path, short_name+extra+extension)

if __name__ == "__main__":
	files = ['apple', 'banana', 'grape', 'peach', 'pear', 'strawberry']
	directory = '/media/sda6/javaprojects/AnnotationTool/src/source/'
	fileformat = "{0}_only_{0}_data.txt"
	for f in files:
		print f
		filename = os.path.join(os.path.join(directory, f), fileformat.format(f))
		print filename
		splitfiles(filename)
