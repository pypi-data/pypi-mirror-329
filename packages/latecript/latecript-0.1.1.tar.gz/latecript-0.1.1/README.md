# Latecript

Latecript is a Python application that transcribes and translates audio from your input devices in real-time using the Speechmatics API. The application provides a Textual-based TUI for an interactive experience.


![Latecript Screenshot](assets/screenshot.png)

(Developped quick and dirty with the help of Copilot)

## Features

- **Real-Time Transcription:** Capture audio and transcribe speech in real-time.
- **Translation:** Translate transcribed text into different languages.
- **TUI Interface:** Interactive Textual UI for settings and displaying logs.
- **Configurable Settings:** Read credentials and configuration from a local JSON file.

## Requirements

- Python 3.12 or above
- [UV](https://github.com/uv-org/uv) (for dependency management)

## Getting your audio output as a usable input. 

### MacOs 

You can use BlackHole for audio loopback. It can be installed via brew: 
```bash
brew install blackhole-2ch
```

While using the app, chose "BlackHole 2ch" as your sound output. In order to still listen to what your mac sound output you can define a multi-output device (with you favourite output device + BlackHole 2ch) in the Audio MIDI setup.  


## Speechmatics API key 

You can generate your speechmatics API key from your user account in speechmatics. 

## Usage

To run Latecript, execute:

   ```bash
   uv run latecript 
   ```

You can provide an alternative settings file via the command line:

```bash
uv run latecript --settings_file /path/to/your/settings.json
```

 The settings file is a json file with the following structure:

```json
{
  "speechmatics_api_key": "Your Speechmatics API Key",
  "output_device": "Blackhole 2ch",
  "transcription_language": "fr",
  "translation_language": "en"
}
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open issues and submit pull requests for improvements and bug fixes. 

This app is not meant to be maintained and was developped in a quick and dirty way. 

## Acknowledgements

- [Speechmatics](https://www.speechmatics.com/) for the API and SDK.
- [Textual](https://github.com/Textualize/textual) for the TUI framework.
- [BlackHole](https://existential.audio/blackhole/) for audio loopback driver for mac. 

