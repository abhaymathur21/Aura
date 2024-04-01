import os
import librosa
import numpy as np
# from keras.models import load_model
import io

classes = ["Aditya", "Abhay", "Shreya"]

# def extract_features(audio_seg):
#     # Convert AudioSegment to bytes using io.BytesIO
#     audio_bytes = io.BytesIO()
#     audio_seg.export(audio_bytes, format='wav')
#     audio_bytes.seek(0)  # Reset file pointer to beginning
    
#     audio, sample_rate = librosa.load(audio_bytes, sr=None)  # Load the audio without resampling
#     stft = np.abs(librosa.stft(audio))  # Short-Time Fourier Transform
#     return stft

def extract_features(file_path):
    print(file_path)
    audio, sample_rate = librosa.load(file_path)  # Load the audio without resampling
    segment_length = 2*sample_rate
    segments=[]
    for i in range(0, len(audio), segment_length):
        segment = audio[i:i+segment_length]
        if len(segment) == segment_length:
            segments.append(segment)
    stft = np.abs(librosa.stft(segments[0]))  # Short-Time Fourier Transform
    return stft

def process_audio(audio_segment):
    # Extract features
    features = extract_features(audio_segment)
    
    # Reshape for CNN input
    features = features.reshape(1, features.shape[0], features.shape[1], 1)
    
    return features

# def load_trained_model(model_path):
#     model = load_model(model_path)
#     return model

def classify_audio(audio_file, model):
    processed_data = process_audio(audio_file)
    # print(processed_data.shape)
    prediction = model.predict(processed_data)
    if np.max(prediction)<0.5:
        return 'None'
    else:
        return classes[np.argmax(prediction)]

# if __name__ == "__main__":
    # Path to the trained model
# model_path = "audio_classification_model.h5"  # Update with the path to your trained model
    
    # Load the trained model
# model = load_trained_model(model_path)
    
    # Path to the audio file to classify
# audio_file_path = "data/shreya/audio_1.wav"  # Update with the path to your WAV audio file
    
    # Classify the audio
# prediction = classify_audio(audio_file_path, model)
# print("Prediction:", prediction)
