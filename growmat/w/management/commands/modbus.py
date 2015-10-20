from django.core.management.base import BaseCommand, CommandError
from w.models import Instrument, Rule
import time

import datetime
import time
from time import gmtime, strftime
import sys

#import subprocess
from django.utils import timezone

import minimalmodbus
#print minimalmodbus.__file__

station = minimalmodbus.Instrument('/dev/ttyAMA0', 1) # port name, slave address (in decimal)

print station.serial.port          # this is the serial port name
#station.debug = True
station.serial.baudrate = 9600   # Baud
station.serial.bytesize = 8
#station.serial.parity   = serial.PARITY_NONE
station.serial.stopbits = 2
station.serial.timeout  = 0.05   # seconds

#instrument2 = minimalmodbus.Instrument('/dev/ttyAMA0', 2) # port name, slave address (in decimal)
#print instrument2.serial.port          # this is the serial port name
#instrument2.debug = True
#instrument2.serial.baudrate = 9600   # Baud
#instrument2.serial.bytesize = 8
#instrument2.serial.parity   = serial.PARITY_NONE
#instrument2.serial.stopbits = 2
#instrument2.serial.timeout  = 0.05   # seconds

#HUMI0 = 0
#HIND0 = 0
#subprocess.Popen(["python", "archive.py"])

def modbus_read(instrument, s):
        #dinstrument = Instrument.objects.get(pk=9)
		#instrument.address, instrument.type + instrument.index)
                
        #instrument.datetime = datetime.datetime.now()
        #print dinstrument.data_datetime
        #dinstrument.insrument_name = 'kuchyn'
        #print dinstrument.insrument_name
        #dinstrument.save()
        try:
            
            #print datetime.datetime.now()
            #print 'ctu'
            #TEMP0 = station.read_register(1, 0) # Registernumber, number of decimals
            #print 'temperature [C]: ' + str(TEMP0 )
            #print 'do db'			
            #dinstrument.data_value = int(TEMP0)
            #print 
            instrument.status = instrument.status & ~Instrument.NT
            
            station.address = instrument.address
            #print station.address
            value = station.read_register(instrument.type + instrument.index, 0)
            if value == 0:#sys.maxint:
                instrument.status = instrument.status | Instrument.IV
                
            else:   
                instrument.status = instrument.status & ~Instrument.IV         
                #instrument.value = value / 1000 #minimalmodbus._bytestringToFloat(registerstring)
                instrument.value = float(value) * 0.001
            
            instrument.datetime = timezone.now()
            
            
            instrument.save()
        except:
            instrument.datetime = timezone.now()
            instrument.status = instrument.status | Instrument.NT
            instrument.save()
            #print 'sensor n/a'
            s.stdout.write('sensor does not response, address {}'.format(instrument.address))
        #instrument.save()
    
    
    

class Command(BaseCommand):

    help = 'Does some magical work'

    def handle(self, *args, **options):
        """ Do your work here """
        
        while 1:
            
            
            instruments = Instrument.objects.order_by('pk')
            #self.stdout.write('There are {} things!'.format(instruments.count()))
            #print "->"
            for instrument in instruments:
                #print "-->"
                #self.stdout.write('reading address {}'.format(instrument.address))
                #self.stdout.write('reading index {}'.format(instrument.type + instrument.index))
                if instrument.address > 0:
                    modbus_read(instrument,self)
                    self.stdout.write('status {}'.format(instrument.status))
                if instrument.address == 0:
                    if instrument.index == 0:
                        #instrument.value = int(time.time())
                        instrument.value = int(strftime("1%H%M%S", gmtime()))
                        instrument.save()
            
            
            
            
            rules = Rule.objects.order_by('pk')
            for rule in rules:
                input_value = Instrument.objects.get(pk=rule.input.pk).value
                operation = rule.operation
                input_parameter = rule.input_parameter
                #calculation = 'if ' + input_value + ' ' + operation + ' ' + parametr + ' : True' 
                #calculation = "if {0} {1} {2}: True".format(input_value, operation, parameter)
                #print calculation
                
                if operation == '==':
                    if input_value == input_parameter:
                        rule.result = True
                    else:
                        rule.result = False
                if operation == '!=':
                    if input_value != input_parameter:
                        rule.result = True
                    else:
                        rule.result = False
                if operation == '>':
                    if input_value > input_parameter:
                        rule.result = True
                    else:
                        rule.result = False
                if operation == '<':
                    if input_value < input_parameter:
                        rule.result = True
                    else:
                        rule.result = False
                
                
                #rule.result = eval(calculation)
                if rule.result != rule.result0:
                    rule.result0 = rule.result
                    rule.datetime = timezone.now()
                    rule.save()
                #print input_value
                #print parameter
                #print rule.result
                #rule.save()
            time.sleep(5)