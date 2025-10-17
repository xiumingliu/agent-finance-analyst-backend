import pandas as pd

def load_transactions_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Date normalize (supports Date / DateKey / DateMonth)
    DATE = next((c for c in ["Date","date","DateKey","DateMonth"] if c in df.columns), None)
    if DATE is None:
        raise RuntimeError("No date-like column found")

    ser = df.copy()
    ser["_date"] = pd.to_datetime(ser[DATE], errors="coerce")

    if ser["_date"].isna().all():
        s = ser[DATE].astype(str).str.replace(r"\D", "", regex=True)
        ser["_date"] = pd.to_datetime(s, format="%Y%m%d", errors="coerce")
        msk = ser["_date"].isna() & s.str.len().eq(6)
        ser.loc[msk, "_date"] = pd.to_datetime(s[msk] + "01", format="%Y%m%d", errors="coerce")

    ser = ser.dropna(subset=["_date"])

    # Amount → numeric
    AMT = next((c for c in ["Amount","amount","Belopp","BELOPP"] if c in ser.columns), None)
    if not AMT:
        raise RuntimeError("Amount column not found")
    ser[AMT] = (
        ser[AMT].astype(str)
        .str.replace(r"\s", "", regex=True)
        .str.replace(",", ".", regex=False)
        .str.replace(r"[^\d\.-]", "", regex=True)
    )
    ser[AMT] = pd.to_numeric(ser[AMT], errors="coerce").fillna(0.0)

    # Account + normalized sign (flip 3xxx so income shows positive)
    ACCT = next((c for c in ["Account","account","ACCNO","account_no"] if c in ser.columns), None)
    ser["_acctnum"] = pd.to_numeric(
        ser[ACCT].astype(str).str.extract(r"(\d+)")[0], errors="coerce"
    ) if ACCT else pd.NA

    is_income = ser["_acctnum"].between(3000, 3999, inclusive="both")
    ser["_amount_norm"] = ser[AMT].where(~is_income, -ser[AMT])

    return ser