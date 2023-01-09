## AudioData-Augmentation

This Github repo is created to perform augmentation on audio dataset, such that the resultant/output audio emulates real-world noisy conditions. Researchers and testers need augmented data in order to make their ML/NN models more robust or to test ML/NN models against several real-world scenarios respectively.
The assumption is that the audio recorded in a real-word setting comes with two types of noise:
1. Additive noise (Ambient noise)
2. Multiplicative noise (Room Impulse Response)

In order to emulate real-world conditions for a studio recorded clean audio dataset, we need to add/multiply these kind of noise to it. There are publicly available license free audios and impulse response available for doing this. The audio and RIR we used for this repo are available in the links below
1. Ambient noise links: [link1](https://quicksounds.com), [link2](https://pixabay.com)
2. Room Impulse Response link: [link1](https://mcdermottlab.mit.edu/Reverb/IR\_Survey.html)

The ambient noise files used in this repo are under *Bg_sound* directory, and the RIR are under *RIR* directory. The files are chosen such that it resembles/emulates a real-world condition (such as a Restaurant, Supermarket and Train station). One can add more scenarios by adding corresponding ambient noise files and RIR files. In case a model is to be tested/trained to work in a specific application scenario, we can augment the dataset with noises that are expected in the desired conditions

The repo contains a code *audioDataAug.py* which takes in a dataset directory (that contains audio files to be augmented), and other noise related files, and it randomly chooses a scenario, and adds relevant noise to it according to the specified SNR.

## Evaluation of German ASR models

This Github repo also publishes the experiments results performed on German ASR models. We augmented the German test dataset available [here](https://www.kaggle.com/datasets/bryanpark/german-single-speaker-speech-dataset?resource=download) with the method and code described above, and we tested the performance of 6 German ASR models at each expermintal iteration. The clean audio and the augmented audio files can be found under *LibrivoxDeSubset* directory. The performance of each model at each iteration can be found under the directories suffixed *_CSV*. The six models used for the experiments are as follows,
1. [Vosk Small DE Model](https://alphacephei.com/vosk/models)
2. [Vosk Zamia DE Model](https://alphacephei.com/vosk/models)
3. [Silero](https://github.com/snakers4/silero-models)
4. [Scribosermo](https://gitlab.com/Jaco-Assistant/Scribosermo/-/tree/master/)
5. [Fine-tuned XLSR-53](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-german)
6. [OpenAI Whisper](https://github.com/openai/whisper)
