import copy, random, os, sys
from getpass import getpass

abc = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P')

is_cheating = False

player_count=1

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

def print_board(s, board):
	global is_cheating
	dimension = len(board) - 1
	player = "Computer"

	if s != "c":
		player = s	

	print("The " + player + "'s table looks like this: \n")

	row_string = "   "
	for i in range(dimension):
		row_string += "   " + abc[i] + "  "

	print(row_string + '\n')

	for i in range(dimension):
		row_string = str(i + 1).rjust(3) + "  "

		for j in range(dimension):
			if board[i][j] == -1:
				row_string += "   "
			elif s == "u" or s== "u2":
				if board[i][j] == "*":
					row_string +=' ' + blue(board[i][j] + ' ')
				elif board[i][j] == "$":
					row_string +=' ' + red(board[i][j] + ' ')
				else:
					row_string += " " + board[i][j] + " "
			elif s == "c":
				if board[i][j] == "*":
					row_string += ' '+ blue(board[i][j]+' ')
				elif board[i][j] == "$":
					row_string += ' '+ red(board[i][j]+' ')
				elif is_cheating == True and board[i][j] != "   ":
					row_string += ' '+ red(board[i][j]+' ')
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
				print_board('u', board)
				input("Press ENTER to continue")
				return board
	
	for ship in ships.keys():
		valid = False

		while not valid:
			clear_console()
			
			print_board(user_name, board)
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
		print_board("u", board)
		
		
	clear_console()
	as_info("You placed all of your ships.")
	print_board("u", board)
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

def user_move(board):
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

def main():
	global is_cheating
	global player_count
	ships = {
		"Aircraft Carrier" : 5,
		"Battleship" : 4,
		"Submarine" : 3,
		"Destroyer" : 3,
		"Patrol" : 2
	}

	dimension = 0
	clear_console()
	
	player_count = input('Do You want to play against an another player (Y/N)? ').upper()
	if player_count == "Y":
		player_count=2
		
	else:
		player_count=1	
	while True:
		dimension = 10 #int(input("How big of a map do you want (between 6-15)? "))

		if dimension < 6 or 15 < dimension:
			as_error('Invalid map size!')
		else:
			break

	board = []
	for i in range(dimension):
		board_row = []

		for j in range(dimension):
			board_row.append(-1)

		board.append(board_row)

	user_board = copy.deepcopy(board)
	user2_board = copy.deepcopy(board)

	user_board.append(copy.deepcopy(ships))
	user2_board.append(copy.deepcopy(ships))

	user_board = user_place_ships(user_board, ships,"User")

	

	if player_count == 2:
		as_info("User 2 is placing the ships now.")
		user2_board = user_place_ships(user2_board, ships, "User 2")
		
	else:
		user2_board = automatically_place_ships(user2_board, ships)

	while True:
		clear_console()
		as_info('Your turn!')
		print_board("c", user2_board)
		
			
			
		user2_board = user_move(user2_board)
		if check_win(user2_board):
			as_success("YOU WON :)")
			show_stats(user2_board)
			rematch()
			break

		print_board("c", user2_board)
		input("Press ENTER to continue")
		clear_console()
		if player_count == 2:
			as_info('Its User 2 turn!')
			print_board("u2",user2_board)
		
		else:
			user_board = computer_move(user_board)

		if user_board == "WIN":
			as_error("The Computer have won :(")
			show_stats(user2_board)
			rematch()
			break

		print_board("u", user_board)
		should_cheat = getpass("Press ENTER to continue")

		if should_cheat.lower() == "map":
			is_cheating = True
		elif should_cheat.lower() == "god":
			is_cheating = True
			last_row_index = len(user2_board) - 1
			remaining_hits = 0
			
			for ship in user2_board[last_row_index].keys():
				remaining_hits += ships[ship]

			for x in range(len(board)):
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
