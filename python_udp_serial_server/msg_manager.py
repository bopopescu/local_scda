



class MessageManager():
   def __init__(self ):
       self.dict     = {}
       self.counters = {}
    
   def get_counters( self ):
        return self.counters
  
   def clear_all_counters( self ):
       for i in self.counters.keys():
            self.counters[i]["counts"] = 0
            self.counters[i]["failures"] = 0
            self.counters[i]["total_failures"] = 0

   def clear_counter( self, address ):
       if self.counters.has_key( address ) :
            self.counters[address]["counts"]         = 0
            self.counters[address]["failures"]       = 0
            self.counters[address]["total_failures"] = 0

   def add_device( self, address, handler ):
       self.counters[address]  = {}
       self.counters[address]["counts"]         = 0
       self.counters[address]["failures"]       = 0
       self.counters[address]["total_failures"] = 0
       self.dict[address] = handler      

   
   def process_msg( self, msg ): 
       #try:
         address = ord(msg[0])      
         if self.dict.has_key(address) :
             response = self.dict[ address].process_msg( address, msg, self.counters[address] )
             if len(response) == 0 :
                return ""
             return response
       #except:
        #   return ""
          
   def ping_devices( self,address):
       print "ping devices"
       return_value = []
       for address in address:      
          if self.dict.has_key(address) :
           return_value.append({ "address":address,  "result":self.dict[ address].ping_device( address ) } )
       return return_value
     
   def ping_all_devices( self ):
       print "ping all devices"
       result = []
       for address in self.dict.keys():
          if hasattr(self.dict[address], 'ping_device'):
               temp = {}
               temp["address"] = address
               temp["result"]  = self.dict[address].ping_device( address )
               result.append( temp )
       print "result",result
       return result


if __name__ == "__main__":
  import json
  import modbus_redis_mgr
  import rs485_mgr   
  import modbus_serial_ctrl

  msg_mgr = MessageManager()
  handler =  modbus_redis_mgr.ModbusRedisServer(msg_mgr)
  msg_mgr.add_device( 255, handler)
  msg_list = []
  msg_list.append([chr(255),chr(254)])
  msg_list[0] = "".join(msg_list[0])
  msg_list.append( json.dumps( [ "test_1","test_2" ]))
  msg_list.append("dc")
  msg_string = "".join(msg_list)
  return_string = msg_mgr.process_msg(msg_string)
  print "return string",return_string[2:-2]
  rs485_interface_1 = rs485_mgr.RS485_Mgr()
  rs485_interface_2 = rs485_mgr.RS485_Mgr()
  serial_interfaces = {}
  serial_interfaces[ "rtu_1" ] = { "handler":rs485_interface_1,"interface_parameters":{ "interface":None, "timeout":.15, "baud_rate":38400 } ,"search_device":"current_monitor" } 
  serial_interfaces[ "rtu_2" ] = { "handler":rs485_interface_2,"interface_parameters":{ "interface":None, "timeout":.15, "baud_rate":38400 } ,"search_device":"main_controller" } 
  remote_devices = {}
  remote_devices["current_monitor"] = { "interface": "rtu_1", "parameters":{ "address":31 , "search_register":0} }
  remote_devices["main_controller"] = { "interface": "rtu_2", "parameters":{ "address":100 , "search_register":0} }
  modbus_serial_ctrl = modbus_serial_ctrl.ModbusSerialCtrl( serial_interfaces,remote_devices,msg_mgr)
  
  msg_mgr.add_device( 31, modbus_serial_ctrl )
  msg_mgr.add_device( 100, modbus_serial_ctrl )
  print msg_mgr.ping_device( 31 )
  print msg_mgr.ping_device( 100 )
  print msg_mgr.ping_all_devices()
