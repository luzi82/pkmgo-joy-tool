import os.path, sys
import json
import logging

def add_argument(parser):
    parser.add_argument("-c", "--config", help="Config file", required=False)
    parser.add_argument("-i", "--account", help="Account", required=False)
    parser.add_argument("-a", "--auth", help="Auth Service", required=False)
    parser.add_argument("-u", "--username", help="Username", required=False)
    parser.add_argument("-p", "--password", help="Password", required=False)

def get_auth(args):
    ret={
        "config":None,
        "account":None,
        "auth":None,
        "username":None,
        "password":None,
    }

    ret['config'] = args.config if (args.config != None) else \
        'config.json' if (os.path.isfile('config.json')) else \
        None
    
    if ret['config'] != None:
        if not os.path.isfile(ret['config']):
            logging.error('Config file not exist')
            sys.exit(-1)
        with open(ret['config']) as config_file:
            config_dict = json.load(config_file)
        ret['account'] = args.account if (args.account != None) else \
            config_dict['account_default'] if ('account_default' in config_dict) else \
            None
        if ret['account'] != None:
            if 'account_dict' not in config_dict:
                logging.error('account_dict not exist')
                sys.exit(-1)
            if ret['account'] not in config_dict['account_dict']:
                logging.error('account not exist')
                sys.exit(-1)
            account = config_dict['account_dict'][ret['account']]
            if 'auth' in account:
                ret['auth'] = account['auth']
            if 'username' in account:
                ret['username'] = account['username']
            if 'password' in account:
                ret['password'] = account['password']

    if args.auth != None:
        ret['auth'] = args.auth
    if args.username != None:
        ret['username'] = args.username
    if args.password != None:
        ret['password'] = args.password

    # Check service
    if ret['auth'] not in ['ptc', 'google']:
        logging.error('Invalid auth service {}'.format(ret['auth']))
        sys.exit(-1)

    # Check password
    if ret['password'] == None:
        logging.error('No password')
        sys.exit(-1)

    return ret
