import sys

sys.path.append('..')
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import FunctionCommon as Fun

reload(sys)
sys.setdefaultencoding('utf8')


class MailSender:
    def __init__(self, smtpserver, senderproxy, sendername, senderproxypasswd):
        self.smtpserver = smtpserver
        self.proxysender = senderproxy
        self.proxyname = sendername
        self.proxypasswd = senderproxypasswd

    def login(self):
        self.smtp_ = smtplib.SMTP(self.smtpserver, port=587, timeout=20)
        # self.smtp_.set_debuglevel(1)
        self.smtp_.ehlo()
        self.smtp_.starttls()
        self.smtp_.ehlo()
        self.smtp_.login(self.proxyname, self.proxypasswd)
        print '>>>>>> MailSender.login() finished '

    def get_content(self, receivermail, date, crash_result, subject, logfile, browser, device,
                    androidversion):
        html = """\
                <html>
                <body>
                <h2><center> 2014-06-10 APPNAME Monkey Test exception explanation</center></h2>
                <table border="1" algin="center">
                <caption><em>Jenkins AutoTest Result</em></caption>
                <tr>
                <tr><th>Jenkins<td><a href='http://10.60.118.93:8080/jenkins/view/Monkey/job/APPNAME_DEVICENAME/'>http://10.60.118.93:8080/jenkins/view/Monkey/job/APPNAME_DEVICENAME/</a>
                <tr><th>Install APK_PATH<td>test.apk
                <tr><th>DeviceInfo<td>DEVICENAME
                <tr><th>System<td>ANDROIDVERSION
                <tr><th>Result<td>Found crash Log, please check out logfile or download attachments
                </table>
                <br>contentsss
                <br>
                <body>
                <html>
                """
        # <img border="0" src="cid:image_win" width="200" length="200" >

        mFile = open(logfile.replace('.log', '.path'))
        strfile = mFile.read()
        mFile.close()
        html = html.replace("2014-06-10", date)
        html = html.replace("10.60.118.93", Fun.get_my_ip())
        html = html.replace("test.apk", strfile.split('/')[-1])
        html = html.replace("contentsss", crash_result)
        html = html.replace('APPNAME', browser)
        html = html.replace('DEVICENAME', device)
        html = html.replace('ANDROIDVERSION', androidversion)
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject.replace('_', '')
        msgRoot['From'] = self.proxysender
        msgRoot['To'] = ",".join(receivermail)

        msgText = MIMEText(html, 'html', 'utf-8')
        msgRoot.attach(msgText)

        txt = MIMEText(open(logfile, 'rb').read(), 'base64', 'gb2312')
        txt["Content-Type"] = 'application/octet-stream'
        txt["Content-Disposition"] = 'attachment; filename="CrashLog.txt"'
        msgRoot.attach(txt)

        print '>>>>>> MailSender.get_content() finished '
        return msgRoot

    def get_device_not_found_content(self, receivermail, date, subject, browser, device):
        html = """\
                <html>
                <body>
                <h2><center> DATE APPNAME Monkey Test exception explanation</center></h2>
                <table border="1" algin="center">
                <caption><em>Jenkins AutoTest Result</em></caption>
                <tr>
                <tr><th>Jenkins</th><td><a href='http://10.60.118.93:8080/jenkins/view/Monkey/job/APPNAME_DEVICENAME/'>http://10.60.118.93:8080/jenkins/view/Monkey/job/APPNAME_DEVICENAME/</a></td></tr>
                <tr><th>DeviceInfo</th><td>DEVICENAME</td></tr>
                </table>
                <body>
                <html>
                """

        html = html.replace("DATE", date)
        html = html.replace("10.60.118.93", Fun.get_my_ip())
        html = html.replace('APPNAME', browser)
        html = html.replace('DEVICENAME', device)

        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject.replace('_', '')
        msgRoot['From'] = self.proxysender
        msgRoot['To'] = ",".join(receivermail)

        msgText = MIMEText(html, 'html', 'utf-8')
        msgRoot.attach(msgText)

        print '>>>>>> MailSender.get_device_not_found_content() finished '
        return msgRoot

    def do_send_mail(self, receivermail, send_content):
        if None == self.smtp_:
            print "smtp_ is None"
            return
        self.smtp_.sendmail(self.proxysender, receivermail, send_content.as_string())
        print '>>>>>> MailSender.do_send_mail() finished '
        print "send e-mail successfully"

    def logout(self):
        self.smtp_.quit()
        print '>>>>>> MailSender.logout() finished '


def sendDeviceNotFound(sender, pwd, receivers, subject, browser, device):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    mailObj = MailSender('smtp.gmail.com', sender, sender, pwd)
    mailObj.login()
    mail_content = mailObj.get_device_not_found_content(receivers, date, subject, browser, device)

    if None != mail_content:
        mailObj.do_send_mail(receivers, mail_content)
    else:
        print "mailObj.get_content error"

    mailObj.logout()
    print '>>>>>> mailObj.sendDeviceNotFound() finished '


def sendException(crash_result, sender, pwd, receivers, subject, logfile,
                  browser, device, androidversion):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    mailObj = MailSender('smtp.gmail.com', sender, sender, pwd)
    mailObj.login()
    mail_content = mailObj.get_content(receivers, date, crash_result, subject, logfile, browser,
                                       device, androidversion)

    if None != mail_content:
        mailObj.do_send_mail(receivers, mail_content)
    else:
        print "mailObj.get_content() error"

    mailObj.logout()
    print '>>> sendException() finished \n'


def test():
    subject = 'ANR crash log'
    sender = ''
    pwd = ''
    receivers = [""]

    apkPathLog = 'filePath.txt'
    monkeyLog = '9250.log'
    logPath = 'D:/4monkey/Log/'
    apkPath = logPath + apkPathLog
    logfile = logPath + monkeyLog
    browser = 'KBrowser'
    device = '9250'
    sendDeviceNotFound(sender, pwd, receivers, subject, browser, device)
