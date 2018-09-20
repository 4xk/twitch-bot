import requests
from credentials import *
from colorama import Back,Fore,Init,Style
init(autoreset = true, convert = true)
def handleCommands(username, msg):
	commands = {
		"ping"		:ping,
		"uptime"	:uptime,
		"roulette"	:roulette,
		"hug"		:hug,
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
		bidding = int(msg.split()[1])
		message = str(bidding)
		return message
	except IndexError:
   		return "You need to specify how many points to bid! @" + username
	except ValueError:
   		return "Yeah, thats not a number @" + username

def hug(username, msg):
	try:
   		user_to_hug = msg.split()[1]
   		response = username + "  hugged @" + user_to_hug
   		print('hugged' + user_to_hug)
   		return response
	except IndexError:
   		return "You need to specify who you want to hug! @" + username
   