from flask import Flask
from flask_ask import Ask, statement, question, session, delegate, request
import requests
from requests.auth import HTTPBasicAuth
import time
import webbrowser
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unidecode


app = Flask(__name__)
ask = Ask(app, "/grafana_dashboards")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def get_dashboards():
    """
    Get the dashboards available within a given Grafana instance

    Grafana API currently returns array of following data structure :
    {
        "id": 2,
        "uid": "Apidexqkk",
        "title": "Blank",
        "uri": "db/blank",
        "url": "/d/Apidexqkk/blank",
        "type": "dash-db",
        "tags": [],
        "isStarred": false
    },

    :return: dict of {"title": {dash_information}}
    """

    sess = requests.Session()
    #TODO Allow configuration via YAML file
    results = sess.get('http://192.168.50.11:3000/api/search', auth=HTTPBasicAuth('admin', 'admin'))
    time.sleep(1)

    data = results.json()

    dashboards = {}
    for i in data:
        dashboards[i['title']] = i

    return dashboards

def get_datasources():
    """
    GET datasources defined within a specific Grafana instance

    Grafana API currently returns an array of this data structure :

    {
        "id": 4,
        "orgId": 1,
        "name": "telegraf",
        "type": "influxdb",
        "typeLogoUrl": "public/app/plugins/datasource/influxdb/img/influxdb_logo.svg",
        "access": "proxy",
        "url": "http://192.168.50.11:8086",
        "password": "",
        "user": "",
        "database": "telegraf",
        "basicAuth": false,
        "isDefault": true,
        "jsonData": {
            "keepCookies": []
        },
        "readOnly": false
    }

    :return: dict - {"name": {datasource_datastructure}}
    """


def get_dialog_state():
    """
    Get current dialog state for multi-turn dialog with Alexa

    :return:
    """
    return session['dialogState']

@app.route('/')
def homepage():
    return

@ask.launch
def start_skill():
    """
    Entry point for Alexa interaction

    :return:
    """
    welcome_message = "Hi there, how can I help you view your infrastructure?"

    return question(welcome_message)

@ask.intent("GetDashboards")
def share_dashboads():
    """
    Get all dashboards available in Grafana instance

    :return: statement - Alexa will read back all available dashboards in Grafana
    """

    dashboards = get_dashboards()

    titles = []
    for title in dashboards:
        titles.append(title)

    # added to identify end of the titles list
    titles.insert(-1, "and")

    return statement("The current available dashboards are... " + '... '.join(titles))

@ask.intent("OpenDashboard")
def open_dashboard():
    """
    Open a specific dashboard available in Grafana

    :return: question - Alexa will ask if there is anything else she can do.
    """
    dialog_state = get_dialog_state()
    dashboards = get_dashboards()

    if dialog_state != "COMPLETED":
        return delegate(speech=None)
    else:
        webbrowser.open('http://192.168.50.11:3000/' + dashboards[request['intent']['slots']['dashboard']['value']]['url'])
        return statement("I've opened the %s dashboard" % request['intent']['slots']['dashboard']['value'])

@ask.intent("NoIntent")
def no_intent():
    no_text = "If you need anything else, please let me know!"
    return statement(no_text)

if __name__ == '__main__':
    app.run(debug=True)
