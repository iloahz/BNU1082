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
        self.desUrl = "http://219.224.30.70/contest/problem_show.php?pid=" + str(pid);
        self.subUrl = "http://219.224.30.70/contest/submit.php?pid=" + str(pid);
        self.postUrl = "http://219.224.30.70/contest/action.php";

def genData(username,password,problem,code):
    data = {};
    data["user_id"] = username;
    data["problem_id"] = problem.pid;
    data["language"] = code.type;
    data["source"] = code.data;
    postData = urllib.urlencode(data)
    return postData;

def countAC(username,password):
    statusUrl = "http://219.224.30.70/contest/status.php?showname=" + username + "&showpid=1082&showres=Accepted&showlang=";
##    url = "http://219.224.30.70/contest"
##    test = urlfetch.fetch(url)
##    print "abc"
##    print url
####    print test.content
##    return 0
    countError = 0
    while True:
        try:
            statusPage = urlfetch.fetch(statusUrl).content
            break
        except apiproxy_errors.DeadlineExceededError:
            countError += 1
            print "Fetch status error", countError
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
    countError = 0
    while True:
        try:
            response = urlfetch.fetch(url="http://219.224.30.70/contest/login.php",
                                      payload=loginPost,
                                      method=urlfetch.POST,
                                      follow_redirects=False)
            break
        except apiproxy_errors.DeadlineExceededError:
            countError += 1
            print "Login error", countError
            pass
    content = response.headers
    cookie = Cookie.SimpleCookie(response.headers.get('set-cookie',''))
##    print "abc"
##    print data
##    print "endof abc"
    countError = 0
    while True:
        try:
            response = urlfetch.fetch(url="http://219.224.30.70/contest/action.php",
                                      payload=data,
                                      method=urlfetch.POST,
                                      headers={"Cookie":make_cookie_header(cookie)},
                                      follow_redirects=False)
            break
        except apiproxy_errors.DeadlineExceededError:
            countError += 1
            print "Post data error", countError
            pass
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
        print "Tried", totSubmit, "times"
        if totSubmit > 50:
            return "Bad RP you've got"
            break;
        time.sleep(5);
    return "You've got an AC!"


##username = raw_input("username:");
##password = raw_input("password:");
##giveAC(username,password);
