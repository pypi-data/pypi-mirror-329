# import typing as tp
# import torch
# import torchaudio


# def apply_reverb(*, 
#          audio_path: tp.Union[str, None] = None, 
#          audio_wav: tp.Union[torch.Tensor, None] = None, 
#          audio_wav_sr: tp.Union[int, None] = None,
#          ir_path: tp.Union[str, None] = None,
#          ir_wav: tp.Union[torch.Tensor, None] = None, 
#          ir_wav_sr: tp.Union[int, None] = None,
#          output_path: tp.Union[str, None] = None,
#          ) -> tp.Tuple[torch.Tensor, torch.Tensor, int]:
#     """
#     Apply convolution reverb to an audio file or tensor.

#     The audio input can now be provided as either:
#       - A tensor of shape (n_channels, n_samples) (single example), or
#       - A tensor of shape (batch_size, n_channels, n_samples).
      
#     In the single-example case the tensor is automatically unsqueezed to add a batch dimension.

#     Args:
#         audio_path: Path to the input audio file.
#         audio_wav: Input audio as a torch.Tensor (n_channels, n_samples) or (batch_size, n_channels, n_samples).
#         audio_wav_sr: Sampling rate of the input audio.
#         ir_path: Path to the impulse response file.
#         ir_wav: Impulse response as a torch.Tensor (n_channels, n_samples).
#         ir_wav_sr: Sampling rate of the impulse response.
#         output_path: Path where the output audio will be saved.

#     Returns:
#         Tuple containing:
#         - Original mono audio waveform (torch.Tensor) with shape (batch_size, n_samples)
#         - Convolved audio waveform (torch.Tensor) with shape (batch_size, n_samples)
#         - Sample rate (int)
#     """
#     # Validate audio input
#     if audio_path is None and audio_wav is None:
#         raise ValueError("Either audio_path or audio_wav must be provided.")
#     if isinstance(audio_path, str) and audio_wav is not None:
#         raise ValueError("Only one of audio_path or audio_wav can be provided.")

#     # Load audio
#     if audio_path is not None:
#         audio_waveform, sr_audio = torchaudio.load(audio_path)  # shape: (n_channels, n_samples)
#         # Add a batch dimension: (1, n_channels, n_samples)
#         audio_waveform = audio_waveform.unsqueeze(0)
#     else:
#         audio_waveform = audio_wav
#         sr_audio = audio_wav_sr
#         # If provided as (n_channels, n_samples), unsqueeze to get (1, n_channels, n_samples)
#         if audio_waveform.dim() == 2:
#             audio_waveform = audio_waveform.unsqueeze(0)
#         elif audio_waveform.dim() != 3:
#             raise ValueError("audio_wav must be a 2D or 3D tensor.")

#     # Load impulse response (IR)
#     if ir_path is not None:
#         ir_waveform, sr_ir = torchaudio.load(ir_path)  # shape: (n_channels, n_samples)
#     else:
#         if ir_wav is None:
#             raise ValueError("Either ir_path or ir_wav must be provided.")
#         ir_waveform, sr_ir = ir_wav, ir_wav_sr
#         if ir_waveform.dim() != 2:
#             raise ValueError("ir_wav must be a 2D tensor of shape (n_channels, n_samples).")

#     # Ensure the sampling rates match
#     if sr_audio != sr_ir:
#         ir_waveform = torchaudio.functional.resample(ir_waveform, sr_ir, sr_audio)

#     # Convert multi-channel audio to mono by averaging channels.
#     # For audio_waveform: shape (batch_size, n_channels, n_samples)
#     if audio_waveform.shape[1] > 1:
#         # print("Input audio is multi-channel. Converting to mono by averaging channels.")
#         audio_waveform = audio_waveform.mean(dim=1, keepdim=True)
#     # For ir_waveform: shape (n_channels, n_samples)
#     if ir_waveform.shape[0] > 1:
#         # print("Impulse response is multi-channel. Converting to mono by averaging channels.")
#         ir_waveform = ir_waveform.mean(dim=0, keepdim=True)
    
#     # Remove the channel dimension for further processing.
#     # audio_batch: shape (batch_size, n_samples)
#     audio_batch = audio_waveform.squeeze(1)
#     # Use the impulse response as a 1D tensor (assuming a single IR is used)
#     ir = ir_waveform.squeeze(0).float()

#     # Ensure signals are in float32
#     audio_batch = audio_batch.float()

#     # Determine the convolution length (assuming all audio samples have the same length)
#     batch_size, audio_length = audio_batch.shape
#     ir_length = ir.numel()
#     n = audio_length + ir_length - 1
#     # Compute next power-of-two for efficient FFT computation
#     n_fft = 2 ** ((n - 1).bit_length())
#     print('n_fft:', n_fft)
#     # Compute FFT of the audio batch along the last dimension
#     A = torch.fft.rfft(audio_batch, n=n_fft, dim=-1)  # shape: (batch_size, n_fft//2 + 1)
#     # Compute FFT of the impulse response
#     B = torch.fft.rfft(ir, n=n_fft)  # shape: (n_fft//2 + 1)

#     # Multiply in frequency domain (broadcasting IR across the batch)
#     # C = A * B
#     C = A 
#     # Compute the inverse FFT to get the convolved signal and trim to expected length
#     convolved = torch.fft.irfft(C, n=n_fft, dim=-1)[:, :n]  # shape: (batch_size, n)

#     # Truncate the convolved signal to match the original audio length if necessary.
#     print('audio_length:', audio_length)
#     print('convolved.shape:', convolved.shape)
#     if audio_length < convolved.shape[1]:
#         convolved = convolved[:, :audio_length]
#     elif audio_length > convolved.shape[1]:
#         raise ValueError("Convolved signal is shorter than the audio signal. Does this happen?")

#     # Save the output if an output path is provided (only supported for batch size 1)
#     if output_path is not None:
#         if batch_size != 1:
#             raise ValueError("Saving output audio is only supported for a batch size of 1.")
#         # torchaudio expects shape (channels, n_samples)
#         convolved_to_save = convolved[0].unsqueeze(0)
#         torchaudio.save(output_path, convolved_to_save, sr_audio)
#         print(f"Convolved audio saved as '{output_path}'.")

#     # Return the original mono audio (batch_size, n_samples) and the convolved audio
#     return audio_batch.unsqueeze(1), convolved.unsqueeze(1), sr_audio



import typing as tp
import torch
import torchaudio
import torch.nn.functional as F

def apply_reverb(*, 
         audio_path: tp.Union[str, None] = None, 
         audio_wav: tp.Union[torch.Tensor, None] = None, 
         audio_wav_sr: tp.Union[int, None] = None,
         ir_path: tp.Union[str, None] = None,
         ir_wav: tp.Union[torch.Tensor, None] = None, 
         ir_wav_sr: tp.Union[int, None] = None,
         output_path: tp.Union[str, None] = None,
         use_partitioned: bool = True,
         block_size: tp.Optional[int] = None,
         ) -> tp.Tuple[torch.Tensor, torch.Tensor, int]:
    """
    Apply convolution reverb to an audio file or tensor.

    The audio input can now be provided as either:
      - A tensor of shape (n_channels, n_samples) (single example), or
      - A tensor of shape (batch_size, n_channels, n_samples).
      
    In the single-example case the tensor is automatically unsqueezed to add a batch dimension.

    Args:
        audio_path: Path to the input audio file.
        audio_wav: Input audio as a torch.Tensor (n_channels, n_samples) or (batch_size, n_channels, n_samples).
        audio_wav_sr: Sampling rate of the input audio.
        ir_path: Path to the impulse response file.
        ir_wav: Impulse response as a torch.Tensor (n_channels, n_samples).
        ir_wav_sr: Sampling rate of the impulse response.
        output_path: Path where the output audio will be saved.
        use_partitioned: If True, uses partitioned convolution (overlap‑add) to avoid potential numerical
                         precision issues with large FFT blocks. This is recommended for long audio signals.
        block_size: Block size (in samples) to use for partitioned convolution. If not provided and 
                    use_partitioned is True, defaults to 10 seconds of audio (sr_audio * 10).
                    
    Returns:
        Tuple containing:
        - Original mono audio waveform (torch.Tensor) with shape (batch_size, 1, n_samples)
        - Convolved audio waveform (torch.Tensor) with shape (batch_size, 1, n_samples)
        - Sample rate (int)
    """
    # Validate audio input
    if audio_path is None and audio_wav is None:
        raise ValueError("Either audio_path or audio_wav must be provided.")
    if isinstance(audio_path, str) and audio_wav is not None:
        raise ValueError("Only one of audio_path or audio_wav can be provided.")

    # Load audio
    if audio_path is not None:
        audio_waveform, sr_audio = torchaudio.load(audio_path)  # shape: (n_channels, n_samples)
        # Add a batch dimension: (1, n_channels, n_samples)
        audio_waveform = audio_waveform.unsqueeze(0)
    else:
        audio_waveform = audio_wav
        sr_audio = audio_wav_sr
        # If provided as (n_channels, n_samples), unsqueeze to get (1, n_channels, n_samples)
        if audio_waveform.dim() == 2:
            audio_waveform = audio_waveform.unsqueeze(0)
        elif audio_waveform.dim() != 3:
            raise ValueError("audio_wav must be a 2D or 3D tensor.")

    # Load impulse response (IR)
    if ir_path is not None:
        ir_waveform, sr_ir = torchaudio.load(ir_path)  # shape: (n_channels, n_samples)
    else:
        if ir_wav is None:
            raise ValueError("Either ir_path or ir_wav must be provided.")
        ir_waveform, sr_ir = ir_wav, ir_wav_sr
        if ir_waveform.dim() != 2:
            raise ValueError("ir_wav must be a 2D tensor of shape (n_channels, n_samples).")

    # Ensure the sampling rates match
    if sr_audio != sr_ir:
        ir_waveform = torchaudio.functional.resample(ir_waveform, sr_ir, sr_audio)

    # Convert multi-channel audio to mono by averaging channels.
    # For audio_waveform: shape (batch_size, n_channels, n_samples)
    if audio_waveform.shape[1] > 1:
        audio_waveform = audio_waveform.mean(dim=1, keepdim=True)
    # For ir_waveform: shape (n_channels, n_samples)
    if ir_waveform.shape[0] > 1:
        ir_waveform = ir_waveform.mean(dim=0, keepdim=True)
    
    # Remove the channel dimension for further processing.
    # audio_batch: shape (batch_size, n_samples)
    audio_batch = audio_waveform.squeeze(1)
    # Use the impulse response as a 1D tensor (assuming a single IR is used)
    ir = ir_waveform.squeeze(0).float()

    # Ensure signals are in float32
    audio_batch = audio_batch.float()

    batch_size, audio_length = audio_batch.shape
    ir_length = ir.numel()

    if not use_partitioned:
        # Process the entire audio block at once.
        n = audio_length + ir_length - 1
        n_fft = 2 ** ((n - 1).bit_length())
        A = torch.fft.rfft(audio_batch, n=n_fft, dim=-1)
        B = torch.fft.rfft(ir, n=n_fft)
        C = A * B
        convolved = torch.fft.irfft(C, n=n_fft, dim=-1)[:, :n]

        # Truncate the convolved signal to match the original audio length.
        if audio_length < convolved.shape[1]:
            convolved = convolved[:, :audio_length]
        elif audio_length > convolved.shape[1]:
            raise ValueError("Convolved signal is shorter than the audio signal. Does this happen?")
    else:
        # Use partitioned convolution (overlap-add) to process the audio in smaller blocks.
        # If block_size is not provided, default to 10 seconds of audio.
        if block_size is None:
            block_size = sr_audio * 10
        L = block_size
        full_length = audio_length + ir_length - 1
        convolved_full = torch.zeros((batch_size, full_length), 
                                     dtype=audio_batch.dtype, device=audio_batch.device)
        # Process each block using overlap-add.
        for start in range(0, audio_length, L):
            block = audio_batch[:, start:min(start+L, audio_length)]
            L_block = block.shape[-1]
            N_block = L_block + ir_length - 1
            n_fft_block = 2 ** ((N_block - 1).bit_length())
            # Compute FFT of the impulse response for the current block size.
            H_block = torch.fft.rfft(ir, n=n_fft_block)
            block_padded = F.pad(block, (0, n_fft_block - L_block))
            A_block = torch.fft.rfft(block_padded, n=n_fft_block, dim=-1)
            Y_block = A_block * H_block
            y_block = torch.fft.irfft(Y_block, n=n_fft_block, dim=-1)[:, :N_block]
            end_index = start + N_block
            # Ensure we don't exceed the allocated output length.
            if end_index > full_length:
                y_block = y_block[:, : full_length - start]
                end_index = full_length
            convolved_full[:, start:end_index] += y_block
        # Trim the final output to match the original audio length.
        convolved = convolved_full[:, :audio_length]

    # Save the output if an output path is provided (only supported for batch size 1).
    if output_path is not None:
        if batch_size != 1:
            raise ValueError("Saving output audio is only supported for a batch size of 1.")
        # torchaudio expects shape (channels, n_samples)
        convolved_to_save = convolved[0].unsqueeze(0)
        torchaudio.save(output_path, convolved_to_save, sr_audio)
        print(f"Convolved audio saved as '{output_path}'.")

    # Return the original mono audio and the convolved audio, each with a channel dimension.
    return audio_batch.unsqueeze(1), convolved.unsqueeze(1), sr_audio