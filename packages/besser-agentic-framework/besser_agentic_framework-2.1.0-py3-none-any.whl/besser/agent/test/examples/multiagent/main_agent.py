# You may need to add your working directory to the Python path. To do so, uncomment the following lines of code
# import sys
# sys.path.append("/Path/to/directory/agentic-framework") # Replace with your directory path
import base64
import logging

from besser.agent.core.agent import Agent
from besser.agent.core.file import File
from besser.agent.core.session import Session
from besser.agent.exceptions.logger import logger

# Configure the logging module (optional)
logger.setLevel(logging.INFO)

# Create the agent
agent = Agent('main_agent')
# Load agent properties stored in a dedicated file
agent.load_properties('../config.ini')
# Define the platform your agent will use
websocket_platform = agent.use_websocket_platform(use_ui=True)

# STATES

initial_state = agent.new_state('initial_state', initial=True)
receive_code_state = agent.new_state('receive_code_state')
awaiting_request_state = agent.new_state('awaiting_request_state')
send_request_state = agent.new_state('send_request_state')
final_state = agent.new_state('final_state')

# INTENTS

yes_intent = agent.new_intent('yes_intent', [
    'yes',
])

no_intent = agent.new_intent('bad_intent', [
    'no',
])


# STATES BODIES' DEFINITION + TRANSITIONS

def initial_body(session: Session):
    websocket_platform.reply(session, "Hello, upload your code before starting.")


def initial_fallback(session: Session):
    websocket_platform.reply(session, "Please, upload a file before starting.")


initial_state.set_body(initial_body)
initial_state.when_file_received_go_to(receive_code_state)
initial_state.set_fallback_body(initial_fallback)


def receive_code_body(session: Session):
    if session.file:
        # Receiving a code file on the first interaction
        file: File = session.file
        code = base64.b64decode(file.base64).decode('utf-8')
        if session.file.type == 'text/x-python':
            code = f"```python\n{code}\n```"
        session.set('code', code)
        session.file = None
    elif session.get('new_code'):
        # Receiving an updated code after finishing the agent workflow
        session.set('code', session.get('new_code'))
    websocket_platform.reply(session, "Thanks, I stored your code in my database. This is how it looks like:")
    websocket_platform.reply(session, session.get('code'))


receive_code_state.set_body(receive_code_body)
receive_code_state.go_to(awaiting_request_state)


def awaiting_request_body(session: Session):
    session.delete('new_code')
    websocket_platform.reply(session, "How can I assist you?")


awaiting_request_state.set_body(awaiting_request_body)
awaiting_request_state.when_no_intent_matched_go_to(send_request_state)


def send_request_body(session: Session):
    websocket_platform.reply(session, "Let's see what I can do...")
    session.send_message_to_websocket(
        url='ws://localhost:8011',
        message={
            "request": session.message,
            "code": session.get('code')
        }
    )


send_request_state.set_body(send_request_body)
send_request_state.when_no_intent_matched_go_to(final_state)


def final_body(session: Session):
    new_code: str = session.message
    session.set('new_code', new_code)
    websocket_platform.reply(session, "Take a look at the new code:")
    websocket_platform.reply(session, new_code)
    websocket_platform.reply(session, "Do yoy want to merge the new code?")
    websocket_platform.reply_options(session, ['Yes', 'No'])


final_state.set_body(final_body)
final_state.when_intent_matched_go_to(yes_intent, receive_code_state)
final_state.when_intent_matched_go_to(no_intent, awaiting_request_state)

# RUN APPLICATION

if __name__ == '__main__':
    agent.run()
