from fastapi import APIRouter, HTTPException
from ..state import df as GLOBAL_DF
from .. import state

router = APIRouter()

@router.get("/kpi/summary")
def kpi_summary():
    df = state.df
    if df is None or df.empty:
        raise HTTPException(500, "Dataframe not loaded")

    is_income = df["_acctnum"].between(3000, 3999, inclusive="both")
    is_cost   = df["_acctnum"].between(4000, 7999, inclusive="both")
    is_pl     = df["_acctnum"].between(3000, 8999, inclusive="both")

    latest_year = int(df["_date"].max().year)
    ytd = df[df["_date"].dt.year == latest_year]

    # show positive revenue; costs usually positive already; net = -sum(PL)
    revenue_ytd   = float(-(ytd.loc[is_income, "_amount_norm"].sum()))
    expenses_ytd  = float((ytd.loc[is_cost,   "_amount_norm"].sum()))
    net_result_ytd= float(-(ytd.loc[is_pl,     "_amount_norm"].sum()))

    return {
        "currency": "SEK",
        "period": {
            "year": latest_year,
            "from": None if ytd.empty else str(ytd["_date"].min().date()),
            "to":   None if ytd.empty else str(ytd["_date"].max().date()),
        },
        "revenue_ytd": revenue_ytd,
        "expenses_ytd": expenses_ytd,
        "net_result_ytd": net_result_ytd,
    }