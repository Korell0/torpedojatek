import copy, random,os,sys
abc = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',)

def green(input):
	return '\033[1;32;32m'+input+'\033[0m'

def red(input):
	return '\033[1;30;31m'+input+'\033[0m'

def blue(input):
	return '\033[1;30;34m'+input+'\033[0m'	

def print_board(s,board):

	player = "Szamitogep"
	if s == "u":
		player = "Jatekos"
	
	print("A " + player + " táblája így néz ki: \n")

	
	#print the horizontal numbers
	row_string = " "
	for i in range(10):
		row_string += "   " + abc[i] + "  "

	print(row_string + '\n')

	row_string = ''

	for i in range(10):
		#print the vertical line number
		if i != 9: 
			row_string += str(i+1) + "  "
		else:
			row_string += str(i+1) + " "

		#print the board values, and cell dividers
		for j in range(10):
			if board[i][j] == -1:
				row_string += "   "
			elif s == "u":
				if board[i][j] == "*":
					row_string +=' '+ blue(board[i][j]+' ')
				elif board[i][j] == "$":
					row_string +=' '+ red(board[i][j]+' ')
				else:
					row_string += " "+board[i][j]+" "

			elif s == "c":
				if board[i][j] == "*":
					row_string +=' '+ blue(board[i][j]+' ')
				elif board[i][j] == "$":
					row_string +=' '+ red(board[i][j]+' ')
				else:
					row_string += "   "
			
			if j != 9:
				row_string += green(" | ")
			
		print(row_string)
		row_string = ''
		
		#print a horizontal line
		if i != 9:
			print(green("   ----------------------------------------------------------"))
		else:
			print("")

def user_place_ships(board,ships):

	user_input=input("Szeretnéd véletlenszerüen letenni a hajóid? (i/n)")
	if user_input.lower()=="i":
		
		board= computer_place_player_ships(board,ships)
		print_board('u',board)
		input("Nyomj ENERT a folytatáshoz.")
		return board

	for ship in ships.keys():

		valid = False
		while(not valid):

			print_board("u",board)
			print("Elhelyezi a " + ship)
			x,y = get_coor()
			ori = f_or_v()
			valid = validate(board,ships[ship],x,y,ori)
			if not valid:
				print("Nem tehetsz ide hajót\nKérlek probáld újra.")
				input("Nyomj ENTERT a fojtatáshoz")

		#place the ship
		board = place_ship(board,ships[ship],ship[0],ori,x,y)
		print_board("u",board)
		
	input("Elhelyezted az összes hajódat nyomj ENTERT hogy elkezdődjön a játék")
	return board

def computer_place_ships(board,ships):

	for ship in ships.keys():
	
		#genreate random coordinates and vlidate the postion
		valid = False
		while(not valid):

			x = random.randint(1,10)-1
			y = random.randint(1,10)-1
			o = random.randint(0,1)
			if o == 0: 
				ori = "f"
			else:
				ori = "v"
			valid = validate(board,ships[ship],x,y,ori)

		#place the ship
		print("A Számítógép elhelyezi a/az  " + ship)
		board = place_ship(board,ships[ship],ship[0],ori,x,y)
	
	return board

def computer_place_player_ships(board,ships):

	for ship in ships.keys():
	
		valid = False
		while(not valid):

			x = random.randint(1,10)-1
			y = random.randint(1,10)-1
			o = random.randint(0,1)
			if o == 0: 
				ori = "f"
			else:
				ori = "v"
			valid = validate(board,ships[ship],x,y,ori)

		print("Véletlen szerűen tetted le  " + ship)
		board = place_ship(board,ships[ship],ship[0],ori,x,y)
	
	return board

def place_ship(board,ship,s,ori,x,y):

	#place ship based on orientation
	if ori == "f":
		for i in range(ship):
			board[x+i][y] = s
	elif ori == "v":
		for i in range(ship):
			board[x][y+i] = s

	return board
	
def validate(board,ship,x,y,ori):

	#validate the ship can be placed at given coordinates
	if ori == "f" and x+ship > abc.index("J"):
		return False
	elif ori == "v" and y+ship > 10:
		return False
	else:
		if ori == "f":
			for i in range(ship):
				if board[x+i][y] != -1:
					return False
		elif ori == "v":
			for i in range(ship):
				if board[x][y+i] != -1:
					return False
		
	return True

def f_or_v():

	#get ship orientation from user
	while(True):
		user_input = input("Függőleges vagy Vízszintesen rakod? (F,V) ? ").lower()
		if user_input == "f" or user_input == "v":
			return user_input
		else:
			print("Nem jó írj F-et vagy V-t")

def get_coor():
	
	while (True):
		coor = input("Add meg a koordinátákat: ")
		try:
			#see that user entered 2 values seprated by comma
			if len(coor) < 2:
				raise Exception("Nemjó egy betűnek és egy számnak kell lennie.");

			#check that 2 values are integers
			x = abc.index(coor[0])
			y = int(coor[1:])-1

			#check that values of integers are between 1 and 10 for both coordinates
			if x > 9 or x < 0 or y > 9 or y < 0:
				raise Exception("Nem jó 1-10 ig kell megadni számokat.")

			#if everything is ok, return coordinates
			return (y,x)
		
		except ValueError:
			print("Nemjó próbáld újra")
		except Exception as e:
			print(e)

def make_move(board,x,y):
	
	
	if board[x][y] == -1:
		return "miss"
	elif board[x][y] == '*' or board[x][y] == '$':
		return "try again"
	else:
		return "hit"

def user_move(board):
	
	#get coordinates from the user and try to make move
	while(True):
		x,y = get_coor()
		res = make_move(board,x,y)
		if res == "hit":
			print("Találat " + str(x+1) + "," + str(y+1))
			check_sink(board,x,y)
			board[x][y] = '$'
			if check_win(board):
				return "WIN"
		elif res == "miss":
			print("Bocsi " + str(x+1) + "," + str(y+1) + " nem talált.")
			board[x][y] = "*"
		elif res == "try again":
			print("Oda már löttél egyszer próbálj más helyet")

		if res != "try again":
			return board

def computer_move(board):
	
	#generate user coordinates from the user and try to make move
	while(True):
		x = random.randint(1,10)-1
		y = random.randint(1,10)-1
		res = make_move(board,x,y)
		if res == "hit":
			print("Találat " + str(x+1) + "," + str(y+1))
			check_sink(board,x,y)
			board[x][y] = '$'
			if check_win(board):
				return "WIN"
		elif res == "miss":
			print("HÁH, " + str(x+1) + "," + str(y+1) + " nem talált.")
			board[x][y] = "*"

		if res != "try again":
			
			return board
	
def check_sink(board,x,y):

	#figure out what ship was hit
	if board[x][y] == "A":
		ship = "Anyahajó"
	elif board[x][y] == "C":
		ship = "Csatahajó"
	elif board[x][y] == "T":
		ship = "Tengeralattjáró" 
	elif board[x][y] == "V":
		ship = "Vadászhajó"
	elif board[x][y] == "F": 
		ship = "Felderítő"
	
	#mark cell as hit and check if sunk
	board[-1][ship] -= 1
	if board[-1][ship] == 0:
		print(ship + " elsüllyedt")
		
def check_win(board):
	
	#simple for loop to check all
	for i in range(10):
		for j in range(10):
			if board[i][j] != -1 and board[i][j] != '*' and board[i][j] != '$':
				return False
	return True

def main():

	#types of ships
	ships = {"Anyahajó":5,
			 "Csatahajó":4,
 			 "Tengeralattjáró":3,
			 "Vadászhajó":3,
			 "Felderítő":2}

	#setup blank 10x10 board
	board = []
	for i in range(10):
		board_row = []
		for j in range(10):
			board_row.append(-1)
		board.append(board_row)

	#setup user and computer boards
	user_board = copy.deepcopy(board)
	comp_board = copy.deepcopy(board)
	auto_user_board = copy.deepcopy(board)
	
	#add ships as last element in the array
	user_board.append(copy.deepcopy(ships))
	comp_board.append(copy.deepcopy(ships))
	auto_user_board.append(copy.deepcopy(ships))
	
	#ship placement
	user_board = user_place_ships(user_board,ships)
	comp_board = computer_place_ships(comp_board,ships)

	#game main loop
	while(1):

		#user move
		os.system('cls' if os.name == 'nt' else 'clear')
		print_board("c",comp_board)
		comp_board = user_move(comp_board)

		#check if user won
		if comp_board == "WIN":
			print("NYERTÉL! :)")
			quit()
			
		#display current computer board
		print_board("c",comp_board)
		input("Ahoz hogy folytasd nyomj ENTERT")
		os.system('cls' if os.name == 'nt' else 'clear')
		#computer move
		user_board = computer_move(user_board)
		
		#check if computer move
		if user_board == "WIN":
			print("A Számítógép nyert! :(")
			quit()
			
		#display user board
		print_board("u",user_board)
		input("Ahoz hogy folytasd nyomj ENTERT")
		os.system('cls' if os.name == 'nt' else 'clear')
if __name__=="__main__":
	main()
