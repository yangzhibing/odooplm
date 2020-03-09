# -*- encoding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, Your own solutions
#    Copyright (C) 2010 OmniaSolutions (<http://omniasolutions.eu>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

'''
Created on 9 Dec 2016

@author: Daniel Smerghetto
'''

from odoo import models
from odoo import api
import logging


class ProductTemplateExtension(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        engineering_code = vals.get('engineering_code', '')
        engineering_revision = vals.get('engineering_revision', 0)
        if engineering_code and not vals.get('default_code') and engineering_code != '-' or self.env.context.get('new_revision', False):
            vals['default_code'] = self.env['product.product'].computeDefaultCode(engineering_code, engineering_revision)
            logging.info('Internal ref set value %s on engineering_code: %r' % (vals['default_code'], engineering_code))
        return super(ProductTemplateExtension, self).create(vals)

    def write(self, vals):
        res = super(ProductTemplateExtension, self).write(vals)
        for prodBrws in self:
            if prodBrws.engineering_code and not prodBrws.default_code and prodBrws.engineering_code != '-' or self.env.context.get('new_revision', False):
                default_code = self.env['product.product'].computeDefaultCode(prodBrws.engineering_code, prodBrws.engineering_revision)
                super(ProductTemplateExtension, self).write({'default_code': default_code})
        return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
