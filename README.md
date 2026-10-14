# FRE-GT-9743 Assignment 4

Chuyu Wu

## Files

- `hw4_ifr_yield_curve.ipynb`: written answer and completed computational tasks, with saved outputs.
- `hw4_ifr_yield_curve.py`: the same computational cells as a Python script.
- `HW4_Written_Answer.md`: separate copy of the written answer.
- `fixedincomelib/`: the complete course library, including the six completed methods.
- `static_files/`: conventions required by the library.

## Run

Use the instructor's Python 3.11 environment and install `requirements.txt`. Start Jupyter from this repository root and run all notebook cells, or run `python hw4_ifr_yield_curve.py` from the root. Keep `static_files` and `fixedincomelib` together with the notebook.

## Results and checks

Default 5Y cashflow: 507.22222222; discount factor: 0.85215599; price: 432.23245579. The funding spread is zero, so the complete funding curve equals the SOFR curve, but the funding node derivative is -2161.16227894 per unit decimal IFR.

All nine code cells were executed sequentially with Python 3.12, NumPy 2.3.5, pandas 2.2.3 and QuantLib 1.41. The instructor's requirements file is retained. Independent checks covered knot conventions, extrapolation, reversed integration limits, all eleven price derivatives, a positive funding spread, and date validation. Maximum absolute discrepancy between analytic and central-difference price derivatives was below 4e-8. The submitted risk calculations use analytic derivatives only.
