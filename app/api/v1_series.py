from fastapi import APIRouter, Query
from .. import state

router = APIRouter()

@router.get("/account-groups")
def account_groups():
    df = state.df
    if df is None or df.empty:
        return {"groups": []}
    col = next((c for c in ["Account group","account_group","Account Group"] if c in df.columns), None)
    if not col:
        return {"groups": ["Income (3xxx)","Costs (4xxx–7xxx)","Other (8xxx)","Assets (1xxx)","Liabilities/Equity (2xxx)"]}
    vals = sorted(df[col].astype(str).fillna("Unknown").str.strip().replace({"": "Unknown"}).unique().tolist())
    return {"groups": vals}

@router.get("/series/amount-by-group")
def series_amount_by_group(group: str | None = Query(None), window: int = Query(3, ge=1, le=24)):
    import pandas as pd
    df = state.df.copy()
    if df is None or df.empty:
        return {"series": [], "meta": {"group": group, "window": window}}

    col = next((c for c in ["Account group","account_group","Account Group"] if c in df.columns), None)
    if col and group:
        df = df[df[col].astype(str).str.strip() == group]
    elif not col and group:
        label = group.lower()
        if "income" in label: df = df[df["_acctnum"].between(3000,3999, inclusive="both")]
        elif "cost" in label: df = df[df["_acctnum"].between(4000,7999, inclusive="both")]
        elif "8xxx" in label or "other" in label: df = df[df["_acctnum"].between(8000,8999, inclusive="both")]
        elif "1xxx" in label or "asset" in label: df = df[df["_acctnum"].between(1000,1999, inclusive="both")]
        elif "2xxx" in label or "liab" in label or "equity" in label: df = df[df["_acctnum"].between(2000,2999, inclusive="both")]

    df["_month"] = df["_date"].dt.to_period("M").dt.to_timestamp()
    ts = (
        df.groupby("_month", as_index=False)["_amount_norm"]
          .sum()
          .rename(columns={"_month": "Date", "_amount_norm": "amount"})
          .sort_values("Date")
    )
    ts["amountMA"] = ts["amount"].rolling(window=window, min_periods=1).mean()
    ts["date"] = ts["Date"].dt.strftime("%Y-%m")
    return {"series": ts[["date","amount","amountMA"]].to_dict(orient="records"), "meta": {"group": group, "window": window}}