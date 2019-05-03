# -*- coding: utf-8 -*-

###############################################################################
#
#    Periodical Sales Report
#
#    Copyright (C) 2019 Aminia Technology
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import api, models
from dateutil.relativedelta import relativedelta
import datetime


class ReportPeriodicalSale(models.AbstractModel):
    _name = 'report.periodical_sales_report.report_periodical_sales'

    @api.model
    def get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        period = data['form']['period']
        state = data['form']['state']
        total_sale = 0.0

        if date_from and date_to:
            domain = [('date_order', '>=', date_from),
                      ('date_order', '<=', date_to)]
        else:
            if period == 'today':
                domain = [('date_order', '>=', datetime.datetime.now()
                           .strftime('%Y-%m-%d 00:00:00')),('date_order',
                            '<=', datetime.datetime.now()
                            .strftime('%Y-%m-%d 23:59:59'))]
            elif period == 'last_week':
                domain = [('date_order', '>=', (datetime.date.today()
                -datetime.timedelta(days=7)).strftime('%Y-%m-%d 00:00:00')),
                 ('date_order', '<=', datetime.datetime.now()
                  .strftime('%Y-%m-%d 23:59:59'))
                ]
            elif period == 'last_month':
                domain = [
                    ('date_order', '>=',
                     (datetime.date.today() - relativedelta(months=1)).
                     strftime('%Y-%m-%d 00:00:00')),
                    ('date_order', '<=',
                     datetime.datetime.now().strftime('%Y-%m-%d 23:59:59'))
                ]
        if state != 'all':
            domain.append(('state','=',state))

        docs = []
        orders = self.env['sale.order'].search(domain)

        for order in orders:
            docs.append({
                'name': order.name,
                'date_order': order.date_order,
                'partner' : order.partner_id.name,
                'amount_total' : order.amount_total
            })
            total_sale += order.amount_total

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'period' : period,
            'date_from': date_from,
            'date_to': date_to,
            'docs': docs,
            'total_sale' : total_sale,
        }