# quantum

This project is dedicated to exploring and implementing quantum algorithms using [Qiskit](https://docs.quantum.ibm.com/guides), an open-source quantum computing framework.

## Overview

This repository will serve as a collection of quantum algorithms, ranging from foundational concepts to advanced implementations. The goal is to provide a hands-on approach to learning quantum computing and experimenting with Qiskit.

## Features

- Implementation of quantum algorithms such as:
  - Simple Quantum Teleportation
  - Superdense Coding
  - Grover's Search Algorithm
  - Shor's Algorithm
  - Quantum Fourier Transform (QFT)
- Simulations and results using Qiskit Aer
- Support for running on IBM Quantum hardware #TODO

## Prerequisites

To get started, ensure you have the following installed:

- Python 3.11 or later
- Qiskit
- Jupyter Notebook

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
4. Open the Jupyter notebooks in the `notebooks/` directory.

5. If you want to run the code on IBM Quantum hardware, set up your IBM Quantum account and add input API token in designated place in the code.

## Usage

1. Run the Jupyter notebooks in the `notebooks/`.
2. Modify and experiment with the code to deepen your understanding.
