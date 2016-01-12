import socket
import time

class UDP_Server():
   def __init__(self, address="",port=5005,time_out=1.0 ):
       self.address   = address
       self.port      = port
       self.time_out  = time_out
       self.sock      = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET -- UDP Socket
       self.sock.bind(("", port))


   def process_msg( self, msg_handler = None ):
       while True:
           try:
               print "waiting to receive"
               self.sock.settimeout(None)  # wait for indefinite time
               input_msg, address = self.sock.recvfrom(1024) # classic modbus message is limited to 256 bytes
	       print "rx address",address,"data",input
               if input_msg != None:
                   addr = ord(input_msg[0])
                   if msg_handler != None:
                       print "msg_handler",msg_handler
                       output_msg = msg_handler.process_msg( input_msg )
                       print [input_msg, output_msg ]
                   else:
                       output_msg = input_msg
                   if output_msg != None:
                      self.sock.settimeout( self.time_out )
                      number_sent = self.sock.sendto(output_msg,address)
                      print "sent byte",number_sent
           except Exception as inst:
               print type(inst)     # the exception instance
               print inst.args      # arguments stored in .args
               print inst           # __str__ allows args to be printed directly
               time.sleep(1)        # allow for control c




if __name__ == "__main__":
  import json
  import modbus_redis_mgr
  import rs485_mgr   
  import modbus_serial_ctrl
  import msg_manager

  msg_mgr         = msg_manager.MessageManager()
  redis_handler   =  modbus_redis_mgr.ModbusRedisServer(msg_mgr)

  rs485_interface_1 = rs485_mgr.RS485_Mgr()
  rs485_interface_2 = rs485_mgr.RS485_Mgr()

  serial_interfaces = {}
  serial_interfaces[ "rtu_1" ] = { "handler":rs485_interface_1,"interface_parameters":{ "interface":None, "timeout":.15, "baud_rate":38400 } ,"search_device":"current_monitor" } 
  serial_interfaces[ "rtu_2" ] = { "handler":rs485_interface_2,"interface_parameters":{ "interface":None, "timeout":.15, "baud_rate":38400 } ,"search_device":"main_controller" } 

  remote_devices = {}
  remote_devices["current_monitor"] = { "interface": "rtu_1", "parameters":{ "address":31 , "search_register":0} }
  remote_devices["main_controller"] = { "interface": "rtu_2", "parameters":{ "address":100 , "search_register":0} }
  remote_devices["remote_1"]        = { "interface": "rtu_2", "parameters":{ "address":125 , "search_register":0} }
  remote_devices["remote_2"]        = { "interface": "rtu_2", "parameters":{ "address":170 , "search_register":0} }

  modbus_serial_ctrl                = modbus_serial_ctrl.ModbusSerialCtrl( serial_interfaces,remote_devices,msg_mgr)

  msg_mgr.add_device( 255, redis_handler)
  msg_mgr.add_device( 31, modbus_serial_ctrl )
  msg_mgr.add_device( 100, modbus_serial_ctrl )
  msg_mgr.add_device( 125, modbus_serial_ctrl )
  msg_mgr.add_device( 170, modbus_serial_ctrl )

  #print msg_mgr.ping_device( 31 )
  #print msg_mgr.ping_device( 100 )
  #print msg_mgr.ping_all_devices()

  udp_server = UDP_Server()
  udp_server.process_msg(msg_mgr)


