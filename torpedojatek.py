import copy, random, os, sys
from getpass import getpass
from datetime import datetime
abc = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P')

is_cheating = False
player_count=1

def main_screen():
	clear_console()
	while True:
		print("1.Singleplayer")
		print("2.Player VS Player")
		print("3.Scoreboard")
		menu_option=input(blue("Please type a number between 1-3 to select an option: "))
		if str(menu_option).isnumeric() and int(menu_option)>0 and int(menu_option)<4:
			clear_console()
			return int(menu_option)
		else:
			clear_console()
			as_error("Choose a NUMBER between 1-3")

def green(input):
	return '\033[1;32;32m'+input+'\033[0m'

def as_success(input):
	print(green(input))

def as_error(input):
	print(red(input))

def red(input):
	return '\033[1;30;31m'+input+'\033[0m'

def blue(input):
	return '\033[1;30;34m'+input+'\033[0m'	

def as_info(input):
	print(blue(input))

def clear_console():
	os.system('cls' if os.name == 'nt' else 'clear')

def index_to_human(coordinate):
	x = abc[coordinate[1]]
	y = coordinate[0] + 1
	return x + str(y)

def show_stats(opponent_board):
	total_miss = 0
	total_hit = 0

	for i in range(len(opponent_board) - 1):
		for j in range(len(opponent_board[i])):
			if opponent_board[i][j] == "*":
				total_miss += 1
			elif opponent_board[i][j] == "$":
				total_hit += 1

	as_info("Match ended with {} round(s).".format(total_hit + total_miss))
	as_error("You missed {} times.".format(total_miss))
	as_info("You had {} hit.".format(total_hit))
	return total_hit+total_miss

def print_board(s, board, is_show_ship=False):
	global is_cheating
	dimension = len(board) - 1
	player = "Computer"

	if s != "c":
		player = s	

	print(player + "'s table looks like this: \n")

	row_string = "   "
	for i in range(dimension):
		row_string += "   " + abc[i] + "  "

	print(row_string + '\n')

	for i in range(dimension):
		row_string = str(i + 1).rjust(3) + "  "

		for j in range(dimension):
			if board[i][j] == -1:
				row_string += "   "
			elif board[i][j] == "*":
				row_string +=' ' + blue(board[i][j] + ' ')
			elif board[i][j] == "$":
				row_string +=' ' + red(board[i][j] + ' ')
			elif is_show_ship ==True:
				row_string += " " + board[i][j] + " "
			else:
				row_string += "   "
			
			
			if j != (dimension - 1):
				row_string += green(" | ")
			
		print(row_string)

		if i != (dimension - 1):
			row_string = '    '

			for asd in range(dimension):
				row_string += "------"

			print(green(row_string))
		else:
			print("")

def without_keys(dictionary, keys):
	return {x: dictionary[x] for x in dictionary if x not in keys}

def user_place_ships(board, ships, user_name):
	placed_ships = []
	dimension = len(board) - 1
	
	if len(placed_ships) != len(ships.keys()):
			as_info("Would You like to place your remaining ships randomly? (Y/N) ")
			user_input = input()

			if user_input.lower() == "y":
				clear_console()
				board = automatically_place_ships(board, without_keys(ships, placed_ships), "You")
				print_board(user_name, board,is_show_ship=True)
				input("Press ENTER to continue")
				return board
	
	for ship in ships.keys():
		valid = False

		while not valid:
			clear_console()
			
			print_board(user_name, board,is_show_ship=True)
			as_info("Placing {} (length: {})".format(ship, ships[ship]))
			x, y = get_coordinate(dimension)
			ori = v_or_h()
			valid = validate(board, ships[ship], x, y, ori)


			if not valid:
				as_error("You can't put a ship there.")
				input("Press ENTER to continue")

		clear_console()
		board = place_ship(board, ships[ship], ship[0], ori, x, y)
		placed_ships.append(ship)
		print_board(user_name, board,is_show_ship=True)
		
		
	clear_console()
	as_info("You placed all of your ships.")
	print_board(user_name, board,is_show_ship=True)
	input("Press ENTER to start the game")
	return board

def automatically_place_ships(board, ships, actor = "The Computer"):
	dimension = len(board) - 1
	for ship in ships.keys():
		valid = False

		while not valid:
			x = random.randint(1, dimension) - 1
			y = random.randint(1, dimension) - 1
			o = random.randint(0, 1)

			if o == 0: 
				ori = "v"
			else:
				ori = "h"

			valid = validate(board, ships[ship], x, y, ori)

		print("{} placed a(n) {}.".format(actor, ship))
		board = place_ship(board, ships[ship], ship[0], ori, x, y)

	return board

def place_ship(board, ship, s, ori, x, y):
	if ori == "v":
		for i in range(ship):
			board[x+i][y] = s
	elif ori == "h":
		for i in range(ship):
			board[x][y+i] = s

	return board
	
def validate(board, ship, x, y, ori):
	dimension = len(board) - 1
	if ori == "v" and x+ship > dimension:
		return False
	elif ori == "h" and y+ship > dimension:
		return False
	else:
		if ori == "v":
			for i in range(ship):
				if board[x+i][y] != -1:
					return False
		elif ori == "h":
			for i in range(ship):
				if board[x][y+i] != -1:
					return False

	return True

def v_or_h():
	while True:
		user_input = input("Do you want to place it Verical or Horizontal (V/H) ? ").lower()

		if user_input == "v" or user_input == "h":
			return user_input
		else:
			as_error("Please write 'V' or 'H'")

def get_coordinate(dimension):
	"""Args:
		dimension (int): width and height of the board.

	Returns:
		(tuple): (row_index, column_index)
	"""

	while True:
		coor = input("Give us the coordinates (e.g.: A1): ")

		try:
			if len(coor) < 2:
				raise Exception("It must be a letter and a number!")

			x = abc.index(coor[0].upper())
			y = int(coor[1:]) - 1

			if x < 0 or (dimension - 1) < x:
				raise Exception("Invalid letter '" + coor[0].upper() + "'. Valid: " + abc[0] + "-" + abc[dimension - 1])

			if y < 0 or (dimension - 1) < y:
				raise Exception("Please give a number between 1-" + str(dimension) + "!")

			return (y,x)
		except ValueError:
			as_error("Try again!")
		except Exception as e:
			as_error(str(e))

def make_move(board, x, y):
	if board[x][y] == -1:
		return "miss"
	elif board[x][y] == '*' or board[x][y] == '$':
		return "try again"
	else:
		return "hit"

def user_move(board,user_name):
	dimension = len(board) - 1
	while(True):
		x, y = get_coordinate(dimension)
		res = make_move(board,x,y)

		clear_console()

		if res == "hit":
			as_success("You hit a ship at " + index_to_human((x, y)) + ".")
			check_sink(board, x, y)
			board[x][y] = '$'
		elif res == "miss":
			as_info("Sorry! " + index_to_human((x, y)) + " is a miss.")
			board[x][y] = "*"
		elif res == "try again":
			as_error("You alredy shot there! Try another place!")
			if player_count==2:
				print_board(user_name, board)
			else:
				print_board("c", board)

		if res != "try again":
			return board

def computer_move(board):
	dimension = len(board) - 1
	while True:
		x = random.randint(1, dimension) - 1
		y = random.randint(1, dimension) - 1
		res = make_move(board, x, y)

		if res == "hit":
			as_error("Computer hit your ship at " + index_to_human((x, y)) + "!")
			check_sink(board, x, y)
			board[x][y] = '$'

			if check_win(board):
				return "WIN"
		elif res == "miss":
			as_info("HAH! Computer missed at " + index_to_human((x, y)) + ".")
			board[x][y] = "*"

		if res != "try again":
			return board
	
def check_sink(board, x, y):
	if board[x][y] == "A":
		ship = "Aircraft Carrier"
	elif board[x][y] == "B":
		ship = "Battleship"
	elif board[x][y] == "S":
		ship = "Submarine" 
	elif board[x][y] == "D":
		ship = "Destroyer"
	elif board[x][y] == "P": 
		ship = "Patrol"

	board[-1][ship] -= 1

	if board[-1][ship] == 0:
		as_info(ship + " has sunk.")

def check_win(board):
	last_row_index = len(board) - 1
	ships = board[last_row_index]
	for ship in ships:
		if ships[ship] != 0:
			return False

	return True

def rematch():
	global is_cheating
	is_cheating = False
	print()
	as_info("Would You like to play again (Y/N)? ")
	answer = input().lower()

	if answer == "y":
		main()

def save_score(winning_player,all_rounds):
	with open("score.txt","a") as f:
		f.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" "+winning_player+" "+str(all_rounds)+"\n")

def get_player(user_board, ships):
	player_name=input("Give us your name...")
	user_place_ships(user_board, ships,player_name)
	return player_name

def init_board(dimension):
	board = []
	for i in range(dimension):
		board_row = []

		for j in range(dimension):
			board_row.append(-1)

		board.append(board_row)
	return board

def singleplayer(user_board,user2_board,ships):
	player1_name=get_player(user_board,ships)
	core(player1_name,"Computer",user_board,user2_board,ships)

def multiplayer(user_board,user2_board,ships):
	player1_name=get_player(user_board,ships)
	clear_console()
	player2_name=get_player(user2_board,ships)
	core(player1_name,player2_name,user_board,user2_board,ships)

def show_score_board():
	score_lines=list()
	output=""
	with open("score.txt","r")as f:
		score_lines=f.read().splitlines()
	score_collum_width=[0]*4
	score_collum_width[2]=len("Player name")
	score_collum_width[3]=len("Score")
	for lines in score_lines:
		cells=lines.split(" ")
		for i in range(len(cells)):
			if score_collum_width[i]<len(cells[i]):
				score_collum_width[i]=len(cells[i])
	output+="Date".rjust(score_collum_width[0])
	output+=" | "
	output+="Time".rjust(score_collum_width[1])
	output+=" | "
	output+="Player name".rjust(score_collum_width[2])
	output+=" | "
	output+="Score".rjust(score_collum_width[3])
	output+=" | \n"
	for line in score_lines:
		parts=line.split(" ")
		for i in range(len(parts)):
			output+=parts[i].rjust(score_collum_width[i])
			output+=" | "
		output+="\n"
	print(output)

def get_map_size():
	while True:
		dimension = int(input("How big of a map do you want (between 6-15)? "))

		if dimension < 6 or 15 < dimension:
			as_error('Invalid map size!')
		else:
			return dimension



def main():
	global player_count
	ships = {
		"Aircraft Carrier" : 5,
		"Battleship" : 4,
		"Submarine" : 3,
		"Destroyer" : 3,
		"Patrol" : 2
	}
	
	menu_option=main_screen()

	if menu_option==1:
		player_count=1
		dimension=get_map_size()

		user_board =init_board(dimension)
		user2_board =init_board(dimension)

		user_board.append(copy.deepcopy(ships))
		user2_board.append(copy.deepcopy(ships))
		singleplayer(user_board,user2_board,ships)

	elif menu_option==2:
		player_count=2
		dimension=get_map_size()

		user_board =init_board(dimension)
		user2_board =init_board(dimension)

		user_board.append(copy.deepcopy(ships))
		user2_board.append(copy.deepcopy(ships))
		multiplayer(user_board,user2_board,ships)
	elif menu_option==3:
		show_score_board()
	else:
		as_error("Please choose a NUMBER between 1-3")

def core(player1_name,player2_name,user_board,user2_board,ships):
	global is_cheating
	while True:
		clear_console()
		as_info(""+player1_name+"'s turn")
		
		if player_count ==2:
			print_board(player2_name,user2_board,is_show_ship=False)
		else:
			print_board("c", user2_board, is_show_ship=False)
			
		user2_board = user_move(user2_board,player2_name)
		if check_win(user2_board,):
			as_success(""+player1_name+" WON :)")
			all_rounds=show_stats(user2_board)
			save_score(player1_name,all_rounds)
			rematch()
			break

		if player_count==2:
			print_board(player2_name,user2_board, is_show_ship=False)  
		else:
			print_board("c", user2_board,is_show_ship=False)
		input("Press ENTER to continue")
		clear_console()
		if player_count == 2:
			as_info('Its '+player2_name +' turn!')
			print_board(player1_name,user_board)
			user_board=user_move(user_board,player1_name)
		else:
			user_board = computer_move(user_board)

		if user_board == "WIN":
			all_rounds=show_stats(user2_board)
			if player_count==2:
				save_score(player2_name,all_rounds)
				as_success(""+player2_name +"have won :(")
			else:
				as_error("The Computer have won :(")
			
			rematch()
			break
		if player_count ==2:
			print_board(player1_name, user_board,)
			should_cheat = getpass("Press ENTER to continue")
		else:
			print_board(player1_name, user_board,is_show_ship=True)
			should_cheat = getpass("Press ENTER to continue")
		if should_cheat.lower() == "map":
			is_cheating = True
		elif should_cheat.lower() == "god":
			is_cheating = True
			last_row_index = len(user2_board) - 1
			remaining_hits = 0
			
			for ship in user2_board[last_row_index].keys():
				remaining_hits += ships[ship]

			for x in range(len(user_board)):
				for y in range(len(user2_board[x])):
					result = make_move(user2_board, x, y)

					if result == "hit":
						check_sink(user2_board, x, y)
						user2_board[x][y] = '$'
						remaining_hits -= 1
					
					if remaining_hits == 1:
						break
					
				if remaining_hits == 1:
					break

if __name__=="__main__":
	main()
