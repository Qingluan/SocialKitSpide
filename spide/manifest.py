import sys
import os
import argparse

# load functional lib 
from Qtornado.qtornado import TreeFile
from Qtornado.log import LogControl
from Qtornado.db_manifest import DbManifest
from Qtornado.lib import ParseExtendsArgues

try:
    from model import tables
    from setting import db_connect_cmd
except ImportError as e:
    pass


LogControl.LOG_LEVEL |= LogControl.INFO
LogControl.LOG_LEVEL |= LogControl.OK

root_path = os.path.dirname(__file__)

def handle_args():
    desc = """
this is a assistant for write web html
weite by Qingluan
github : http://github.com/Qingluan
    """
    parser = argparse.ArgumentParser(usage='it is usage for qingluanTornado ', description=desc)
    parser.add_argument('-u','--unintall',action="store_true",default=False,help="uninstall this project")
    parser.add_argument('-c','--add-controller',default=None)
    parser.add_argument('-t','--theme-choice',default=None)
    parser.add_argument('--db-update', action='store_true', default=False, help='change db structure for model.py, not work in Mongo db')
    parser.add_argument('--db-create', action='store_true', default=False, help='create sql table from model.py, not work in Mongo db')
    parser.add_argument('--db-drop', default='', help='drop a sql table, not work in Mongo db')
    parser.add_argument('--websocket',action="store_true", default=False, help="websocket mode")
    parser.add_argument('-e','--extends',default=None,help="this will create a new html by extends another template ")
    parser.add_argument('-a','--args',default='',help="this is a extends arguments to control something, @example: -a 'left:1,content:2' ")
    # args,remind = parser.parse_known_args(args)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = handle_args()

    workpath =  os.path.dirname(__file__) #  
    tree = TreeFile(workpath)
    extend_args = ParseExtendsArgues(args.args)

    if args.db_create:
        db = DbManifest(db_connect_cmd, tables)
        db.db_created()
        sys.exit(0)

    if args.db_update:
        db = DbManifest(db_connect_cmd, tables)

    if args.unintall:
        os.popen("rm -rf ./*")

    if args.add_controller:
        if args.extends and args.theme_choice:
            tree.add_controller(
                args.add_controller, 
                extends=args.extends, 
                websocket=args.websocket,
                theme=args.theme_choice,
                **extend_args.args
                )
        
        elif args.extends:
            tree.add_controller(
                args.add_controller, 
                extends=args.extends, 
                websocket=args.websocket,
                **extend_args.args
                )

        elif args.theme_choice:
            tree.add_controller(
                args.add_controller, 
                theme=args.theme_choice, 
                websocket=args.websocket,
                **extend_args.args
                )
        elif not args.add_controller:
            LogControl.err("None args err")
        else:
            tree.add_controller(
                args.add_controller, 
                websocket=args.websocket,
                theme=args.theme_choice,
                extends=args.extends,
                **extend_args.args
                )

