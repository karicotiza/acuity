from pathlib import Path as __Path
from torch import cuda as __cuda
from core.settings import NN_SETTINGS as __NN_SETTINGS
from logic.services import decoder as __decoder
from logic.services import converter as __converter
from logic.services import cache as __cache
from logic.services import recognition as __recognition


decoder: __decoder.Decoder = __decoder.Decoder()

if isinstance(__NN_SETTINGS['CONVERTER_FORMAT'], str):
    __format: str = __NN_SETTINGS['CONVERTER_FORMAT']

if isinstance(__NN_SETTINGS['CONVERTER_BITRATE'], str):
    __bitrate: str = __NN_SETTINGS['CONVERTER_BITRATE']

if isinstance(__NN_SETTINGS['CONVERTER_MONO'], bool):
    __mono: bool = __NN_SETTINGS['CONVERTER_MONO']

converter: __converter.Convertor = __converter.Convertor(
    format=__format,
    bitrate=__bitrate,
    mono=__mono,
)


cache: __cache.Cache = __cache.Cache()


if isinstance(__NN_SETTINGS['MODEL_PATH'], __Path):
    __path: __Path = __NN_SETTINGS['MODEL_PATH']

if isinstance(__NN_SETTINGS['SAMPLE_RATE'], int):
    __sample_rate: int = __NN_SETTINGS['SAMPLE_RATE']

if __cuda.is_available():
    recognition: __recognition.IRecognitionModel = __recognition.XLSR53_GPU(
        path=__path,
        sample_rate=__sample_rate,
    )

else:
    recognition: __recognition.IRecognitionModel = __recognition.XLSR53_CPU(
        path=__path,
        sample_rate=__sample_rate,
    )
