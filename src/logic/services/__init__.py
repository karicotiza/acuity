from pathlib import Path
from logic.services import recognition as __recognition
from logic.services import decoder as __decoder

decoder: __decoder.Decoder = __decoder.Decoder()

recognition: __recognition.IRecognitionModel = __recognition.XLSR53(
    path=Path('..', '..', 'model')
)
