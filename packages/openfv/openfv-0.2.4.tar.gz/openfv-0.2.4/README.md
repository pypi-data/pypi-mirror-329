# OpenFV

A Python package for computer vision in Frequency Domain.

## Installation
You can install the package using pip:

bash
pip install openfv

## Usage
Here's a basic example of how to use the package:

import cv2
import openfv as fv

# Load an image
image = cv2.imread('your_image.png')

# Homomorphic filtering
filtered_image = fv.ww_homomorphic_filter(image, d0=30, rh=2.0, rl=0.5, c=2)

# Amplitude spectrum calculation
spectrum_image = fv.ww_amplitude_spectrum(image)

# Spectral residual saliency map generation
saliency_map = fv.ww_spectral_residual_saliency(image, sigma=2.5, apply_hann=True)

# phase congruency edge
edge_map = fv.ww_phase_congruency_edge(image)


## Input
- NumPy array representing an image
- Supports both 2D (grayscale) and 3D (RGB) arrays
- For functions requiring grayscale input (e.g., ww_homomorphic_filter), RGB images must be converted to grayscale.
- For functions supporting RGB input (e.g., ww_amplitude_spectrum), RGB images are processed directly.

## Output
- uint8 grayscale image (for most functions)
- Check specific function documentation for exceptions.

## Dependencies
- numpy (tested with 1.19.0 or later)
- scipy (tested with 1.15.1 or later)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Author
Wonwoo Park (bemore.one@gmail.com)

## Version History
0.2.3: phase congruency edge added
0.2.1: hann window function added in SRSM function
0.2.0: spectral residual saliency map added
0.1.9: amplitude spectrum added
0.1.5: homomorphic filter added
0.1.0: Initial release