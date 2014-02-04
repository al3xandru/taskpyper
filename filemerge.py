#
# merge files - merge two folders with no duplicate files
#
g_sWelcome = """
merge_files - merge files from two directories into one.

The files from the "from" directory will be moved to the "to" directory, while
duplicated files will be removed. If two files are in the same name but are
different in signature (revision time, size), the new one will be renamed.

Author: Yue Zhang, 2006R
"""
import sys,os
import filecmp
import shutil

#
# Given a path, filename and extention, return a full path name without collision
#
def fileid_alloc(sPath, sPathFrom, sFileName, sExtension):
	global nDuplicateName, nDuplicateContent
	nIndex = 0
	sNewFileName = os.path.join(sPath, sFileName + sExtension)
	if os.path.exists(sNewFileName):
		nDuplicateName += 1
		if filecmp.cmp(sNewFileName, os.path.join(sPathFrom, sFileName + sExtension)):
			nDuplicateContent += 1
			return sNewFileName
	while os.path.exists(sNewFileName):
		nIndex += 1
		sNewFileName = os.path.join(sPath, sFileName + str(nIndex) + sExtension)
	return sNewFileName
	
#
# Main function
#
def merge_files(folder_from, folder_to):
	for sFullFileName in os.listdir(folder_from):
		sFileName, sExtension = os.path.splitext(sFullFileName)
		sNewFileName = fileid_alloc(folder_to, folder_from, sFileName, sExtension)
		shutil.move(os.path.join(folder_from, sFullFileName), sNewFileName)
		
#
# Main entry
#
if __name__ == '__main__':
	global nDuplicateName, nDuplicateContent
	nDuplicateName = 0
	nDuplicateContent = 0
	print g_sWelcome
	if len(sys.argv) != 3:
		print "Usage: merge_files.py folder_from folder_to"
		sys.exit(0)
	merge_files(sys.argv[1], sys.argv[2])
	print "In all %d duplicate file names processed, among which %d
				duplicate contents are merged and the rest are allocated new name."
				% (nDuplicateName, nDuplicateContent) 