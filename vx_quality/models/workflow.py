# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WorkflowActionRuleAccount(models.Model):
    _inherit = ['documents.workflow.rule']

    create_model = fields.Selection(selection_add=[('quality.alert', "Quality Alert")])

    def create_record(self, documents=None):
        rv = super(WorkflowActionRuleAccount, self).create_record(documents=documents)
        if self.create_model == 'quality.alert':
            qa_obj = self.env['quality.alert']
            team_id = qa_obj._get_default_team_id()
            qa_ids = qa_obj.create({'user_id': self.env.user.id,
                'team_id': team_id or False})
            context = dict(self._context, default_user_id=self.env.user.id,
                default_team_id=team_id)
            action = {
                'type': 'ir.actions.act_window',
                'res_model': 'quality.alert',
                'name': "Quality Alerts",
                'view_id': False,
                'view_mode': 'tree',
                'views': [(False, "kanban"), (False, "list"), (False, "form")],
                'domain': [('id', 'in', qa_ids.ids or [])],
                'context': context,
            }
            print('---------action-------', action)
            return action
        return rv
