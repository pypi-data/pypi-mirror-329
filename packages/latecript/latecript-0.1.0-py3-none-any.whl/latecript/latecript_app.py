from textual import on
from textual.app import App, ComposeResult
from textual.widgets import (
    Header,
    Footer,
    Log,
    Select,
    Static,
    Rule,
    TabbedContent,
    TabPane,
    Label,
    Input,
    TextArea,
    Switch,
)
from textual.containers import Horizontal, Vertical
from pydantic import BaseModel
from enum import Enum
import speechmatics
from .services import pyaudio_handler, speechmatics_handler
import httpx
from datetime import datetime


class Languages(str, Enum):
    FRENCH = "fr"
    ENGLISH = "en"


languages_select_list = [(Languages.FRENCH, 1), (Languages.ENGLISH, 2)]


class LatecriptSettings(BaseModel):
    speechmatics_api_key: str
    output_device: str
    input_language: Languages = Languages.FRENCH
    translation_language: Languages | None = Languages.ENGLISH


audio_processor = pyaudio_handler.AudioProcessor()


def stream_callback(in_data, frame_count, time_info, status):
    audio_processor.write_audio(in_data)
    return in_data, pyaudio_handler.pyaudio.paContinue


class LatecriptApp(App):
    BINDINGS = [
        ("t", "show_tab('transcript_tab')", "Transcript"),
        ("s", "show_tab('settings_tab')", "Settings"),
        ("q", "quit", "Quit"),
    ]

    CSS_PATH = "latecript_app.tcss"

    input_device = None
    speechmatics_websocket = None
    stream = None

    current_speaker = None
    current_translation_speaker = None

    def __init__(self, settings: LatecriptSettings | None = None) -> None:
        super().__init__()
        self.settings = settings

    def compose(self) -> ComposeResult:
        yield Header()

        with TabbedContent():
            with TabPane("Transcript", id="transcript_tab"):
                with Horizontal(classes="transcript_controls"):
                    yield Label("Transcript", classes="label")
                    yield Switch(value=False, id="transcript_switch", animate=True)
                with Horizontal():
                    with Vertical():
                        yield Static("Transcript")
                        yield TextArea(
                            "", id="transcriptwidget", name="Transcript", read_only=True
                        )
                    with Vertical():
                        yield Static("Translation")
                        yield TextArea(
                            "", id="translatewidget", name="Translation", read_only=True
                        )
            with TabPane("Settings", id="settings_tab"):
                with Horizontal(classes="settings_inputs_containers"):
                    yield Label("Speechmatics API Key:", classes="label")
                    yield Input(
                        id="speechmatics_api_key",
                        name="Speechmatics API Key",
                        value=self.settings.speechmatics_api_key
                        if self.settings
                        else "",
                        classes="config_input",
                    )
                yield Rule()
                with Horizontal(classes="settings_inputs_containers"):
                    yield Label("Input devices:", classes="label")
                    yield Select(
                        pyaudio_handler.get_devices_list(),
                        id="audio_devices",
                        name="Audio Devices",
                        value=pyaudio_handler.get_device_by_name(
                            self.settings.output_device
                        )
                        if self.settings
                        else 0,
                    )
                yield Rule()
                with Horizontal(classes="settings_inputs_containers"):
                    yield Label("Transcription:", classes="label")
                    yield Select(
                        languages_select_list,
                        value=1,
                        id="transcription_language",
                        name="Transcription Language",
                    )
                    yield Label("Translation:", classes="label")
                    yield Select(
                        languages_select_list,
                        value=2,
                        id="translation_language",
                        name="Translation Language",
                    )
                yield Rule()
            with TabPane("Log", id="log_tab"):
                yield Log(id="logwidget", name="Log")

        yield Footer()

    def on_mount(self) -> None:
        if self.settings is None:
            self.action_show_tab("settings_tab")

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab

    @on(Switch.Changed, "#transcript_switch")
    async def handle_transcript_switch(self, event: Switch.Changed) -> None:
        """Handle transcript switch toggle"""
        if event.value:
            self.update_log("Starting transcription...")
            input_device = self.query_one("#audio_devices", Select).value
            sample_rate = int(
                pyaudio_handler.get_device_info_by_index(input_device)[
                    "defaultSampleRate"
                ]
            )

            self.stream = pyaudio_handler.get_stream(
                input_device_index=input_device,
                rate=sample_rate,
                stream_callback=stream_callback,
                channels=1,  # pyaudio_handler.get_device_info_by_index(input_device)["maxInputChannels"]
            )

            speechmatics_api_key = self.query_one("#speechmatics_api_key", Input).value
            transcript_language_selected_index = self.query_one(
                "#transcription_language", Select
            ).value
            translation_language_selected_index = self.query_one(
                "#translation_language", Select
            ).value

            transcript_language = languages_select_list[
                transcript_language_selected_index - 1
            ][0].value

            translation_language = languages_select_list[
                translation_language_selected_index - 1
            ][0].value

            self.update_log(f"Transcript language: {transcript_language}")

            # transcript_language = "fr"
            # translation_language = "en"

            self.speechmatics_websocket = speechmatics_handler.get_speechmatics_client(
                speechmatics_api_key=speechmatics_api_key,
                transcript_language=transcript_language,
            )

            transcription_config = speechmatics_handler.get_transcription_config(
                transcript_language=transcript_language,
                translation_language=translation_language,
                max_delay=1,
            )

            self.speechmatics_websocket.add_event_handler(
                event_name=speechmatics.models.ServerMessageType.AddTranscript,
                event_handler=self.update_transcript,
            )

            self.speechmatics_websocket.add_event_handler(
                event_name=speechmatics.models.ServerMessageType.AddTranslation,
                event_handler=self.update_translation,
            )

            settings = speechmatics_handler.get_audio_config(
                sample_rate=sample_rate,
            )

            try:
                self.run_worker(
                    self.speechmatics_websocket.run(
                        audio_processor, transcription_config, settings
                    )
                )
            except KeyboardInterrupt as e:
                print("Transcription stopped")
                raise e
            except httpx.HTTPStatusError as e:
                self.log_in_transcript(f"HTTPStatusError: {e}")
            except Exception as e:
                raise e

        else:
            # User toggled OFF
            self.update_log("Stopping transcription...")
            # Stop websocket
            if self.speechmatics_websocket:
                self.speechmatics_websocket.stop()
            # Stop/close stream
            if self.stream:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
                self.stream = None

            if self.current_speaker is not None:
                self.current_speaker = None

            if self.current_translation_speaker is not None:
                self.current_translation_speaker = None

            self.update_log("Transcription and translation stopped.")

            transcript_log = self.query_one("#transcriptwidget", TextArea)
            transcript_log.move_cursor(transcript_log.document.end)
            transcript_log.insert("\n\n---------\n\n")

            translate_log = self.query_one("#translatewidget", TextArea)
            translate_log.move_cursor(translate_log.document.end)
            translate_log.insert("\n\n---------\n\n")

    def update_transcript(self, msg) -> None:
        transcript_log = self.query_one("#transcriptwidget", TextArea)

        for result in msg["results"]:
            speaker = result["alternatives"][0]["speaker"]
            content = result["alternatives"][0]["content"]
            transcript_log.move_cursor(transcript_log.document.end)

            if self.current_speaker != speaker:
                if self.current_speaker is not None:
                    transcript_log.insert("\n\n")
                transcript_log.insert(f"{speaker}: ")
                self.current_speaker = speaker

            transcript_log.insert(content + " ")

    def update_translation(self, msg) -> None:
        translate_log = self.query_one("#translatewidget", TextArea)

        for result in msg.get("results", []):
            speaker = result["speaker"]
            content = result["content"]
            translate_log.move_cursor(translate_log.document.end)

            if self.current_translation_speaker != speaker:
                if self.current_translation_speaker is not None:
                    translate_log.insert("\n\n")
                translate_log.insert(f"{speaker}: ")
                self.current_translation_speaker = speaker

            translate_log.insert(content + " ")

    def update_log(self, message: str) -> None:
        log_widget = self.query_one("#logwidget", Log)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_widget.write_line(f"[{timestamp}] {message}")
