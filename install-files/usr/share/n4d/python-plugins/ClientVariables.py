import xmlrpc.client
import ssl

import lliurex.net

import n4d.server.core
import n4d.responses


class ClientVariables:
	
	def __init__(self):
		
		self.core=n4d.server.core.Core.get_core()
		
	#def init
	
	def n4d_cron(self,minutes):
		
		if minutes%2==0:
			try:
				self.startup(None)
			except Exception as e:
				print(e)
		
	#def n4d_cron
	
	def startup(self,options):

		if not self.core.variable_exists("REMOTE_VARIABLES_SERVER")["return"]:
			self.core.set_variable("REMOTE_VARIABLES_SERVER","server",{"info":"N4d Remote server"})
			
		if self.core.get_variable("REMOTE_VARIABLES_SERVER")==None:
			self.core.set_variable("REMOTE_VARIABLES_SERVER","server",{"info":"N4d Remote server"})
		
		self.core.pprint("ClientVariables",True)
	
	#def startup
	
#class ClientVariables

if __name__=="__main__":
	
	cv=ClientVariables()
