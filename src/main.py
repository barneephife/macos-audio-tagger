import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QLabel, QLineEdit, QPushButton, QFileDialog, QSpinBox, QComboBox, QMessageBox
from PyQt6.QtCore import Qt
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC

class AudioTagger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Audio Metadata Editor')
        self.setGeometry(100, 100, 600, 400)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel('No file selected')
        select_button = QPushButton('Select File')
        select_button.clicked.connect(self.selectFile)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(select_button)
        layout.addLayout(file_layout)

        # Metadata fields
        self.fields = {}
        self.createField('title', 'Title', layout)
        self.createField('artist', 'Artist', layout)
        self.createField('albumartist', 'Album Artist', layout)
        self.createField('album', 'Album', layout)
        
        # Disc and track numbers
        disc_track_layout = QHBoxLayout()
        self.createSpinField('discnumber', 'Disc Number', disc_track_layout)
        self.createSpinField('tracknumber', 'Track Number', disc_track_layout)
        layout.addLayout(disc_track_layout)

        self.createField('date', 'Year', layout)
        self.createField('genre', 'Genre', layout)
        self.createField('comment', 'Comment', layout)
        self.createField('composer', 'Composer', layout)

        # Save button
        save_button = QPushButton('Save Changes')
        save_button.clicked.connect(self.saveChanges)
        layout.addWidget(save_button)

    def createField(self, key, label, layout):
        field_layout = QHBoxLayout()
        field_layout.addWidget(QLabel(f'{label}:'))
        self.fields[key] = QLineEdit()
        field_layout.addWidget(self.fields[key])
        layout.addLayout(field_layout)

    def createSpinField(self, key, label, layout):
        field_layout = QHBoxLayout()
        field_layout.addWidget(QLabel(f'{label}:'))
        self.fields[key] = QSpinBox()
        self.fields[key].setRange(0, 999)
        field_layout.addWidget(self.fields[key])
        layout.addLayout(field_layout)

    def selectFile(self):
        fname, _ = QFileDialog.getOpenFileName(
            self,
            'Select Audio File',
            '',
            'Audio Files (*.mp3 *.m4a *.flac)'
        )
        if fname:
            self.current_file = fname
            self.file_label.setText(fname.split('/')[-1])
            self.loadMetadata()

    def loadMetadata(self):
        if not self.current_file:
            return

        audio = File(self.current_file, easy=True)
        if audio is None:
            QMessageBox.warning(self, 'Error', 'Could not load audio file metadata')
            return

        # Clear all fields
        for field in self.fields.values():
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QSpinBox):
                field.setValue(0)

        # Load metadata based on file type
        if isinstance(audio, EasyID3):
            self.loadID3Metadata(audio)
        elif isinstance(audio, MP4):
            self.loadMP4Metadata(audio)
        elif isinstance(audio, FLAC):
            self.loadFLACMetadata(audio)

    def loadID3Metadata(self, audio):
        mapping = {
            'title': 'title',
            'artist': 'artist',
            'albumartist': 'albumartist',
            'album': 'album',
            'date': 'date',
            'genre': 'genre',
            'composer': 'composer'
        }

        for field, tag in mapping.items():
            if tag in audio:
                self.fields[field].setText(audio[tag][0])

        # Handle disc and track numbers
        if 'discnumber' in audio:
            disc_num = audio['discnumber'][0].split('/')[0]
            self.fields['discnumber'].setValue(int(disc_num))

        if 'tracknumber' in audio:
            track_num = audio['tracknumber'][0].split('/')[0]
            self.fields['tracknumber'].setValue(int(track_num))

    def saveChanges(self):
        if not self.current_file:
            return

        try:
            audio = File(self.current_file, easy=True)
            if audio is None:
                raise Exception('Could not load audio file')

            # Update metadata based on file type
            if isinstance(audio, EasyID3):
                self.saveID3Metadata(audio)
            elif isinstance(audio, MP4):
                self.saveMP4Metadata(audio)
            elif isinstance(audio, FLAC):
                self.saveFLACMetadata(audio)

            QMessageBox.information(self, 'Success', 'Metadata updated successfully')

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to save metadata: {str(e)}')

    def saveID3Metadata(self, audio):
        mapping = {
            'title': 'title',
            'artist': 'artist',
            'albumartist': 'albumartist',
            'album': 'album',
            'date': 'date',
            'genre': 'genre',
            'composer': 'composer'
        }

        for field, tag in mapping.items():
            value = self.fields[field].text().strip()
            if value:
                audio[tag] = value

        # Handle disc and track numbers
        disc_num = self.fields['discnumber'].value()
        if disc_num > 0:
            audio['discnumber'] = str(disc_num)

        track_num = self.fields['tracknumber'].value()
        if track_num > 0:
            audio['tracknumber'] = str(track_num)

        audio.save()

def main():
    app = QApplication(sys.argv)
    ex = AudioTagger()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()