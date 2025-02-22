import numpy as np
from scipy import fftpack
import scipy.signal
import scipy.ndimage

## -----------------------------------------------------
def ww_spectral_residual_saliency(image, sigma=2.5, apply_hann=False):
    """
    입력 이미지의 spectral residual saliency map을 계산합니다.
    Hann window를 전처리로 적용할지 여부를 선택할 수 있습니다.

    Parameters:
    -----------
    image : ndarray
        입력 이미지 (grayscale 또는 RGB)
    sigma : float
        Gaussian blur의 표준 편차 (기본값: 2.5)
    apply_hann : bool
        Hann window를 전처리로 적용할지 여부 (기본값: False)

    Returns:
    --------
    ndarray
        Saliency map 이미지 (grayscale)
    """
    # RGB 이미지를 grayscale로 변환
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)

    # Hann window 적용 여부
    if apply_hann:
        # 2D Hann window 생성
        hann_1d_row = np.hanning(image.shape[0])
        hann_1d_col = np.hanning(image.shape[1])
        hann_2d = np.outer(hann_1d_row, hann_1d_col)
        # 이미지에 Hann window 적용
        image = image * hann_2d

    # 2D 푸리에 변환 수행 및 주파수 이동
    f = fftpack.fft2(image)
    f_shift = fftpack.fftshift(f)

    # 진폭과 위상 계산
    A = np.abs(f_shift)
    P = np.angle(f_shift)

    # 로그 진폭 계산 (0 로그 방지 위해 작은 값 추가)
    L = np.log(A + 1e-9)

    # 평균 필터 생성 (3x3)
    kernel = np.ones((3, 3)) / 9

    # 로그 진폭의 평균 계산
    L_avg = scipy.signal.convolve2d(L, kernel, mode='same')

    # Spectral residual 계산
    R = L - L_avg

    # 주파수 도메인에서 saliency 계산
    S = np.exp(R) * np.exp(1j * P)

    # 역 푸리에 변환
    S_unshifted = fftpack.ifftshift(S)
    saliency_complex = fftpack.ifft2(S_unshifted)

    # Saliency map 계산 (제곱 크기)
    saliency = np.abs(saliency_complex)**2

    # Gaussian blur 적용
    saliency = scipy.ndimage.gaussian_filter(saliency, sigma=sigma)

    # [0, 255] 범위로 정규화
    saliency = (saliency - np.min(saliency)) / (np.max(saliency) - np.min(saliency)) * 255

    return saliency.astype(np.uint8)

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
    # Convert RGB to grayscale if needed
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)
    
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
    
    spectrum_8bit = (amplitude_spectrum * 255).astype(np.uint8)
    
    return spectrum_8bit

## -----------------------------------------------------
def ww_phase_congruency_edge(image, nscales=4, norient=6, minWaveLength=3, mult=2.1, sigmaOnf=0.55):
    """
    Phase Congruency를 사용하여 이미지의 에지를 감지합니다.

    Parameters:
    -----------
    image : ndarray
        입력 이미지 (grayscale 또는 RGB)
    nscales : int
        스케일의 수 (기본값: 4)
    norient : int
        방향의 수 (기본값: 6)
    minWaveLength : int
        최소 파장 (기본값: 3)
    mult : float
        파장 증가 배수 (기본값: 2.1)
    sigmaOnf : float
        필터의 대역폭을 제어하는 sigma (기본값: 0.55)

    Returns:
    --------
    ndarray
        Phase Congruency 에지 맵 (grayscale)
    """
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)

    # 이미지 크기
    rows, cols = image.shape

    # 푸리에 변환
    imagefft = fftpack.fft2(image)

    # 주파수 성분
    u = np.fft.fftfreq(rows)
    v = np.fft.fftfreq(cols)
    u, v = np.meshgrid(u, v, indexing='ij')
    radius = np.sqrt(u**2 + v**2)
    radius[0, 0] = 1.0  # DC 성분을 피하기 위해

    # 각도 계산
    theta = np.arctan2(v, u)

    # 로그 가보르 필터 생성
    def log_gabor_filter(scale, orient):
        wavelength = minWaveLength * (mult ** scale)
        fo = 1.0 / wavelength  # 중심 주파수
        log_gabor = np.exp(- (np.log(radius / fo))**2 / (2 * np.log(sigmaOnf)**2))
        log_gabor[0, 0] = 0.0

        # 방향 필터
        angle = orient * np.pi / norient
        ds = np.cos(theta - angle)
        dc = np.sin(theta - angle)
        spread = np.exp(- (theta - angle)**2 / (2 * (np.pi / norient)**2))

        return log_gabor * spread

    # Phase Congruency 계산
    sumE_O = np.zeros((rows, cols), dtype=complex)
    sumO_E = np.zeros((rows, cols), dtype=complex)
    sumAn = np.zeros((rows, cols))

    for orient in range(norient):
        for scale in range(nscales):
            filter = log_gabor_filter(scale, orient)
            filtered = filter * imagefft
            ifft = fftpack.ifft2(filtered)
            sumE_O += ifft
            sumO_E += np.abs(ifft)
            sumAn += np.abs(filtered)

    # Phase Congruency
    pc = np.abs(sumE_O) / (sumAn + 1e-6)

    # [0, 255]로 정규화
    pc = (pc - np.min(pc)) / (np.max(pc) - np.min(pc)) * 255

    return pc.astype(np.uint8)