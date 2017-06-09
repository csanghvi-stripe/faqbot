#Credits: https://github.com/mk200789/hello_slackbot

import os
import time
from slackclient import SlackClient
import sys
import json
from threading import Thread
from time import sleep
from flask import Flask, flash, make_response, Response, redirect, render_template, request, session, abort
from random import randint
import requests
import base64
from urllib.parse import parse_qsl
import apiai

with open('tokens.json') as json_data_file:
    data = json.load(json_data_file)
print (data)

slack_bot_token = data["SLACK_BOT_TOKEN"]
verification_token = data["VERIFICATION_TOKEN"]
client_id = data["CLIENT_ID"]
client_secret = data["CLIENT_SECRET"]
api_ai_token = data["APIAI_DEVELOPER_ACCESS_TOKEN"]
bot_id = data["SLACK_BOT_ID"]


# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistant memory store.
authed_teams = {}


READ_WEBSOCKET_DELAY = 0.5 #per second

#bot name
# BOT_NAME = 'demobot'
BOT_NAME = "bots101"

#get bot id
#BOT_ID = os.environ.get('SLACK_BOT_ID')
BOT_ID = ""

#get slack bot token
SLACK_BOT_TOKEN = slack_bot_token

#get aiapi access token
APIAI_ACCESS_TOKEN = api_ai_token

#set slack client
slack_client = SlackClient("")
sc = ""

#set apiai client
apiai_client = apiai.ApiAI(APIAI_ACCESS_TOKEN)

# constants
AT_BOT = ""

CLIENT_ID = client_id
CLIENT_SECRET = client_secret 


app = Flask(__name__)

@app.route("/")
def index():
    ret = "Flask App!"
    return (ret)

@app.route("/help", methods=["GET", "POST"])
def help():
    #respond to /bot101 help
    helpertext = {"text":"I can support questions like: `what is a bot`, `how to build a bot`, `what are types of bot`"}
    return Response(json.dumps(helpertext), mimetype='application/json')



@app.route("/authorize", methods=["GET", "POST"])
def authorize():
    """
    This route is called by Slack after the user installs our app. It will
    exchange the temporary authorization code Slack sends for an OAuth token
    which we'll save on the bot object to use later.
    To let the user know what's happened it will also render a thank you page.
    """
    # Let's grab that temporary authorization code Slack's sent us from
    # the request's parameters.
    code_arg = request.args.get('code')
    print ("code from slack is:", code_arg)
    # The bot's auth method to handles exchanging the code for an OAuth token
    #code = request.data.decode("utf-8").args.get('code')
    #print (code)
    sc = auth(code_arg)
    thread = Thread(target = threaded_function, args = (sc, ))
    thread.start()
    #thread.join()

    return render_template("thanks.html")


@app.route("/slack")
def add_to_slack():
    """This route renders the installation page with 'Add to Slack' button."""
    # Since we've set the client ID and scope on our Bot object, we can change
    # them more easily while we're developing our app.
    client_id = CLIENT_ID
    scope = "bot,incoming-webhook,chat:write:bot,commands"
    # Our template is using the Jinja templating language to dynamically pass
    # our client id and scope
    return render_template("slack.html", client_id=client_id, scope=scope)

def auth(code):
    """
    Authenticate with OAuth and assign correct scopes.
    Save a dictionary of authed team information in memory on the bot
    object.

    Parameters
    ----------
    code : str
    temporary authorization code sent by Slack to be exchanged for an
    OAuth token

    """
    # After the user has authorized this app for use in their Slack team,
    # Slack returns a temporary authorization code that we'll exchange for
    # an OAuth token using the oauth.access endpoint
    auth_response = slack_client.api_call(
    "oauth.access",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    code=code
    )
    # To keep track of authorized teams and their associated OAuth tokens,
    # we will save the team ID and bot tokens to the global
    # authed_teams object
    print (auth_response)

    team_id = auth_response["team_id"]
    authed_teams[team_id] = {"bot_token":
    auth_response["bot"]["bot_access_token"]}

    # Then we'll reconnect to the Slack Client with the correct team's
    # bot token
    print ("bot token is: ", authed_teams[team_id]["bot_token"])
    sc = SlackClient(authed_teams[team_id]["bot_token"])

    return sc



@app.route("/listening", methods=["GET", "POST"])
def actions():
    """
    This route listens for incoming events from Slack and uses the event
    handler helper function to route events to our Bot.
    """
    ##First update the chat to remove the attachments


    dict1 = {}
    secondtext = request.get_data().decode("utf-8")
    data = dict(parse_qsl(secondtext))
    payload = json.loads(data['payload'])
    print (payload)
    print (payload["actions"][0]["value"])
    if payload["actions"][0]["value"] == "learnmore" :
        print (payload["response_url"])
            # Response to action_url

        dict1 = {
        	"text":":white_check_mark: Sure, You will find more details here:",
        	"replace_original": False,
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": "#36a64f",
                    "pretext": "",
                    "title": "Slack API Documentation",
                    "title_link": "https://api.slack.com/",
                    "text": "Learn Everything about building a bot",
                    "footer": "Slack API",
                    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"

                }
            ]
        }
    elif payload["actions"][0]["value"] == "api" :
        print (payload["response_url"])
        dict1 = {
        	"text":":white_check_mark: Sure, You will find more details here:",
        	"replace_original": False,
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": "#36a64f",
                    "pretext": "",
                    "title": "Slack API Documentation",
                    "title_link": "https://api.slack.com/",
                    "text": "Learn Everything about building a bot",
                    "footer": "Slack API",
                    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"

                }
            ]
        }

    elif payload["actions"][0]["value"] == "youtube" :
        print (payload["response_url"])
        dict1 = {
        	"text":":white_check_mark: Sure, You will find more details here:",
        	"replace_original": False,
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": "#36a64f",
                    "pretext": "",
                    "title": "Slack Youtube Video for API.AI",
                    "title_link": "https://www.youtube.com/watch?v=cCCKOLFEXBU",
                    "text": "Learn Everything about building a bot",
                    "footer": "Slack API",
                    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"

                }
            ]
        }



    elif payload["actions"][0]["value"] == "No" :
        print (payload["response_url"])
        dict1 = {"text":":white_check_mark: You are awesome",
                	"replace_original": False}


    else :
        print ("sorry, kela mila")

    #secondtext = json.loads(request.get_data().decode('utf-8'))

    #decoded = base64.b64decode(request.get_data())
    #data = json.loads(decoded.decode('utf-8'))
    #print ("\nthird attempt: ", data)

    #slack_event = json.loads(request.data.decode("utf-8"),strict=False)
    #print ("slack event is: ", slack_event)

    #Update the chat and remove the attachment
    #payload["response_url"]
    team_id=payload["team"]["id"]
    sc = SlackClient(authed_teams[team_id]["bot_token"])
    ts = payload["original_message"]["ts"]
    channel = payload["channel"]["id"]
    text = payload["original_message"]["text"]
    attachments = []

    sc.api_call("chat.update", ts=ts, channel=channel, text=text, as_user=True, attachments= attachments)


    return Response(json.dumps(dict1), mimetype='application/json')

def threaded_function(sc):
    startClient(sc)
	#app.run(host='0.0.0.0', port=80)


def parse_slack_output(slack_rtm_output, atbot):
	output_list = slack_rtm_output
	#AT_BOT = atbot
	print (atbot)
	if output_list and len(output_list) > 0:
		for output in output_list:
			# print "output: ", len(output.keys()), output , "\n\n", BOT_ID, "\n\n"
			if output and 'text' in output and atbot in output['text']:
			# return text after the @ mention, whitespace removed
				return output['text'].split(atbot)[1].strip().lower(), output['channel']
			elif output and 'text' in output and output['channel'].startswith('D') and not 'bot_id' in output:
				return output['text'].strip().lower(), output['channel']
	return None, None



def handle_command(command, channel,sc):
	attachments = []
	response = "Not sure what you mean. \nPlease use the /help to know how I can help you"
	request = apiai_client.text_request()
	request.query = command
	r = request.getresponse().read()

    #slack_event = json.loads(request.data.decode("utf-8"),strict=False)
	ai_response = json.loads(r.decode("utf-8"), strict=False)['result']
	#ai_response = json.loads(r)['result']
	print (ai_response)
	print ('first line \n')
	if 'smalltalk' in ai_response['action']:
		print (ai_response['fulfillment']['speech'])
		print ('second line \n')
		response = ai_response['fulfillment']['speech']
	elif 'intentName' in ai_response['metadata'] and ai_response['metadata']['intentName'] == 'bot.define':
		response = ai_response['fulfillment']['messages'][0]['speech']
		print (response)
		attachments = [{
                        "text": "Need to know more?",
                        "attachment_type": "default",
                        "callback_id": "demo_button_id",
                        "fallback": "wowweee!",
                        "color": "#f44262",
                        "actions": [{
                                "name": "part_1",
                                "text": "Yes",
                                "type": "button",
                                "value": "learnmore"
                                },{
                                "name": "part_3",
                                "text": "No",
                                "type": "button",
                                "value": "No"
                                }
                        ]
                }]
	elif 'intentName' in ai_response['metadata'] and ai_response['metadata']['intentName'] == 'bot.features':
		response = ai_response['fulfillment']['messages'][0]['payload']['slack']['text']
		print ('bot.features line \n')
		print (response)
		attachments = []


	elif 'intentName' in ai_response['metadata'] and ai_response['metadata']['intentName'] == 'bot.steps':
		response = ai_response['fulfillment']['messages'][0]['payload']['slack']['text']
		print ('bot.steps \n')
		print (response)
		attachments = [{
                                "text": "Need to know more?",
                                "attachment_type": "default",
                                "callback_id": "demo_button_id",
                                "fallback": "wowweee!",
                                "color": "#f44262",
                                "actions": [{
                                        "name": "part_1",
                                        "text": "Yes",
                                        "type": "button",
                                        "value": "api"
                                        },{
                                        "name": "part_3",
                                        "text": "No",
                                        "type": "button",
                                        "value": "No"
                                        }
                                ]
                        }]
	elif 'intentName' in ai_response['metadata']:
		response = ai_response['fulfillment']['messages'][0]['payload']['slack']['text']
		attachments = ai_response['fulfillment']['messages'][0]['payload']['slack']['attachments']

		print ('Everything Else API.AI line \n')
		print (response)
		attachments = []

	else:
		print ('random')

	final_response=":robot_face: ```" + response + "```"
	sc.api_call("chat.postMessage", channel=channel, text=response, as_user=True, unfurl_links=False, attachments= attachments)


def startClient(sc):
    atbot = ""
    api_call = sc.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        #print (users)
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                BOT_ID = user.get('id')
                AT_BOT = "<@" + BOT_ID + ">"
                atbot = AT_BOT
                print (atbot)
            #else:
                #print("could not find bot user with the name " + user.get('name'))

        if sc.rtm_connect():
            print(BOT_NAME + " connected and running!")
            while True:
                rtm = sc.rtm_read()
                if rtm:
                    print (rtm)
                    command, channel = parse_slack_output(rtm, atbot)
                    if command and channel:
                        handle_command(command, channel,sc)
                        time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print(BOT_NAME + " not connected!")



if __name__ == '__main__':
	#thread = Thread(target = threaded_function, args = (10, ))
	#thread.start()
	#thread.join()
    app.run(host='0.0.0.0', port=80)
    thread.join()
    print ("thread finished...exiting")
