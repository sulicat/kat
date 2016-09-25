# this program has to do the following things
# 	read blackboard
# 	read my emails
# 	read my task maneger
# 	read reddit and ask reddit
# 	display all this info in a user friendly way
# 	must be able to complete and upload new tasks
# 	should be expandable !

from unicurses import *
import time
import requests
import datetime

import task_scraper
import reddit_askreddit_scraper

# start with a class to represent a functionality, must include:
# 	functionality name
# 	method that activates it
#	icon that represents it
# 	screen that draws what this functionality does
# 	icon guidlines:
#		width must be - 	x
# 		height must be - 	y


# -------------------------------------------------------------------------------------------------------------------

class functionality:		# build ------- ( "nameOfFunctionality", x, y, method of action, width(**), height(**) )
	name = ""
	width = 10
	height = 10
	x = 0
	y = 0
	window = newwin(0,0,10,10)
	state = "neutral"			# options ---- neutral , alert 
	flashing = True
	category = "misc"
	left_key = 260
	right_key = 261
	up_key = 259
	down_key = 258
	scroll_up_key = 119
	scroll_down_key = 115
	select_key = 10
	return_key = 263


	# constructor
	# functionality ( "label", int x, int y, run(), draw(), move_left(), move_right(), move_up(), move_down(), scroll_up(), scroll_down(), select() )
	def __init__ ( self, name, x, y, action, draw, move_left = None, move_right = None, move_up = None, move_down = None, scroll_up = None, scroll_down = None, select = None):
		self.name = name
		self.run = action
		self.draw = draw
		self.x = x
		self.y = y
		self.move_left = move_left
		self.move_right = move_right
		self.move_up = move_up
		self.move_down = move_down
		self.scroll_down = scroll_down
		self.scroll_up = scroll_up
		self.select = select

	def perform_action ( self ):
		self.run( window_content, panel_content )
		global program_state
		program_state = "action"	

	def draw_icon ( self ):
		global program_state

		if self.x < screen_width and self.x >= 0 and self.y < screen_height and self.y >= 0:
			self.window = newwin( self.height, self.width, self.y, self.x )	

			if self.state == "selected":
				wbkgd( self.window, color_pair( 5 ) )
			else:
				wbkgd( self.window, color_pair( 2 ) )


			box( self.window, 0,0 )
			
			# make sure the text fits in the box
			if len(self.name) <= (int)(self.width - 2):
				wmove(self.window, (int)((self.height/2) - 1), (int)((self.width/2) - (len(self.name)/2)) )	
				waddstr( self.window, self.name)
			
			# chop string to make it fit in area
			if len(self.name) >= (int)((self.width-2)*(self.height-2)):
				self.name = self.name[ 0 : (int)((self.width-2)*(self.height-2)) ]

			# loop through string and print out parts
			if len(self.name) > (int)(self.width-2):
				temp_end = (int)(len(self.name)/((int)(self.width-2)))
				temp_i = 0

				for i in range ( 0, temp_end ):

					wmove(self.window, (int)(self.height/2) + i - (int)(temp_end/2) , 1 )	

					if self.name[ i*(int)(self.width-2) : (i*(int)(self.width-2))+1 ] == " ":
						waddstr( self.window, self.name[ (i*(int)(self.width-2))+1 : (i+1)*((int)(self.width-2)) ] )

					else:
						waddstr( self.window, self.name[ (i*(int)(self.width-2)) : (i+1)*((int)(self.width-2)) ] )	

					temp_i = (i+1)*((int)(self.width-2))

				wmove(self.window, getyx(self.window)[0]+1, 1)
				waddstr( self.window, self.name[ temp_i:: ] )	



			self.panel = new_panel( self.window )

			if program_state != "icons":
				bottom_panel(self.panel)
		

	def set_position ( self, x, y ):
		self.x = x
		self.y = y	

	def set_size ( self, x, y ):
		self.width = x
		self.height = y	

	def set_flashing ( self, b ):
		self.flashing = b

	def set_state ( self, s ):
		self.state = s

	def set_category ( self, c ):
		self.category = c

	def bring_to_top( self ):
		top_panel( self.panel )

	def scroll_up( self ):
		self.scroll_up()

	def scroll_down( self ):
		self.scroll_down()

		
	def draw_content( self ):
		self.draw( window_content, panel_content )

# ------------------------------------------------------------------------------------------------------------------- 



screen = initscr()
start_color()
use_default_colors()
noecho()
keypad(screen, True)
curs_set( False )

# -----------------
# colors 

init_pair( 1, COLOR_WHITE, -1 )				# WHITE / Trans 	---- 1
init_pair( 2, COLOR_GREEN, -1 )				# GREEN / Trans 	---- 2
init_pair( 3, COLOR_BLUE, -1 )				# Blue / Trans  	---- 3
init_pair( 4, COLOR_RED, -1 )				# Red / Trans 		---- 4
init_pair( 5, COLOR_BLACK, COLOR_GREEN )	# Bkack / Green 	---- 5
init_pair( 6, COLOR_BLACK, COLOR_GREEN )	# Black / Green 	---- 5
init_pair( 7, COLOR_WHITE, COLOR_WHITE )	# Black / Green 	---- 5



# different icon states
# -- neutral
# -- selected
# -- alert-selected
# -- alert


# -----------------
# functionality here 

functions = []
num_across = 10
num_down = 5
status_bar_string = " THis is a status bar. It works I hope"
status_bar_data = []
mode = "standalone"
left_key = 260
right_key = 261
up_key = 259
down_key = 258
scroll_up_key = 119
scroll_down_key = 115
select_key = 10
return_key = 263
check_connection_counter = 0
check_connection_string = ""

# different modes
# -- standalone
# -- connected
# -- thinking

screen_width = getmaxyx( screen )[1]
screen_height = getmaxyx( screen )[0]
width_block = (int)(screen_width/num_across)
height_block = (int)((screen_height)/num_down)
x_offset = 0
y_offset = (int)(screen_height * 0.1)
scroll_speed = (int)((screen_height)/num_down)

# DIFFERENT PROGRAM STATES ---------
# 1 - icons 	------	this is for the main menu
# 2 - action 	------	this is for the program content
program_state = "icons"

window_content = newwin( screen_height, screen_width, 0, 0 )
panel_content = new_panel(window_content)

def test():
	print "hello world"

s = test

# functionality ( "label", int x, int y, run(), draw(), move_left(), move_right(), move_up(), move_down(), scroll_up(), scroll_down(), select() )
functions.append( functionality( "Tasks ", 60, 0, task_scraper.scrape_task_maneger, task_scraper.draw_content, scroll_down = task_scraper.scroll_down, scroll_up=task_scraper.scroll_up ) )
functions.append( functionality( "r/AskReddit", 60, 0, reddit_askreddit_scraper.scrape_askReddit, reddit_askreddit_scraper.draw, move_left = reddit_askreddit_scraper.left, move_right = reddit_askreddit_scraper.right, move_up = reddit_askreddit_scraper.up, move_down = reddit_askreddit_scraper.down ,select = reddit_askreddit_scraper.select, scroll_up = reddit_askreddit_scraper.scroll_up, scroll_down = reddit_askreddit_scraper.scroll_down ) )



functions[0].set_state("selected")



temp_counter_y = 0
# this handles the positioning of the elements
temp_counter_x = 0
for i in range ( 0, len(functions) ):
	
	functions[i].set_size ( width_block, height_block )
	functions[i].set_position( (temp_counter_x*width_block) + x_offset , (temp_counter_y*height_block) + y_offset )

	temp_counter_x += 1
	if temp_counter_x == num_across:
		temp_counter_x = 0
		temp_counter_y += 1


# --------------------------------------------------------------------------------------------------------------------
# - main methods


window_status_bar = newwin( (int)(screen_height * 0.1), screen_width, 0,0 )
wbkgd( window_status_bar, color_pair(6) )
wmove( window_status_bar, (int)((screen_height * 0.1)/2), (int)(screen_width/2) - (int)(len(status_bar_string)/2)   )
waddstr( window_status_bar, status_bar_string )
panel_status_bar = new_panel( window_status_bar )

# drawing the status bar
def update_status_bar( ):

	global status_bar_data
	global check_connection_counter
	wmove( window_status_bar, (int)((screen_height * 0.1)/2), (int)(screen_width/2) - (int)(len(status_bar_string)/2)   )
	waddstr( window_status_bar, " "*len(status_bar_string) )

	wmove( window_status_bar, 0,0 )
	temp_bar_height = (int)(screen_height * 0.1)
	temp_bar_width = screen_width
	temp_bar_elements = int(len(status_bar_data)/2)

	temp_length_top = 0
	temp_length_bottom = 0
	temp_padding = 0
	temp_array_spots = []
	temp_count_top = 0
	temp_count_bottom = 0

	for i in range( 0, len(status_bar_data) ):
		if len(status_bar_data[i]) > int(temp_bar_width*0.2):
			status_bar_data[i] = status_bar_data[i][ 0 :int(temp_bar_width*0.2) ]

	# clear the status bar
	for i in range(0, temp_bar_height):
		wmove( window_status_bar, i, 0 )
		waddstr( window_status_bar, " "*temp_bar_width)

	for i in range ( 0,len(status_bar_data) ):
		if i % 2 != 0 :
			temp_length_bottom += len(status_bar_data[i])
		else:
			temp_length_top += len(status_bar_data[i])	


	if temp_length_top > temp_length_bottom:
		temp_padding = int((temp_bar_width - temp_length_top)/temp_bar_elements)
	else:
		temp_padding = int((temp_bar_width - temp_length_bottom)/temp_bar_elements)	


	for i in range ( 0,len(status_bar_data) ):
		if i % 2 != 0:
			temp_array_spots.append( ((i/2)*temp_padding) + temp_count_top )
			temp_count_top += len(status_bar_data[i])
		else:
			temp_array_spots.append(0)

	for i in range ( 0,len(status_bar_data) ):
		if i % 2 != 0:
			wmove( window_status_bar, int(temp_bar_height/2)+1, temp_array_spots[i] + temp_padding )
			waddstr( window_status_bar, status_bar_data[i] )
		else:
			wmove( window_status_bar, int(temp_bar_height/2)-1, temp_array_spots[i-1] + temp_padding )
			waddstr( window_status_bar, status_bar_data[i-2] )	


def get_status_bar_data():
	global status_bar_data
	global check_connection_counter
	global check_connection_string
	status_bar_data = []

	# To display the Selected Item
	status_bar_data.append( "Selected" )

	for i in range( 0,len(functions) ):
		if functions[i].state == "selected":
			status_bar_data.append( functions[i].name )

	# display the current mode of the program		
	status_bar_data.append( "Mode" )
	status_bar_data.append( mode )

	# display the current connectivity
	status_bar_data.append( "Connection" )
	

	if check_connection_counter == 0:	
		try:
			temp_r = requests.get("http://www.google.com")
			check_connection_string = "Working"
		except requests.exceptions.RequestException:
			check_connection_string = "None"


	check_connection_counter += 1
	if check_connection_counter == 15:
		check_connection_counter = 0
	

	status_bar_data.append( check_connection_string )

	# display the current time
	status_bar_data.append( " Date/Time " )

	temp_s = ""
	temp_s += str(datetime.datetime.today().month) + "/" + str(datetime.datetime.today().day) + " -- " + str(datetime.datetime.today().hour) + ":" + str(datetime.datetime.today().minute)
	status_bar_data.append( temp_s )
			


def update_icon_position( change_x, change_y ):
	change_y = (int)(change_y)
	change_x = (int)(change_x)
	for i in range ( 0, len(functions) ):
		functions[i].set_position( functions[i].x + change_x, functions[i].y + change_y )


def draw_screen ():
	# this will handle the drawing of the icons
	for i in range ( 0, len(functions) ):
		functions[i].draw_icon()	

	top_panel( panel_status_bar )	
	update_panels()
	doupdate()	

def clear_content_screen():
	global window_content
	temp_x = getmaxyx(window_content)[1]
	temp_y = getmaxyx(window_content)[0]

	for i in range (0,temp_y):
		wmove(window_content, i, 0)
		waddstr(window_content, " "*temp_x)

def clear_main_screen( ):
	global screen
	for i in range( 0,getmaxyx(screen)[0]  ):
		wmove( screen, i, 0)
		waddstr( screen, " "*getmaxyx( screen )[1] )


# deals with the movement commands on icons 
def move(s):

	if s == "left":
		
		for i in range (0, len(functions)):
			if functions[i].state == "selected":
				functions[i].set_state("neutral")
				if i != 0:
					functions[ i-1 ].set_state( "selected" )
					break
				else:
					functions[ len(functions)-1 ].set_state( "selected" )
					break
		get_status_bar_data()
		update_status_bar()	
		draw_screen()

	elif s == "right":
		
		for i in range (0, len(functions) ):
			if functions[i].state == "selected":
				functions[i].set_state("neutral")
				
				if i != len(functions)-1:
					functions[i+1].set_state( "selected" )
					break
				else:
					functions[0].set_state( "selected" )
					break	
		get_status_bar_data()
		update_status_bar()	
		draw_screen()
	
	elif s == "up":
		
		for i in range (0, len(functions) ):
			if functions[i].state == "selected":
				functions[i].set_state("neutral")
				
				if i - num_across >= 0:
					functions[i - num_across].set_state( "selected" )
					break
				else:
					if len(functions) + (i-num_across) + 2 < len(functions):
						temp_num = len(functions) + (i-num_across) + 2
					else:
						temp_num = len(functions) + (i-num_across) + 2 - num_across
					functions[temp_num].set_state( "selected" )
					break
		get_status_bar_data()
		update_status_bar()	
		draw_screen()			

	elif s == "down":
		
		for i in range (0, len(functions) ):
			if functions[i].state == "selected":
				functions[i].set_state("neutral")
				
				if i + num_across < len(functions):
					functions[i + num_across].set_state( "selected" )
					break
				else:
					temp_num = i%num_across
					functions[temp_num].set_state( "selected" )
					break
		get_status_bar_data()
		update_status_bar()			
		draw_screen()			



# --------------------------------------------------------------------------------------------------------------------

wbkgd( window_content, color_pair( 2 ) )

draw_screen()
# program loop
program_on = True
while program_on == True:
	key = wgetch( screen )
	
	if key == 27:
		program_on = False
		break
	elif key == return_key:
			program_state = "icons"
			clear_content_screen()
			clear_main_screen( )
			draw_screen()
		
	# key listen for the icon page 
	if program_state == "icons":

		if key == left_key:
			move("left")
		
		elif key == right_key:
			move("right")

		elif key == up_key:
			move("up")

		elif key == down_key:
			move("down")
		
		elif key == scroll_down_key:
			update_icon_position( 0, scroll_speed )
			draw_screen()

		elif key == scroll_up_key:
			update_icon_position( 0, -scroll_speed )
			draw_screen()

		elif key == select_key:
			for i in range ( 0,len(functions) ):
				if functions[i].state == "selected":
					functions[i].perform_action()


	elif program_state == "action":
		
		for i in range (0, len(functions)):
			
			if functions[i].state == "selected":
				
				# scroll up
				if key == functions[i].scroll_up_key and functions[i].scroll_up != None:
					functions[i].scroll_up()
					clear_content_screen()
					functions[i].draw_content()

				# scroll down	
				if key == functions[i].scroll_down_key and functions[i].scroll_down != None:
					functions[i].scroll_down()
					clear_content_screen()
					functions[i].draw_content()

				# left	
				if key == functions[i].left_key and functions[i].move_left != None:
					functions[i].move_left()
					clear_content_screen()
					functions[i].draw_content()

				# right	
				if key == functions[i].right_key and functions[i].move_right != None:
					functions[i].move_right()
					clear_content_screen()
					functions[i].draw_content()

				# up	
				if key == functions[i].up_key and functions[i].move_up != None:
					functions[i].move_up()
					clear_content_screen()
					functions[i].draw_content()	

				# down	
				if key == functions[i].down_key and functions[i].move_down != None:
					functions[i].move_down()
					clear_content_screen()
					functions[i].draw_content()

				# select	
				if key == functions[i].select_key and functions[i].select != None:
					functions[i].select()
					clear_content_screen()
					functions[i].draw_content()	



	
	else:
		print key

						




time.sleep(1)
endwin()
