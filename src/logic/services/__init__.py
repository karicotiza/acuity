from pathlib import Path
from logic.services import decoder as __decoder
from logic.services import converter as __converter
from logic.services import cache as __cache
from logic.services import recognition as __recognition


decoder: __decoder.Decoder = __decoder.Decoder()

converter: __converter.Convertor = __converter.Convertor()

cache: __cache.Cache = __cache.Cache()

recognition: __recognition.IRecognitionModel = __recognition.XLSR53(
    path=Path('..', '..', 'model')
)
