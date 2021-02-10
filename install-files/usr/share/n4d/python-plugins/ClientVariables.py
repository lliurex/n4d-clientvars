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
		
		if not self.core.variable_exists("CLIENT_INTERNAL_INTERFACE")["return"]:
			iface=self.get_internal_interface()
			if iface!=None:
				self.core.set_variable('CLIENT_INTERNAL_INTERFACE',iface,{"info":"Client network interface"})
		
		status=False
		ret=self.update_mnt_variable()
		if ret["status"]==0:
			status=True
		print("\t* Updating MOUNT_SOURCES variable... %s"%status)
		if not status:
			self.core.pprint("ClientVariables",ret["msg"])
	
	#def startup
	
	def get_internal_interface(self):
		
		try:
			context=ssl._create_unverified_context()
			c = xmlrpc.client.ServerProxy('https://server:9779',context=context,allow_none=True)
			ret=c.get_variable("INTERNAL_NETWORK")
			if ret["status"]!=0:
				raise Exception()
			internal_network=ret["return"]
			ret=c.get_variable("INTERNAL_MASK")
			if ret["status"]!=0:
				raise Exception()
			internal_mask=ret["return"]
			network=str(internal_network)+"/"+str(internal_mask)
			
			for dinfo in lliurex.net.get_devices_info():
				if lliurex.net.is_ip_in_range(dinfo["ip"],network):
					return dinfo["name"]
			
		except:
			return None
		
	#def get_internal_interface
	
	def update_mnt_variable(self):
		
		try:

			context=ssl._create_unverified_context()
			c = xmlrpc.client.ServerProxy('https://server:9779',context=context,allow_none=True)

			#WIP 
			ret=c.get_shared_folders("","NetFoldersManager")
			
			if ret["status"]!=0:
				raise Exception()
			
			dic=ret["return"]
			
			#for testing purposes we are connecting to a llx19 server
			#dic=c.get_shared_folders("","NetFoldersManager")
			
			mnt_var={}
			if dic==None:
				mnt_var={}
			else:
				try:
					for item in dic:
						if type(dic[item])==type({}):
							if "dst" not in dic[item] or "fstype" not in dic[item]:
								pass
							else:
								mnt_var[item]=dic[item]
					
				except:
					mnt_var={}
					
			new_dic=mnt_var
			if len(new_dic)>0:
				self.core.set_variable("MOUNT_SOURCES",new_dic)
			else:
				
				try:
					orig=self.core.get_variable("MOUNT_SOURCES")["return"]
					new_dic={}
					
					for item in orig:
						if type(orig[item])==type({}):
							if "dst" not in dic[item] or "fstype" not in dic[item]:
								pass
							else:
								new_dic[item]=orig[item]
					self.core.set_variable("MOUNT_SOURCES",new_dic)
					
				except:
					mnt_var={}
					self.core.set_variable("MOUNT_SOURCES",mnt_var)
					return n4d.responses.build_failed_call_response()
			
			return n4d.responses.build_successful_call_response()
		
		except Exception as e:
			return n4d.responses.build_failed_call_response()
				
				
		
		
	#def update_mnt_variable
	
	
	
#class ClientVariables

if __name__=="__main__":
	
	cv=ClientVariables()
	cv.update_mnt_variable()
