#!/usr/bin/env python
#
#

from helper.o365_subs import *
import json


def main():
   # Provided information/arguments
   # dir_id = Directory ID
   # app_id = Application ID

   dir_id = ''
   app_id = ''

   # Function call, created on variable o365call
   # Initial function executes login
   o365call = o365_subs(dir_id,app_id) 

   # API call: current subscriptions status
   status = o365call.subs_stats()
   print('\nCurrent subscriptions status:')
   print json.dumps(status,indent=2)

   # API call: toggle all subscriptions on
   print('\nToggling on all subscriptions\n')
   o365call.subs_on(status)

   # API call: new subscriptions status
   status = o365call.subs_stats()
   print('New subscriptions status:')
   print json.dumps(status,indent=2)

if __name__ == '__main__':
   main()
