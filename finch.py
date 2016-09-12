import os
import time
from slackclient import SlackClient

# constants
BOT_NAME        = "finch"
BOT_ID          = os.environ.get("BOT_ID")
SLACK_BOT_TOKEN = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
AT_BOT          = "<@" + BOT_ID + ">"
ANON_COMMAND    = "-a"

# instantiate Slack client
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))

# TODO: grab username from message to be used in handle_command text
def parse_input(slack_rtm_output):
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			if output and "text" in output and AT_BOT in output["text"]: # if type text and bot is mentioned
				content = output["text"].split(AT_BOT)[1].strip().lower() # text after the @ mention, whitespace removed
				return content, output["channel"]
	return None, None

def handle_command(content, channel):
	default_response = "Thanks! Your response has been *recorded to be discussed at our next meeting*."

	# parse out command
	if content.startswith(ANON_COMMAND):
		command = ANON_COMMAND
		content = content.split(ANON_COMMAND)[1].strip().lower()
	else:
		command = ""

	# evaluate content text
	if content == "":
		response = "*You didn't write anything.* :angry: Mention me `@finch [message]` along with a thought or question that you want to discuss! You can also use `@finch -a [message]` to submit an anonymous response."
	else:
		# TODO: send text to Google Sheets

		if command == ANON_COMMAND:
			response = default_response + " _Submitted anonymously_"
		else:
			response = default_response


	slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1 # delay between reading from firehose (in seconds)
	if slack_client.rtm_connect():
		print("Finch connected and running!")
		while True:
			content, channel = parse_input(slack_client.rtm_read())
			if channel:
				handle_command(content, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")
