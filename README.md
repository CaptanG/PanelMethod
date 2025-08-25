# Panel Method for an underwater body Added Mass Calculation

This repository implements a **3D panel method** to compute the **added mass** of an underwater body in heave (vertical oscillation). The added mass is an important hydrodynamic property that represents the additional inertia a body experiences due to the surrounding fluid.

The method discretizes the hull surface into panels, computes influence coefficients between them, and solves a boundary value problem using potential flow theory.

---

## Features

- Object-oriented implementation:
  - `Point` and `Vector` classes for geometry operations.
  - `Panel` class for quadrilateral panels with centroid, normal, and area calculation.
- Reads **mesh input** from a text file (`mesh_nptel.txt`).
- Constructs:
  - **Influence matrix (A)**.
  - **Right-hand side (B)** vector.
- Solves the resulting linear system for potential coefficients (`Φ`).
- Computes **added mass** in heave.
- Includes **3D panel visualization** using `matplotlib`.

---

## Input File Format

The code expects a mesh file named **`mesh_nptel.txt`** in the working directory. The file should contain:

1. **Number of points** on the first line.
2. A list of points (index, x, y, z).
3. **Number of panels** after the list of points.
4. A list of panels, where each line specifies the indices of four points forming a quadrilateral panel.

---

## Usage

### Requirements
- Python 3.x
- Libraries:
  - `numpy`
  - `matplotlib`

Install dependencies with:
```bash
pip install numpy matplotlib
