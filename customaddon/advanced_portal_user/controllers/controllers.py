# -*- coding: utf-8 -*-
from datetime import datetime, date
import pytz
import werkzeug
from odoo import http, exceptions, _
from odoo.exceptions import ValidationError, UserError
from odoo.http import request


class AdvancedPortalUser(http.Controller):
    @http.route('/portal_user/create_attendances', website=True, auth='user', type="http", methods=['POST', 'GET'],
                csrf=False)
    def portal_user_create_attendances(self, **kw):
        user_id = request.env.user.id
        employee_id = request.env.user.employee_related.id
        employee_name = request.env.user.employee_related.name
        current_att = request.env['hr.attendance'].sudo().search([('employee_id', '=', employee_id),
                                                                  ('user_id', '=', user_id),
                                                                  ('check_in', '!=', None),
                                                                  ('check_out', '=', None)])
        check_in_obj = current_att['check_in']
        check_in_str = str(check_in_obj)[:16]
        check_out_obj = current_att['check_out']
        check_out_str = str(check_out_obj)[:16]
        return request.render("advanced_portal_user.portal_user_create_attendances",
                              {'check_in_str': check_in_str,
                               'check_in_obj': check_in_obj,
                               'check_out_obj': check_out_obj,
                               'check_out_str': check_out_str,
                               'employee_name': employee_name
                               })

    @http.route('/portal_user/save_attendances', website=True, auth='user', type="http", methods=['POST', 'GET'],
                csrf=False)
    def portal_user_save_attendances(self, **kw):
        user_id = request.env.user.id
        employee_id = request.env.user.employee_related.id
        today = date.today().strftime("%Y-%m-%d")
        today_str = str(today)
        start_time = request.env['ir.config_parameter'].sudo().get_param('advanced_portal_user.time_in')
        if start_time:
            pass
        else:
            start_time = '07:00:00'
        end_time = request.env['ir.config_parameter'].sudo().get_param('advanced_portal_user.time_out')
        if end_time:
            pass
        else:
            end_time = '19:00:00'
        start_date_time = datetime.strptime(today + ' ' + start_time + '.000000', '%Y-%m-%d %H:%M:%S.%f')
        end_date_time = datetime.strptime(today + ' ' + end_time + '.000000', '%Y-%m-%d %H:%M:%S.%f')
        current_time_str = str(datetime.now(pytz.timezone('Asia/Saigon'))).replace("+07:00", "")
        current_time_obj = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M:%S.%f')
        current_att = request.env['hr.attendance'].sudo().search([('employee_id', '=', employee_id),
                                                                  ('user_id', '=', user_id),
                                                                  ('check_in', '!=', None),
                                                                  ('check_out', '=', None)])
        current_att_check_in = current_att['check_in']
        current_att_check_in_str = str(current_att_check_in)[:10]
        if start_date_time < current_time_obj < end_date_time:
            if current_att:
                if current_att_check_in_str != today_str:
                    current_att.sudo().write({'check_out': current_att_check_in})
                    request.env['hr.attendance'].sudo().create({
                        'employee_id': employee_id,
                        'user_id': user_id,
                        'check_in': current_time_obj,
                    })
                else:
                    current_att.sudo().write({'check_out': current_time_obj})
            else:
                request.env['hr.attendance'].sudo().create({
                    'employee_id': employee_id,
                    'user_id': user_id,
                    'check_in': current_time_obj,
                })
        else:
            raise ValidationError(_('Cannot create new attendance record out of time regulations'))
        return werkzeug.utils.redirect('/portal_user/create_attendances')

    @http.route('/portal_user/create_leaves', website=True, auth='user', type="http", methods=['POST', 'GET'], csrf=False)
    def generate_template_create_leaves(self, **kw):
        user_id = request.env.user.id
        employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)]).id
        leave_type = request.env['hr.leave.type'].sudo().search([])
        # ('allocation_type', '=', 'no')
        all_leave = request.env['hr.leave'].sudo().search([('employee_id', '=', employee_id)])
        total_hours = 0
        for leave in all_leave:
            total_hours += leave['number_of_days']
        return request.render("advanced_portal_user.portal_user_create_leaves", {'leave_type': leave_type})

    @http.route('/portal_user/save_leaves', auth='user', website=True, type="http", methods=['POST', 'GET'], csrf=False)
    def portal_user_create_leaves(self, **kw):
        user_id = request.env.user.id
        employee_id = request.env.user.employee_related.id
        date_from_str = kw['date_from']
        time_from_obj_default_date = str(datetime.strptime(date_from_str[11:], '%I:%M %p'))
        full_time_from_str = date_from_str[:11] + time_from_obj_default_date[11:] + '.' + '000000'
        full_time_from_obj = datetime.strptime(full_time_from_str, '%m/%d/%Y %H:%M:%S.%f')
        date_to_str = kw['date_to']
        time_to_obj_default_date = str(datetime.strptime(date_to_str[11:], '%I:%M %p'))
        full_time_to_str = date_to_str[:11] + time_to_obj_default_date[11:] + '.' + '000000'
        full_time_to_obj = datetime.strptime(full_time_to_str, '%m/%d/%Y %H:%M:%S.%f')
        leave_type_kw = int(kw['leave_type'])
        leave_type = request.env['hr.leave.type'].sudo().search([('id', '=', leave_type_kw)]).id
        leave_val = {
            'private_name': kw.get('private_name'),
            'state': 'confirm',
            'user_id': user_id,
            'employee_id': employee_id,
            'holiday_status_id': leave_type,
            'date_from': full_time_from_obj,
            'date_to': full_time_to_obj,
            'holiday_type': 'employee',
        }
        ####
        #compute number_of_day in model not working by anyway
        ###
        #missing field request_date_from and request_date_to
        ###
        request.env['hr.leave'].sudo().create(leave_val)

        return request.render("advanced_portal_user.success_to_create_leave_request", {})

    @http.route('/portal_user/create_over_time', website=True, auth='user', type="http", methods=['POST', 'GET'], csrf=False)
    def portal_user_create_over_time(self, **kw):
        user_id = http.request.env.user.id
        employee_id = request.env.user.employee_related.id
        return request.render("advanced_portal_user.portal_user_create_over_time", {'employee_id': employee_id})

    @http.route('/portal_user/save_over_time', website=True, auth='user', type="http", methods=['POST', 'GET'],
                csrf=False)
    def portal_user_save_over_time(self, **kw):
        user_id = http.request.env.user.id
        employee_id = request.env.user.employee_related.id
        time_from_str = kw['time_from']
        time_from_obj_default_date = str(datetime.strptime(time_from_str[11:], '%I:%M %p'))
        full_time_from_str = time_from_str[:11] + time_from_obj_default_date[11:] + '.' + '000000'
        full_time_from_obj = datetime.strptime(full_time_from_str, '%m/%d/%Y %H:%M:%S.%f')
        time_to_str = kw['time_to']
        time_to_obj_default_date = str(datetime.strptime(time_to_str[11:], '%I:%M %p'))
        full_time_to_str = time_to_str[:11] + time_to_obj_default_date[11:] + '.' + '000000'
        full_time_to_obj = datetime.strptime(full_time_to_str, '%m/%d/%Y %H:%M:%S.%f')
        description = kw['description']
        approver = request.env['hr.employee'].sudo().search([('id', '=', employee_id)]).leave_manager_id.id
        if not approver:
            approver = 1
        over_time_val = {
            'user_id': user_id,
            'employee_id': employee_id,
            'description': description,
            'time_from': full_time_from_obj,
            'time_to': full_time_to_obj,
            'approver': approver,
        }
        request.env['hr.over.time'].sudo().create(over_time_val)
        return request.render("advanced_portal_user.success_to_create_over_time_request", {})

    @http.route('/portal_user/set_payroll_time', website=True, auth='user', type="http", methods=['POST', 'GET'], csrf=False)
    def portal_user_set_payroll(self, **kw):
        user_id = http.request.env.user.id
        return request.render("advanced_portal_user.portal_user_set_payroll_time", {})

    @http.route('/portal_user/payroll_detail', website=True, auth='user', type="http", methods=['POST', 'GET'],
                csrf=False)
    def portal_user_view_payroll(self, **kw):
        user_id = http.request.env.user.id
        employee_id = request.env.user.employee_related.id
        payroll_set_month = kw['month'] + '/15/' + kw['year']
        datetime_set_obj = datetime.strptime(payroll_set_month, '%m/%d/%Y')
        date_set_obj = datetime_set_obj.date()
        payslip_list = request.env['hr.payslip'].sudo().search([('employee_id', '=', employee_id)])
        if payslip_list:
            for payslip in payslip_list:
                if payslip['date_from'] <= date_set_obj <= payslip['date_to']:
                    payslip_id = payslip.id
                    payslip_line = request.env['hr.payslip.line'].sudo().search([('slip_id', '=', payslip_id)])
                    payslip_line_total = 0
                    for payslip_line_element in payslip_line:
                        payslip_line_total += payslip_line_element['total']
        else:
            raise ValidationError(_('There are no available payroll for this month'))
        return request.render("advanced_portal_user.portal_user_detail_payroll", {'payslip_line': payslip_line, 'payslip_line_total':payslip_line_total})
