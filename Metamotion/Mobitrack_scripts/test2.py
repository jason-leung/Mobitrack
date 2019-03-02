import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

mobitrack_status = False

def mobitrack_connect(e):
  global mobitrack_status
  last_mobitrack_status = False
  logging.debug('Connecting to Mobitrack...')
  while(True):
    while(mobitrack_status):
      logging.debug('processStep()')
      time.sleep(0.5)
    if(last_mobitrack_status == True and mobitrack_status == False):
      logging.debug('endSession()')
    last_mobitrack_status = mobitrack_status


def mobitrack_controller(e):
  global mobitrack_status
  logging.debug('Starting Mobitrack controller...')

  while(True):
    user_input = input()
    if(user_input == '0'):
      mobitrack_status = False
      print("Setting Status:", user_input)
    elif(user_input == '1'):
      mobitrack_status = True
      print("Setting Status:", user_input)

e = threading.Event()

t1 = threading.Thread(name='Mobitrack', target=mobitrack_connect, args=(e,))
t2 = threading.Thread(name='Controller', target=mobitrack_controller, args=(e,))


t1.start()
t2.start()
print("Enter Mobitrack Status (0 = off, 1 = on):")
