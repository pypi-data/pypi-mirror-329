import wave

import pyaudio
import librosa
import soundfile as sf
import speech_recognition as sr
import threading

from Orange.data import Domain, StringVariable, Table

import Orange.data
from AnyQt.QtCore import QTimer
from AnyQt.QtWidgets import QApplication
from AnyQt.QtWidgets import QPushButton
from AnyQt.QtWidgets import (
    QTextEdit,
    QFileDialog, QMessageBox
)
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output


class OWSpeech_To_Text(widget.OWWidget):
    name = "Speech To Text"
    description = "Convert speech (MP3/WAV) to text and output to Orange Data Mining"
    icon = "icons/speech_to_text.png"
    priority = 1001


    class Outputs:
        data = Output("Data", Orange.data.Table)


    def __init__(self):
        super().__init__()

        # **Déplacer le contenu vers self.mainArea**
        self.mainArea.layout().setSpacing(10)

        # Zone de texte pour afficher le texte extrait
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText("Texte transcrit ici...")
        self.text_area.setReadOnly(True)

        self.button_load = QPushButton("📂 Charger un fichier MP3/WAV", self)
        self.button_load.clicked.connect(self.load_audio_file)

        self.button_record = QPushButton("🎤 Enregistrer", self)
        self.button_record.clicked.connect(self.start_recording)

        self.button_stop = QPushButton("🛑 Arrêter", self)
        self.button_stop.clicked.connect(self.stop_recording)
        self.button_stop.setEnabled(False)

        self.button_process = QPushButton("📝 Transcrire", self)
        self.button_process.clicked.connect(self.process_recording)
        self.button_process.setEnabled(False)  # Désactivé au début

        # **Ajout des widgets à la zone principale (mainArea)**
        self.mainArea.layout().addWidget(self.text_area)
        self.mainArea.layout().addWidget(self.button_load)
        self.mainArea.layout().addWidget(self.button_record)
        self.mainArea.layout().addWidget(self.button_stop)
        self.mainArea.layout().addWidget(self.button_process)

        # Variables pour l'enregistrement
        self.audio_filename = "recorded_audio.wav"
        self.recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []

    def load_audio_file(self):
        """Charge un fichier MP3 ou WAV et effectue la reconnaissance vocale."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier audio", "", "Fichiers Audio (*.mp3 *.wav)")
        if not file_path:
            return

        if file_path.endswith(".mp3"):
            self.text_area.setText("🔄 Conversion MP3 → WAV en cours...")
            file_path = self.convert_mp3_to_wav(file_path)

        if not file_path:
            QMessageBox.warning(self, "Erreur", "Impossible de convertir le fichier MP3 en WAV.")
            return

        self.transcribe_audio(file_path)

    def convert_mp3_to_wav(self, mp3_path):
        """Convertit un fichier MP3 en WAV pour la transcription avec librosa."""
        try:
            y, sr = librosa.load(mp3_path, sr=44100)  # Charger le MP3
            wav_path = mp3_path.replace(".mp3", ".wav")
            sf.write(wav_path, y, sr)  # Sauvegarde en WAV
            return wav_path
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Échec de la conversion MP3 : {e}")
            return None

    def start_recording(self):
        """Démarre l'enregistrement audio."""
        if self.recording:
            return

        self.recording = True
        self.frames = []

        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1,
                                      rate=44100, input=True,
                                      frames_per_buffer=1024)

        self.text_area.setText("🎤 Enregistrement en cours... Cliquez sur 'Arrêter' pour terminer.")
        self.button_record.setEnabled(False)
        self.button_stop.setEnabled(True)

        # **Démarrer l’enregistrement sur un thread séparé**
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def record_audio(self):
        """Boucle d'acquisition audio qui stocke les données en temps réel."""
        while self.recording:
            try:
                data = self.stream.read(1024, exception_on_overflow=False)
                self.frames.append(data)
            except IOError as e:
                print(f"Erreur audio : {e}")
                break

    def stop_recording(self):
        """Arrête l'enregistrement audio et sauvegarde les données."""
        if not self.recording:
            return

        self.recording = False
        self.recording_thread.join()  # Attendre la fin du thread avant de fermer

        self.stream.stop_stream()
        self.stream.close()

        if not self.frames:
            self.text_area.setText("❌ Aucun son enregistré. Réessayez.")
            self.button_record.setEnabled(True)
            self.button_stop.setEnabled(False)
            return

        # Sauvegarde du fichier WAV
        with wave.open(self.audio_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))

        self.text_area.setText("✅ Enregistrement terminé. Cliquez sur 'Transcrire' pour convertir en texte.")
        self.button_record.setEnabled(True)
        self.button_stop.setEnabled(False)
        self.button_process.setEnabled(True)

    def process_recording(self):
        """Transcrit l'enregistrement effectué."""
        self.transcribe_audio(self.audio_filename)

    def transcribe_audio(self, file_path):
        """Effectue la reconnaissance vocale sur un fichier audio."""
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            self.text_area.setText("🔄 Traitement en cours...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Amélioration du bruit ambiant
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            if not text.strip():
                raise sr.UnknownValueError
            self.text_area.setText(f"📜 Texte extrait : {text}")
            self.send_output(text)
        except sr.UnknownValueError:
            self.text_area.setText("❌ Impossible de comprendre l'audio.")
            self.send_output()
        except sr.RequestError as e:
            self.text_area.setText(f"⚠️ Erreur Google Speech : {e}")

    def send_output(self, text):
        """Envoie le texte transcrit sous forme de tableau Orange Data."""
        print("Texte", text)
        if text == "":
            text = "No Input"
        data = [[]]
        domain = Domain([],
                        metas=[StringVariable('Texte')])
        self.Outputs.data.send(Table.from_numpy(domain, data, metas=[[text]]))

    def closeEvent(self, event):
        """Ferme correctement l’application en libérant les ressources audio."""
        self.audio.terminate()
        event.accept()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = OWSpeech_To_Text()
    window.show()
    sys.exit(app.exec_())