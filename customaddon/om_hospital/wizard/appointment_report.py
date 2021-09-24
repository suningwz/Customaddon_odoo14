from odoo import api, models, fields, _


class AppointmentReportWizard(models.TransientModel):
    _name = "appointment.report.wizard"
    _description = "Print Appointment Report"

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    date_from = fields.Date()
    date_to = fields.Date()

    def action_print_report(self):
        domain = []
        patient_id = self.patient_id
        date_from = self.date_from
        date_to = self.date_to
        if patient_id:
            domain = domain + [('patient_id', '=', patient_id.id)]
        if patient_id:
            domain = domain + [('date_appointment', '>=', date_from)]
        if patient_id:
            domain = domain + [('date_appointment', '<=', date_to)]
        appointments = self.env['hospital.appointment'].search_read(domain)
        appointment_list = []
        for appoint in appointments:
            val = {
                'name': appoint['name'],
                'note': appoint['note'],
                'age': appoint['age']
            }
            appointment_list.append(val)
        data = {
            'form_data': self.read()[0],
            'appointments': appointment_list
        }
        return self.env.ref('om_hospital.action_report_appointment').report_action(self, data=data)
