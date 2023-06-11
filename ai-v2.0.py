import os
import logging
import argparse
import json
import google.auth
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

import google_assistant_helpers as assistant_helpers
import google_assistant_helpers.auth_helpers as auth_helpers
import google_assistant_helpers.audio_helpers as audio_helpers
import google_assistant_helpers.device_helpers as device_helpers

from tenacity import retry, stop_after_attempt, retry_if_exception

import grpc
import google.rpc.code_pb2 as error_codes
import google.rpc.status_pb2 as status

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)

# Device configurations
device_model_id = 'your-device-model-id'
device_id = 'your-device-id'

# Path to your client secret file
client_secrets = 'path/to/client_secret.json'

# Path to save the OAuth2 credentials
credentials_file = 'path/to/credentials.json'

# Audio recording configurations
audio_sample_rate = 16000
audio_sample_width = 2
audio_iter_size = 320
audio_block_size = 640
audio_flush_size = 1280

# Logging configurations
logging.basicConfig(level=logging.DEBUG)

# Google Assistant GRPC configurations
grpc_channel = None
grpc_deadline = None

# Setup OAuth2 credentials
credentials = auth_helpers.load_credentials(credentials_file, scopes=[
    'https://www.googleapis.com/auth/assistant-sdk-prototype',
    'https://www.googleapis.com/auth/gcm',
    'https://www.googleapis.com/auth/grpc',
])

# Create gRPC channel
grpc_channel = auth_helpers.create_grpc_channel(
    'embeddedassistant.googleapis.com',
    credentials
)

# Device configuration
device_handler = device_helpers.DeviceRequestHandler(device_id)

# Create and start the audio recording thread
audio_recorder = audio_helpers.AudioRecorder(
    sample_rate=audio_sample_rate,
    sample_width=audio_sample_width,
    block_size=audio_block_size,
    flush_size=audio_flush_size
)

# Create an assistant
class SampleAssistant(object):
    def __init__(self, channel):
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(channel)
        self.deadline = 60 * 3 + 5

    @retry(reraise=True, stop=stop_after_attempt(3), retry=retry_if_exception())
    def assist(self, text_query):
        continue_conversation = False
        device_actions_futures = []
        self.audio_inject = None

        # Configure the assistant request
        self.device_config = device_helpers.DeviceConfig(
            device_model_id=device_model_id,
            device_id=device_id,
            device_notification_supported=True,
        )
        self.audio_config = device_helpers.AudioInputConfig(
            encoding=device_helpers.AudioEncoding.LINEAR16,
            sample_rate_hertz=audio_sample_rate,
        )
        self.dialog_state_in = embedded_assistant_pb2.DialogStateIn(
            language_code='en-US',
            conversation_state=b'',
            is_new_conversation=True,
        )
        self.query_input = embedded_assistant_pb2.QueryInput(
            text=embedded_assistant_pb2.TextInput(
                text=text_query,
                language_code='en-US',
            )
        )
        self.mic_state = embedded_assistant_pb2.ConverseState(
            conversation_state=b'',
            microphone_mode=embedded_assistant_pb2.ConverseState.CLOSE_MICROPHONE,
        )
        self.audio_out_config = embedded_assistant_pb2.AudioOutConfig(
            encoding=device_helpers.AudioEncoding.LINEAR16,
            sample_rate_hertz=audio_sample_rate,
            volume_percentage=0,
        )

        # Start the conversation
        self.assistant.Assist.side_effect = self._assistant_assist
        self.audio_generator = self._audio_generator()

        # Send the first ConverseRequest
        self.assistant.Converse(self.gen_converse_request())

        return continue_conversation, device_actions_futures

    def gen_converse_request(self):
        converse_state = None
        if self.audio_inject:
            converse_state = embedded_assistant_pb2.ConverseState(
                conversation_state=self.dialog_state_out.conversation_state,
                microphone_mode=embedded_assistant_pb2.ConverseState.DIALOG_FOLLOW_ON,
            )
            config = embedded_assistant_pb2.ConverseConfig(
                audio_in_config=self.audio_config,
                audio_out_config=self.audio_out_config,
                converse_state=converse_state,
            )
            return embedded_assistant_pb2.ConverseRequest(config=config, audio_in=self.audio_inject)
        else:
            config = embedded_assistant_pb2.ConverseConfig(
                audio_in_config=self.audio_config,
                audio_out_config=self.audio_out_config,
                converse_state=converse_state,
            )
            return embedded_assistant_pb2.ConverseRequest(config=config)

    def _audio_generator(self):
        with audio_recorder:
            while True:
                if self.mic_state.microphone_mode == embedded_assistant_pb2.ConverseState.DIALOG_FOLLOW_ON and not self.audio_inject:
                    chunk = audio_recorder.get_frame()
                else:
                    chunk = self.audio_inject
                    self.audio_inject = None

                if chunk:
                    yield embedded_assistant_pb2.AudioIn(audio_binary=chunk)

    def _assistant_assist(self, assist_request):
        if assist_request.audio_in:
            audio_recorder.write_frames(assist_request.audio_in.audio_binary)
        if assist_request.dialog_state_in.conversation_state:
            self.dialog_state_in.conversation_state = assist_request.dialog_state_in.conversation_state
        if assist_request.dialog_state_in.volume_percentage != 0:
            self.audio_out_config.volume_percentage = assist_request.dialog_state_in.volume_percentage

        self.dialog_state_out = None
        if len(assist_request.audio_in.audio_binary) == 0:
            self.mic_state.microphone_mode = embedded_assistant_pb2.ConverseState.CLOSE_MICROPHONE
        elif self.mic_state.microphone_mode == embedded_assistant_pb2.ConverseState.CLOSE_MICROPHONE:
            self.mic_state.microphone_mode = embedded_assistant_pb2.ConverseState.OPEN_MICROPHONE

        for resp in self.assistant.Assist(self.gen_assist_request()):
            if resp.dialog_state_out.conversation_state:
                self.dialog_state_out.conversation_state = resp.dialog_state_out.conversation_state
            if resp.dialog_state_out.volume_percentage != 0:
                self.audio_out_config.volume_percentage = resp.dialog_state_out.volume_percentage
            if resp.audio_out.audio_data:
                yield resp.audio_out.audio_data
            if resp.dialog_state_out.microphone_mode == embedded_assistant_pb2.DialogStateOut.CLOSE_MICROPHONE:
                self.mic_state.microphone_mode = embedded_assistant_pb2.ConverseState.CLOSE_MICROPHONE
                if resp.dialog_state_out.supplemental_display_text:
                    print(resp.dialog_state_out.supplemental_display_text)
                if resp.dialog_state_out.conversation_state:
                    continue_conversation = True
                    device_actions_futures = device_handler(device_id, resp.dialog_state_out.conversation_state,
                                                            self.device_config)

                    return continue_conversation, device_actions_futures

        continue_conversation = False
        device_actions_futures = []
        return continue_conversation, device_actions_futures

    def gen_assist_request(self):
        if self.mic_state.microphone_mode == embedded_assistant_pb2.ConverseState.OPEN_MICROPHONE:
            self.audio_in_config.encoding = embedded_assistant_pb2.AudioInConfig.LINEAR16
            self.audio_in_config.sample_rate_hertz = audio_sample_rate
            self.audio_in_config.volume_percentage = 0
            self.audio_in_config.sample_rate_hertz = audio_sample_rate
            self.audio_in_config.sample_width = audio_sample_width
            self.audio_in_config.iter_size = audio_iter_size
            self.audio_in_config.block_size = audio_block_size
            self.audio_in_config.flush_size = audio_flush_size
            self.audio_inject = None
        elif self.mic_state.microphone_mode == embedded_assistant_pb2.ConverseState.CLOSE_MICROPHONE:
            self.audio_in_config.encoding = embedded_assistant_pb2.AudioInConfig.LINEAR16
            self.audio_in_config.sample_rate_hertz = audio_sample_rate
            self.audio_in_config.volume_percentage = 0
            self.audio_in_config.sample_rate_hertz = audio_sample_rate
            self.audio_in_config.sample_width = audio_sample_width
            self.audio_in_config.iter_size = audio_iter_size
            self.audio_in_config.block_size = audio_block_size
            self.audio_in_config.flush_size = audio_flush_size
            self.audio_inject = b''

        converse_state = embedded_assistant_pb2.ConverseState(
            conversation_state=self.dialog_state_in.conversation_state,
            microphone_mode=self.mic_state.microphone_mode,
        )
        config = embedded_assistant_pb2.ConverseConfig(
            audio_in_config=self.audio_in_config,
            audio_out_config=self.audio_out_config,
            converse_state=converse_state,
        )

        return embedded_assistant_pb2.AssistRequest(config=config, audio_in=self.audio_generator())

# Handle the conversation
def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--query',
        type=str,
        default='Hello',
        help='Query to send to the Assistant'
    )
    args = parser.parse_args()

    with SampleAssistant(grpc_channel) as assistant:
        continue_conversation, _ = assistant.assist(args.query)

# Run the program
if __name__ == '__main__':
    main()
