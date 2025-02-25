from xl_router import Router as Router_
from flask import request
from flask import request
import time
import platform


class Router(Router_):
    def verify_user(self):
        token = request.headers.get('token')
        if token == '999999':
            return True
        else:
            return False
       
