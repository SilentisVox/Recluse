from core.CommandHandler                import CommandHandler
from core.Generator                     import Generator
from core.NetworkListener               import NetworkListener
from core.StagerListener                import StagerListener
from core.ConnectionHandler             import ConnectionHandler
from core.Settings                      import Settings

import core.TextAssets

def main():
	print(core.TextAssets.banner())

	generator                           = Generator
	networklistener                     = NetworkListener
	stagerlistener                      = StagerListener
	connectionhandler                   = ConnectionHandler
	settings                            = Settings

	commandhandler                      = CommandHandler(
		generator, 
		networklistener, 
		stagerlistener,
		connectionhandler,
		settings
	)

	while True:
		try:
			user_input                  = input(core.TextAssets.prompt)
			commandhandler.read_input(user_input)

		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	main()