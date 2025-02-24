import hurtful_py as hp

with hp.Microphone() as mic:
    mic.record(duration=5, output_file='test.wav')
print('end')
