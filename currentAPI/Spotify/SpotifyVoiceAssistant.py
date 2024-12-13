import speech_recognition as sr
import controller as ct
import sys
import pyttsx3

def text_to_speech(text):
    """Convert text to speech using pyttsx3 and play directly"""
    engine = pyttsx3.init()
    engine.say(text)  # Convert text to speech
    engine.runAndWait()  # Wait until speech is finished

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        text_to_speech("Initializing microphone...")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def listen_for_speech(self, prompt=None):
        if prompt:
            text_to_speech(f"\n {prompt}")
        with self.mic as source:
            try:
                # text_to_speech("Listening...")
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio).lower()
                text_to_speech(f"You said: '{text}'")
                return text
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                text_to_speech("Sorry, couldn't understand. Please try again.")
                return None
            except sr.RequestError as e:
                text_to_speech(f"Connection error: {e}")
                return None

    def get_yes_no(self, prompt):
        while True:
            response = self.listen_for_speech(prompt + " Say 'yes' or 'no'.")
            if response in ["yes", "no"]:
                return response == "yes"
            text_to_speech("Please respond with 'yes' or 'no'.")

class PlaylistCreator:
    def __init__(self):
        self.speech_handler = SpeechHandler()

    def create_playlist(self):
        text_to_speech("\nCreating a new playlist...")

        # Get and confirm the playlist name
        while True:
            name = self.speech_handler.listen_for_speech("What name would you like for your playlist?")
            if name and self.speech_handler.get_yes_no(f"You said '{name}'. Is that correct?"):
                break

        # Get public and collaborative settings
        is_public = self.speech_handler.get_yes_no("Should the playlist be public?")
        is_collaborative = self.speech_handler.get_yes_no("Should the playlist be collaborative?")
        
        # Get description if wanted
        description = ""
        if self.speech_handler.get_yes_no("Would you like to add a description?"):
            description = self.speech_handler.listen_for_speech("Please say your description") or ""

        # Show and confirm the playlist details
        text_to_speech("\nPlaylist Details:")
        text_to_speech(f"Name: {name}")
        text_to_speech(f"Public: {'Yes' if is_public else 'No'}")
        text_to_speech(f"Collaborative: {'Yes' if is_collaborative else 'No'}")
        if description:
            text_to_speech(f"Description: {description}")
        text_to_speech("Playlist created successfully!")
        if description:
            ct.createPlaylist(name, is_public, is_collaborative, description)
        else:
            ct.createPlaylist(name, is_public, is_collaborative)

class SpotifyVoiceAssistant:
    def __init__(self):
        self.speech_handler = SpeechHandler()
        self.playlist_creator = PlaylistCreator()
        
    def show_help(self):
        """Display available commands"""
        text_to_speech("\nAvailable commands:")
        text_to_speech("• Play - Resume playback")
        text_to_speech("• Pause - Pause playback")
        text_to_speech("• Skip/Next - Play next track")
        text_to_speech("• Previous/Go back - Play previous track")
        text_to_speech("• Shuffle on/off - Toggle shuffle mode")
        text_to_speech("• Repeat Song - Toggle to repeat song")
        text_to_speech("• Repeat Playlist - Toggle to repeat playlist")
        text_to_speech("• Repeat off - Toggles off repeat")
        text_to_speech("• Create - Start playlist creation")
        text_to_speech("• Help - Show this help message")
        text_to_speech("• Exit - Quit the program")
        # new additions
        text_to_speech("• Volume up - Raise the volume")
        text_to_speech("• Volume down - Lower the volume")
        text_to_speech("• Mute - Mute the volume")
        text_to_speech("• Max volume - Set volume to the maximum")
        text_to_speech("• Add current song to playlist - Add the currently playing song to a playlist")
        text_to_speech("• Add previous song to playlist - Add the previously played song to a playlist")
        text_to_speech("• Play playlist - Play a specified playlist")
        text_to_speech("• Advance - Jump to a specific time in the current track")

    def process_command(self, command):
        """Process voice commands for Spotify control"""
        try:
            if "play playlist" in command:
                playlist_name = self.speech_handler.listen_for_speech("Please say the name of the playlist you want to play.")
                if playlist_name:
                    text_to_speech(f"Playing playlist: {playlist_name}")
                    ct.playPlaylist(playlist_name)
                else:
                    text_to_speech("Could not recognize the playlist name. Please try again.")
                
            elif "pause" in command:
                text_to_speech("Paused")
                ct.pauseSong()
            
            elif "skip" in command or "next" in command:
                text_to_speech("Skipping to next track")
                ct.skipSong()
            
            elif "add" in command and "previous" in command:
                name = self.speech_handler.listen_for_speech("What playlist do you want to add to?")
                if name:
                    text_to_speech(f"Adding to {name}")
                    ct.addPreviousSongToPlaylist(name)
                else:
                    text_to_speech("Could not recognize the playlist name. Please try again.")
                
            elif "add" in command and "current" in command:
                name = self.speech_handler.listen_for_speech("What playlist do you want to add to?")
                if name:
                    text_to_speech(f"Adding to {name}")
                    ct.addCurrentSongToPlaylist(name)
                else:
                    text_to_speech("Could not recognize the playlist name. Please try again.")
                
            elif "previous" in command or "go back" in command:
                text_to_speech("Playing previous track")
                ct.previousSong()
            
            elif "shuffle on" in command:
                text_to_speech("Shuffle enabled")
                ct.shuffle(True)
            
            elif "shuffle off" in command:
                text_to_speech("Shuffle disabled")
                ct.shuffle(False)
            
            elif "repeat off" in command:
                text_to_speech("Repeat disabled")
                ct.repeat('off')
            
            elif "repeat song" in command:
                text_to_speech("Repeating song")
                ct.repeat('song')
            
            elif "repeat playlist" in command:
                text_to_speech("Setting playlist to repeat")
                ct.repeat('playlist')
            
            elif "create" in command:
                text_to_speech("Creating playlist")
                self.playlist_creator.create_playlist()
                
            elif "volume up" in command:
                text_to_speech("Raising volume")
                ct.volumeUp()
                
            elif "volume down" in command:
                text_to_speech("Lowering volume")
                ct.volumeDown()
            
            elif "mute" in command:
                text_to_speech("Muting")
                ct.mute()
            
            elif "max volume" in command:
                text_to_speech("Setting max volume.")
                ct.maxVolume()
                
            elif "advance" in command:
                seek_time = self.speech_handler.listen_for_speech("What time do you want to advance/seek to?")
                text_to_speech(f"Seeking to {seek_time}")
                ct.seekTo(int(seek_time))
                
            elif "play" in command:
                text_to_speech("Playing")
                ct.playSong()
            
            elif "help" in command:
                self.show_help()
            
            else:
                text_to_speech("Unknown command. Say 'help' for available commands.")
        except Exception as e:
            text_to_speech(f"Error processing command: {e}")

    def run(self):
        text_to_speech("\nVoice-Controlled Spotify Assistant")
        text_to_speech("Say 'help' for available commands or 'exit' to quit.")
        
        while True:
            command = self.speech_handler.listen_for_speech()
            if not command:
                continue
            if "exit" in command:
                text_to_speech("\nGoodbye!")
                sys.exit(0)
            else:
                self.process_command(command)

def main():
    assistant = SpotifyVoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
