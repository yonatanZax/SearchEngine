
IR Search engine project, Part 1 and Part 2


* Important:
1. Check the import list at the bottom of this file before running the executable file.
	* The folder "import files.zip" contains some of the imports for the project.

2. Check that at least 'Corpus size' is available in the Posting's path on the disk.
			
* Executable is located in the project's folder.
  By double clicking on the "RunMain.bat" file the gui window will pop.
  - Runs with py2exe 

How to use the engine:
	- in case you want to build the engine on a new corpus:
		- At part 1 choose the directory of the new corpus at 'Corpus path'.
		- Choose a path for the files to be saved in at 'Posting path'.
		- Press build and wait untill the engine finishes.
		  Meanwhile you can check our cool & smart progress bar that works according to the actual corpus and merging process.
		- After the build is done click on 'Upload' to load the data.
		- Now you can switch to Part 2 by clicking it at the top right corner.
		- For understading Part 2 please read the instructions for it below.
	-in case you already built the engine before and just want the search the data:
		- Choose the path of the posting files saved with 'Posting path'.
		- Click on 'Upload' to upload the data.
		- Now you can switch to Part 2 by clicking it at the top right corner.
		- At Part 2 you can either enter your own query by simply writing it at 'Query' and click 'Run query'
		  or you can enter a file through the 'Query File' and click 'Run query from file'.
		- You can choose to use Stem and Sementics by checking the check-box
		- After the run you can save the output to a file. make sure you chose a directory path at 'Save Results'
		- You can see the most dominant Entities of the files that came back from the query by clicking 'Show Entities'		


Gui details part 1: ( From top to bottom )
	
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
			Changes according to the current state.
			Displays detailed information to the user.
			




 
Gui details part 2: ( From top to bottom ) 
	
	* Gui has a single window, very intuitive to work with.
	* At that bottom there is a status line for the user.
	* While process is running, some buttons will be DISABLED until its done.

	Query file path - two options
			1. Enter query's path
			2. Find the directory with a searchable window (click the 'Browse' button).
	
	Save results path - two options
			1. Enter wanted path.
			2. Find the directory with a searchable window (click the 'Browse' button).
			
	Cities - 
			It's posible to choose one or more cities from the list.
			* Note that the list will pressent cities only if found in corpus.
			
			
	Checkboxes:
			1. " Stemming " : Use stemming
			
	
	Run query button - 
		This button runs the query written in the textbox "Query"
		* To make sure the path is valid:
			1. Checks that the textbox is not empty.
		
	Run query from file button - 
		Run all the queries in the file and displays it in the output window.
			1. Checks that the query file path exists.
			
	Make Three Runs button - 
		From the Query path creates three result files.
		Runs:
			1. noStem noSem
			2. Stem noSem
			3. Stem Sem
			
	Show Entities Button - 
		After a run is printed in the output window.
		User can view the top5 five entities for every doc in the list.
	
	
	Save to Trec_Eval Button - 
		* Checks the given path in the Save results textbox.
		Saves the results in a new file called: "results.txt".
		* Note that it will override the prev file if exists.
			
			



			
# Import list:

	# General
	import os
	import shutil
	import string
	import py2exe

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














