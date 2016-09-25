This file will sum up KAT
made by suli

______________________________________________________________________________________________________________________________________________
KAT.py

Important Variables

	functions			----	List 	- 	takes function object
	num_across			----	int	-	number of icons that fit in screen width
	num_down			----	int 	-	number of icons that fit in screen height
	status_bar_string		----	str 	- 	This is what is diplayed in the status bar
	status_bar_data			----	List 	- 	Will fill a array of strings of the data needed
	left_key			----	int	-	keycode to move left
	right_key			----	int	-	keycode to move right
	up_key				----	int	-	keycode to move up
	left_key			----	int	-	keycode to move left
	scroll_up_key			----	int	-	keycode to scroll up
	scroll_down_key			----	int	-	keycode to scroll down
	select_key			----	int 	- 	keycode to select
	return_key			----	int 	- 	keycode to return

Important Functions
	
	update_status_bar( string )				----	This will put the string in the status bar. Full refresh
	get_status_bar_data ( )					----	Will populate status_bar_data
	Update_icon_position( int x, int y )			----	Add an offset to the icons
	draw_screen( )						----	Will update everything on the screen AND move status 	bar to top of draw stack
	clear_content_screen( )					----	Will fill up the content window with spaces. Effectivley making it blank			

Objects
	
	functionality( str label, int x, int y,  action(), draw(), move_left(), move_right(), move_up(), move_down(), scroll_up(), scroll_down() )
		
		-- methods:
			* draw_icons()
			* perform_action()
			* set_position()
			* set_size()
			* set_flashing()
			* set_state()
			* set_category()
			* bring_to_top()
			* scroll_up()
			* scroll_down()

______________________________________________________________________________________________________________________________________________
task_scraper.py

Important Variables
		
		*****

Important Functions	
		
		scrape_task_maneger ( obj window, obj panel )		----	Will scrape LISTVIEW, fill given window with data.
		draw_content ( obj window, obj panel )			----	This will redraw the contetn window.
		scroll_up( )						----	Will scroll content up 
		scroll_down( )						----	Will scroll content down

_______________________________________________________________________________________________________________________________________________
reddit_askreddit_scraper.py

important variables

		*****

important functions

		scrape_askreddit( obj window, obj panel )			----	Will get html data and display it
		draw( obj window, obj panel )					----	Will draw the scraped data 		
		left( )								----	move left
		right( )							----	move right
		up( )								----	move up
		down( )								----	move down
		scroll_up( )							----	scroll up
		scroll_down( )							----	scroll down

Objects

	askreddit_thread_object( )

		vars:
		-	title 					 str 
		-	comments_count 				str
		- 	author					str
		- 	comments_content			arr[ str ]
		-	comments_author				arr[ str ]


