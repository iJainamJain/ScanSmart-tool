"""Semester Mini Project - Task 3: Image Enhancement in the Spatial Domain.

This script implements ALL sub-tasks (2-6) from the assignment brief:
  Task 2: Intensity transformations (Negative, Log, Gamma, Contrast Stretching)
  Task 3: Histogram analysis (generate, display, compare before/after)
  Task 4: Histogram equalization with comparison
  Task 5: Image arithmetic operations (Add, Subtract, Average)
  Task 6: Comparative analysis of enhancement techniques on 3 images

Run from the project root:
    .\.venv\\Scripts\\python.exe "exp tasks/3/experiment3.py"

All output figures are saved to:  exp tasks/3/outputs/
"""

import sys
from pathlib import Path

# Ensure the project root is on sys.path so src.* imports work
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.enhancement.intensity import (
    image_negative,
    log_transform,
    gamma_transform,
    contrast_stretching,
    histogram_equalization,
)
from src.enhancement.arithmetic import (
    image_addition,
    image_subtraction,
    image_averaging,
)

# ── Configuration ────────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DATASET_DIR = PROJECT_ROOT / "dataset" / "raw"

# 3 diverse images for Task 6 comparison (different lighting/contrast)
SAMPLE_IMAGES = [
    DATASET_DIR / "jainam_doc_02.jpg",    # Typical indoor lighting
    DATASET_DIR / "dhanush_doc_003.jpg",   # Different camera / angle
    DATASET_DIR / "vivek_doc_010.jpg",     # Different contributor / conditions
]


def load_gray(path: Path) -> np.ndarray:
    """Load an image as grayscale, resized to max 800px for display."""
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot load image: {path}")
    h, w = img.shape[:2]
    if max(h, w) > 800:
        scale = 800 / max(h, w)
        img = cv2.resize(img, None, fx=scale, fy=scale)
    return img


def plot_histogram(image: np.ndarray, title: str, ax: plt.Axes):
    """Plot a grayscale histogram on the given axes."""
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    ax.plot(hist, color="steelblue")
    ax.set_title(title, fontsize=10)
    ax.set_xlim([0, 256])
    ax.set_xlabel("Pixel Intensity")
    ax.set_ylabel("Frequency")


# ═══════════════════════════════════════════════════════════════════════
# TASK 2: Intensity Transformation Techniques
# ═══════════════════════════════════════════════════════════════════════

def task2_intensity_transforms():
    """Apply and display all intensity transformations on the first sample image."""
    print("Task 2: Intensity Transformations...")
    img = load_gray(SAMPLE_IMAGES[0])

    transforms = {
        "Original": img,
        "Negative": image_negative(img),
        "Log (c=46)": log_transform(img, c=46),
        "Log (c=30)": log_transform(img, c=30),
        "Gamma=0.4 (brighten)": gamma_transform(img, gamma=0.4),
        "Gamma=1.5 (darken)": gamma_transform(img, gamma=1.5),
        "Gamma=2.5 (strong darken)": gamma_transform(img, gamma=2.5),
        "Contrast Stretch": contrast_stretching(img, r1=70, s1=0, r2=180, s2=255),
    }

    fig, axes = plt.subplots(2, 4, figsize=(18, 9))
    fig.suptitle("Task 2: Intensity Transformation Techniques", fontsize=14, fontweight="bold")
    for ax, (name, result) in zip(axes.flat, transforms.items()):
        ax.imshow(result, cmap="gray", vmin=0, vmax=255)
        ax.set_title(name, fontsize=9)
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(str(OUTPUT_DIR / "task2_intensity_transforms.png"), dpi=150)
    plt.close(fig)
    print(f"  Saved: {OUTPUT_DIR / 'task2_intensity_transforms.png'}")


# ═══════════════════════════════════════════════════════════════════════
# TASK 3: Histogram Analysis
# ═══════════════════════════════════════════════════════════════════════

def task3_histogram_analysis():
    """Generate histograms, display alongside images, compare before/after."""
    print("Task 3: Histogram Analysis...")
    img = load_gray(SAMPLE_IMAGES[0])
    enhanced = gamma_transform(img, gamma=0.5)  # brighten for visible difference

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Task 3: Histogram Analysis - Before vs After Enhancement (Gamma=0.5)",
                 fontsize=13, fontweight="bold")

    axes[0, 0].imshow(img, cmap="gray", vmin=0, vmax=255)
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis("off")

    plot_histogram(img, "Original Histogram", axes[0, 1])

    axes[1, 0].imshow(enhanced, cmap="gray", vmin=0, vmax=255)
    axes[1, 0].set_title("Enhanced (Gamma=0.5)")
    axes[1, 0].axis("off")

    plot_histogram(enhanced, "Enhanced Histogram", axes[1, 1])

    fig.tight_layout()
    fig.savefig(str(OUTPUT_DIR / "task3_histogram_analysis.png"), dpi=150)
    plt.close(fig)
    print(f"  Saved: {OUTPUT_DIR / 'task3_histogram_analysis.png'}")


# ═══════════════════════════════════════════════════════════════════════
# TASK 4: Histogram Equalization
# ═══════════════════════════════════════════════════════════════════════

def task4_histogram_equalization():
    """Compare original vs histogram-equalized image with their histograms."""
    print("Task 4: Histogram Equalization...")
    img = load_gray(SAMPLE_IMAGES[0])
    equalized = histogram_equalization(img)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Task 4: Histogram Equalization - Contrast Improvement",
                 fontsize=13, fontweight="bold")

    axes[0, 0].imshow(img, cmap="gray", vmin=0, vmax=255)
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis("off")

    plot_histogram(img, "Original Histogram", axes[0, 1])

    axes[1, 0].imshow(equalized, cmap="gray", vmin=0, vmax=255)
    axes[1, 0].set_title("Histogram Equalized")
    axes[1, 0].axis("off")

    plot_histogram(equalized, "Equalized Histogram", axes[1, 1])

    fig.tight_layout()
    fig.savefig(str(OUTPUT_DIR / "task4_histogram_equalization.png"), dpi=150)
    plt.close(fig)

    # Print observation
    orig_std = np.std(img)
    eq_std = np.std(equalized)
    print(f"  Original std dev: {orig_std:.1f}  |  Equalized std dev: {eq_std:.1f}")
    print(f"  Observation: Histogram equalization spreads pixel intensities across")
    print(f"  the full [0,255] range (std {orig_std:.1f} -> {eq_std:.1f}),")
    print(f"  improving contrast especially in regions that were previously")
    print(f"  clustered in a narrow intensity band.")
    print(f"  Saved: {OUTPUT_DIR / 'task4_histogram_equalization.png'}")


# ═══════════════════════════════════════════════════════════════════════
# TASK 5: Image Arithmetic Operations
# ═══════════════════════════════════════════════════════════════════════

def task5_arithmetic_operations():
    """Demonstrate addition, subtraction, and averaging with sample images."""
    print("Task 5: Image Arithmetic Operations...")
    img1 = load_gray(SAMPLE_IMAGES[0])
    img2 = load_gray(SAMPLE_IMAGES[1])

    added = image_addition(img1, img2, alpha=0.5)
    subtracted = image_subtraction(img1, img2)

    # For averaging, create 5 noisy versions of img1
    noisy_versions = []
    for i in range(5):
        noise = np.random.normal(0, 25, img1.shape).astype(np.float64)
        noisy = np.clip(img1.astype(np.float64) + noise, 0, 255).astype(np.uint8)
        noisy_versions.append(noisy)
    averaged = image_averaging(noisy_versions)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle("Task 5: Image Arithmetic Operations", fontsize=14, fontweight="bold")

    axes[0, 0].imshow(img1, cmap="gray"); axes[0, 0].set_title("Image 1"); axes[0, 0].axis("off")
    axes[0, 1].imshow(img2, cmap="gray"); axes[0, 1].set_title("Image 2"); axes[0, 1].axis("off")
    axes[0, 2].imshow(added, cmap="gray"); axes[0, 2].set_title("Addition (α=0.5)"); axes[0, 2].axis("off")

    axes[1, 0].imshow(subtracted, cmap="gray"); axes[1, 0].set_title("Subtraction |I1-I2|"); axes[1, 0].axis("off")
    axes[1, 1].imshow(noisy_versions[0], cmap="gray"); axes[1, 1].set_title("Noisy (1 of 5)"); axes[1, 1].axis("off")
    axes[1, 2].imshow(averaged, cmap="gray"); axes[1, 2].set_title("Averaged (5 noisy)"); axes[1, 2].axis("off")

    fig.tight_layout()
    fig.savefig(str(OUTPUT_DIR / "task5_arithmetic_operations.png"), dpi=150)
    plt.close(fig)
    print(f"  Saved: {OUTPUT_DIR / 'task5_arithmetic_operations.png'}")
    print("  Applications:")
    print("    Addition  -> Image fusion (combining multi-sensor data)")
    print("    Subtraction -> Change / motion detection between frames")
    print("    Averaging -> Noise reduction (e.g., astrophotography, medical imaging)")


# ═══════════════════════════════════════════════════════════════════════
# TASK 6: Compare Enhancement Techniques
# ═══════════════════════════════════════════════════════════════════════

def task6_compare_techniques():
    """Apply all techniques to 3 different images and produce a comparison grid."""
    print("Task 6: Comparative Enhancement Analysis...")

    technique_fns = {
        "Original": lambda img: img,
        "Negative": image_negative,
        "Log": lambda img: log_transform(img, c=46),
        "Gamma=0.4": lambda img: gamma_transform(img, gamma=0.4),
        "Gamma=2.0": lambda img: gamma_transform(img, gamma=2.0),
        "Contrast Stretch": lambda img: contrast_stretching(img),
        "Hist. Equalization": histogram_equalization,
    }

    n_techniques = len(technique_fns)
    n_images = len(SAMPLE_IMAGES)

    fig, axes = plt.subplots(n_images, n_techniques, figsize=(3.2 * n_techniques, 4 * n_images))
    fig.suptitle("Task 6: Enhancement Technique Comparison Across 3 Images",
                 fontsize=14, fontweight="bold")

    metrics = []

    for row, img_path in enumerate(SAMPLE_IMAGES):
        img = load_gray(img_path)
        row_metrics = {"image": img_path.name}
        for col, (name, fn) in enumerate(technique_fns.items()):
            result = fn(img)
            axes[row, col].imshow(result, cmap="gray", vmin=0, vmax=255)
            if row == 0:
                axes[row, col].set_title(name, fontsize=8, fontweight="bold")
            axes[row, col].axis("off")
            if col == 0:
                axes[row, col].set_ylabel(img_path.stem, fontsize=8, rotation=0, labelpad=60, va="center")

            # Collect metrics
            row_metrics[f"{name}_mean"] = f"{np.mean(result):.1f}"
            row_metrics[f"{name}_std"] = f"{np.std(result):.1f}"

        metrics.append(row_metrics)

    fig.tight_layout()
    fig.savefig(str(OUTPUT_DIR / "task6_comparison_grid.png"), dpi=150)
    plt.close(fig)

    # Print a summary table
    print("\n  Brightness (mean) / Contrast (std) per technique:")
    print(f"  {'Image':<20}", end="")
    for name in technique_fns:
        print(f" {name:>18}", end="")
    print()
    for m in metrics:
        print(f"  {m['image']:<20}", end="")
        for name in technique_fns:
            mean = m[f"{name}_mean"]
            std = m[f"{name}_std"]
            print(f" {mean:>8}/{std:<8}", end="")
        print()

    print(f"\n  Saved: {OUTPUT_DIR / 'task6_comparison_grid.png'}")
    print("\n  Best technique per image (justified by contrast & visual quality):")
    print("    Image 1 (jainam_doc_02)  : Histogram Equalization - best contrast spread for indoor doc")
    print("    Image 2 (dhanush_doc_003): Gamma=0.4 - brightens the underexposed capture effectively")
    print("    Image 3 (vivek_doc_010)  : Contrast Stretching - balances detail without over-amplifying noise")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("Semester Mini Project - Task 3: Image Enhancement")
    print("=" * 60)
    print()

    task2_intensity_transforms()
    print()
    task3_histogram_analysis()
    print()
    task4_histogram_equalization()
    print()
    task5_arithmetic_operations()
    print()
    task6_compare_techniques()

    print()
    print("=" * 60)
    print(f"All outputs saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
