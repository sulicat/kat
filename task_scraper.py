import time
from unicurses import *
import requests

init_pair( 1, COLOR_WHITE, -1 )				# WHITE / Trans 	---- 1
init_pair( 2, COLOR_GREEN, -1 )				# GREEN / Trans 	---- 2
init_pair( 3, COLOR_BLUE, -1 )				# Blue / Trans  	---- 3
init_pair( 4, COLOR_RED, -1 )				# Red / Trans 		---- 4
init_pair( 5, COLOR_BLACK, COLOR_GREEN )	# Red / Blue 		---- 5
init_pair( 6, COLOR_WHITE, COLOR_BLUE )		# Black / Green 	---- 6

url = "http://sulicat.com/listview/sulimyfatcat.php?file=sulimyfatcat"

scroll_offset_y = 2
scroll_offset_x = 0
scroll_speed = 1

try:
	page = requests.get(url)
	html = page.content
	wifi = True
except requests.exceptions.RequestException:
	wifi = False


scrapedStrings = []
pre_completeList = []

foundScript = False
scriptTagNumber = 0
startNumber = 0

numberList = []
classList = []
taskList = []
dueDateList = []
taskCounter = 1
taskNumber = 0

def scroll_up():
	global scroll_offset_y
	scroll_offset_y -= scroll_speed

def scroll_down():
	global scroll_offset_y
	scroll_offset_y += scroll_speed 	

def scrape_task_maneger( window, panel ):
	if wifi == True:
		page = requests.get(url)
		html = page.content

		global scrapedStrings
		scrapedStrings = []
		global pre_completeList
		pre_completeList = []

		global foundScript
		foundScript = False
		global scriptTagNumber
		scriptTagNumber = 0
		global startNumber
		startNumber = 0

		global numberList
		numberList = []
		global classList
		classList = []
		global taskList
		taskList = []
		global dueDateList
		dueDateList = []
		global taskCounter
		taskCounter = 1
		global taskNumber
		taskNumber = 0

		# look for the script tag
		for x in range (0, len(html) - 10 ):
			if html[x: x+8] == "<script>" and foundScript == False:
				startNumber = x + 5
				break


		# now start from after the first script tag to find first line of tasks
		for i in range ( startNumber, len(html) ):
			if html[ i: i+8 ] == "<script>":
				
				for x in range ( i, len(html) ):
					if html[ x: x+9 ] == "</script>":
						#print html[ i+56: x ]
						scrapedStrings.append( html[ i+57: x] )
						break

		# scan through array of semi-readable data and fix it
		for i in range (0, len(scrapedStrings) -1 ):

			# clean up '_
			if len( scrapedStrings[i]) > 2 and scrapedStrings[i][0:2] == "' ":
				scrapedStrings[i] = scrapedStrings[i][2: len( scrapedStrings[i] ) - 7 ] 

			# clean up _'
			if scrapedStrings[i][0:2] == " '" and len( scrapedStrings[i]) > 2:
				scrapedStrings[i] = scrapedStrings[i][2: len( scrapedStrings[i] ) - 7 ]

			# cleam up '
			if scrapedStrings[i][0:1] == "'" and len( scrapedStrings[i]) > 1:
				scrapedStrings[i] = scrapedStrings[i][1: len( scrapedStrings[i] ) - 7 ]

			# now remove tags with SPAN
			if scrapedStrings[i][0:6] != "<span>" and scrapedStrings[i][0:5] != "span>":
				pre_completeList.append( scrapedStrings[i] )

		for i in range (0, len(pre_completeList)):
			#put item is number list
			if taskCounter == 1:
				numberList.append( taskNumber )
				taskCounter += 1
				taskNumber += 1
			
			elif taskCounter == 2:
				classList.append( pre_completeList[i][ 0:len( pre_completeList[i]) - 7 ] )
				taskCounter += 1

			elif taskCounter == 3:
				taskList.append( pre_completeList[i] )
				taskCounter += 1

			elif taskCounter == 4:
				dueDateList.append( pre_completeList[i] )
				taskCounter += 1

			elif taskCounter == 5:
				taskCounter = 1
		

		# find the longest class and task
		max_class = 0
		max_task = 0
		max_due_date = 0
		for i in range ( 0, len(taskList)):
			if len(taskList[i]) > max_task:
				max_task = 	len(taskList[i])
			if len(classList[i]) > max_class:
				max_class = len(classList[i])		
			if len(dueDateList[i]) > max_due_date:
				max_due_date = len(dueDateList[i])

		temp_start_x = int((getmaxyx(window)[1] - max_class - max_task - max_due_date - 6)/2)

		wbkgd(window, color_pair(1))
			
		if scroll_offset_y + 1 > 0 and scroll_offset_y + 1 < getmaxyx(window)[0]:
			wmove(window, 1 + scroll_offset_y, temp_start_x + scroll_offset_x)
			waddstr(window, "Num")

			wmove(window, 1 + scroll_offset_y, temp_start_x + 5 + scroll_offset_x)
			waddstr(window, "Class")

			wmove(window, 1 + scroll_offset_y, temp_start_x + 5 + max_class + 3 + scroll_offset_x)
			waddstr(window, "Task")

			wmove(window, 1 + scroll_offset_y, temp_start_x + 5 + max_class + max_task + 3 + 3 + scroll_offset_x)
			waddstr(window, "Date Due")


		paddin_y = 3

		wbkgd(window, color_pair(2))

		wmove( window, paddin_y + scroll_offset_y, temp_start_x + scroll_offset_x)
		for i in range ( 0 , len(taskList)):
			waddstr(window, str(numberList[i]))
			wmove( window, getyx(window)[0]+1, temp_start_x )

		wmove( window, paddin_y + scroll_offset_y, temp_start_x + 5 + scroll_offset_x)
		for i in range ( 0 , len(taskList)):
			waddstr(window, str(classList[i]))
			wmove( window, getyx(window)[0]+1, temp_start_x + 5)

		wmove( window, paddin_y + scroll_offset_y, temp_start_x + 5 + max_class + 3 + scroll_offset_x)
		for i in range ( 0 , len(taskList)):
			waddstr(window, str(taskList[i]))
			wmove( window, getyx(window)[0]+1, temp_start_x + 5 + max_class + 3)

		wmove( window, paddin_y + scroll_offset_y, temp_start_x + 5 + max_class + 3 + max_task + 3 + scroll_offset_x)
		for i in range ( 0 , len(taskList)):
			waddstr(window, str(dueDateList[i]))
			wmove( window, getyx(window)[0]+1, temp_start_x + 5 + max_class + 3 + 3 + max_task)		

	
		top_panel( panel )
		update_panels()
		doupdate()

	else:

		waddstr( window, "No Wifi" )

		top_panel( panel )
		update_panels()
		doupdate()




def draw_content( window, panel ):

	max_class = 0
	max_task = 0
	max_due_date = 0
	for i in range ( 0, len(taskList)):
		if len(taskList[i]) > max_task:
			max_task = 	len(taskList[i])
		if len(classList[i]) > max_class:
			max_class = len(classList[i])		
		if len(dueDateList[i]) > max_due_date:
			max_due_date = len(dueDateList[i])

	temp_start_x = int((getmaxyx(window)[1] - max_class - max_task - max_due_date - 6)/2)

	wbkgd(window, color_pair(1))
	
	if scroll_offset_y > 0 and scroll_offset_y  < getmaxyx(window)[0]:

		wmove(window, 1 + scroll_offset_y, temp_start_x + scroll_offset_x)
		waddstr(window, "Num")

		wmove(window, 1 + scroll_offset_y, temp_start_x + 5 + scroll_offset_x)
		waddstr(window, "Class")

		wmove(window, 1 + scroll_offset_y, temp_start_x + 5 + max_class + 3 + scroll_offset_x)
		waddstr(window, "Task")

		wmove(window, 1 + scroll_offset_y, temp_start_x + 5 + max_class + max_task + 3 + 3 + scroll_offset_x)
		waddstr(window, "Date Due")


	paddin_y = 2

	wbkgd(window, color_pair(2))

	# wmove( window, paddin_y + scroll_offset_y, temp_start_x + scroll_offset_x)
	# for i in range ( 0 , len(taskList)):
	# 	wmove( window, getyx(window)[0]+1, temp_start_x )	
	# 	if getyx(window)[0] > 1 and getyx(window)[0]+1 < getmaxyx(window)[0]:
	# 			waddstr(window, str(numberList[i]))

	# wmove( window, paddin_y + scroll_offset_y, temp_start_x + 5 + scroll_offset_x)
	# for i in range ( 0 , len(taskList)):
	# 	wmove( window, getyx(window)[0]+1, temp_start_x + 5)
	# 	if getyx(window)[0] > 1 and getyx(window)[0]+1 < getmaxyx(window)[0]:
	# 		waddstr(window, str(classList[i]))

	# wmove( window, paddin_y + scroll_offset_y, temp_start_x + 5 + max_class + 3 + scroll_offset_x)
	# for i in range ( 0 , len(taskList)):
	# 	wmove( window, getyx(window)[0]+1, temp_start_x + 5 + max_class + 3)
	# 	if getyx(window)[0] > 1 and getyx(window)[0]+1 < getmaxyx(window)[0]:
	# 		waddstr(window, str(taskList[i]))
		

	# wmove( window, paddin_y + scroll_offset_y, temp_start_x + 5 + max_class + 3 + max_task + 3 + scroll_offset_x)
	# for i in range ( 0 , len(taskList)):
	# 	wmove( window, getyx(window)[0]+1, temp_start_x + 5 + max_class + 3 + 3 + max_task)
	# 	if getyx(window)[0] > 1 and getyx(window)[0]+1 < getmaxyx(window)[0]:		
	# 		waddstr(window, str(dueDateList[i]))
		
	# move to the start of list
	temp_i = 0
	if paddin_y + scroll_offset_y > 0 and paddin_y + scroll_offset_y < getmaxyx( window )[0]:
		temp_i = 0
		wmove( window, paddin_y + scroll_offset_y, temp_start_x + scroll_offset_x)
	elif paddin_y + scroll_offset_y <= 0:
		temp_i = -1 * (scroll_offset_y + paddin_y)	
		wmove( window, 0, temp_start_x + scroll_offset_x)
	
	for i in range ( temp_i , len(taskList)):
		wmove( window, getyx(window)[0]+1, temp_start_x )	
		if getyx(window)[0] > 1 and getyx(window)[0]+1 < getmaxyx(window)[0]:
				waddstr(window, str(numberList[i]))



	temp_i = 0
	if paddin_y + scroll_offset_y > 0 and paddin_y + scroll_offset_y < getmaxyx( window )[0]:
		temp_i = 0
		wmove( window, paddin_y + scroll_offset_y, temp_start_x + scroll_offset_x + 5)
	elif paddin_y + scroll_offset_y <= 0:
		temp_i = -1 * (scroll_offset_y + paddin_y)	
		wmove( window, 0, temp_start_x + scroll_offset_x + 5 )
	
	for i in range ( temp_i , len(taskList)):
		wmove( window, getyx(window)[0]+1, temp_start_x + 5)	
		if getyx(window)[0] > 1 and getyx(window)[0]+1 < getmaxyx(window)[0]:
				waddstr(window, str(classList[i]))



	temp_i = 0
	if paddin_y + scroll_offset_y > 0 and paddin_y + scroll_offset_y < getmaxyx( window )[0]:
		temp_i = 0
		wmove( window, paddin_y + scroll_offset_y, temp_start_x + scroll_offset_x + 5 + max_class + 3)
	elif paddin_y + scroll_offset_y <= 0:
		temp_i = -1 * (scroll_offset_y + paddin_y)	
		wmove( window, 0, temp_start_x + scroll_offset_x + 5 + max_class + 3 )
	
	for i in range ( temp_i , len(taskList)):
		wmove( window, getyx(window)[0]+1, temp_start_x + 5 + max_class + 3)	
		if getyx(window)[0] > 1 and getyx(window)[0]+1 < getmaxyx(window)[0]:
				waddstr(window, str(taskList[i]))			



	temp_i = 0
	if paddin_y + scroll_offset_y > 0 and paddin_y + scroll_offset_y < getmaxyx( window )[0]:
		temp_i = 0
		wmove( window, paddin_y + scroll_offset_y, temp_start_x + scroll_offset_x + 5 + max_class + 3 + max_task + 3)
	elif paddin_y + scroll_offset_y <= 0:
		temp_i = -1 * (scroll_offset_y + paddin_y)	
		wmove( window, 0, temp_start_x + scroll_offset_x + 5 + max_class + 3 + max_task + 3 )
	
	for i in range ( temp_i , len(taskList)):
		wmove( window, getyx(window)[0]+1, temp_start_x + 5 + max_class + 3 + max_task + 3)	
		if getyx(window)[0] > 1 and getyx(window)[0]+1 < getmaxyx(window)[0]:
				waddstr(window, str(dueDateList[i]))			
			


	update_panels()
	doupdate()