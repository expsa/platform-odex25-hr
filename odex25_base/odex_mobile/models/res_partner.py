from odoo import models, fields, api
import json, requests

class Partner(models.Model):

    _inherit = 'res.partner'

    firebase_registration_ids = fields.One2many(
        "firebase.registration", "partner_id", readonly=True
    )

    def send_notification(self, message_title, message_body,data=None, all_device=True):
        if all_device:
            import json
            record = self.env['firebase.notification'].sudo().create({
                        "title":str(message_title), 
                        "body":str(message_body),
                        "meta": str(json.dumps(data)) if data else None,
                        "partner_ids":[(4,self.id)],
                        "is_system":True,
                        "sent":True
                    })
  
            for reg in self.firebase_registration_ids:
                reg.with_context(lang=self.lang).send_message(message_title, message_body,data={
                        "title":str(message_title), 
                        "body":str(message_body),
                        "meta": str(json.dumps(data)) if data else None,
                        "is_system":"true",
                        'viewed':"false",
                        "sent":"true",
                        "data":str(record.create_date),
                        "id":str(record.id)
                })
        else:
            self.firebase_registration_ids[0].with_context(lang=self.lang).send_message(message_title, message_body, data=data)

    def user_push_notification(self, fcm_token):
        url = "https://fcm.googleapis.com/fcm/send"
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'key=%s' % (self.env.user.company_id.fcm_server_key)
        }
        body = json.dumps({
            "to": fcm_token,
            "direct_boot_ok": True,
            "notification": {
                "title": "Test",
                "body": "test"
            }
        })
        try:
            respons = requests.post(url=url, data=body, headers=header)
            return True
        except Exception as e:
            return False
