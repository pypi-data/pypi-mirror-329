# OpenFV

A Python package for computer vision in Frequency Domain.

## Installation

You can install the package using pip:

```bash
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
saliency_map = fv.ww_spectral_residual_saliency(image, sigma=2.5)

'''

## Input/Output
Input
NumPy array representing an image
Supports both 2D (grayscale) and 3D (RGB) arrays
RGB images are automatically converted to grayscale
Output
uint-8 grayscale image.

## Dependencies
numpy >= 1.19.0
scipy >= 1.15.1

## License
This project is licensed under the MIT License - see the LICENSE file for details.
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Author
Wonwoo Park (bemore.one@gmail.com)

## Version History
0.2.0: spectral residual saliency map added
0.1.9: amplitude spectrum added
0.1.5: homomorphic filter added
0.1.0: Initial release