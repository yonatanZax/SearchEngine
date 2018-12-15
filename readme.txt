301730354_204662779
IR Search engine project, Part 1

*********				Readme file				*********

* Important - Check the import list at the bottom of this file before running the exe file.
			- Check that at least 'Corpus size' is available in the Posting's path on the disk.

* Executable is located in the project's folder.
  By double clicking on the "RunMain.bat" file the gui window will pop.
  - Runs with py2exe



Gui details: ( From top to bottom )

	* Gui has a single window, very intuitive to work with.
	* At that bottom there is a status line for the user.
	* While process is running, some buttons will be DISABLED until its done.

	Corpus path - two options
			1. Enter corpus's path
			2. Find the directory with a searchable window (click the 'Find' button).

	Posting path - two options
			1. Enter posting's path.
			2. Find the directory with a searchable window (click the 'Find' button).

	Language -
			It's posible to choose a language from the drop table.
			* Note that the list will update after the indexing is done.

	Stemming -
			Checkbox that let's the user choose if 'Build' should include Stemming.
			* This button will also be relevant while the user is asking to 'Load'/'Show' the terms dictionary.

	Delete button -
			This button deletes the folder written inside the "Posting path".
			* To make sure the path is valid:
				1. Checks that a folder called "SavedFiles" exists in the given path.
				2. If the savedfiles folder exists, it will be deleted.

	Build button -
			This button Starts the process.
			1. Checks that the corpus path exists and has the file "stop_words.txt"
			2. Checks that the posting path exists.
			3. Create a folder called "SavedFiles", where all the data will be saved.

	Progress bar -
			* Build time might be long while running a large corpus.
			  We found out that this bar is essential to make a better user experience.
				1. 'Posting' - let's the user know how when posting is about to be done.
				2. 'Merge' - let's the user know how when marge is about to be done.

			* Note that due to the multiprocessing, merge progress starts before the posting gets to 100%.


	Dictionary buttons:
	1. Upload -
			Generates the terms dictionary from all the small files.
			* Terms are splitted by the first character into 27 files.
				1. Checks the 'Stemming' checkbox to know which data to show the user.
				2. Checks that a 'SavedFiles' folder exists.

	2. Show -
			Displays the terms dictionary to the user in another window.
			Tables fields: "Term | df | sumTf | # posting line"
				1. Checks that the wanted data was already loaded (meaning the user used the upload button)


	Summary -
			Displays the summary of the 'Build' process.
			Output example:

				** Run without stemming - Details **
						Number of Terms:  524973
						Number of Docs:   472513
						Parsing Time:     0:18:32
						Merging Time:     0:07:23
						Everything took:  0:25:55

	Status bar -
			Changes by the current state.
			Displays detailed information to the user.



# Import list:

	# General
	import py2exe
	import os
	import shutil
	import string

	# Threads
	from datetime import datetime
	from concurrent.futures import ProcessPoolExecutor
	from concurrent.futures import ThreadPoolExecutor
	from concurrent.futures import as_completed
	from threading import Thread

	# Parsing
	import re
	from nltk.stem import snowball
	import lxml.html

	# Merge
	import heapq


	#GUI
	from tkinter import filedialog
	from tkinter import *
	from tkinter.ttk import *

	#API
	from restcountries.api import RestCountries
	import geocoder



