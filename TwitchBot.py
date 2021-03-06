import socket, re, os
import Commands
from credentials import *
from colorama import Back,Fore,init,Style

s = socket.socket()
s.connect(("irc.chat.twitch.tv", 6667))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN #{}\r\n".format(CHAN).encode("utf-8"))

prefix = "$"

connected = False
run = True

def sendMessage(message):
    s.send("PRIVMSG #{} :{}\r\n".format(CHAN, message).encode("utf-8"))
if not os.path.exists('data'):
    os.mkdir('data')
if not os.path.exists('data/' + CHAN):
    os.mkdir('data/' + CHAN)

while run:
    response = s.recv(2048).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0)
        message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        message = message.sub("", response).rstrip('\n')

        if 'End of /NAMES list' in message:
            connected = True
            print('Joined #' + CHAN)

        if connected:
            if 'End of /NAMES list' in message:
                pass
            else:
                if not os.path.exists('data/' + CHAN + '/' + username.title()):
                        os.mkdir('data/' + CHAN + '/' + username.title())
                        __ = open('data/' + CHAN + '/' + username.title() + '/.points', 'w+')
                        __.write('1000')
                        __.close()
                if message[0] != prefix:
                    print("< " + username.title() + ':', message) # Standard
                else:
                    message = message.replace(prefix, "")
                    message = message.strip()
                    print("< " + Fore.YELLOW + username.title() + ':', prefix + message) # Command
                    response = Commands.handleCommands(username, message)
                    if response != None:
                        print("> " + Fore.GREEN + response)
                        sendMessage(response)