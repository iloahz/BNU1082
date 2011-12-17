import urllib
import urllib2
import Cookie
import time
from google.appengine.api import urlfetch
from google.appengine.runtime import apiproxy_errors

class code:
    def __init__(self, filename):
        self.type = "1";
        self.data = open(filename,"r").read();

class problem:
    def __init__(self, pid):
        self.pid = pid;
        self.desUrl = "http://acm.bnu.edu.cn/contest/problem_show.php?pid=" + str(pid);
        self.subUrl = "http://acm.bnu.edu.cn/contest/submit.php?pid=" + str(pid);
        self.postUrl = "http://acm.bnu.edu.cn/contest/action.php";

def genData(username,password,problem,code):
    data = {};
    data["user_id"] = username;
    data["problem_id"] = problem.pid;
    data["language"] = code.type;
    data["source"] = code.data;
    postData = urllib.urlencode(data)
    return postData;

def countAC(username,password):
    statusUrl = "http://acm.bnu.edu.cn/contest/status.php?showname=" + username + "&showpid=1082&showres=Accepted&showlang=";
    while True:
        try:
            statusPage = urlfetch.fetch(statusUrl).content
            break
        except apiproxy_errors.DeadlineExceededError:
            pass
    AC = -3;
    while True:
        loc = statusPage.find("Accepted");
        if (loc<0):
            break;
        AC += 1;
        statusPage = statusPage[loc+1:len(statusPage)];
    return AC;

def make_cookie_header(cookie):
    ret = ""
    for val in cookie.values():
        ret+="%s=%s; "%(val.key, val.value)
    s = ""
    for i in ret:
        if i!=',':
            s += i
    return s

def submit(problem,data,username,password):
    loginData = {};
    loginData["username"] = username;
    loginData["password"] = password;
    loginPost = urllib.urlencode(loginData)
    response = urlfetch.fetch(url="http://acm.bnu.edu.cn/contest/login.php",
                              payload=loginPost,
                              method=urlfetch.POST,
                              follow_redirects=True)
    content = response.headers
    cookie = Cookie.SimpleCookie(response.headers.get('set-cookie',''))
##    print "abc"
##    print data
##    print "endof abc"
    response = urlfetch.fetch(url="http://acm.bnu.edu.cn/contest/action.php",
                              payload=data,
                              method=urlfetch.POST,
                              headers={"Cookie":make_cookie_header(cookie)},
                              follow_redirects=False)
##    content = response.content

def giveAC(username,password):
    totSubmit = 0
    p1082 =  problem(1082);
    c1082 = code("bnu1082.cpp");
    data = genData(username,password,p1082,c1082);
    nowAC = countAC(username,password);
    while countAC(username,password)==nowAC:
        submit(p1082,data,username,password);
        totSubmit += 1
        if totSubmit > 50:
            break;
        time.sleep(5);


##username = raw_input("username:");
##password = raw_input("password:");
##giveAC(username,password);
