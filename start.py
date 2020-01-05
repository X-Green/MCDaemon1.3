# -*- coding: utf-8 -*-

import __future__
from configparser import ConfigParser
from utils import *
import time
import importlib
import os
import sys
import threading
import traceback

config = None
logger = None
server = None
plugins = []
events_manager = EventManager.EventManager()

if __name__ == '__main__':
    print('Hello world.')


def init():
    global config, logger, server
    config = get_config('config.ini')
    logger = MCDLogger.get_logger(config['Paths']['Logs'])
    startpath = config['Paths']['Logs']
    events_manager.register_event_listener('onRawInfoGet', InfoManager.parse_raw_info)
    server = ServerManager.Server(startpath)

    while True:
        try:
            tick()
        except (SystemExit, IOError, KeyboardInterrupt):
            log('server stopped', 30)
            terminate()
        except Exception:
            log('error ticking MCD', 40)
            log(traceback.format_exc(), 50)
            server.stop()
            sys.exit(0)


def terminate():
    pass


def get_config(cfg_path: str):
    l_config = ConfigParser()
    l_config.read(cfg_path, encoding='utf-8')
    return l_config


def assemble_plugins():
    plugins.clear()

    plugin_path = config['Paths']['Plugins']
    if not os.path.exists(plugin_path):
        plugin_path = 'plugins/'

    plugin_files = os.listdir(plugin_path)

    for pl_filename in plugin_files:
        pl_filepath = plugin_path + pl_filename

        if os.path.isfile(pl_filepath) and pl_filepath.endswith('.py'):
            single_plugin_module = importlib.import_module(pl_filepath)

            plugin_name = getattr(single_plugin_module, 'plugin_name', pl_filename[:-3])
            plugins.append(plugin_name)

            if hasattr(single_plugin_module, 'on_initialized'):
                t = threading.Thread(single_plugin_module.on_initialized)
                t.setDaemon(True)
            else:
                log("plugin '%s' wasn't initialized" % plugin_name, 30)


def tick():
    receive = InfoManager.recv(server)
    if receive != '':
        print('-> ' + receive)

        time.sleep(0.1)


def log(contents, state=20):
    MCDLogger.log(logger, state, contents)
    # states: DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
