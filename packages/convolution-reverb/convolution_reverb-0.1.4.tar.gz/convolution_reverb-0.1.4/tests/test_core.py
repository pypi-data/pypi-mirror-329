import pytest
import torch
import tempfile
import os
import torchaudio
from convolution_reverb import apply_reverb

@pytest.fixture
def sample_audio():
    # Create a simple sine wave
    sample_rate = 44100
    duration = 1  # seconds
    t = torch.linspace(0, duration, int(sample_rate * duration))
    waveform = torch.sin(2 * torch.pi * 440 * t)  # 440 Hz sine wave
    return waveform.unsqueeze(0), sample_rate

@pytest.fixture
def sample_ir():
    # Create a simple impulse response
    sample_rate = 44100
    duration = 0.5  # seconds
    t = torch.linspace(0, duration, int(sample_rate * duration))
    waveform = torch.exp(-5 * t) * torch.sin(2 * torch.pi * 200 * t)
    return waveform.unsqueeze(0), sample_rate

def test_apply_reverb_with_tensor(sample_audio, sample_ir):
    audio_wav, sr_audio = sample_audio
    ir_wav, _ = sample_ir
    
    # Save IR to temporary file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as ir_file:
        torchaudio.save(ir_file.name, ir_wav, sr_audio)
        
        # Test the function
        original, convolved, sr = apply_reverb(
            audio_wav=audio_wav,
            audio_wav_sr=sr_audio,
            ir_path=ir_file.name
        )
        
    # Clean up
    os.unlink(ir_file.name)
    
    # Assertions
    assert isinstance(original, torch.Tensor)
    assert isinstance(convolved, torch.Tensor)
    assert isinstance(sr, int)
    assert sr == sr_audio
    assert convolved.dim() == 1
    assert convolved.max() <= 1.0
    assert convolved.min() >= -1.0

def test_apply_reverb_with_files(sample_audio, sample_ir):
    audio_wav, sr_audio = sample_audio
    ir_wav, _ = sample_ir
    
    # Save temporary files
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as audio_file, \
         tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as ir_file, \
         tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as output_file:
        
        torchaudio.save(audio_file.name, audio_wav, sr_audio)
        torchaudio.save(ir_file.name, ir_wav, sr_audio)
        
        # Test the function
        original, convolved, sr = apply_reverb(
            audio_path=audio_file.name,
            ir_path=ir_file.name,
            output_path=output_file.name
        )
        
        # Check if output file exists and can be loaded
        assert os.path.exists(output_file.name)
        loaded_wav, loaded_sr = torchaudio.load(output_file.name)
        
    # Clean up
    os.unlink(audio_file.name)
    os.unlink(ir_file.name)
    os.unlink(output_file.name)
    
    # Assertions
    assert isinstance(original, torch.Tensor)
    assert isinstance(convolved, torch.Tensor)
    assert isinstance(sr, int)
    assert sr == sr_audio
    assert loaded_sr == sr_audio
    assert loaded_wav.shape[1] == convolved.shape[0]

def test_input_validation():
    # Test that providing both audio_path and audio_wav raises an error
    with pytest.raises(ValueError, match="Only one of audio_path or audio_wav can be provided"):
        apply_reverb(
            audio_path="dummy.wav",
            audio_wav=torch.zeros(1, 1000),
            audio_wav_sr=44100,
            ir_path="dummy_ir.wav"
        )
    
    # Test that providing neither audio_path nor audio_wav raises an error
    with pytest.raises(ValueError, match="Either audio_path or audio_wav must be provided"):
        apply_reverb(
            ir_path="dummy_ir.wav"
        ) 