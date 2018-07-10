#!/usr/bin/env python

__author__ = 'pabloquiroga'
author_email = 'pablo.quiroga@ecstech.com'

import json
import requests
import sys
import getpass

class o365_subs(object):

   def __init__(self,dir_id,app_id):
      """
         Initial common variables set
         app_id => Application ID
         headers => REST API added headers
         resource_url => URL to be managed
         login_url => token gathering URL
         base_url => subscriptions API URL
      """
      self.app_id = app_id
      self.headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
      self.resource_url = 'https://manage.office.com'
      self.login_url = 'https://login.microsoftonline.com/{}/oauth2/token'.format(dir_id)
      self.base_url = self.resource_url + '/api/v1.0/{}/activity/feed/subscriptions'.format(dir_id)

      # Login call
      self.login()

   def login(self):

      # Secret key input request
      s_key = getpass.unix_getpass("Enter the Secret Key to interact with Office365: ")
      s_key = s_key.replace('+', '%2B')

      # data entry for REST API call
      data = ('grant_type=client_credentials&client_id={}'
              '&client_secret={}&resource={}'.format(self.app_id,s_key,self.resource_url))

      # Token gathering
      r = requests.post(self.login_url, headers=self.headers, data=data)
      try:
         self.headers.update({'Authorization': 'Bearer '+r.json()['access_token']})
      except:
         print('Authentication Failed')
         sys.exit(1)

   def subs_stats(self):

      # Setting up default subscriptions status
      subs_stats_dict = {
                        'Audit.Exchange' : 'disabled',
                        'Audit.General' : 'disabled',
                        'Audit.AzureActiveDirectory' : 'disabled',
                        'DLP.All' : 'disabled',
                        'Audit.SharePoint' : 'disabled'
                        }

      # Gather subscriptions status
      subs_stats = requests.get(self.base_url+'/list', headers=self.headers).json()

      # List parsing and dictionary creation
      for content in subs_stats:
         subs_stats_dict.update({content['contentType']:content['status']})
      return subs_stats_dict

   def subs_on(self,subs):

      # Subscription status toggle on
      for content in subs:
         requests.post(self.base_url+'/start?contentType={}'.format(content), headers=self.headers)
