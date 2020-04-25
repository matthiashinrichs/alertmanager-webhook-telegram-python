import telegram, json, logging
from dateutil import parser
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.secret_key = 'iaia4545'
basic_auth = BasicAuth(app)

# Yes need to have -, change it!
chatID = "-xchatIDx"

# Authentication conf, change it!
app.config['BASIC_AUTH_FORCE'] = xbasicAUTHx
app.config['BASIC_AUTH_USERNAME'] = 'XXXUSERNAME'
app.config['BASIC_AUTH_PASSWORD'] = 'XXXPASSWORD'

# Bot token, change it!
bot = telegram.Bot(token="botToken")

logging.basicConfig(level=logging.INFO)

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    try:
        content = json.loads(request.get_data())
        print(content)
        app.logger.info("\t%s",content)
        for alert in content['alerts']:
            message = "Status: "+alert['status']+"\n"
            if 'name' in alert['labels']:
                message += "Instance: "+alert['labels']['instance']+"("+alert['labels']['name']+")\n"
            elif 'instance' in alert['labels']:
                message += "Instance: "+alert['labels']['instance']+"\n"
            else:
                message += "Instance: "+alert['labels']['alertname']+"\n"
            if 'info' in alert['annotations']:
                message += "Info: "+alert['annotations']['info']+"\n"
            if 'summary' in alert['annotations']:
                message += "Summary: "+alert['annotations']['summary']+"\n"                
            if 'description' in alert['annotations']:
                message += "Description: "+alert['annotations']['description']+"\n"
            if 'message' in alert['annotations']:
                message += "Description: "+alert['annotations']['message']+"\n"
            if alert['status'] == "resolved":
                correctDate = parser.parse(alert['endsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Resolved: "+correctDate
            elif alert['status'] == "firing":
                correctDate = parser.parse(alert['startsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Started: "+correctDate
            bot.sendMessage(chatID, text=message)
            return "Alert OK", 200
    except Exception as error:       
        bot.sendMessage(chatID, text="Error to read json: "+str(error))
        app.logger.info("\t%s",error)
        return "Alert fail", 200

@app.route('/', methods = ['GET', 'POST'])
def respond():
    return "."

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=9119)
