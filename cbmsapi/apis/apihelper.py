import os
import json
import sys
import traceback

from django.apps import apps
from django.db import connection
from django.contrib.auth import get_user_model
User = get_user_model()

# from ...utils.logger import myLogger
# from hudson import settings

"""
  API Helper Class
"""

class ApiHelper():

    def run_query(self, sql_filename=None, params=None):
        """
        Run query from a given sql file using the given parameters
        """
        with open(sql_filename, "r") as sql_file:
            sql = sql_file.read()
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            desc = cursor.description 
            data =  [
                dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall() 
            ]
        return data
        
    def get_unique_dict(self, obj, data):
        """
        Get a sict of <field_name>: <field_value>
        Fields of the given object with a unique constraint
        and supplied data
        """
        unique_dict = {}
        unique_fields = self.get_unique_fields(obj)
        if not set(unique_fields) <= set(data.keys()):
            raise Exception("Required fields missing: %s", str(unique_fields))
        for field in unique_fields:
            if data[field] is not None:
                unique_dict[field] = data[field]
        return unique_dict
