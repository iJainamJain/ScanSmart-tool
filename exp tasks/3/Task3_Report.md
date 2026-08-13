# Task 3 Report: Image Enhancement in the Spatial Domain

**Course:** Digital Image Processing — Semester Mini Project  
**Team:** SmartScan AI  

---

## Aim

To implement and analyse spatial-domain image enhancement techniques — intensity transformations, histogram operations, and image arithmetic — and integrate them as pre-processing capabilities in the SmartScan AI document scanner.

---

## Enhancement Techniques Implemented

### 1. Intensity Transformations (`src/enhancement/intensity.py`)

| Technique | Formula | Purpose |
|-----------|---------|---------|
| **Image Negative** | s = 255 − r | Inverts intensity; useful for enhancing white/bright details embedded in dark regions |
| **Log Transform** | s = c · log(1 + r) | Compresses high-intensity ranges, expands low-intensity ranges; useful for dark images |
| **Gamma (Power-Law)** | s = c · r^γ | γ < 1 brightens, γ > 1 darkens; widely used for display calibration and exposure correction |
| **Contrast Stretching** | Piecewise linear mapping | Stretches a narrow intensity band to [0, 255]; improves washed-out images |

### 2. Histogram Operations (`src/enhancement/histogram.py` + `intensity.py`)

- **Histogram Generation**: `cv2.calcHist` computes the frequency distribution of pixel intensities.
- **Histogram Equalization**: Redistributes pixel intensities so the CDF is approximately linear, maximising contrast.

### 3. Image Arithmetic (`src/enhancement/arithmetic.py`)

| Operation | Formula | Practical Application |
|-----------|---------|----------------------|
| **Addition** | α·I₁ + (1−α)·I₂ | Image fusion (combining multi-sensor data) |
| **Subtraction** | \|I₁ − I₂\| | Change/motion detection between frames |
| **Averaging** | (1/N) Σ Iₖ | Noise reduction (astrophotography, medical imaging) |

---

## Sample Input/Output Images

All generated figures are in `exp tasks/3/outputs/`:

- `task2_intensity_transforms.png` — Side-by-side comparison of all intensity transforms
- `task3_histogram_analysis.png` — Image + histogram before and after gamma enhancement
- `task4_histogram_equalization.png` — Original vs equalized with both histograms
- `task5_arithmetic_operations.png` — Addition, subtraction, and averaging demonstrations
- `task6_comparison_grid.png` — All techniques applied to 3 different images

---

## Observations

### Histogram Equalization (Task 4)
- The original histogram is clustered in a narrow band (low contrast).
- After equalization, the histogram spreads across the full [0, 255] range.
- Standard deviation increases noticeably, confirming improved contrast.
- **Conclusion**: Histogram equalization is effective for documents with poor/uneven lighting but can amplify noise in already-bright regions.

### Technique Comparison (Task 6)
- **Histogram Equalization** works best on indoor documents where contrast is inherently low — it pulls out text strokes that were barely visible.
- **Gamma correction (γ < 1)** is preferred for underexposed captures — it brightens without the harsh redistribution that equalization introduces.
- **Contrast Stretching** provides the most controlled enhancement — it expands a chosen intensity range without affecting regions outside the breakpoints.
- **Log Transform** is aggressive at compressing highlights; useful for documents photographed under strong directional light.
- **Negative** has limited practical use for document scanning but is essential in medical imaging (e.g., X-ray film → digital positive).

---

## Challenges Faced

1. **Parameter sensitivity**: Log and gamma transforms require careful tuning of `c` and `γ`; wrong values either wash out or crush the image.
2. **Noise amplification**: Histogram equalization amplifies sensor noise alongside useful detail — this is why our main pipeline uses CLAHE (localised equalization) instead.
3. **Arithmetic dimension mismatch**: Real dataset images have different resolutions, so arithmetic operations require explicit resizing before computation.

---

## Conclusion

Spatial-domain enhancement techniques are powerful tools for improving document image quality before segmentation. Through measurement (not guesswork), we confirmed that histogram equalization and gamma correction are the most impactful for our document scanning use case. These techniques are now available as reusable modules in our project and integrated into both the CLI and Streamlit GUI pipelines.
