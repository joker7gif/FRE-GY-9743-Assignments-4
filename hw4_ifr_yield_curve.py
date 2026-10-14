"""FRE-GT-9743 HW4 - Chuyu Wu. Run from the repository root."""
# %%
import numpy as np
import pandas as pd
from IPython.display import display

from fixedincomelib import (
    qfAddPeriod,
    qfAccrued,
    qfCreateData1D,
    qfCreateDataCollection,
    qfCreateBuildMethod,
    qfCreateModelBuildMethodCollection,
    qfCreateModel,
    qfDiscountFactor,
)
from fixedincomelib.date import Date

# %%
value_date = "2026-10-07"
payment_currency = "USD"  # Placeholder; currently ignored by the model.
query_tenors = ["6M", "1Y", "2Y", "5Y", "10Y", "15Y"]

projection_ifr = pd.DataFrame(
    {
        "values": [
            0.030, 0.031, 0.032, 0.033, 0.034,
            0.035, 0.036, 0.037, 0.038, 0.039,
        ]
    },
    index=pd.Index([f"{year}Y" for year in range(1, 11)], name="Tenor"),
)

funding_ifr = pd.DataFrame(
    {"values": [0.0]},
    index=pd.Index(["1Y"], name="Tenor"),
)

display(projection_ifr.rename(columns={"values": "SOFR-1B IFR"}))
display(funding_ifr.rename(columns={"values": "SOFR-1B-FLAT IFR spread"}))

# %%
projection_data = qfCreateData1D(
    "INSTANTANEOUS FORWARD RATE",
    "SOFR-1B-IFR",
    projection_ifr,
)

funding_data = qfCreateData1D(
    "INSTANTANEOUS FORWARD RATE",
    "SOFR-1B-FUNDING-IFR",
    funding_ifr,
)

data_collection = qfCreateDataCollection([projection_data, funding_data])
display(data_collection.display())

# %%
projection_bm = qfCreateBuildMethod(
    "YIELD_CURVE_INDEX",
    {
        "TARGET": "SOFR-1B",
        "INSTANTANEOUS FORWARD RATE": "SOFR-1B-IFR",
    },
)

funding_bm = qfCreateBuildMethod(
    "YIELD_CURVE_FUNDING",
    {
        "TARGET": "SOFR-1B-FLAT",
        "REFERENCE INDEX":"SOFR-1B",
        "INSTANTANEOUS FORWARD RATE": "SOFR-1B-FUNDING-IFR",
    },
)

build_methods = qfCreateModelBuildMethodCollection([projection_bm, funding_bm])

# %%
model = qfCreateModel(
    value_date,
    "YIELD_CURVE",
    data_collection,
    build_methods,
)

projection_component = model.retrieve_model_component(projection_bm.target_index)
funding_component = model.retrieve_model_component(funding_bm.target_index)

state_table = pd.concat(
    [
        pd.DataFrame({
            "Component": projection_bm.target,
            "Tenor": projection_data.axis1,
            "Time (years)": projection_component.state_data[0],
            "IFR": projection_component.state_data[1],
        }),
        pd.DataFrame({
            "Component": funding_bm.target,
            "Tenor": funding_data.axis1,
            "Time (years)": funding_component.state_data[0],
            "IFR": funding_component.state_data[1],
        }),
    ],
    ignore_index=True,
)

display(state_table)

# %%
query_dates = [value_date] + [
    qfAddPeriod(value_date, tenor, "F", "USGS")
    for tenor in query_tenors
]

discount_factors = pd.DataFrame({
    "Tenor": ["Value date"] + query_tenors,
    "Date": query_dates,
    "SOFR-1B": [
        qfDiscountFactor(model, "SOFR-1B", date, payment_currency)
        for date in query_dates
    ],
    "Funding component only": [
        funding_component.discount_factor(Date(date))
        for date in query_dates
    ],
    "SOFR-1B-FLAT": [
        qfDiscountFactor(model, "SOFR-1B-FLAT", date, payment_currency)
        for date in query_dates
    ],
})

display(discount_factors.round(8))

# %%
from fixedincomelib import qfCreateProductFixedAccruedCashflow

# Product inputs: edit these and rerun all three cells.
product_tenor = "5Y"
product_notional = 100.0
product_accrual_basis = "ACT/360"
termination_date = qfAddPeriod(value_date, product_tenor, "F", "USGS")

product = qfCreateProductFixedAccruedCashflow(
    effective_date=value_date,
    termination_date=termination_date,
    currency=payment_currency,
    notional=product_notional,
    accrual_basis=product_accrual_basis,
    payment_date=termination_date,
)

# %%
c = product.notional * product.accrued
df = qfDiscountFactor(
    model, "SOFR-1B-FLAT", product.payment_date.ISO(), payment_currency
)
V = c * df

price_table = pd.DataFrame([{
    "Payment date": product.payment_date.ISO(),
    "Cashflow (c)": c,
    "Discount factor": df,
    "Price (V)": V,
}])
display(price_table.round(8))

# %%
# Curve time uses the model's day count, not the product's accrual basis.
T = qfAccrued(
    model.value_date.ISO(), product.payment_date.ISO(), "ACT/ACT (ISDA)"
)

projection_interpolator = projection_component.state_data_interpolator
funding_interpolator = funding_component.state_data_interpolator
projection_weights = projection_interpolator.gradient_of_integrated_value_wrt_ordinate(0.0, T)
funding_weights = funding_interpolator.gradient_of_integrated_value_wrt_ordinate(0.0, T)

# Chain rule: V already includes both SOFR and funding discount factors.
projection_risk = -V * projection_weights
funding_risk = -V * funding_weights

# Parameter order: SOFR nodes, then funding nodes.
X_I = np.concatenate([
    projection_component.state_data[1], funding_component.state_data[1]
])
risk = np.concatenate([projection_risk, funding_risk])

risk_table = pd.DataFrame({
    "Component": (
        [projection_bm.target] * len(projection_risk)
        + [funding_bm.target] * len(funding_risk)
    ),
    "Tenor": projection_data.axis1 + funding_data.axis1,
    "IFR (X_I)": X_I,
    "dV/dX_I": risk,
})
display(risk_table.round(8))
