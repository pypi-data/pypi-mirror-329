import socket
from .bug_scanner import BugScanner

class PingScanner(BugScanner):
    host_list = []
    port_list = []

    def log_info(self, **kwargs):
        kwargs.setdefault('color', '')
        kwargs.setdefault('status', '')
        kwargs.setdefault('host', '')

        CC = self.logger.special_chars['CC']
        kwargs['CC'] = CC

        colors = {
            'status': '\033[92m',
            'port': '\033[95m',
            'host': '\033[96m',
        }

        messages = [
            f'{colors["status"]}{{status:<8}}{CC}',
            f'{colors["port"]}{{port:<6}}{CC}',
            f'{colors["host"]}{{host:<20}}{CC}',
        ]

        super().log('  '.join(messages).format(**kwargs))

    def get_task_list(self):
        for host in self.filter_list(self.host_list):
            for port in self.filter_list(self.port_list):
                yield {
                    'host': host,
                    'port': port,
                }

    def init(self):
        super().init()
        self.log_info(status='Status', port='Port', host='Host')
        self.log_info(status='------', port='----', host='----')

    def task(self, payload):
        host = payload['host']
        port = payload['port']

        if not host:
            return
        
        self.log_replace(f"{host}:{port}")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, int(port)))
            sock.close()

            if result == 0:
                data = {
                    'host': host,
                    'port': port,
                    'status': 'OPEN'
                }
                self.task_success(data)
                self.log_info(**data)

        except Exception:
            pass

        self.log_replace()