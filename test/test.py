import requests

email = """
<p>This email was set as the recovery address for your Proton Account.<br>
Please verify this email belongs to you.<br>
Verify email<br>
Verification ensures we can safely assist you in case of sign-in issues or suspicious activity.<br>
Thank you,<br>
The Proton Team<p>
"""



def sendEmail(name, subject, content):
    api_url = 'https://api.elasticemail.com/v2/email/send'
    api_key = 'D9E601E4609BF2D4ECCE49A260510FCC45E9EC18D40EAF477321DD1F2B9FC0500FC47FE45F9B8053859F6D4B08DFBEEC'
    params = {
        'apikey': api_key,
        'from': 'vmessenger@proton.me',
        'fromName': name,
        'to': 'vignesharplayboyvicky@gmail.com',
        'subject': subject,
        'bodyHtml': content,
        'isTransactional': True
    }
    response = requests.post(api_url, data=params)
    if response.status_code == 200:
        return True
    else:
        return False

sendEmail("Vicky", "test", email)