from watson_developer_cloud import conversation_v1

USERNAME = "17f9272a-a613-4cd4-b4a2-d2997333d8e3"
PASSWORD = "lTzpYkbjTsKE"
WORKSPACE_ID = "a347dca1-629e-4bbb-af35-d51aae52bf7a"
context = {}

def handle_command(command):
    """Receives commands directed at the bot and determines if they are valid commands.
    If so, then acts on the commands. If not, returns back what it needs for clarification."""
    conversation = conversation_v1.ConversationV1(
        username = USERNAME,
        password = PASSWORD,
        version = '2016-06-20'
        )

    responseFromWatson = conversation.message(
        workspace_id = WORKSPACE_ID,
        message_input = {'text': command},
        context = context
        )

    print(responseFromWatson)

if __name__ == "__main__":
    handle_command("hello")
