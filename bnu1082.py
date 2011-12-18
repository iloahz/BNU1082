#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import webapp2
from submit import giveAc, giveAcOnce

class Submit(webapp2.RequestHandler):
    def post(self):
        username = cgi.escape(self.request.get('username'))
        password = cgi.escape(self.request.get('password'))
        content = giveAc(username,password)
        self.response.out.write(content)

class SubmitOnce(webapp2.RequestHandler):
    def get(self):
        username = cgi.escape(self.request.get('username'))
        password = cgi.escape(self.request.get('password'))
        totalSubmit = cgi.escape(self.request.get('totalSubmit'))
        res = giveAcOnce(username,password)
        a = res[0]
        b = res[1]
        s = ""
##        s += str(a) + " " + str(b) + " " + str(a<b) + "_____"
        if a < b:
            s += r"You've got an AC!"
        else:
            s += "This is the " + str(totalSubmit) + ".. time of submitting for you,";
        s += " Currently you have " + str(b) + " AC(s)."
        self.response.out.write(s)

app = webapp2.WSGIApplication([('/Submit', Submit),
                               ('/SubmitOnce',SubmitOnce)],
                              debug=True)
