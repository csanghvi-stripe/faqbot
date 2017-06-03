import os
import time
from slackclient import SlackClient
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

#bot name
# BOT_NAME = 'demobot'
BOT_NAME = "faqbot"

#get bot id
BOT_ID = os.environ.get('SLACK_BOT_ID')

#get slack bot token
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

#get aiapi access token
APIAI_ACCESS_TOKEN = os.environ.get('APIAI_DEVELOPER_ACCESS_TOKEN')
#APIAI_ACCESS_TOKEN = "696bcad329ed4327981a0ba711b4f663"

#set slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)

#set apiai client
apiai_client = apiai.ApiAI(APIAI_ACCESS_TOKEN)


# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"


def parse_slack_output(slack_rtm_output):
	output_list = slack_rtm_output

	if output_list and len(output_list) > 0:
		for output in output_list:
			# print "output: ", len(output.keys()), output , "\n\n", BOT_ID, "\n\n"
				if output and 'text' in output and AT_BOT in output['text']:
					# return text after the @ mention, whitespace removed
					return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
				elif output and 'text' in output and output['channel'].startswith('D') and not 'bot_id' in output:
					return output['text'].strip().lower(), output['channel']
	return None, None



def handle_command(command, channel):
	attachments = []
	response = "Not sure what you mean. \nPlease use the " + EXAMPLE_COMMAND + "* command with numbers :robot_face:"
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
                        "text": "Does this help?",
                        "attachment_type": "default",
                        "callback_id": "demo_button_id",
                        "fallback": "wowweee!",
                        "color": "#f44262",
                        "actions": [{
                                "name": "part_1",
                                "text": "Yes",
                                "type": "button",
                                "value": "val_1"
                                },{
                                "name": "part_2",
                                "text": "Partially",
                                "type": "button",
                                "value": "val_2"
                                },{
                                "name": "part_3",
                                "text": "No",
                                "type": "button",
                                "value": "val_3"
                                }
                        ]
                }]
	elif 'intentName' in ai_response['metadata'] and ai_response['metadata']['intentName'] == 'help':
		response = "Welcome. The best way to learn is by example. Follow this 2 step guide in how to use me."
		# msg = "To load your event data ask me this: \n Load event data from /home/ubuntu/data/events/event_data.csv\n\nTo Load your meta data ask me this: \n Load metadata from /home/ubuntu/data/meta\n\nClick 1 to continue"
		attachments = [{
			"text": "Click 1 if you have not loaded your data. Otherwise, please continue on to 2.",
			"attachment_type": "default",
			"callback_id": "demo_button_id",
			"fallback": "wowweee!",
			"color": "#f44262",
			"actions": [{
				"name": "part_1",
				"text": "1",
				"type": "button",
				"value": "val_1"
				},{
				"name": "part_2",
				"text": "2",
				"type": "button",
				"value": "val_2"
				},{
				"name": "part_3",
				"text": "3",
				"type": "button",
				"value": "val_3"
				}
			]
		}]
	elif command.startswith(EXAMPLE_COMMAND):
		response = "Sure...write some more code then I can do that!"
		attachments = [{
			"text": "Do you want to see a youtube video?",
			"attachment_type": "default",
			"callback_id": "demo_button_id",
			"fallback": "wowweee!",
			"color": "#dd2e4e",
			"actions": [{
				"name": "yes",
				"text": "Yes",
				"type": "button",
				"value": "yes"
				},{
				"name": "no",
				"text": "No",
				"type": "button",
				"value": "no"
				}
			]
		}]
	final_response="```" + response + "```"
	slack_client.api_call("chat.postMessage", channel=channel, text=final_response, as_user=True, attachments= attachments)



if __name__ == '__main__':
	READ_WEBSOCKET_DELAY = 0.5 #per second
	if slack_client.rtm_connect():
		print(BOT_NAME + " connected and running!")
		while True:
			rtm = slack_client.rtm_read()

			if rtm:
				print (rtm)

			command, channel = parse_slack_output(rtm)

			if command and channel:
				handle_command(command, channel)

			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print(BOT_NAME+ " not connected!")
