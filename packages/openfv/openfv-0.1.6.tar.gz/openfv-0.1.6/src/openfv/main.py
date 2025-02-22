import numpy as np
from scipy import fftpack

## ------------------------------------------------
def ww_homomorphic_filter(image, d0=30, rh=2.0, rl=0.5, c=2):
    """
    Homomorphic filtering of an input image.
    
    Parameters:
    -----------
    image : ndarray
        Input image (grayscale)
    d0 : float
        Cutoff distance (default: 30)
    rh : float
        High frequency gain (default: 2.0)
    rl : float
        Low frequency gain (default: 0.5)
    c : float
        Constant controlling filter sharpness (default: 2)
        
    Returns:
    --------
    ndarray
        Filtered image
    """
    # Take log of image
    image_log = np.log1p(np.array(image, dtype="float"))
    
    # Get image size
    rows, cols = image_log.shape
    
    # Create meshgrid for filter
    u = np.arange(rows)
    v = np.arange(cols)
    u, v = np.meshgrid(u, v, indexing='ij')
    
    # Center coordinates
    u = u - rows//2
    v = v - cols//2
    
    # Calculate distances from center
    D = np.sqrt(u**2 + v**2)
    
    # Create homomorphic filter
    H = (rh - rl) * (1 - np.exp(-c * (D**2 / d0**2))) + rl
    
    # Apply FFT
    image_fft = fftpack.fft2(image_log)
    image_fft_shifted = fftpack.fftshift(image_fft)
    
    # Apply filter
    filtered_image = H * image_fft_shifted
    
    # Inverse FFT
    filtered_image_unshifted = fftpack.ifftshift(filtered_image)
    filtered_image_ifft = fftpack.ifft2(filtered_image_unshifted)
    
    # Take exp and return real part
    result = np.expm1(np.real(filtered_image_ifft))
    
    # Normalize to [0, 255]
    result = result - np.min(result)
    result = result / np.max(result) * 255
    
    return result.astype(np.uint8)

## -----------------------------------------------------
def ww_amplitude_spectrum(image):
    """
    입력 이미지의 2D 푸리에 변환을 수행하고 진폭 스펙트럼을 반환합니다.
    
    Parameters:
        image (numpy.ndarray): 입력 이미지 배열 (2D grayscale 또는 3D RGB)
        
    Returns:
        numpy.ndarray: 정규화된 진폭 스펙트럼 이미지
    """
    # 입력 이미지가 3D(RGB)인 경우 grayscale로 변환
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)
    
    # 2D 푸리에 변환 수행
    f_transform = np.fft.fft2(image)
    
    # 주파수 성분을 중앙으로 이동
    f_shift = np.fft.fftshift(f_transform)
    
    # 진폭 스펙트럼 계산
    amplitude_spectrum = np.abs(f_shift)
    
    # log scale로 변환하여 시각화 개선
    amplitude_spectrum = np.log1p(amplitude_spectrum)
    
    # 0-1 범위로 정규화
    amplitude_spectrum = (amplitude_spectrum - np.min(amplitude_spectrum)) / \
                        (np.max(amplitude_spectrum) - np.min(amplitude_spectrum))
    
    return amplitude_spectrum