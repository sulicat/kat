import time
from unicurses import *
import requests

header_files = { "User-Agent": "Mozilla/5.0" }
URL = "https://www.reddit.com/r/AskReddit/"

try:
	page = requests.get( URL, headers=header_files )
	html = page.content
except requests.exceptions.RequestException:
	page = "NA"
	html = "there is no connection to r/AskReddit"

scroll_offset_y = 0
scroll_offset_x = 0
scroll_speed = 1
thread_objects = []

init_pair( 1, COLOR_WHITE, -1 )				# WHITE / Trans 	---- 1
init_pair( 2, COLOR_GREEN, -1 )				# GREEN / Trans 	---- 2
init_pair( 3, COLOR_BLUE, -1 )				# Blue / Trans  	---- 3
init_pair( 4, COLOR_RED, -1 )				# Red / Trans 		---- 4
init_pair( 5, COLOR_BLACK, COLOR_GREEN )	# Red / Blue 		---- 5
init_pair( 6, COLOR_WHITE, COLOR_BLUE )		# Black / Green 	---- 6

# ---------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------------------------------- #

class askreddit_thread_object :
	
	title = ""
	author = ""
	link = ""
	comments_count = ""
	comments_authors = []
	comments_content = []
	selected = False


	def __init__ ( self, link=None, title=None, author=None, comments_count=None, comments_authors=None, comments_content=None ):
		
		if link != None:
			self.link = link

		if title != None:
			self.title = title

		if author != None:
			self.author = author
			
		if comments_count != None:
			self.comments_count = comments_count	

		if comments_authors != None:
			self.comments_authors = comments_authors

		if comments_content != None:
			self.comments_authors = comments_content		
			

	def set_content ( self, link=None, title=None, author=None, comments_count=None, comments_authors=None, comments_content=None ):
		
		if link != None:
			self.link = link

		if title != None:
			self.title = title

		if author != None:
			self.author = author
			
		if comments_count != None:
			self.comments_count = comments_count	

		if comments_authors != None:
			self.comments_authors = comments_authors

		if comments_content != None:
			self.comments_authors = comments_content		

	def set_state( self, x ):
		self.selected = x			



# ---------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------------------------------- #



def scrape_askReddit( window, panel ):
	global html
	global thread_objects
	global scroll_offset_y
	global scroll_speed

	temp_start_title = 0
	temp_end_title = 0
	temp_start_link = 0
	temp_end_link = 0
	done_link = False
	temp_start_comments = 0
	temp_end_comments = 0
	temp_start_author = 0
	temp_end_author = 0
	temp_counter = 0
	temp_arr = []

	# delete the parts of the html that cause trouble
	for i in range ( 0 , len(html) - 10 ):
		if html [ i : i+10 ] == "MODERATORS":
			for x in range ( i , len(html) ):
				if html[ x : x+5 ] == "</ul>":
					html = html[0:i] + html[x::]
					break
			break			


	# loop through and find every thread TITLE section
	for i in range ( 0 , len(html) - 15 ):
		if html[i : i+15 ] == "title may-blank":
			
			for x in range( i + 15, len(html) - 15 ):
				# check when the link starts
				if html[ x : x+5 ] == "href=":
					temp_start_link = x+6
					x = x + 6
				
				# check when the link end
				if html[ x : x+2 ] == '/"':
					temp_end_link = x
					x = x + 2
					done_link = True

				# check when the title starts
				if html [ x : x+1 ] == ">" and done_link == True:
					temp_start_title = x+1
					x = x+1

				if html[ x : x+4 ] == "</a>" and done_link == True:
					temp_end_title = x
					break

			# waddstr( window, html[ temp_start_link : temp_end_link ] )
			# wmove( window, getyx(window)[0]+1, 0 )
			# waddstr( window, html[ temp_start_title : temp_end_title ] )
			# wmove( window, getyx(window)[0]+1, 0 )
			thread_objects.append(   askreddit_thread_object( link = html[ temp_start_link : temp_end_link ], title = html[ temp_start_title : temp_end_title ] )    )


	temp_counter = 0		
	# loop to find the comments 
	for i in range ( 0 , len(html) - 18 ):
		if html[ i : i + 18 ] == "comments may-blank":

			for x in range ( i, len(html) - 18 ):
				if html[ x : x+1 ] == ">":
					temp_start_comments = x+1
					x = x+1

				if html[ x : x+4] == "</a>":
					temp_end_comments = x
					break

			# waddstr( window, html[ temp_start_comments : temp_end_comments ] )
			# wmove( window, getyx(window)[0]+1, 0 )
			thread_objects[ temp_counter ].set_content( comments_count = html[ temp_start_comments : temp_end_comments ] )
			temp_counter += 1


	temp_counter = 0
	# loop to find the authors
	for i in range ( 0 , len(html) - 16 ):
		if html[ i : i+16 ] == "author may-blank":

			for x in range ( i, len(html) - 16):
				if html[ x : x + 1 ] == ">":
					temp_start_author = x+1
					x = x +1

				if html[ x : x+4 ] == "</a>":
					temp_end_author = x
					break


			# waddstr( window, html[ temp_start_author : temp_end_author ] )
			# wmove( window, getyx(window)[0]+1, 0 )
			thread_objects[ temp_counter ].set_content( author = html[ temp_start_author : temp_end_author ] )
			temp_counter += 1

	

	# now we have the data in the thread_object array
	# we will display it, to do that we can use an outside function
	

	if len( thread_objects ) > 1:
		for i in range ( 0,len(thread_objects) ):
			thread_objects[i].set_state( False )
		thread_objects[0].set_state( True )
	
	# wmove( window, scroll_offset_y, scroll_offset_x )
	# for i in range ( 0, len(thread_objects) ):

	# 	if thread_objects[i].selected == True:
	# 		waddstr( window, "#"*(getmaxyx( window )[1]-1) )			
	# 	else:
	# 		waddstr( window, "-"*(getmaxyx( window )[1]-1) )		
			
	# 	wmove( window, getyx( window )[0]+1, 0 )	
	# 	waddstr( window, thread_objects[i].title )
	# 	wmove( window, getyx( window )[0]+1, 0 )
	# 	waddstr( window, thread_objects[i].author )
	# 	wmove( window, getyx( window )[0]+1, 0 )
	# 	waddstr( window, thread_objects[i].comments_count )
	# 	wmove( window, getyx( window )[0]+1, 0 )

	# 	if thread_objects[i].selected == True:
	# 		waddstr( window, "#"*(getmaxyx( window )[1]-1) )
	# 	else:
	# 		waddstr( window, "-"*(getmaxyx( window )[1]-1) )

	# 	wmove( window, getyx( window )[0]+1, 0 )	


	temp_start_x = scroll_offset_x
	temp_start_y = scroll_offset_y
	temp_start_i = 0

	for i in range ( 0, len(thread_objects) ):

			# draw the top border
		if temp_start_y >= 0 and temp_start_y <= getmaxyx( window )[0]:
			wmove( window, temp_start_y, temp_start_x )

			if thread_objects[i].selected == True:
				waddstr( window, "#"*(getmaxyx( window )[1]-1) )
			else:
				waddstr( window, "-"*(getmaxyx( window )[1]-1) )
	
			wmove( window, getyx( window )[0]+1, 0 )
			temp_start_y = getyx( window )[0]
		else:
			temp_start_y += 1

		# draw the title
		if temp_start_y >= 0 and temp_start_y <= getmaxyx( window )[0]:
			wmove( window, temp_start_y, temp_start_x )
			waddstr( window, thread_objects[i].title )
			wmove( window, getyx( window )[0]+1, 0 )
			temp_start_y = getyx( window )[0]
		else:
			temp_start_y += 1

		# draw the author
		if temp_start_y >= 0 and temp_start_y <= getmaxyx( window )[0]:
			wmove( window, temp_start_y, temp_start_x )
			waddstr( window, thread_objects[i].author )
			wmove( window, getyx( window )[0]+1, 0 )
			temp_start_y = getyx( window )[0]
		else:
			temp_start_y += 1

		# draw the comment count	
		if temp_start_y >= 0 and temp_start_y <= getmaxyx( window )[0]:
			wmove( window, temp_start_y, temp_start_x )
			waddstr( window, thread_objects[i].comments_count )
			wmove( window, getyx( window )[0]+1, 0 )
			temp_start_y = getyx( window )[0]
		else:
			temp_start_y += 1	

		# draw the bottom border	
		if temp_start_y >= 0 and temp_start_y <= getmaxyx( window )[0]:
			wmove( window, temp_start_y, temp_start_x )

			if thread_objects[i].selected == True:
				waddstr( window, "#"*(getmaxyx( window )[1]-1) )
			else:
				waddstr( window, "-"*(getmaxyx( window )[1]-1) )

			wmove( window, getyx( window )[0]+1, 0 )
			temp_start_y = getyx( window )[0]
		else:
			temp_start_y += 1	


	top_panel( panel )
	update_panels()
	doupdate()






def draw( window, panel ):
	
	global thread_objects
	global scroll_offset_y
	global scroll_offset_x

	# wmove( window, scroll_offset_y, scroll_offset_x )
	# for i in range ( 0, len(thread_objects) ):

	# 	if thread_objects[i].selected == True:
	# 		waddstr( window, "#"*(getmaxyx( window )[1]-1) )			
	# 	else:
	# 		waddstr( window, "-"*(getmaxyx( window )[1]-1) )	

	# 	wmove( window, getyx( window )[0]+1, 0 )	
	# 	waddstr( window, thread_objects[i].title )
	# 	wmove( window, getyx( window )[0]+1, 0 )
	# 	waddstr( window, thread_objects[i].author )
	# 	wmove( window, getyx( window )[0]+1, 0 )
	# 	waddstr( window, thread_objects[i].comments_count )
	# 	wmove( window, getyx( window )[0]+1, 0 )

		# if thread_objects[i].selected == True:
		# 	waddstr( window, "#"*(getmaxyx( window )[1]-1) )
		# else:
		# 	waddstr( window, "-"*(getmaxyx( window )[1]-1) )

	# 	wmove( window, getyx( window )[0]+1, 0 )



	temp_start_x = scroll_offset_x
	temp_start_y = scroll_offset_y
	temp_start_i = 0

	for i in range ( 0, len(thread_objects) ):

		# draw the top border
		if temp_start_y >= 0 and temp_start_y <= getmaxyx( window )[0]:
			wmove( window, temp_start_y, temp_start_x )

			if thread_objects[i].selected == True:
				waddstr( window, "#"*(getmaxyx( window )[1]-1) )
			else:
				waddstr( window, "-"*(getmaxyx( window )[1]-1) )
	
			wmove( window, getyx( window )[0]+1, 0 )
			temp_start_y = getyx( window )[0]
		else:
			temp_start_y += 1

		# draw the title
		if temp_start_y >= 0 and temp_start_y <= getmaxyx( window )[0]:
			wmove( window, temp_start_y, temp_start_x )
			waddstr( window, thread_objects[i].title )
			wmove( window, getyx( window )[0]+1, 0 )
			temp_start_y = getyx( window )[0]
		else:
			temp_start_y += 1

		# draw the author
		if temp_start_y >= 0 and temp_start_y <= getmaxyx( window )[0]:
			wmove( window, temp_start_y, temp_start_x )
			waddstr( window, thread_objects[i].author )
			wmove( window, getyx( window )[0]+1, 0 )
			temp_start_y = getyx( window )[0]
		else:
			temp_start_y += 1

		# draw the comment count	
		if temp_start_y >= 0 and temp_start_y <= getmaxyx( window )[0]:
			wmove( window, temp_start_y, temp_start_x )
			waddstr( window, thread_objects[i].comments_count )
			wmove( window, getyx( window )[0]+1, 0 )
			temp_start_y = getyx( window )[0]
		else:
			temp_start_y += 1	

		# draw the bottom border	
		if temp_start_y >= 0 and temp_start_y <= getmaxyx( window )[0]:
			wmove( window, temp_start_y, temp_start_x )

			if thread_objects[i].selected == True:
				waddstr( window, "#"*(getmaxyx( window )[1]-1) )
			else:
				waddstr( window, "-"*(getmaxyx( window )[1]-1) )

			wmove( window, getyx( window )[0]+1, 0 )
			temp_start_y = getyx( window )[0]
		else:
			temp_start_y += 1	


	top_panel( panel )
	update_panels()
	doupdate()

def select():
	print "selected"

def scroll_up():
	global scroll_offset_y
	global scroll_speed
	scroll_offset_y += scroll_speed	

def scroll_down():
	global scroll_offset_y
	global scroll_speed	
	scroll_offset_y -= scroll_speed

def left():
	print "move left"

def right():
	print "move right"



def up():
	global thread_objects
	
	for i in range( 0,len(thread_objects) ):

		if thread_objects[i].selected == True:
			thread_objects[i].set_state( False )
			temp_i = i
			break

	if temp_i == 0:
		thread_objects[ len(thread_objects) - 1 ].set_state( True )
	else:		
		thread_objects[ temp_i - 1 ].set_state( True )



def down():
	global thread_objects
	temp_i = 0

	for i in range( 0,len(thread_objects) ):

		if thread_objects[i].selected == True:
			thread_objects[i].set_state( False )
			temp_i = i
			break

	if temp_i == len( thread_objects ) - 1:
		thread_objects[ 0 ].set_state( True )
	else:		
		thread_objects[ temp_i + 1 ].set_state( True )		