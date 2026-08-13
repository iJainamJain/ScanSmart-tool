"""Intensity transformation techniques for image enhancement.

Implements classical spatial-domain transforms used in digital image
processing: negative, log, gamma (power-law), and contrast stretching.
"""

import cv2
import numpy as np


def image_negative(image: np.ndarray) -> np.ndarray:
    """Compute the negative (complement) of an image: output = 255 - image."""
    return 255 - image


def log_transform(image: np.ndarray, c: float = 46.0) -> np.ndarray:
    """Apply log transformation: output = c * log(1 + image).

    The constant c scales the output to the full [0, 255] range.
    Default c=46 is derived from 255 / log(256).

    Parameters
    ----------
    image : np.ndarray
        Input grayscale image.
    c : float
        Scaling constant. Higher values brighten the output.
    """
    img_float = image.astype(np.float64)
    result = c * np.log1p(img_float)
    return np.clip(result, 0, 255).astype(np.uint8)


def gamma_transform(image: np.ndarray, gamma: float = 1.0, c: float = 1.0) -> np.ndarray:
    """Apply power-law (gamma) transformation: output = c * image^gamma.

    Parameters
    ----------
    image : np.ndarray
        Input grayscale image.
    gamma : float
        Gamma value. <1 brightens, >1 darkens.
    c : float
        Scaling constant (usually 1.0).
    """
    img_normalized = image.astype(np.float64) / 255.0
    result = c * np.power(img_normalized, gamma) * 255.0
    return np.clip(result, 0, 255).astype(np.uint8)


def contrast_stretching(image: np.ndarray, r1: int = 70, s1: int = 0,
                        r2: int = 180, s2: int = 255) -> np.ndarray:
    """Apply piecewise linear contrast stretching.

    Maps [0, r1] -> [0, s1], [r1, r2] -> [s1, s2], [r2, 255] -> [s2, 255].

    Parameters
    ----------
    image : np.ndarray
        Input grayscale image.
    r1, s1 : int
        First breakpoint (input, output).
    r2, s2 : int
        Second breakpoint (input, output).
    """
    lut = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        if i <= r1:
            lut[i] = int((s1 / max(r1, 1)) * i) if r1 > 0 else 0
        elif i <= r2:
            lut[i] = int(((s2 - s1) / max(r2 - r1, 1)) * (i - r1) + s1)
        else:
            lut[i] = int(((255 - s2) / max(255 - r2, 1)) * (i - r2) + s2)
    return cv2.LUT(image, lut)


def histogram_equalization(image: np.ndarray) -> np.ndarray:
    """Apply histogram equalization to improve contrast.

    Uses OpenCV's equalizeHist for efficient computation.
    """
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.equalizeHist(image)
