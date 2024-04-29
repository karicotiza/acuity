import librosa
import torch

from io import BytesIO
from numpy import ndarray
from pathlib import Path
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor  # type: ignore
from transformers.feature_extraction_utils import BatchFeature  # type: ignore
from transformers.modeling_outputs import CausalLMOutput  # type: ignore


class IRecognitionModel:

    def recognize(self, data: BytesIO) -> str:
        raise NotImplementedError


class XLSR53(IRecognitionModel):
    __necessary_files: list[str] = [
        'config.json',
        'preprocessor_config.json',
        'pytorch_model.bin',
        'vocab.json',
    ]

    __link: str = (
        'https://huggingface.co/jonatasgrosman/' +
        'wav2vec2-large-xlsr-53-english/tree/main'
    )

    def __init__(self, path: Path, sample_rate: int) -> None:
        self.__path = path

        self.__validate()

        self.__processor = Wav2Vec2Processor.from_pretrained(path)
        self.__model = Wav2Vec2ForCTC.from_pretrained(path)
        self.__sample_rate = sample_rate

    def __validate(self) -> None:
        if not self.__path.exists():
            not_exist_message: str = f'{self.__path.absolute()} does not exist'
            raise ValueError(not_exist_message)

        missing_necessary_files: list[str] = []
        available_files: list[str] = []

        for file in self.__path.iterdir():
            available_files.append(file.name)

        for file_ in self.__necessary_files:
            if file_ not in available_files:
                missing_necessary_files.append(file_)

        if missing_necessary_files:
            memory: list[str] = [
                'Missing files:',
                str(missing_necessary_files),
                'get them at',
                self.__link
            ]

            message: str = ' '.join(memory)

            raise ValueError(message)

    def recognize(self, data: BytesIO) -> str:
        numpy_array: ndarray = librosa.load(data, sr=self.__sample_rate)[0]

        inputs: BatchFeature = self.__processor(
            numpy_array,
            sampling_rate=self.__sample_rate,
            return_tensors='pt',
            padding=True,
        )

        with torch.no_grad():
            outputs: CausalLMOutput = self.__model(
                inputs.input_values, attention_mask=inputs.attention_mask,
            )

            logits: torch.Tensor = outputs.logits

        ids: torch.Tensor = torch.argmax(logits, dim=-1)
        predicted_sentences: list = self.__processor.batch_decode(ids)

        if predicted_sentences:
            return predicted_sentences[0]

        else:
            return ''
