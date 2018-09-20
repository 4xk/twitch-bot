import requests
from credentials import *
from colorama import Back,Fore,init,Style
import random
init(autoreset = True, convert = True)
def handleCommands(username, msg):
	commands = {
		"ping"		:ping,
		"uptime"	:uptime,
		"roulette"	:roulette,
		"hug"		:hug,
		"thanks"	:thanks,
		"thank"		:thanks,
		"points"    :points
	}
	cmd = msg.split()[0]
	if cmd in commands:
		response = commands[cmd](username, msg)
		return response

	else:
		return None

def ping(username, msg):
	message = "pong! @" + username
	return message

def uptime(username, msg):
	url = 'https://v1.decapi.me/twitch/uptime/?channel=' + CHAN
	r = requests.get(url)
	message = r.text + " @" + username
	return message

def roulette(username, msg):
	try:
		current_points = 0
		f = open('data/' + CHAN + '/' + username.title() + '/.points', 'r')
		bidding = int(msg.split()[1])
		try:
			current_points = int(f.read())
			f.seek(0)
		except ValueError:
			return "Something went wrong internally. debug=" + int(f.read())
		f.close()
		if current_points <= 0:
			return "Not enough points @" + username
		won = random.choice([False,False,True])
		if won:
			current_points += (bidding)
			message = 'You won %s points! You now have %s points. @%s' % (bidding, current_points, username)
		else:
			current_points -= bidding
			message = 'You lost %s points! You now have %s points. :( @%s' % (bidding, current_points, username)
		open('data/' + CHAN + '/' + username.title() + '/.points', 'w').close()
		f = open('data/' + CHAN + '/' + username.title() + '/.points', 'w')
		f.write(str(current_points))
		f.close()
		return message
	except IndexError:
   		return "You need to specify how many points to bid! @" + username
	except ValueError:
   		return "Yeah, thats not a number @" + username

def hug(username, msg):
	try:
   		user_to_hug = msg.split()[1]
   		response = username + "  hugged " + user_to_hug
   		return response
	except IndexError:
   		return "You need to specify who you want to hug! @" + username
def thanks(username, msg):
	try:
   		user_to_thank = msg.split()[1]
   		response = username + "  thanked " + user_to_thank
   		return response
	except IndexError:
   		return "You need to specify who you want to thank! @" + username
def points(username, msg):
	return open('data/' + CHAN + '/' + username.title() + '/.points', 'r').read() + ' @' + username