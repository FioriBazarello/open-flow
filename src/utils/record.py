import pyaudio
import threading
import wave
import tempfile

class Record:
    def __init__(self, channels=1, rate=44100, chunk=1024, format=pyaudio.paInt16):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.format = format
        self.audio = None
        self.stream = None
        self.frames = []
        self.recording = False
        self._thread = None

    def start(self):
        if not self.recording:
            self.frames = []
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            self.recording = True
            self._thread = threading.Thread(
                target=self._record_audio,
                daemon=True,
            )
            self._thread.start()

    def stop(self, output_path=None):
        if self.recording:
            self.recording = False
            if self._thread:
                self._thread.join()
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.audio:
                self.audio.terminate()
                self.audio = None
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                output_path = temp_file.name
                temp_file.close()
            with wave.open(output_path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
            return output_path
        return None

    def toggle_recording(self):
        if self.recording:
            return self.stop()
        else:
            self.start()
            return None

    def _record_audio(self):
        while self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data) 