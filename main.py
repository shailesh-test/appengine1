# Copyright 2016 Google Inc.
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

# [START app]
import logging

# [START all]
import cgi
import textwrap
import urllib

# [START imports]
from flask import Flask, render_template, request
from google.appengine.ext import ndb
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]

# [START Stock]
class Stock(ndb.Model):
    """Models an individual Stock entry with Stock quote and other required attributes"""
    #quote = ndb.StringProperty()
    name = ndb.StringProperty()
    industrytype = ndb.StringProperty()
    companytype = ndb.StringProperty()
# [END Stock]


# [START Stock]
class StockPrice(ndb.Model):
    """Models an individual Stock Price entry with Stock quote and other price details"""
    quote = ndb.StringProperty()
    estimated_price = ndb.FloatProperty()
    percentage_diff = ndb.FloatProperty()
    last_updated = ndb.DateTimeProperty(auto_now_add=True)
# [END Stock]


# [START main]
@app.route('/main')
def addStock():
    return render_template('addstock.html')
# [END form]

@app.route('/stock')
def stock_get():
    quote = request.args.get('quote')
    stock = Stock.get_by_id(quote)
    if(not(stock is None)):
        return render_template(
            'stockdetails.html',
        quote = stock.key.id(),
        name = stock.name,
        industrytype = stock.industrytype,
        companytype = stock.companytype)
    else:
        return "<h1>Invalid Stock Quote specified</h1>"

# [START stock_post]
@app.route('/stock', methods=['POST'])
def stock_post():
    quote = request.form['quote']
    name = request.form['name']
    industrytype = request.form['industrytype']
    companytype = request.form['companytype']

    # Add stock in database
    stock_key = Stock(id = quote, name = name, industrytype = industrytype, companytype = companytype).put()
    # [END sustock_postbmitted]
    
    # [START render_template]
    return render_template(
        'stockdetails.html',
    quote = quote,
    name = name,
    industrytype = industrytype,
    companytype = companytype,
    message = "Thaks for adding Stock " + quote)
    
    # [END render_template]

# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
