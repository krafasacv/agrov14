from odoo import models, fields, api
import socket

class HostName(models.Model):
    _inherit = 'res.user'

    def HostName(self):
        hostname = str(socket.gethostname())
        self.signature = hostname