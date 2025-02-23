import numpy as np
from scipy import fftpack
import scipy.signal
import scipy.ndimage
import cv2

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
def ww_phase_congruency_edge(    image,
    nscale=4,          # 스케일 수를 줄임 (4 → 3)
    norient=4,         # 방향 수를 늘림 (6 → 8)
    minWaveLength=3,   # 최소 파장을 줄임 (3 → 2)
    mult=1.2,          # 파장 증가 배수를 줄임 (2.1 → 1.8)
    sigmaOnf=0.9,     # 필터 대역폭을 줄임 (0.55 → 0.35)
    k=9.0,             # 노이즈 임계값을 높임 (2.0 → 3.0)
    cutOff=0.5,        # 컷오프 임계값을 낮춤 (0.5 → 0.3)
    g=9.0,            # 기울기를 높임 (10.0 → 15.0)
    epsilon=0.01    # 작은 값을 더 작게 (0.0001 → 0.00001)
):
    """
    C++ 구현을 기반으로 한 Phase Congruency 에지 검출
    
    Parameters:
    -----------
    image : ndarray
        입력 이미지 (grayscale 또는 RGB)
    nscale : int
        스케일의 수 (기본값: 4)
    norient : int
        방향의 수 (기본값: 6)
    기타 매개변수들은 Phase Congruency 계산에 필요한 상수들
    """
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)
    
    # 이미지를 float로 변환
    image = image.astype(np.float64) / 255.0
    rows, cols = image.shape
    
    # DFT를 위한 최적 크기 계산
    dft_rows = cv2.getOptimalDFTSize(rows)
    dft_cols = cv2.getOptimalDFTSize(cols)
    
    # 이미지 패딩
    padded = np.zeros((dft_rows, dft_cols))
    padded[:rows, :cols] = image
    
    # FFT 계산
    dft = np.fft.fft2(padded)
    dft_shift = np.fft.fftshift(dft)
    
    # 좌표 그리드 생성
    y, x = np.meshgrid(np.arange(dft_rows) - dft_rows//2,
                      np.arange(dft_cols) - dft_cols//2,
                      indexing='ij')
    radius = np.sqrt(x**2 + y**2)
    theta = np.arctan2(-x, y)
    
    # 반지름 정규화
    radius = radius / (min(dft_rows, dft_cols) / 2)
    
    # 로그 가보르 필터 생성
    log_gabor = []
    for s in range(nscale):
        wavelength = minWaveLength * mult**s
        fo = 1.0 / wavelength
        log_gabor.append(np.exp(-(np.log(radius/fo + epsilon))**2 / (2 * sigmaOnf**2)))
        log_gabor[-1][dft_rows//2, dft_cols//2] = 0
    
    # 각 방향에 대한 처리
    pc_sum = np.zeros((rows, cols))
    
    for o in range(norient):
        # 방향 필터 생성
        angle = o * np.pi / norient
        ds = np.cos(theta - angle)
        dc = np.sin(theta - angle)
        spread = np.exp(-(theta - angle)**2 / (2 * (np.pi/norient)**2))
        
        energy = np.zeros((rows, cols))
        sum_e = np.zeros((rows, cols), dtype=complex)
        
        # 각 스케일에 대한 처리
        for s in range(nscale):
            # 필터 적용
            filt = log_gabor[s] * spread
            result = np.fft.ifft2(np.fft.ifftshift(dft_shift * filt))
            result = result[:rows, :cols]
            
            # 에너지 누적
            if s == 0:
                sum_e = result
                max_an = np.abs(result)
                sum_an = max_an
            else:
                sum_e += result
                sum_an += np.abs(result)
                max_an = np.maximum(max_an, np.abs(result))
        
        # Phase Congruency 계산
        abs_e = np.abs(sum_e) + epsilon
        energy = np.real(sum_e) / abs_e
        
        # 노이즈 제거
        t = np.mean(abs_e) * k
        energy = np.maximum(energy - t, 0)
        
        # 가중치 적용
        weight = 1.0 / (1.0 + np.exp(g * (cutOff - sum_an / (max_an + epsilon))))
        pc_sum += energy * weight
    
    # 결과 정규화
    pc_sum = (pc_sum - np.min(pc_sum)) / (np.max(pc_sum) - np.min(pc_sum)) * 255
    
    return pc_sum.astype(np.uint8)