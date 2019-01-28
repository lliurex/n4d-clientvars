import xmlrpclib



class ClientVariables:
	
	def __init__(self):
		
		pass
		
	#def init
	
	def n4d_cron(self,minutes):
		
		if minutes%2==0:
			try:
				self.startup(None)
			except Exception as e:
				print e
		
	#def n4d_cron
	
	def startup(self,options):


		if objects['VariablesManager'].get_variable('REMOTE_VARIABLES_SERVER') is None:
			objects['VariablesManager'].init_variable('REMOTE_VARIABLES_SERVER')
			
		if objects['VariablesManager'].get_variable('CLIENT_INTERNAL_INTERFACE') is None:
			print objects['VariablesManager'].init_variable('CLIENT_INTERNAL_INTERFACE')
	
		print("\t* Updating MOUNT_SOURCES variable... " + str(self.update_mnt_variable()[0]))


		
	#def startup
	
	def update_mnt_variable(self):
		
		try:

			c=xmlrpclib.ServerProxy("https://server:9779")
			#HACK FOR TESTING
			#c=xmlrpclib.ServerProxy("https://localhost:9779")
			
			dic=c.get_shared_folders("","NetFoldersManager")

			'''
			try:
				orig=objects["VariablesManager"].get_variable("MOUNT_SOURCES")
			except Exception as e:
				#hack for testingi
				print e
				#orig=c.get_variable("","VariablesManager","MOUNT_SOURCES")
				return [False,str(e)]
			'''
			mnt_var={}
			if dic==None:
				mnt_var={}
			else:
				try:
					for item in dic:
						if type(dic[item])==type({}):
							if not dic[item].has_key("dst") or not dic[item].has_key("fstype"):
								pass
							else:
								mnt_var[item]=dic[item]
					
				except:
					mnt_var={}
					

			#new_dic=dict(dic.items()+mnt_var.items())
			
			new_dic=mnt_var
			
			if len(new_dic)>0:
			
				if not objects["VariablesManager"].set_variable("MOUNT_SOURCES",new_dic)[0]:
					objects["VariablesManager"].add_variable("MOUNT_SOURCES",new_dic,None,"N4D mount variable",["ClientVariables"])
			
			else:
				
				try:
					orig=objects["VariablesManager"].get_variable("MOUNT_SOURCES")
					new_dic={}
					
					for item in orig:
						if type(orig[item])==type({}):
							if not orig[item].has_key("dst") or not orig[item].has_key("fstype"):
								pass
							else:
								new_dic[item]=orig[item]
					
					
					
					
					objects["VariablesManager"].set_variable("MOUNT_SOURCES",new_dic)[0]
					
					
				except:
					mnt_var={}
					objects["VariablesManager"].set_variable("MOUNT_SOURCES",mnt_var)[0]
					
					return[False,str(e)]
				
				
				
			
			return [True,""]
		
		except Exception as e:
			print e
			return [False,str(e)]
				
				
		
		
	#def update_mnt_variable
	
	
	
#class ClientVariables

if __name__=="__main__":
	
	cv=ClientVariables()
	cv.update_mnt_variable()
