"""
Utility functions for the MamaSight package.
"""
import os
import requests
from pathlib import Path
import subprocess
from typing import Optional, Tuple
import torch


def check_device_availability() -> Tuple[str, str]:
    """
    Check for CUDA availability and return appropriate device strings.
    
    Returns:
        Tuple of (yolo_device, ocr_device) strings
    """
    cuda_available = torch.cuda.is_available()
    device = 'cuda' if cuda_available else 'cpu'
    
    if cuda_available:
        gpu_name = torch.cuda.get_device_name(0)
        memory_info = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # Convert to GB
        print(f"CUDA is available. Using GPU: {gpu_name} with {memory_info:.2f} GB memory")
    else:
        print("CUDA is not available. Using CPU.")
    
    return device, device


def download_model(url: str, save_path: Path, model_name: str = "model.pt") -> Optional[Path]:
    """
    Download a model from a URL.
    
    Args:
        url: URL to download from
        save_path: Directory to save to
        model_name: Name of model file
        
    Returns:
        Path to downloaded file or None if download failed
    """
    save_path.mkdir(exist_ok=True, parents=True)
    model_path = save_path / model_name
    
    # Skip if model already exists
    if model_path.exists():
        print(f"Model already exists at {model_path}")
        return model_path
    
    print(f"Downloading model from {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        
        with open(model_path, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = downloaded / total_size * 100
                        print(f"\rDownload progress: {percent:.1f}%", end="")
        
        print("\nDownload complete!")
        return model_path
    except Exception as e:
        print(f"Download failed: {e}")
        return None


def try_huggingface_download(repo_id: str, filename: str, save_dir: Path) -> bool:
    """
    Try to download a file from HuggingFace using huggingface-cli.
    
    Args:
        repo_id: HuggingFace repository ID
        filename: File to download
        save_dir: Directory to save to
        
    Returns:
        True if download was successful, False otherwise
    """
    try:
        subprocess.run(
            ["huggingface-cli", "download", repo_id, filename, "--local-dir", str(save_dir)],
            check=True,
            capture_output=True
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"huggingface-cli error: {e}")
        return False