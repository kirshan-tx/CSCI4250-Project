import sys
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import subprocess
import os

class ProgramRunner(QObject):
    def __init__(self):
        super().__init__()
        self.process = None  # Track the running process
        self.media_player = QMediaPlayer()

    @pyqtSlot()
    def run_program(self):
        if not getattr(self, 'running', False):  # Check if already running
            try:
                self.play_audio()
                self.running = True  # Set the flag to indicate the program is running
                program_path = os.path.join('currentAPI', 'Spotify', 'SpotifyVoiceAssistant.py')
                self.process = subprocess.Popen([sys.executable, program_path])  # Save the process handle
            except Exception as e:
                print(f"Error running program: {e}")
        else:
            print("Program is already running.")

    @pyqtSlot()
    def stop_program(self):
        if self.process:
            try:
                self.play_audio()
                self.process.terminate()  # Terminate the running program
                self.process.wait()  # Wait for the process to exit
                self.process = None  # Reset the process handle
                self.running = False  # Reset the running flag
                print("Program stopped.")
            except Exception as e:
                print(f"Error stopping program: {e}")
        else:
            print("No program running.")

    def play_audio(self):
        try:
            audio_file = os.path.join('ui', 'sound.mp3')  # Replace with the actual path to your MP3 file
            url = QUrl.fromLocalFile(audio_file)  # Load the audio file
            self.media_player.setMedia(QMediaContent(url))  # Set the media content
            self.media_player.play()  # Play the audio
        except Exception as e:
            print(f"Error playing audio: {e}")

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    program_runner = ProgramRunner()
    engine.rootContext().setContextProperty("programRunner", program_runner)
    qml_file = QUrl.fromLocalFile(os.path.join('ui', 'themes.qml'))  
    engine.load(qml_file)
    
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())