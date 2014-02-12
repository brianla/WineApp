from flask import *
import Routes


# LAUNCH SERVER ****************************************************************

if __name__ == '__main__':
    Routes.app.debug = True #REMOVE IN PRODUCTION
    Routes.app.run(host='0.0.0.0', port=9654)
