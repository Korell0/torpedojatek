import copy, random

def print_board(s,board):

	player = "Computer"
	if s == "u":
		player = "User"
	
	print "The " + player + "'s board look like this: \n"

	#horizontal
	print " ",
	for i in range(10):
		print "  " + str(i+1) + "  ",
	print "\n"

	for i in range(10):
	
		#vertical
		if i != 9: 
			print str(i+1) + "  ",
		else:
			print str(i+1) + " ",

		#board values, and cell dividers
		for j in range(10):
			if board[i][j] == -1:
				print ' ',	
			elif s == "u":
				print board[i][j],
			elif s == "c":
				if board[i][j] == "*" or board[i][j] == "$":
					print board[i][j],
				else:
					print " ",
			
			if j != 9:
				print " | ",
		print
		
		#print a horizontal line
		if i != 9:
			print "   ----------------------------------------------------------"
		else: 
			print 

def user_place_ships(board,ships):

	for ship in ships.keys():

		#get coordinates
		valid = False
		while(not valid):

			print_board("u",board)
			print "Placing a/an " + ship
			x,y = get_coor()
			ori = v_or_h()
			valid = validate(board,ships[ship],x,y,ori)
			if not valid:
				print "Cannot place a ship there.\nPlease take a look at the board and try again."
				raw_input("Hit ENTER to continue")

		#ship place
		board = place_ship(board,ships[ship],ship[0],ori,x,y)
		print_board("u",board)
		
	raw_input("Done placing user ships. Hit ENTER to continue")
	return board


def computer_place_ships(board,ships):

	for ship in ships.keys():
	
		#random pos
		valid = False
		while(not valid):

			x = random.randint(1,10)-1
			y = random.randint(1,10)-1
			o = random.randint(0,1)
			if o == 0: 
				ori = "v"
			else:
				ori = "h"
			valid = validate(board,ships[ship],x,y,ori)

		#place the ship
		print "Computer placing a/an " + ship
		board = place_ship(board,ships[ship],ship[0],ori,x,y)
	
	return board