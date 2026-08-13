"""Image arithmetic operations for enhancement.

Implements addition, subtraction, and averaging of images, which are
fundamental operations in spatial-domain image processing.
"""

import cv2
import numpy as np


def image_addition(img1: np.ndarray, img2: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    """Add two images with weighted blending.

    Practical application: Image fusion — combining information from
    multiple sensors (e.g., visible + infrared) into a single composite.

    Parameters
    ----------
    img1, img2 : np.ndarray
        Input images (must have the same dimensions).
    alpha : float
        Weight for img1 (img2 gets weight 1-alpha).
    """
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.addWeighted(img1, alpha, img2_resized, 1 - alpha, 0)


def image_subtraction(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    """Subtract img2 from img1 to highlight differences.

    Practical application: Change detection / motion detection —
    subtracting a reference frame from the current frame reveals
    moving objects or structural changes between two captures.

    Parameters
    ----------
    img1, img2 : np.ndarray
        Input images (must have the same dimensions).
    """
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.absdiff(img1, img2_resized)


def image_averaging(images: list[np.ndarray]) -> np.ndarray:
    """Average multiple images to reduce random noise.

    Practical application: Noise reduction — averaging N noisy captures
    of the same scene reduces random noise by a factor of sqrt(N),
    commonly used in astrophotography and medical imaging.

    Parameters
    ----------
    images : list of np.ndarray
        List of images to average (all must have the same dimensions).
    """
    if not images:
        raise ValueError("At least one image is required for averaging.")
    target_shape = images[0].shape[:2]
    accumulator = np.zeros(images[0].shape, dtype=np.float64)
    for img in images:
        resized = cv2.resize(img, (target_shape[1], target_shape[0]))
        accumulator += resized.astype(np.float64)
    result = accumulator / len(images)
    return result.astype(np.uint8)
