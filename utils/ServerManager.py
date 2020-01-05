# -*- coding: utf-8 -*-

import __future__
import re
import utils.MCDLogger


class Server:
    def __init__(self, logger, startpath='start.sh'):
        self._handler = ServerHandler(startpath)
        self.logger = logger

    def execute(self, data, tail='\n'):  # puts a command in STDIN with \n to execute
        self._handler.send_msg(data + tail)

    def recv(self):
        pass

    def _cmd_stop(self):  # stop the server using command
        self._handler.send_msg('stop\n')

    def _force_stop(self):  # stop the server using pclose, donnt use it until necessary
        try:
            self._handler.process.kill()
        except Exception:
            raise RuntimeError

        del self

    def stop(self):
        self._cmd_stop()
        try:

            self._force_stop()
            self.logger('forced server to stop')
        except Exception:
            pass

    def say(self, data):
        self.execute('tellraw @a {"text":"' + str(data) + '"}')

    def tell(self, player, data):
        self.execute('tellraw ' + player + ' {"text":"' + str(data) + '"}')

    def log(self, contents, state=20):
        utils.MCDLogger.log(self.logger, state, contents)
        # states: DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50


class ServerHandler:
    def __init__(self, start_path):
        self.process = None

    def send_msg(self, message):
        pass


class Info:
    def __init__(self, raw=''):
        self.hour, self.min, self.sec, \
            self.sourceProcess, self.player, self.content = None, None, None, None, None, None
        self.raw = raw
        self.parse_line(raw)

    def parse_line(self, line: str):
        self.hour = line[1:3]
        self.min = line[4:6]
        self.sec = line[7:9]
        try:
            self.sourceProcess = re.search(r'[[](.*?)[]]', line[11:]).group()[1:-1]
        except Exception:
            pass
        if (self.sourceProcess == 'Server thread/INFO') and (line[33:].startswith('<')):
            player = re.search(r'[<](.*?)[>]', line[33:]).group()[1:-1]
            self.player = player
            if player != '':
                content = line[33:].replace('[' + self.sourceProcess + ']: ', '', 1)
                self.content = content.replace('<' + self.player + '> ', '', 1)
        else:
            self.player = ''
            self.content = line[11:].replace('[' + self.sourceProcess + ']: ', '', 1)
        return self
