import wave

import pyaudio


class MicrophoneReader:
    def __init__(self, rate=44100, channels=1, chunk=1024, format_audio=pyaudio.paInt16):
        """
        Инициализация настроек аудио

        :param rate: Частота дискретизации (по умолчанию 44100 Гц)
        :param channels: Количество каналов (1 - моно, 2 - стерео)
        :param chunk: Размер блока (количество сэмплов за один вызов чтения)
        :param format_audio: Формат аудиоданных (по умолчанию pyaudio.paInt16)
        """
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.format = format_audio
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start_stream(self):
        """
        Запускает аудиопоток для чтения данных с микрофона.
        """
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        print("Аудиопоток запущен.")

    def read_chunk(self):
        """
        Считывает один блок данных из аудиопотока.

        :return: Данные аудио в байтах.
        """
        if self.stream is not None:
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                return data
            except Exception as e:
                print(f"Ошибка при чтении данных: {e}")
                return None
        else:
            raise RuntimeError("Аудиопоток не запущен. Вызовите start_stream().")

    def stop_stream(self):
        """
        Останавливает аудиопоток и освобождает ресурсы.
        """
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            print("Аудиопоток остановлен.")
        else:
            raise RuntimeError("Аудиопоток не запущен.")

    def record(self, seconds):
        """
        Записывает аудио с микрофона в течение указанного времени.

        :param seconds: Время записи в секундах.
        :return: Записанные аудиоданные в байтах.
        """
        self.start_stream()
        frames = []
        print(f"Начало записи аудио на {seconds} секунд...")
        num_chunks = int(self.rate / self.chunk * seconds)
        for _ in range(num_chunks):
            data = self.read_chunk()
            if data is not None:
                frames.append(data)
        self.stop_stream()
        print("Запись завершена.")
        return b''.join(frames)


def save_to_wav(filename, audio_data, rate=44100, channels=1, format=pyaudio.paInt16):
    """
    Сохраняет аудиоданные в WAV-файл.

    :param filename: Имя файла для сохранения.
    :param audio_data: Аудиоданные в байтах.
    :param rate: Частота дискретизации.
    :param channels: Количество каналов.
    :param format: Формат аудиоданных.
    """
    audio = pyaudio.PyAudio()
    sample_width = audio.get_sample_size(format)
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sample_width)
    wf.setframerate(rate)
    wf.writeframes(audio_data)
    wf.close()
    print(f"Файл сохранён как {filename}.")


if __name__ == "__main__":
    # Пример использования библиотеки
    reader = MicrophoneReader()
    audio_data = reader.record(5)  # Записываем 5 секунд аудио
    save_to_wav("output.wav", audio_data)
