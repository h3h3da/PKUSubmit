import requests
import json
import re
import datetime

# 导入用户信息
with open('config.json', 'r', encoding='UTF-8') as f:
    config_data = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Origin": "https://iaaa.pku.edu.cn"
}

BASIC = {
    "sqbh":"",
    "crxqd":"燕园",
    "crxzd":"校外",
    "qdxm": config_data["gate"],
    "zdxm": "",
    "crxrq":"",
    "email": config_data["email"],
    "lxdh": config_data["phone"],
    "crxsy": config_data["reason"],
    "crxjtsx": config_data["desc"],
    "gjdqm":"156",
    "ssdm":"11",
    "djsm":"01",
    "xjsm":"08",
    "jd": config_data["street"],
    "bcsm":"无",
    "crxxdgj": config_data["route"],
    "dfx14qrbz":"y",
    "sfyxtycj":"",
    "tjbz":"",
    "shbz":"",
    "shyj":""
}

wechat_key = config_data["wechat_key"]


LOG = "```"
def log(s):
    global LOG
    LOG += s + "\n"

def logv(vname, v):
    global LOG
    LOG += vname + " " + str(v) + "\n"

def fail(reason, msg):
    log(reason)
    log(msg)
    raise Exception(f"""{reason}\n\n{msg}\n""")

def finish_log():
    global LOG
    LOG += "```\n\n"

def oauth_login(sess):
    post_data = {
        "appid": "portal2017",
        "userName": config_data["username"],
        "password": config_data["password"],
        "redirUrl": "https://portal.pku.edu.cn/portal2017/ssoLogin.do"
    }
    login_url = "https://iaaa.pku.edu.cn/iaaa/oauthlogin.do"
    resp = sess.post(login_url, data=post_data, headers=headers)
    j = json.loads(resp.text)
    if not j["success"]:
        fail("Fail in login:", resp.text)
    return j["token"]

def sso_login(sess, token):
    url = f"https://portal.pku.edu.cn/portal2017/ssoLogin.do?_rand=0.6444242332881047&token={token}"
    resp = sess.get(url, headers=headers)

def getSimsoToken(sess):
    url = "https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=stuCampusExEn"
    resp = sess.get(url, allow_redirects=False, headers=headers)
    found = re.findall(r'token=([a-z0-9]+)&', resp.headers['Location'])
    if len(found) != 1:
        fail("Fail in getSimsoToken: no token in `Location`", resp.headers['Location'])
    return found[0]
 
def simsoLogin(sess, token):
    url = f"https://simso.pku.edu.cn/ssapi/simsoLogin?token={token}"
    resp = sess.get(url, headers=headers)
    j = json.loads(resp.text)
    if not j["success"]:
        fail("Fail in simsoLogin", resp.text)
    return j

def get_curr_application(sess, sid):
    url = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/getSqzt?sid={sid}"
    resp = sess.get(url, headers=headers)
    j = json.loads(resp.text)
    if not j["success"]:
        fail("Fail in get_curr_application", resp.text)
    return j

def check_new_application(sess, sid):
    url = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/newApplyCheck?sid={sid}"
    resp = sess.get(url, headers=headers)

def save_application(sess, sid, application_id):
    url = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/saveSqxx?sid={sid}"
    application_data = BASIC
    if application_id:
        application_data["sqbh"] = application_id
    print(application_data)
    resp = sess.post(url, json=application_data, headers=headers)
    j = json.loads(resp.text)
    if not j["success"]:
        fail("Fail in save_application", resp.text)
    
def remove_file(sess, sid, application_id):
    url1 = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/getZmclxx?sid={sid}&sqbh={application_id}"
    imgs = json.loads(sess.get(url1, headers=headers).text)
    if imgs["success"]:
        for im in imgs["rows"]:
            url2 = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/removeZmcl?sid={sid}&clid={im['clid']}"
            resp = sess.post(url2, headers=headers)

def upload_file(sess, file_type, file_path, sid, application_id):
    url = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/uploadZmcl?sid={sid}"
    data = {
        "cldms": file_type,
        "sqbh": application_id
    }
    files = {"files": open(file_path, "rb")}
    resp = sess.post(url, data=data, files=files, headers=headers)
    j = json.loads(resp.text)
    if not j["success"]:
        fail("Fail in upload_file", resp.text)


def submit(sess, sid, application_id):
    url = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/submitSqxx?sid={sid}&sqbh={application_id}"
    resp = sess.get(url, headers=headers)
    j = json.loads(resp.text)
    if not j["success"]:
        fail("Fail in submit", resp.text)

def logout(sess, sid):
    url = f"https://simso.pku.edu.cn/ssapi/logout?sid={sid}"
    sess.get(url)
    url = f"https://portal.pku.edu.cn/portal2017/logout.do?_redir_2_webvpn=1"
    sess.get(url)

def wechat_push(key, title, message):
    url = f"https://sc.ftqq.com/{key}.send?text={title}&desp={message}"
    requests.get(url)

def main():
    title = "备案成功 "
    msg = ""
    try:
        sess = requests.Session()

        # Login operations
        oauth_token = oauth_login(sess)
        logv("oauth_token", oauth_token)
        sso_login(sess, oauth_token)
        simso_token = getSimsoToken(sess)
        logv("simso_token", simso_token)
        simso_meta = simsoLogin(sess, simso_token)
        sid = simso_meta["sid"]
        logv("simso_meta", simso_meta)
        sess.cookies.set("sid", simso_meta["sid"], domain="pku.edu.cn")

        # initialize application
        check_new_application(sess, sid)
        curr_application = get_curr_application(sess, sid)
        
        # set data info
        BASIC["crxrq"] = curr_application["row"]["defaultCrxrq"]

        application_id = ""
        if "lastSqxx" in curr_application["row"]:
            if curr_application["row"]["lastSqxx"]["crxrq"] == BASIC["crxrq"]:
                application_id = curr_application["row"]["lastSqxx"]["sqbh"]
        save_application(sess, sid, application_id)

        # get application id
        curr_application = get_curr_application(sess, sid)
        if "lastSqxx" not in curr_application["row"]:
            fail("Cannot find lastSqxx", json.dumps(curr_application))
        application_id = curr_application["row"]["lastSqxx"]["sqbh"]
        logv("application_id", application_id)

        # upload pic
        file_type = "dstys"
        if str(config_data["file_type"]) == '1':
            file_type = "bjjkb"
        file_path = config_data["file"]
        remove_file(sess, sid, application_id)
        upload_file(sess, file_type, file_path, sid, application_id)

        # submit
        submit(sess, sid, application_id)

        # logout
        logout(sess, sid)
    except Exception as e:
        title = "备案失败"
        log(str(e))
    
    title += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f")
    msg += LOG

    if wechat_key:
        wechat_push(wechat_key, title, msg)

if __name__ == "__main__":
    main()
    finish_log()
    print(LOG)