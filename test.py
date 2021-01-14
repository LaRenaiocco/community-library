"""Back End Tests"""
#run code in terminal: 
# python3 -m unittest test.py 

from unittest import TestCase
from flask import session
from model import connect_to_db, db, example_data
from server import app
import helper
import crud
import api

if __name__ == '__main__':
    unittest.main()