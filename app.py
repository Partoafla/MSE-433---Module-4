import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EP Lab — Smart Case Planning & Workflow Tracking",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Hide sidebar and its toggle completely */
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* Content padding */
.main .block-container { padding-top: 16px !important; padding-bottom: 40px; }

/* ── KPI card ── */
.kpi-card {
    background: #f0f4ff; border-left: 4px solid #1a56db;
    border-radius: 8px; padding: 14px 18px; color: #0d1b2a;
}
.kpi-value { font-size: 24px; font-weight: 700; color: #1a56db; line-height: 1.2; }
.kpi-label { font-size: 11px; color: #6b7280; text-transform: uppercase;
             letter-spacing: 0.6px; margin-top: 4px; }

/* ── Callout boxes ── */
.box-yellow { background:#fffbeb; border-left:4px solid #f59e0b;
              border-radius:6px; padding:14px 18px; margin:8px 0; color:#1c1917; }
.box-red    { background:#fef2f2; border-left:4px solid #ef4444;
              border-radius:6px; padding:14px 18px; margin:8px 0; color:#1c1917; }
.box-green  { background:#f0fdf4; border-left:4px solid #22c55e;
              border-radius:6px; padding:14px 18px; margin:8px 0; color:#1c1917; }
.box-blue   { background:#eff6ff; border-left:4px solid #3b82f6;
              border-radius:6px; padding:14px 18px; margin:8px 0; color:#1c1917; }
.box-orange { background:#fff7ed; border:1px solid #f97316;
              border-radius:8px; padding:16px 20px; margin:12px 0; color:#1c1917; }

/* ── Risk badges ── */
.risk-low    { background:#f0fdf4; border:2px solid #22c55e;
               border-radius:10px; padding:20px; text-align:center; color:#1c1917; }
.risk-medium { background:#fffbeb; border:2px solid #f59e0b;
               border-radius:10px; padding:20px; text-align:center; color:#1c1917; }
.risk-high   { background:#fef2f2; border:2px solid #ef4444;
               border-radius:10px; padding:20px; text-align:center; color:#1c1917; }

/* ── Page titles ── */
.page-title {
    font-size: 28px; font-weight: 700; color: #0d1b2a;
    margin-bottom: 4px; line-height: 1.2;
}
.page-subtitle {
    font-size: 14px; color: #6b7280; margin-bottom: 22px; line-height: 1.65;
}

/* ── Equation box ── */
.eq-box {
    background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px;
    padding: 14px 18px; font-family: monospace; font-size: 12px;
    line-height: 1.8; margin: 8px 0; word-break: break-word; color: #0d1b2a;
}

/* ── Step labels (form / result column headers) ── */
.step-label {
    font-size: 11px; color: #6b7280; text-transform: uppercase;
    letter-spacing: 0.8px; font-weight: 600; margin-bottom: 6px; margin-top: 0;
}

/* ── Ghost button — Add to Day Schedule ── */
[data-testid="stMarkdownContainer"]:has(.ghost-btn-marker)
    + [data-testid="stButton"] button {
    background-color: #ffffff !important;
    color: #0d1b2a !important;
    border: 1.5px solid #0d1b2a !important;
}
[data-testid="stMarkdownContainer"]:has(.ghost-btn-marker)
    + [data-testid="stButton"] button:hover {
    background-color: #f8fafc !important;
}

/* ── Helper text below buttons ── */
.helper-text {
    font-size: 11px; color: #9ca3af; text-align: center; margin-top: 2px; margin-bottom: 0;
}

/* ── Consistent spacing between result sections ── */
.result-spacer { margin-top: 18px; }

/* ── Red outlined button (Clear Schedule) ── */
[data-testid="stMarkdownContainer"]:has(.red-btn-marker)
    + [data-testid="stButton"] button {
    background-color: #ffffff !important;
    color: #ef4444 !important;
    border: 1.5px solid #ef4444 !important;
}
[data-testid="stMarkdownContainer"]:has(.red-btn-marker)
    + [data-testid="stButton"] button:hover {
    background-color: #fef2f2 !important;
}

/* ── Red X delete button ── */
[data-testid="stMarkdownContainer"]:has(.del-btn-marker)
    + [data-testid="stButton"] button {
    background-color: transparent !important;
    color: #ef4444 !important;
    border: 1px solid #ef4444 !important;
    padding: 2px 6px !important;
    font-size: 12px !important;
    min-height: unset !important;
}
[data-testid="stMarkdownContainer"]:has(.del-btn-marker)
    + [data-testid="stButton"] button:hover {
    background-color: #fef2f2 !important;
}

/* ── Alternating case list rows ── */
[data-testid="stMarkdownContainer"]:has(.row-even-marker)
    + [data-testid="stHorizontalBlock"] {
    background-color: #f8fafc;
    border-radius: 4px;
    padding: 4px 2px;
}
[data-testid="stMarkdownContainer"]:has(.row-odd-marker)
    + [data-testid="stHorizontalBlock"] {
    background-color: #ffffff;
    border-radius: 4px;
    padding: 4px 2px;
}

/* ── Section label (reused across tabs) ── */
.section-label {
    font-size: 11px; color: #6b7280; text-transform: uppercase;
    letter-spacing: 0.8px; font-weight: 600; margin-bottom: 4px; margin-top: 8px;
}

/* ── Table header row (navy background) ── */
[data-testid="stMarkdownContainer"]:has(.table-header-marker)
    + [data-testid="stHorizontalBlock"] {
    background-color: #0d1b2a;
    border-radius: 6px 6px 0 0;
    padding: 6px 4px;
}
[data-testid="stMarkdownContainer"]:has(.table-header-marker)
    + [data-testid="stHorizontalBlock"] p,
[data-testid="stMarkdownContainer"]:has(.table-header-marker)
    + [data-testid="stHorizontalBlock"] strong {
    color: #ffffff !important;
    font-size: 12px;
    letter-spacing: 0.3px;
}

/* ── TEE / anatomy score panels ── */
.anatomy-score-value {
    font-size: 48px; font-weight: 300; font-family: monospace;
    line-height: 1; margin-bottom: 6px;
}
.rf-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 7px 0; border-bottom: 1px solid #e5e7eb; font-size: 13px; color: #374151;
}
.rf-row:last-child { border-bottom: none; }
.rf-val { font-family: monospace; font-size: 12px; font-weight: 600; }
.rf-pill { font-size: 11px; font-weight: 600; padding: 2px 9px; border-radius: 12px; margin-left: 8px; }
.pill-low  { background:#f0fdf4; color:#16a34a; }
.pill-mod  { background:#fffbeb; color:#d97706; }
.pill-high { background:#fef2f2; color:#dc2626; }
.bmi-flag { font-size: 12px; padding: 6px 12px; border-radius: 6px; margin-top: 6px; display: inline-block; }
.bmi-normal    { background:#f0fdf4; color:#15803d; border:1px solid #bbf7d0; }
.bmi-overweight{ background:#fffbeb; color:#b45309; border:1px solid #fde68a; }
.bmi-obese     { background:#fef2f2; color:#dc2626; border:1px solid #fecaca; }
.section-divider {
    font-size: 11px; color: #6b7280; text-transform: uppercase;
    letter-spacing: 0.8px; font-weight: 700;
    border-bottom: 2px solid #e5e7eb; padding-bottom: 4px; margin: 18px 0 12px;
}
</style>
""", unsafe_allow_html=True)

# ── Colour constants ──────────────────────────────────────────────────────────
BLUE   = "#1a56db"
GREEN  = "#22c55e"
ORANGE = "#f59e0b"
RED    = "#ef4444"
GREY   = "#6b7280"
NAVY   = "#0d1b2a"

PHYS_COLORS  = {"Dr. A": BLUE, "Dr. B": RED, "Dr. C": GREEN}
RISK_COLORS  = {"Low": GREEN, "Medium": ORANGE, "High": RED}
PHYS_MAP     = {"Dr. A": 0, "Dr. B": 1, "Dr. C": 2}

EXTRA_KEYWORDS = ["CTI", "BOX", "PST BOX", "SVC", "AAFL", "TROUBLESHOOT"]

COLS = [
    "CASE", "DATE", "PHYSICIAN", "PT_PREP", "ACCESS", "TSP", "PRE_MAP",
    "ABL_DURATION", "ABL_TIME", "N_ABL", "N_APP", "LA_DWELL", "CASE_TIME",
    "AVG_CASE_TIME", "SKIN_SKIN", "AVG_SKIN_SKIN", "POST_CARE",
    "AVG_TURNOVER", "PT_OUT_TIME", "PT_IN_OUT", "NOTE",
]
TIME_COLS = [
    "PT_PREP", "ACCESS", "TSP", "PRE_MAP", "ABL_DURATION", "ABL_TIME",
    "N_ABL", "N_APP", "LA_DWELL", "CASE_TIME", "AVG_CASE_TIME",
    "SKIN_SKIN", "AVG_SKIN_SKIN", "POST_CARE", "AVG_TURNOVER",
    "PT_OUT_TIME", "PT_IN_OUT",
]
STEP_COLS   = ["PT_PREP", "ACCESS", "TSP", "PRE_MAP", "ABL_DURATION", "POST_CARE"]
STEP_LABELS = ["Pt Prep", "Vascular Access", "TSP", "Pre-Map", "Ablation", "Post Care"]


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data() -> pd.DataFrame:
    # Row 0: blank | Row 1: title | Row 2: column headers (col 0 blank, data cols 1-21)
    # Row 3: units sub-header | Row 4+: case data
    df = pd.read_excel(
        "MSE433_M4_Data.xlsx",
        sheet_name="All Data",
        skiprows=2,
        header=0,
    )
    df = df.iloc[1:].reset_index(drop=True)           # drop units row
    df = df.iloc[:, 1 : len(COLS) + 1].copy()         # skip blank col 0
    df.columns = COLS

    df = df[df["CASE"].notna()].copy()
    df = df[df["CASE"].astype(str).str.strip().str.len() > 0].copy()
    df = df[df["PT_IN_OUT"].notna()].copy()
    df["_tmp"] = df["PT_IN_OUT"].astype(str).str.strip()
    df = df[~df["_tmp"].isin(["", "nan", "None"])].drop(columns="_tmp")

    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
    for c in TIME_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    def _is_extra(note):
        if pd.isna(note):
            return False
        return any(kw in str(note).upper() for kw in EXTRA_KEYWORDS)

    df["CASE_TYPE"]   = df["NOTE"].apply(lambda n: "Extra Procedure" if _is_extra(n) else "Standard PVI")
    df["MONTH"]       = df["DATE"].dt.to_period("M")
    df["MONTH_LABEL"] = df["DATE"].dt.strftime("%b %Y")
    return df


# ══════════════════════════════════════════════════════════════════════════════
# BENCHMARKS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def get_benchmarks(_df: pd.DataFrame) -> dict:
    df_std = _df[_df["CASE_TYPE"] == "Standard PVI"].copy()
    mask_d = df_std["PHYSICIAN"].astype(str).str.contains("Dr. D", na=False)
    df_sp  = df_std[~mask_d].copy()

    steps = {}
    for col, lbl in zip(STEP_COLS, STEP_LABELS):
        d = df_std[col].dropna()
        steps[col] = {
            "label": lbl, "mean": float(d.mean()), "median": float(d.median()),
            "std": float(d.std()), "min": float(d.min()), "max": float(d.max()),
            "p25": float(d.quantile(0.25)), "p75": float(d.quantile(0.75)),
            "p90": float(d.quantile(0.90)), "values": d.values, "n": len(d),
        }

    physician_steps = {}
    for phys in ["Dr. A", "Dr. B", "Dr. C"]:
        sub = df_sp[df_sp["PHYSICIAN"] == phys]
        physician_steps[phys] = {}
        for col, lbl in zip(STEP_COLS, STEP_LABELS):
            d = sub[col].dropna()
            n = len(d)
            if n >= 5:
                physician_steps[phys][col] = {
                    "label": lbl, "mean": float(d.mean()), "std": float(d.std()),
                    "p90": float(d.quantile(0.90)), "values": d.values, "n": n,
                }
            else:
                physician_steps[phys][col] = {**steps[col], "fallback": True}

    physician = {}
    physician_feature_means = {}
    for phys in ["Dr. A", "Dr. B", "Dr. C"]:
        sub = df_sp[df_sp["PHYSICIAN"] == phys]
        pt  = sub["PT_IN_OUT"].dropna()
        physician[phys] = {
            "mean": float(pt.mean()) if len(pt) > 0 else float(df_std["PT_IN_OUT"].mean()),
            "std":  float(pt.std())  if len(pt) > 1 else float(df_std["PT_IN_OUT"].std()),
            "n":    len(pt),
        }
        physician_feature_means[phys] = {
            "N_ABL":   float(sub["N_ABL"].dropna().mean())   if len(sub) > 0 else float(_df["N_ABL"].dropna().mean()),
            "PT_PREP": float(sub["PT_PREP"].dropna().mean()) if len(sub) > 0 else float(_df["PT_PREP"].dropna().mean()),
        }

    pt_vals = df_std["PT_IN_OUT"].dropna()
    tsp_vals = df_std["TSP"].dropna()

    return {
        "steps":                   steps,
        "physician":               physician,
        "physician_steps":         physician_steps,
        "physician_feature_means": physician_feature_means,
        "p50":      float(pt_vals.quantile(0.50)),
        "p75":      float(pt_vals.quantile(0.75)),
        "tsp_p25":  float(tsp_vals.quantile(0.25)),
        "tsp_med":  float(tsp_vals.median()),
        "tsp_p75":  float(tsp_vals.quantile(0.75)),
        "global_std_avg":  float(pt_vals.mean()),
        "global_std_std":  float(pt_vals.std()),
        "turnover_avg":    float(_df["AVG_TURNOVER"].dropna().mean()),
    }


# ══════════════════════════════════════════════════════════════════════════════
# LINEAR REGRESSION MODEL (numpy OLS — no scipy/sklearn needed)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def train_model():
    df = load_data()
    df_m = df.copy()
    df_m["EXTRA_FLAG"] = (df_m["CASE_TYPE"] == "Extra Procedure").astype(float)
    df_m["PHYS_ENC"]   = df_m["PHYSICIAN"].map(PHYS_MAP)

    feature_cols = ["N_ABL", "TSP", "PHYS_ENC", "PT_PREP", "EXTRA_FLAG"]
    df_m = df_m[feature_cols + ["PT_IN_OUT"]].dropna()

    X = df_m[feature_cols].values.astype(float)
    y = df_m["PT_IN_OUT"].values.astype(float)

    X_aug = np.column_stack([np.ones(len(X)), X])
    coeffs, _, _, _ = np.linalg.lstsq(X_aug, y, rcond=None)

    y_pred       = X_aug @ coeffs
    ss_res       = float(np.sum((y - y_pred) ** 2))
    ss_tot       = float(np.sum((y - y.mean()) ** 2))
    r2           = float(1.0 - ss_res / ss_tot) if ss_tot > 1e-10 else 0.0
    residual_std = float(np.std(y - y_pred))

    feat_display = [
        "Ablation Sites (N_ABL)",
        "TSP Duration (min)",
        "Physician (encoded: A=0, B=1, C=2)",
        "Patient Prep Time (min)",
        "Extra Procedure (0/1 flag)",
    ]
    return {
        "coeffs":       coeffs,
        "r2":           r2,
        "residual_std": residual_std,
        "n_train":      int(len(y)),
        "intercept":    float(coeffs[0]),
        "coefs":        coeffs[1:].tolist(),
        "feat_display": feat_display,
        "feature_cols": feature_cols,
    }


# ── Load ──────────────────────────────────────────────────────────────────────
try:
    df         = load_data()
    BMK        = get_benchmarks(df)
    MODEL_DATA = train_model()
except FileNotFoundError:
    st.error("Data file not found. Place MSE433_M4_Data.xlsx in the same folder as app.py and restart.")
    st.stop()
except Exception as exc:
    st.error(f"Failed to load data: {exc}")
    st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
if "schedule" not in st.session_state:
    st.session_state.schedule = []
if "risk_result" not in st.session_state:
    st.session_state.risk_result = None
if "risk_inputs" not in st.session_state:
    st.session_state.risk_inputs = None
if "calc_history" not in st.session_state:
    st.session_state.calc_history = []


# ══════════════════════════════════════════════════════════════════════════════
# RISK ENGINE  (unchanged logic)
# ══════════════════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════════
# ANATOMY SCORING — ported from AFib React repo (utils.js)
# Inputs: fossa ovalis (mm), septal angle (°), LA diameter (mm), prior, afib type, bmi, age
# ══════════════════════════════════════════════════════════════════════════════

def compute_anatomy_score(fo: float, sa: float, la: float,
                           prior: bool, afib: str,
                           bmi: float | None = None,
                           age: int | None = None) -> dict:
    """
    Composite anatomical risk score (0–100) combining TEE measurements,
    clinical history, BMI, and age. Ported + extended from the AFib React repo.
    Returns score, TSP difficulty level, and per-factor breakdown.
    """
    # Fossa ovalis thickness — main driver of TSP difficulty
    # Normal: 1.0–2.5 mm | Elevated: 2.5–3.5 mm | High: >3.5 mm
    fo_score = round(((fo - 1.0) / 5.0) * 30)          # 0–30 pts

    # Septal angle — unusual angle makes needle approach harder
    sa_score = 22 if sa > 85 else (12 if sa < 55 else 5)

    # Left atrial diameter — larger LA = more mapping complexity + more ablation sites
    la_score = 20 if la > 50 else (10 if la > 42 else 3)

    # Prior ablation — scar tissue significantly raises TSP difficulty
    prior_score = 18 if prior else 0

    # AFib type — persistent/long-standing usually requires additional lesion sets
    afib_map = {"Paroxysmal": 0, "Persistent": 10, "Long-Standing Persistent": 18}
    afib_score = afib_map.get(afib, 0)

    # BMI — obesity proxy for access difficulty and prep time (guest lecture)
    bmi_score = 0
    bmi_flag  = "Normal"
    if bmi is not None and bmi > 0:
        if bmi >= 35:
            bmi_score = 10; bmi_flag = "Obese (Class II+)"
        elif bmi >= 30:
            bmi_score = 6;  bmi_flag = "Obese (Class I)"
        elif bmi >= 25:
            bmi_score = 3;  bmi_flag = "Overweight"
        else:
            bmi_flag = "Normal"

    # Age — older patients have higher procedural risk and longer recovery
    age_score = 0
    if age is not None and age > 0:
        if age >= 80:   age_score = 8
        elif age >= 70: age_score = 5
        elif age >= 60: age_score = 2

    raw = fo_score + sa_score + la_score + prior_score + afib_score + bmi_score + age_score + 5
    score = min(100, raw)

    # TSP difficulty from imaging measurements (matches AFib repo logic)
    if fo > 3.5 or sa > 85 or prior:
        tsp_difficulty = "High"
        tsp_pred_text  = "12–25+ min"
        tsp_body = (
            "Thick fossa ovalis or unusual septal angle detected. "
            "Recommend: first case of day, most experienced physician, "
            "RF needle + ICE echo guidance ready before incision."
        )
    elif fo > 2.5 or sa > 75:
        tsp_difficulty = "Medium"
        tsp_pred_text  = "6–12 min"
        tsp_body = (
            "Fossa ovalis slightly thickened. "
            "Standard needle approach with ICE guidance on standby. "
            "Recommend scheduling as 2nd case of day."
        )
    else:
        tsp_difficulty = "Low"
        tsp_pred_text  = "2–6 min"
        tsp_body = (
            "Normal septal anatomy detected. "
            "Routine approach. No special preparation needed."
        )

    return {
        "score":          score,
        "tsp_difficulty": tsp_difficulty,
        "tsp_pred_text":  tsp_pred_text,
        "tsp_body":       tsp_body,
        "bmi_flag":       bmi_flag,
        "breakdown": {
            "Fossa ovalis thickness":   fo_score,
            "Septal angle":             sa_score,
            "Left atrial diameter":     la_score,
            "Prior ablation":           prior_score,
            "AFib type":                afib_score,
            "BMI":                      bmi_score,
            "Age":                      age_score,
        },
    }


def riskLevel_anatomy(score: int) -> str:
    if score >= 65: return "High"
    if score >= 35: return "Moderate"
    return "Low"


# ══════════════════════════════════════════════════════════════════════════════
# RISK ENGINE — OLS model (unchanged) + anatomy augmentation
# ══════════════════════════════════════════════════════════════════════════════
def compute_risk(prior_ablation, anatomy, extra_proc, physician, time_of_day,
                 fo=2.5, sa=70, la=40, afib_type="Paroxysmal",
                 bmi=None, age=None) -> dict:
    """
    Extended risk function. Combines:
      - OLS regression model (trained on 145 cases) → predicted duration + CI
      - Anatomical score (TEE measurements, BMI, age) → composite 0-100 score
      - Scheduling logic from original Streamlit app (unchanged)
    """
    md = MODEL_DATA

    # ── OLS prediction (original logic preserved exactly) ──
    prior_bool = prior_ablation == "Yes"
    tsp_base   = {"Simple": BMK["tsp_p25"], "Moderate": BMK["tsp_med"], "Complex": BMK["tsp_p75"]}[anatomy]
    tsp_est    = tsp_base + (8.0 if prior_bool else 0.0)
    tsp_est    = min(tsp_est, BMK["steps"]["TSP"]["max"])

    # If TEE measurements available, refine TSP estimate from actual fossa ovalis thickness
    if fo != 2.5 or sa != 70:   # non-default → user entered real measurements
        if fo > 3.5 or sa > 85 or prior_bool:
            tsp_est = max(tsp_est, BMK["tsp_p75"] + (8.0 if prior_bool else 0.0))
        elif fo > 2.5 or sa > 75:
            tsp_est = max(tsp_est, BMK["tsp_med"])

    # BMI → adjust PT_PREP estimate
    phys_fm  = BMK["physician_feature_means"][physician]
    n_abl    = phys_fm["N_ABL"]
    pt_prep  = phys_fm["PT_PREP"]
    if bmi is not None and bmi >= 35:
        pt_prep += 10      # obese: significant positioning difficulty (guest lecture)
    elif bmi is not None and bmi >= 30:
        pt_prep += 5
    elif bmi is not None and bmi >= 25:
        pt_prep += 2

    extra_flag = 0.0 if extra_proc == "None — Standard PVI Only" else 1.0
    phys_enc   = float(PHYS_MAP[physician])

    x_vec     = np.array([1.0, n_abl, tsp_est, phys_enc, pt_prep, extra_flag])
    predicted = float(np.dot(md["coeffs"], x_vec))
    predicted = max(40.0, predicted)

    lo = max(40.0, predicted - md["residual_std"])
    hi = predicted + md["residual_std"]

    risk = "Low" if predicted < BMK["p50"] else ("Medium" if predicted < BMK["p75"] else "High")

    # ── Anatomy score (new — from AFib repo) ──
    anat = compute_anatomy_score(fo, sa, la, prior_bool, afib_type, bmi, age)
    anat_level = riskLevel_anatomy(anat["score"])

    # ── Risk drivers ──
    score   = 0
    drivers = []

    if prior_bool:
        score += 1
        drivers.append(f"Prior ablation — TSP raised to {tsp_est:.0f} min (scar tissue effect).")

    if anatomy == "Moderate":
        score += 1
        drivers.append(f"Moderate anatomy — TSP estimated at {tsp_est:.0f} min (historical median).")
    elif anatomy == "Complex":
        score += 2
        drivers.append(f"Complex anatomy — TSP estimated at {tsp_est:.0f} min (historical 75th percentile).")

    # TEE-derived drivers
    if fo > 3.5:
        drivers.append(f"Fossa ovalis {fo:.1f} mm — thick septum significantly increases TSP difficulty.")
    elif fo > 2.5:
        drivers.append(f"Fossa ovalis {fo:.1f} mm — mildly thickened; monitor TSP duration carefully.")
    if sa > 85:
        drivers.append(f"Septal angle {sa}° — unusual angle expected to complicate needle approach.")
    if la > 50:
        drivers.append(f"Left atrial diameter {la} mm — enlarged LA may require additional ablation sites.")
    elif la > 42:
        drivers.append(f"Left atrial diameter {la} mm — borderline enlarged; watch pre-map duration.")

    # AFib type
    afib_drivers = {
        "Persistent":             "Persistent AFib — additional lesion sets (BOX/PST BOX) likely; increases ablation time.",
        "Long-Standing Persistent":"Long-standing persistent AFib — highest complexity; plan for extended ablation duration.",
    }
    if afib_type in afib_drivers:
        score += 1 if afib_type == "Persistent" else 2
        drivers.append(afib_drivers[afib_type])

    # BMI
    if bmi is not None and bmi >= 35:
        score += 2
        drivers.append(f"BMI {bmi:.0f} — Class II+ obesity. Expect extended PT prep (+10 min est.) and access difficulty.")
    elif bmi is not None and bmi >= 30:
        score += 1
        drivers.append(f"BMI {bmi:.0f} — Class I obesity. Prep time adjustment applied (+5 min est.).")
    elif bmi is not None and bmi >= 25:
        drivers.append(f"BMI {bmi:.0f} — overweight. Minor prep adjustment applied (+2 min est.).")

    # Age
    if age is not None and age >= 80:
        score += 2
        drivers.append(f"Age {age} — elevated procedural risk; longer post-care and recovery monitoring expected.")
    elif age is not None and age >= 70:
        score += 1
        drivers.append(f"Age {age} — slightly increased monitoring time expected in post-care.")

    extra_scores = {"CTI Ablation": 1, "BOX Isolation": 2, "SVC Isolation": 2, "Multiple Extra Procedures": 3}
    if extra_proc in extra_scores:
        score += extra_scores[extra_proc]
        drivers.append(f"{extra_proc} flagged — increases predicted time via extra procedure coefficient.")

    if physician == "Dr. C":
        drivers.append(f"Dr. C has only {BMK['physician']['Dr. C']['n']} cases — prediction uncertainty is higher.")

    if time_of_day == "Afternoon":
        score += 1
        drivers.append("Afternoon slot — elevated overrun risk regardless of predicted duration.")

    # TSP label for display
    tsp_s     = {"Simple": 0, "Moderate": 1, "Complex": 2}[anatomy] + (1 if prior_bool else 0)
    if fo > 3.5 or sa > 85: tsp_s = max(tsp_s, 2)
    tsp_label = {0: "Low (2–8 min)", 1: "Moderate (8–20 min)"}.get(tsp_s, "High (15–37 min)")

    sched_map = {
        ("Low",    "Morning"):   "Suitable for any slot.",
        ("Low",    "Afternoon"): "Suitable for afternoon slot — low complexity.",
        ("Medium", "Morning"):   "Schedule early in the morning block to allow buffer if case runs long.",
        ("Medium", "Afternoon"): "Prefer morning block — medium complexity risks afternoon overrun.",
        ("High",   "Morning"):   "First morning slot only. Reserve a 2.5–3.5 hr block. Alert backup team.",
        ("High",   "Afternoon"): "Reschedule to first morning slot. High complexity in afternoon is high overrun risk.",
    }
    sched_rec = sched_map.get((risk, time_of_day), "Refer to scheduling coordinator.")

    return {
        "score":      score,
        "risk":       risk,
        "lo":         lo,
        "hi":         hi,
        "center":     predicted,
        "tsp_label":  tsp_label,
        "tsp_est":    tsp_est,
        "sched_rec":  sched_rec,
        "drivers":    drivers,
        "r2":         md["r2"],
        # New anatomy fields
        "anatomy_score":  anat["score"],
        "anatomy_level":  anat_level,
        "tsp_difficulty": anat["tsp_difficulty"],
        "tsp_pred_text":  anat["tsp_pred_text"],
        "tsp_body":       anat["tsp_body"],
        "bmi_flag":       anat.get("bmi_flag", ""),
        "anat_breakdown": anat["breakdown"],
    }


# ── UI helpers ────────────────────────────────────────────────────────────────
def kpi_card(label, value, color=BLUE):
    return (
        f"<div class='kpi-card' style='border-left-color:{color}'>"
        f"<div class='kpi-value' style='color:{color}'>{value}</div>"
        f"<div class='kpi-label'>{label}</div></div>"
    )


def duration_gauge(predicted: float, lo: float, hi: float) -> go.Figure:
    """Horizontal gauge showing predicted duration vs historical distribution."""
    std_pt   = df[df["CASE_TYPE"] == "Standard PVI"]["PT_IN_OUT"].dropna()
    hist_min = float(std_pt.min())
    hist_max = float(std_pt.max())
    p25      = float(std_pt.quantile(0.25))
    p50      = float(std_pt.quantile(0.50))
    p75      = float(std_pt.quantile(0.75))

    fig = go.Figure()

    # Invisible base trace to establish axis range
    fig.add_trace(go.Scatter(
        x=[hist_min - 8, hist_max + 8], y=[0.5, 0.5],
        mode="markers", marker=dict(opacity=0, size=1),
        showlegend=False, hoverinfo="skip",
    ))

    # Color zone backgrounds
    for x0, x1, color in [
        (hist_min, p50,      "#dcfce7"),
        (p50,      p75,      "#fef9c3"),
        (p75,      hist_max, "#fee2e2"),
    ]:
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=0.30, y1=0.70,
                      fillcolor=color, line_width=0)

    # Prediction interval band
    fig.add_shape(type="rect", x0=lo, x1=hi, y0=0.25, y1=0.75,
                  fillcolor=BLUE, opacity=0.22, line_width=0)

    # Predicted value marker (vertical line)
    fig.add_shape(type="line", x0=predicted, x1=predicted, y0=0.12, y1=0.88,
                  line=dict(color=BLUE, width=3))

    # Predicted value label
    fig.add_annotation(x=predicted, y=0.92, xanchor="center", yanchor="bottom",
                       text=f"<b>{predicted:.0f} min</b>",
                       showarrow=False, font=dict(color=BLUE, size=12))

    # Tick marks and labels at key percentiles
    for pval, plabel in [
        (hist_min, f"Min<br>{hist_min:.0f}"),
        (p25,      f"P25<br>{p25:.0f}"),
        (p50,      f"Median<br>{p50:.0f}"),
        (p75,      f"P75<br>{p75:.0f}"),
        (hist_max, f"Max<br>{hist_max:.0f}"),
    ]:
        fig.add_shape(type="line", x0=pval, x1=pval, y0=0.27, y1=0.30,
                      line=dict(color="#94a3b8", width=1))
        fig.add_annotation(x=pval, y=0.20, xanchor="center", yanchor="top",
                           text=plabel, showarrow=False,
                           font=dict(color="#94a3b8", size=9))

    fig.update_layout(
        height=135,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(range=[hist_min - 8, hist_max + 8], visible=False),
        yaxis=dict(range=[0, 1.1], visible=False),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_risk, tab_schedule, tab_debrief = st.tabs([
    "Pre-Case Risk Score", "OR Day Schedule Builder", "Post-Case Debrief"
])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — PRE-CASE RISK SCORE
# ══════════════════════════════════════════════════════════════════════════════
with tab_risk:
    st.markdown("<div class='page-title'>Pre-Case Risk Score</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>"
        "Enter patient details and TEE imaging measurements to generate a pre-case risk assessment. "
        "The OLS model (R²=0.49, n=145 cases) predicts case duration. "
        "TEE measurements produce a separate anatomical difficulty score."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<hr style='border:none;border-top:1.5px solid #0d1b2a;margin:0 0 22px 0'>",
        unsafe_allow_html=True,
    )

    col_form, col_result = st.columns([1, 1.2], gap="large")

    with col_form:

        # ── Patient demographics ──────────────────────────────────────────────
        st.markdown("<div class='section-divider'>Patient demographics</div>", unsafe_allow_html=True)
        with st.container(border=True):
            d1, d2 = st.columns(2)
            patient_first = d1.text_input("First name", placeholder="e.g. Maria", key="risk_first")
            patient_last  = d2.text_input("Last name",  placeholder="e.g. Okonkwo", key="risk_last")
            d3, d4, d5 = st.columns(3)
            patient_dob = d3.date_input("Date of birth", value=None, key="risk_dob",
                                        help="Used to calculate age automatically.")
            patient_mrn = d4.text_input("MRN", placeholder="e.g. 2026-0412", key="risk_mrn")
            # Derive age from DOB; fall back to manual entry if DOB not set
            if patient_dob is not None:
                from datetime import date as _date
                patient_age = (_date.today() - patient_dob).days // 365
                d5.metric("Age", f"{patient_age} yrs", help="Calculated from date of birth.")
            else:
                patient_age = d5.number_input("Age (if DOB unknown)", min_value=18,
                                              max_value=99, value=65, step=1, key="risk_age")
            patient_label = st.text_input(
                "Case label (optional)",
                placeholder="e.g. Pt 001 — appears in history log",
                key="risk_label"
            )

        # ── Scheduling ────────────────────────────────────────────────────────
        st.markdown("<div class='section-divider'>Scheduling</div>", unsafe_allow_html=True)
        with st.container(border=True):
            s1, s2, s3 = st.columns(3)
            physician   = s1.selectbox("Physician", ["Dr. A", "Dr. B", "Dr. C"], key="risk_phys")
            sched_time  = s2.time_input("Scheduled time", key="risk_time")
            time_of_day = s3.radio("Time of day", ["Morning", "Afternoon"], horizontal=True, key="risk_tod")

        # ── Clinical profile ──────────────────────────────────────────────────
        st.markdown("<div class='section-divider'>Clinical profile</div>", unsafe_allow_html=True)
        with st.container(border=True):
            c1, c2 = st.columns(2)
            afib_type = c1.selectbox(
                "AFib type",
                ["Paroxysmal", "Persistent", "Long-Standing Persistent"],
                key="risk_afib",
                help="Persistent/long-standing AFib typically requires additional lesion sets beyond standard PVI."
            )
            prior_ablation = c2.radio(
                "Prior ablation?", ["No", "Yes"], horizontal=True, key="risk_prior",
                help="Redo cases have scar tissue that significantly raises TSP difficulty."
            )
            c3, c4 = st.columns(2)
            extra_proc = c3.selectbox(
                "Extra procedure planned?",
                ["None — Standard PVI Only", "CTI Ablation", "BOX Isolation",
                 "SVC Isolation", "Multiple Extra Procedures"],
                key="risk_extra",
                help="Any additional ablation target beyond standard pulmonary vein isolation."
            )
            bmi_val = c4.number_input(
                "BMI (optional)",
                min_value=0.0, max_value=70.0, value=0.0, step=0.5, key="risk_bmi",
                help="Used to flag access difficulty and adjust prep time estimate. Not in current dataset."
            )
            bmi_input = bmi_val if bmi_val > 0 else None
            clinical_notes = st.text_area(
                "Clinical notes (optional)",
                placeholder="e.g. Difficult venous access history. Active cold flagged. Anticoagulation managed.",
                height=72, key="risk_notes"
            )

        # ── TEE ultrasound measurements ───────────────────────────────────────
        st.markdown("<div class='section-divider'>TEE ultrasound measurements</div>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:12px;color:#6b7280;margin:-6px 0 10px'>From pre-procedure imaging. "
            "These drive the TSP difficulty prediction and anatomical risk score. "
            "Leave at defaults if imaging is not yet available — confidence will be lower.</p>",
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            fo_val = st.slider(
                "Fossa ovalis thickness (mm)",
                min_value=1.0, max_value=6.0, value=2.5, step=0.1, key="risk_fo",
                help="Normal: 1.0–2.5 mm · Elevated: 2.5–3.5 mm · High risk: >3.5 mm"
            )
            sa_val = st.slider(
                "Septal angle (°)",
                min_value=40, max_value=110, value=70, step=1, key="risk_sa",
                help="Normal: 55–80° · Difficult: >85°"
            )
            la_val = st.slider(
                "Left atrial diameter (mm)",
                min_value=30, max_value=65, value=40, step=1, key="risk_la",
                help="Normal: <40 mm · Borderline: 40–50 mm · Enlarged: >50 mm"
            )

            # Inline measurement summary
            fo_flag = "high" if fo_val > 3.5 else ("mod" if fo_val > 2.5 else "low")
            sa_flag = "high" if sa_val > 85 else ("mod" if sa_val < 55 else "low")
            la_flag = "high" if la_val > 50 else ("mod" if la_val > 42 else "low")
            pill_css = {"low": "pill-low", "mod": "pill-mod", "high": "pill-high"}
            fo_txt = "High risk" if fo_val > 3.5 else ("Elevated" if fo_val > 2.5 else "Normal")
            sa_txt = "Difficult" if sa_val > 85 else ("Steep" if sa_val < 55 else "Normal")
            la_txt = "Enlarged" if la_val > 50 else ("Borderline" if la_val > 42 else "Normal")

            tc1, tc2, tc3 = st.columns(3)
            tc1.markdown(
                f"<div style='font-size:11px;color:#6b7280;margin-bottom:2px'>Fossa ovalis</div>"
                f"<div style='font-size:14px;font-weight:600'>{fo_val:.1f} mm "
                f"<span class='rf-pill {pill_css[fo_flag]}'>{fo_txt}</span></div>",
                unsafe_allow_html=True
            )
            tc2.markdown(
                f"<div style='font-size:11px;color:#6b7280;margin-bottom:2px'>Septal angle</div>"
                f"<div style='font-size:14px;font-weight:600'>{sa_val}° "
                f"<span class='rf-pill {pill_css[sa_flag]}'>{sa_txt}</span></div>",
                unsafe_allow_html=True
            )
            tc3.markdown(
                f"<div style='font-size:11px;color:#6b7280;margin-bottom:2px'>Left atrium</div>"
                f"<div style='font-size:14px;font-weight:600'>{la_val} mm "
                f"<span class='rf-pill {pill_css[la_flag]}'>{la_txt}</span></div>",
                unsafe_allow_html=True
            )

        # ── Derive anatomy level from TEE for OLS model ───────────────────────
        # Anatomy complexity slider removed — TEE measurements are the single source of truth
        if fo_val > 3.5 or sa_val > 85:
            anatomy = "Complex"
        elif fo_val > 2.5 or sa_val > 75:
            anatomy = "Moderate"
        else:
            anatomy = "Simple"

        # ── Buttons ───────────────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        calc_clicked = st.button("Calculate Risk", type="primary", use_container_width=True)
        st.markdown('<span class="ghost-btn-marker"></span>', unsafe_allow_html=True)
        add_sched = st.button(
            "Add to Day Schedule",
            use_container_width=True,
            disabled=st.session_state.risk_result is None,
        )
        st.markdown(
            "<p class='helper-text'>Add to Day Schedule is only available after calculating risk.</p>",
            unsafe_allow_html=True,
        )

    # ── Compute on click ──────────────────────────────────────────────────────
    if calc_clicked:
        result = compute_risk(
            prior_ablation, anatomy, extra_proc, physician, time_of_day,
            fo=fo_val, sa=sa_val, la=la_val,
            afib_type=afib_type, bmi=bmi_input, age=int(patient_age)
        )
        st.session_state.risk_result = result
        st.session_state.risk_inputs = {
            "physician": physician, "anatomy": anatomy, "extra_proc": extra_proc,
            "prior": prior_ablation, "time_of_day": time_of_day,
            "fo": fo_val, "sa": sa_val, "la": la_val,
            "afib_type": afib_type, "bmi": bmi_input, "age": int(patient_age),
        }
        name_str = f"{patient_first} {patient_last}".strip() or "—"
        lbl = patient_label.strip() or f"Calculation {len(st.session_state.calc_history) + 1}"
        st.session_state.calc_history.append({
            "Label":       lbl,
            "Patient":     name_str,
            "MRN":         patient_mrn or "—",
            "Age":         int(patient_age),
            "Physician":   physician,
            "AFib Type":   afib_type,
            "Extra Proc":  extra_proc.replace("None — Standard PVI Only", "Standard PVI"),
            "Prior Abl.":  prior_ablation,
            "BMI":         f"{bmi_input:.0f}" if bmi_input else "—",
            "FO (mm)":     f"{fo_val:.1f}",
            "SA (°)":      str(sa_val),
            "LA (mm)":     str(la_val),
            "Sched. Risk": result["risk"],
            "Anat. Score": result["anatomy_score"],
            "TSP Pred.":   result["tsp_difficulty"],
            "Duration":    f"{result['lo']:.0f}–{result['hi']:.0f} min",
        })

    r = st.session_state.risk_result

    # ── Results column ────────────────────────────────────────────────────────
    with col_result:
        if r is None:
            st.markdown(
                "<div style='display:flex;align-items:center;justify-content:center;"
                "min-height:500px;text-align:center;color:#9ca3af;'>"
                "<div><div style='font-size:32px;margin-bottom:14px'>📋</div>"
                "<div style='font-size:15px;line-height:1.7'>"
                "Complete the form and click<br><b>Calculate Risk</b> to see the assessment."
                "</div></div></div>",
                unsafe_allow_html=True,
            )
        else:
            risk_color = RISK_COLORS[r["risk"]]
            anat_color = {"Low": GREEN, "Moderate": ORANGE, "High": RED}[r["anatomy_level"]]
            tsp_color  = {"Low": GREEN, "Medium": ORANGE, "High": RED}[r["tsp_difficulty"]]

            # ══════════════════════════════════════════════════════════════════
            # GROUP 1 — SCHEDULING RISK (OLS model output)
            # ══════════════════════════════════════════════════════════════════
            st.markdown(
                "<div style='font-size:11px;font-weight:700;color:#6b7280;"
                "text-transform:uppercase;letter-spacing:.08em;"
                "border-bottom:2px solid #e5e7eb;padding-bottom:5px;margin-bottom:12px'>"
                "Scheduling risk — OLS model</div>",
                unsafe_allow_html=True,
            )
            with st.container(border=True):

                # Overall risk verdict
                risk_bg  = {"Low":"#f0fdf4","Medium":"#fffbeb","High":"#fef2f2"}[r["risk"]]
                risk_bdr = {"Low":"#22c55e","Medium":"#f59e0b","High":"#ef4444"}[r["risk"]]
                risk_sub = {
                    "Low":    "Predicted duration below historical median — fits standard slot.",
                    "Medium": "Predicted duration between 50th–75th percentile — add buffer time.",
                    "High":   "Predicted duration above 75th percentile — extended slot required.",
                }[r["risk"]]
                st.markdown(
                    f"<div style='background:{risk_bg};border:1.5px solid {risk_bdr};"
                    f"border-radius:8px;padding:14px 18px;margin-bottom:14px'>"
                    f"<div style='font-size:22px;font-weight:700;color:{risk_color}'>"
                    f"{r['risk']} Overrun Risk</div>"
                    f"<div style='font-size:13px;color:#374151;margin-top:4px'>{risk_sub}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                # Duration gauge
                st.markdown(
                    "<div style='font-size:12px;font-weight:600;color:#374151;"
                    "margin-bottom:4px'>Predicted duration vs historical distribution</div>",
                    unsafe_allow_html=True,
                )
                st.plotly_chart(
                    duration_gauge(r["center"], r["lo"], r["hi"]),
                    use_container_width=True, config={"displayModeBar": False},
                )

                # Duration + scheduling KPIs
                kc1, kc2 = st.columns(2)
                kc1.markdown(
                    kpi_card("Predicted duration", f"{r['lo']:.0f}–{r['hi']:.0f} min", risk_color),
                    unsafe_allow_html=True
                )
                kc2.markdown(
                    kpi_card("Recommended slot",
                             "60 min" if r["center"] < 60 else ("90 min" if r["center"] < 80 else "120 min"),
                             NAVY),
                    unsafe_allow_html=True
                )

                st.markdown("<br>", unsafe_allow_html=True)

                # Scheduling recommendation
                sched_bg  = "#fffbeb"
                sched_bdr = "#f59e0b"
                if r["risk"] == "Low":   sched_bg, sched_bdr = "#f0fdf4", "#22c55e"
                if r["risk"] == "High":  sched_bg, sched_bdr = "#fef2f2", "#ef4444"
                st.markdown(
                    f"<div style='background:{sched_bg};border-left:4px solid {sched_bdr};"
                    f"border-radius:0 6px 6px 0;padding:12px 16px'>"
                    f"<div style='font-size:11px;font-weight:700;color:#6b7280;"
                    f"text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px'>"
                    f"Scheduling recommendation</div>"
                    f"<div style='font-size:13px;color:#1c1917'>{r['sched_rec']}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                st.markdown("<br>", unsafe_allow_html=True)

                # Risk drivers
                st.markdown(
                    "<div style='font-size:12px;font-weight:600;color:#374151;margin-bottom:6px'>"
                    "Risk drivers</div>",
                    unsafe_allow_html=True,
                )
                if r["drivers"]:
                    for d in r["drivers"]:
                        st.markdown(f"- {d}")
                else:
                    st.markdown(
                        "<div style='font-size:13px;color:#16a34a'>No significant risk factors identified.</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                # ── How this prediction works (OLS model) ─────────────────────
                with st.expander("How this prediction works"):
                    md_  = MODEL_DATA
                    coef = md_["coefs"]
                    r2_v = md_["r2"]
                    st.markdown(
                        f"<p style='font-size:12px;color:{GREY};margin:0 0 10px'>"
                        f"R² = {r2_v:.3f} — the OLS model explains {r2_v*100:.0f}% of case time variance. "
                        f"Remaining variance reflects unobserved factors: staff composition, equipment status, "
                        f"PACU availability, patient anatomy not captured in the dataset."
                        f" | Trained on {md_['n_train']} cases.</p>",
                        unsafe_allow_html=True,
                    )
                    signs = [("+" if c >= 0 else "−") for c in coef]
                    terms = "  ".join(
                        f"{s} {abs(c):.2f}×({n})"
                        for s, c, n in zip(signs, coef, md_["feat_display"])
                    )
                    st.markdown(
                        f"<div class='eq-box'>Predicted PT_IN_OUT = {md_['intercept']:.1f}  {terms}</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown("**What each coefficient means:**")
                    for exp in [
                        f"N_ABL ({coef[0]:+.2f} min/site): each extra ablation site ≈ {abs(coef[0]):.1f} min.",
                        f"TSP ({coef[1]:+.2f} min/min): each extra TSP minute cascades into total time — largest variability source.",
                        f"Physician ({coef[2]:+.2f} min/unit): A=0, B=1, C=2; captures workflow differences.",
                        f"PT Prep ({coef[3]:+.2f} min/min): extra prep time (e.g. obesity) propagates into duration.",
                        f"Extra Proc ({coef[4]:+.2f} min): any extra ablation target adds ~{abs(coef[4]):.0f} min average.",
                    ]:
                        st.markdown(f"- {exp}")
                    st.markdown(
                        "<div class='box-orange' style='font-size:12px;margin-top:10px'>"
                        "The anatomical risk score (0–100) is a separate composite index from TEE measurements, "
                        "BMI, and age. It is not part of the OLS model and does not affect the duration prediction — "
                        "it provides clinical context for procedural difficulty."
                        "</div>",
                        unsafe_allow_html=True,
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            # ══════════════════════════════════════════════════════════════════
            # GROUP 2 — ANATOMICAL ASSESSMENT (TEE measurements)
            # ══════════════════════════════════════════════════════════════════
            st.markdown(
                "<div style='font-size:11px;font-weight:700;color:#6b7280;"
                "text-transform:uppercase;letter-spacing:.08em;"
                "border-bottom:2px solid #e5e7eb;padding-bottom:5px;margin-bottom:12px'>"
                "Anatomical assessment — TEE measurements</div>",
                unsafe_allow_html=True,
            )
            with st.container(border=True):

                # Anatomy score + TSP side by side
                ac1, ac2 = st.columns(2)

                # Anatomy score card
                anat_bg  = {"Low":"#f0fdf4","Moderate":"#fffbeb","High":"#fef2f2"}[r["anatomy_level"]]
                anat_bdr = {"Low":"#22c55e","Moderate":"#f59e0b","High":"#ef4444"}[r["anatomy_level"]]
                ac1.markdown(
                    f"<div style='background:{anat_bg};border:1.5px solid {anat_bdr};"
                    f"border-radius:8px;padding:14px 16px;height:100%'>"
                    f"<div style='font-size:11px;font-weight:700;color:#6b7280;"
                    f"text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px'>"
                    f"Anatomical complexity score</div>"
                    f"<div style='font-size:40px;font-weight:700;color:{anat_color};"
                    f"line-height:1;margin-bottom:4px'>{r['anatomy_score']}"
                    f"<span style='font-size:18px;font-weight:400;color:#6b7280'> / 100</span></div>"
                    f"<div style='font-size:13px;font-weight:600;color:{anat_color}'>"
                    f"{r['anatomy_level']} anatomical complexity</div>"
                    f"<div style='background:#e5e7eb;border-radius:3px;height:5px;"
                    f"overflow:hidden;margin-top:8px'>"
                    f"<div style='background:{anat_color};width:{r['anatomy_score']}%;height:100%'>"
                    f"</div></div></div>",
                    unsafe_allow_html=True,
                )

                # TSP difficulty card
                tsp_bg  = {"Low":"#f0fdf4","Medium":"#fffbeb","High":"#fef2f2"}[r["tsp_difficulty"]]
                tsp_bdr = {"Low":"#22c55e","Medium":"#f59e0b","High":"#ef4444"}[r["tsp_difficulty"]]
                tsp_pct = {"Low": 22, "Medium": 55, "High": 88}[r["tsp_difficulty"]]
                ac2.markdown(
                    f"<div style='background:{tsp_bg};border:1.5px solid {tsp_bdr};"
                    f"border-radius:8px;padding:14px 16px;height:100%'>"
                    f"<div style='font-size:11px;font-weight:700;color:#6b7280;"
                    f"text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px'>"
                    f"TSP difficulty</div>"
                    f"<div style='font-size:28px;font-weight:700;color:{tsp_color};"
                    f"line-height:1;margin-bottom:4px'>{r['tsp_difficulty']}</div>"
                    f"<div style='font-size:13px;color:#374151'>Predicted: "
                    f"<strong>{r['tsp_pred_text']}</strong></div>"
                    f"<div style='background:#e5e7eb;border-radius:3px;height:5px;"
                    f"overflow:hidden;margin-top:8px'>"
                    f"<div style='background:{tsp_color};width:{tsp_pct}%;height:100%'>"
                    f"</div></div></div>",
                    unsafe_allow_html=True,
                )

                st.markdown("<br>", unsafe_allow_html=True)

                # TSP clinical recommendation
                st.markdown(
                    f"<div style='background:#f8fafc;border-left:4px solid {tsp_bdr};"
                    f"border-radius:0 6px 6px 0;padding:12px 16px'>"
                    f"<div style='font-size:11px;font-weight:700;color:#6b7280;"
                    f"text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px'>"
                    f"TSP preparation guidance</div>"
                    f"<div style='font-size:13px;color:#1c1917;line-height:1.6'>"
                    f"{r['tsp_body']}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                st.markdown("<br>", unsafe_allow_html=True)

                # TEE measurement summary table
                st.markdown(
                    "<div style='font-size:12px;font-weight:600;color:#374151;margin-bottom:8px'>"
                    "Measurement summary</div>",
                    unsafe_allow_html=True,
                )
                rows = [
                    ("Fossa ovalis thickness", f"{r.get('fo_val', fo_val):.1f} mm",
                     "high" if fo_val > 3.5 else ("mod" if fo_val > 2.5 else "low"),
                     "High risk (>3.5 mm)" if fo_val > 3.5 else ("Elevated (2.5–3.5 mm)" if fo_val > 2.5 else "Normal (<2.5 mm)")),
                    ("Septal angle", f"{sa_val}°",
                     "high" if sa_val > 85 else ("mod" if sa_val < 55 else "low"),
                     "Difficult (>85°)" if sa_val > 85 else ("Steep (<55°)" if sa_val < 55 else "Normal (55–85°)")),
                    ("Left atrial diameter", f"{la_val} mm",
                     "high" if la_val > 50 else ("mod" if la_val > 42 else "low"),
                     "Enlarged (>50 mm)" if la_val > 50 else ("Borderline (42–50 mm)" if la_val > 42 else "Normal (<42 mm)")),
                ]
                pill_css = {"low": "pill-low", "mod": "pill-mod", "high": "pill-high"}
                for label_m, value_m, flag_m, interp_m in rows:
                    st.markdown(
                        f"<div class='rf-row'>"
                        f"<span style='min-width:190px;font-size:13px'>{label_m}</span>"
                        f"<span style='font-family:monospace;font-size:13px;font-weight:600;"
                        f"min-width:56px'>{value_m}</span>"
                        f"<span class='rf-pill {pill_css[flag_m]}'>{interp_m}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                # BMI flag inline if applicable
                if r.get("bmi_flag") and r["bmi_flag"] not in ("", "Normal"):
                    bmi_cls = "bmi-obese" if "Obese" in r["bmi_flag"] else "bmi-overweight"
                    st.markdown(
                        f"<div class='bmi-flag {bmi_cls}' style='margin-top:10px'>"
                        f"BMI: <strong>{r['bmi_flag']}</strong> — "
                        f"Prep time estimate adjusted upward. Ensure positioning support and larger-bore access."
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                # Anatomy factor breakdown — collapsed by default
                with st.expander("Score breakdown by factor"):
                    for factor, pts in r["anat_breakdown"].items():
                        if pts == 0:
                            continue
                        bar_w = max(4, round(pts / 30 * 100))
                        st.markdown(
                            f"<div class='rf-row'>"
                            f"<span style='min-width:200px;font-size:13px'>{factor}</span>"
                            f"<div style='flex:1;background:#e5e7eb;border-radius:3px;"
                            f"height:6px;overflow:hidden;margin:0 12px'>"
                            f"<div style='background:#1a56db;width:{bar_w}%;height:100%'></div></div>"
                            f"<span style='font-family:monospace;font-size:12px;"
                            f"font-weight:600;min-width:52px;text-align:right'>+{pts} pts</span>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )



    st.markdown(
        "<div class='box-red' style='font-size:12px;margin-top:16px'>"
        "<b>Disclaimer:</b> Predictions are based on a small single-centre dataset (n=145). "
        "For educational and planning purposes only — not for clinical decision-making."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Calculation history ───────────────────────────────────────────────────
    if st.session_state.calc_history:
        st.divider()
        h1, h2 = st.columns([6, 1])
        h1.markdown("#### Calculation history")
        if h2.button("Clear", key="clear_history"):
            st.session_state.calc_history = []
            st.rerun()
        st.dataframe(pd.DataFrame(st.session_state.calc_history), hide_index=True, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — OR DAY SCHEDULE BUILDER
# ══════════════════════════════════════════════════════════════════════════════
with tab_schedule:
    st.markdown("<div class='page-title'>OR Day Schedule Builder</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>"
        "Build the day's full case list and see a projected timeline before the OR opens. "
        "The optimiser reorders cases so high-complexity procedures run in the morning block "
        "where overruns are least disruptive."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Section 1: Controls ───────────────────────────────────────────────────
    st.markdown("<div class='section-label'>Controls</div>", unsafe_allow_html=True)
    st.divider()
    ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([2, 2, 1.8, 1.2])
    with ctrl1:
        or_start_str = st.time_input("OR start time", value=datetime.strptime("07:30", "%H:%M").time())
        st.caption("The time the first patient enters the lab.")
    with ctrl2:
        turnover_default = int(BMK["turnover_avg"]) if not np.isnan(BMK["turnover_avg"]) else 15
        turnover_min = st.number_input(
            "Turnover time between cases (min)",
            min_value=5, max_value=45, value=turnover_default, step=5,
        )
        st.caption("Room reset time between cases — historical average is 14 min.")
    with ctrl3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Optimize Case Order", type="primary", use_container_width=True,
                     disabled=len(st.session_state.schedule) < 2):
            risk_order = {"High": 0, "Medium": 1, "Low": 2}
            st.session_state.schedule.sort(
                key=lambda c: (risk_order[c["risk"]], -c["duration_est"])
            )
            st.session_state["optimized"] = True
            st.rerun()
        st.caption("Moves high-risk and longest cases to the morning block to reduce afternoon overrun risk.")
    with ctrl4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<span class="red-btn-marker"></span>', unsafe_allow_html=True)
        if st.button("Clear Schedule", use_container_width=True):
            st.session_state.schedule = []
            st.session_state.pop("optimized", None)
            st.rerun()

    if st.session_state.pop("optimized", False):
        st.success("Schedule optimised — complex cases moved to morning block.")

    # ── Section 2: Add a Case (quick entry fallback) ─────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Add a Case</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown(
        "<p style='font-size:12px;color:#6b7280;margin-bottom:8px'>"
        "Add cases here or from the <b>Pre-Case Risk Score</b> tab using 'Add to Day Schedule'. "
        "Both paths use the same full assessment — physician, clinical profile, TEE measurements, and BMI.</p>",
        unsafe_allow_html=True,
    )
    with st.expander("Add a case to today's schedule",
                     expanded=len(st.session_state.schedule) == 0):

        # ── Scheduling ────────────────────────────────────────────────────────
        st.markdown("<div class='section-label'>Scheduling</div>", unsafe_allow_html=True)
        qa1, qa2, qa3, qa4 = st.columns(4)
        add_label  = qa1.text_input("Case label", placeholder="e.g. Pt 004", key="add_lbl")
        add_phys   = qa2.selectbox("Physician", ["Dr. A", "Dr. B", "Dr. C"], key="add_phys")
        add_tod    = qa3.radio("Time of day", ["Morning", "Afternoon"], horizontal=True, key="add_tod")
        add_extra  = qa4.selectbox("Extra procedure?",
                                   ["None — Standard PVI Only", "CTI Ablation",
                                    "BOX Isolation", "SVC Isolation",
                                    "Multiple Extra Procedures"], key="add_extra")

        # ── Clinical profile ──────────────────────────────────────────────────
        st.markdown("<div class='section-label' style='margin-top:12px'>Clinical profile</div>", unsafe_allow_html=True)
        qb1, qb2, qb3, qb4 = st.columns(4)
        add_afib   = qb1.selectbox("AFib type",
                                   ["Paroxysmal", "Persistent", "Long-Standing Persistent"],
                                   key="add_afib")
        add_prior  = qb2.radio("Prior ablation?", ["No", "Yes"], horizontal=True, key="add_prior")
        add_bmi    = qb3.number_input("BMI (optional)", min_value=0.0, max_value=70.0,
                                      value=0.0, step=0.5, key="add_bmi")
        add_age    = qb4.number_input("Age", min_value=18, max_value=99, value=65,
                                      step=1, key="add_age")
        add_bmi_input = add_bmi if add_bmi > 0 else None

        # ── TEE ultrasound measurements ───────────────────────────────────────
        st.markdown("<div class='section-label' style='margin-top:12px'>TEE ultrasound measurements</div>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:11px;color:#6b7280;margin:-4px 0 8px'>"
            "Leave at defaults if imaging not yet available — anatomy complexity will be used instead.</p>",
            unsafe_allow_html=True,
        )
        qc1, qc2, qc3 = st.columns(3)
        add_fo = qc1.slider("Fossa ovalis (mm)", min_value=1.0, max_value=6.0,
                            value=2.5, step=0.1, key="add_fo",
                            help="Normal: <2.5 mm · Elevated: 2.5–3.5 mm · High: >3.5 mm")
        add_sa = qc2.slider("Septal angle (°)", min_value=40, max_value=110,
                            value=70, step=1, key="add_sa",
                            help="Normal: 55–80° · Difficult: >85°")
        add_la = qc3.slider("Left atrial diameter (mm)", min_value=30, max_value=65,
                            value=40, step=1, key="add_la",
                            help="Normal: <40 mm · Borderline: 40–50 mm · Enlarged: >50 mm")

        # Live TEE flags
        pill_css = {"low":"pill-low", "mod":"pill-mod", "high":"pill-high"}
        fo_f = "high" if add_fo > 3.5 else ("mod" if add_fo > 2.5 else "low")
        sa_f = "high" if add_sa > 85  else ("mod" if add_sa < 55  else "low")
        la_f = "high" if add_la > 50  else ("mod" if add_la > 42  else "low")
        fo_t = "High risk" if add_fo > 3.5 else ("Elevated" if add_fo > 2.5 else "Normal")
        sa_t = "Difficult" if add_sa > 85  else ("Steep"    if add_sa < 55  else "Normal")
        la_t = "Enlarged"  if add_la > 50  else ("Borderline" if add_la > 42 else "Normal")
        qc1.markdown(
            f"<div style='font-size:12px;margin-top:4px'>{add_fo:.1f} mm "
            f"<span class='rf-pill {pill_css[fo_f]}'>{fo_t}</span></div>",
            unsafe_allow_html=True
        )
        qc2.markdown(
            f"<div style='font-size:12px;margin-top:4px'>{add_sa}° "
            f"<span class='rf-pill {pill_css[sa_f]}'>{sa_t}</span></div>",
            unsafe_allow_html=True
        )
        qc3.markdown(
            f"<div style='font-size:12px;margin-top:4px'>{add_la} mm "
            f"<span class='rf-pill {pill_css[la_f]}'>{la_t}</span></div>",
            unsafe_allow_html=True
        )

        # Derive anatomy from TEE (same logic as risk tab)
        if add_fo > 3.5 or add_sa > 85:
            add_anatomy = "Complex"
        elif add_fo > 2.5 or add_sa > 75:
            add_anatomy = "Moderate"
        else:
            add_anatomy = "Simple"

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Add to schedule", type="primary", use_container_width=True, key="btn_add_case"):
            r_add = compute_risk(
                add_prior, add_anatomy, add_extra, add_phys, add_tod,
                fo=add_fo, sa=add_sa, la=add_la,
                afib_type=add_afib, bmi=add_bmi_input, age=int(add_age)
            )
            lbl = add_label.strip() if add_label.strip() else f"Case {len(st.session_state.schedule) + 1}"
            st.session_state.schedule.append({
                "label":        lbl,
                "physician":    add_phys,
                "extra_proc":   add_extra,
                "anatomy":      add_anatomy,
                "prior":        add_prior,
                "time_of_day":  add_tod,
                "risk":         r_add["risk"],
                "duration_est": r_add["center"],
                "lo":           r_add["lo"],
                "hi":           r_add["hi"],
                "quick_add":    False,
            })
            st.rerun()

    if not st.session_state.schedule:
        st.markdown(
            "<div style='text-align:center;padding:60px 20px;color:#9ca3af'>"
            "<div style='font-size:32px;margin-bottom:12px'>📋</div>"
            "<div style='font-size:15px'>No cases scheduled yet.</div>"
            "<div style='font-size:13px;margin-top:6px'>"
            "Go to <b>Pre-Case Risk Score</b> and click 'Add to Day Schedule' "
            "after calculating a risk score.</div></div>",
            unsafe_allow_html=True,
        )
    else:
        cases = st.session_state.schedule

        base_dt  = datetime.combine(datetime.today(), or_start_str)
        cursor   = base_dt
        timeline = []
        for c in cases:
            start  = cursor
            end    = start + timedelta(minutes=c["duration_est"])
            cursor = end + timedelta(minutes=turnover_min)
            timeline.append({"start": start, "end": end, "turnover_end": cursor})

        total_or_min = int((timeline[-1]["turnover_end"] - base_dt).total_seconds() // 60)
        est_finish   = timeline[-1]["end"]   # last case end = patient leaves OR
        n_high       = sum(1 for c in cases if c["risk"] == "High")
        n_medium     = sum(1 for c in cases if c["risk"] == "Medium")

        # Dynamic constraint: patient must leave OR by 4:15 PM (PACU needs 45 min, staff leave 5 PM)
        clearance_deadline = datetime.combine(datetime.today(), datetime.strptime("16:15", "%H:%M").time())
        last_case          = cases[-1]
        last_start         = timeline[-1]["start"]
        latest_start       = clearance_deadline - timedelta(minutes=last_case["duration_est"])
        margin_min         = (latest_start - last_start).total_seconds() / 60

        # Est. Finish KPI colour
        finish_delta_min = (est_finish - clearance_deadline).total_seconds() / 60
        if finish_delta_min > 15:
            finish_clr = RED
        elif finish_delta_min > 0:
            finish_clr = ORANGE
        else:
            finish_clr = GREEN

        # ── Section 3: Day Summary ────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Day Summary</div>", unsafe_allow_html=True)
        st.divider()
        st.markdown("<br>", unsafe_allow_html=True)

        k1, k2, k3, k4, k5 = st.columns(5)
        for col, lbl, val, clr in [
            (k1, "Cases Today",       len(cases),                        BLUE),
            (k2, "Total OR Time",     f"{total_or_min} min",             BLUE),
            (k3, "Est. Finish",       est_finish.strftime("%I:%M %p"),   finish_clr),
            (k4, "High-Risk Cases",   n_high,                            RED    if n_high   > 0 else GREEN),
            (k5, "Medium-Risk Cases", n_medium,                          ORANGE if n_medium > 0 else GREEN),
        ]:
            col.markdown(kpi_card(lbl, val, clr), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if margin_min > 30:
            st.markdown(
                "<div class='box-green'>"
                "<b>Schedule is within safe limits.</b> Last case projected to finish by 4:15 PM."
                "</div>",
                unsafe_allow_html=True,
            )
        elif margin_min >= 0:
            st.markdown(
                "<div class='box-yellow'>"
                "<b>Caution:</b> Last case is cutting close. Patient may not clear OR by 4:15 PM "
                "if any delays occur."
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            latest_start_str = latest_start.strftime("%I:%M %p")
            st.markdown(
                f"<div class='box-red'>"
                f"<b>Schedule Overrun Risk:</b> Based on predicted duration, the last patient is "
                f"unlikely to leave OR by 4:15 PM. The latest safe start for this case was "
                f"{latest_start_str}. PACU staff leave at 5:00 PM. Consider removing the last "
                f"case or adjusting the schedule."
                f"</div>",
                unsafe_allow_html=True,
            )

        # ── Section 4: Timeline and Case List ────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Timeline and Case List</div>", unsafe_allow_html=True)
        st.divider()

        # Gantt chart
        color_map     = {"Low": GREEN, "Medium": ORANGE, "High": RED}
        fig_gantt     = go.Figure()
        plotted_risks = set()

        for c, t in zip(cases, timeline):
            t_dur = (t["turnover_end"] - t["end"]).total_seconds() / 60
            fig_gantt.add_trace(go.Bar(
                x=[t_dur], y=[c["label"]], orientation="h",
                base=[(t["end"] - base_dt).total_seconds() / 60],
                marker=dict(color="#e5e7eb", line=dict(color="white", width=1),
                            cornerradius=4),
                showlegend=False, width=0.65,
                hovertemplate=f"Room turnover ({turnover_min} min)<extra></extra>",
            ))
            p_dur = (t["end"] - t["start"]).total_seconds() / 60
            clr   = color_map[c["risk"]]
            show  = c["risk"] not in plotted_risks
            plotted_risks.add(c["risk"])
            fig_gantt.add_trace(go.Bar(
                x=[p_dur], y=[c["label"]], orientation="h",
                base=[(t["start"] - base_dt).total_seconds() / 60],
                marker=dict(color=clr, line=dict(color="white", width=1.5),
                            cornerradius=4),
                name=f"{c['risk']} Risk", showlegend=show,
                text=f"{c['label']} ({c['physician']})",
                textposition="inside", insidetextanchor="middle", width=0.72,
                hovertemplate=(
                    f"<b>{c['label']}</b> | {c['physician']}<br>"
                    f"Est: {c['lo']:.0f}–{c['hi']:.0f} min | Risk: {c['risk']}<br>"
                    f"Extra: {c['extra_proc']}<extra></extra>"
                ),
            ))

        total_span = total_or_min + turnover_min
        tick_vals  = list(range(0, total_span + 30, 30))
        tick_text  = [(base_dt + timedelta(minutes=m)).strftime("%I:%M %p") for m in tick_vals]

        or_start_min = or_start_str.hour * 60 + or_start_str.minute

        # OR Clearance Deadline line at 4:15 PM (orange dashed)
        clearance_x = 16 * 60 + 15 - or_start_min
        if 0 < clearance_x <= total_span + 60:
            fig_gantt.add_shape(
                type="line",
                x0=clearance_x, x1=clearance_x,
                y0=-0.5, y1=len(cases) - 0.5,
                line=dict(color="#f97316", width=2, dash="dash"),
                layer="above",
            )
            fig_gantt.add_annotation(
                x=clearance_x, y=-0.5,
                text="OR Clearance Deadline",
                showarrow=False,
                font=dict(color="#f97316", size=11),
                yanchor="top",
                xanchor="center",
            )

        # End-of-Day vertical line at 5:00 PM (red dashed)
        eod_x = 17 * 60 - or_start_min
        if 0 < eod_x <= total_span + 60:
            fig_gantt.add_shape(
                type="line",
                x0=eod_x, x1=eod_x,
                y0=-0.5, y1=len(cases) - 0.5,
                line=dict(color="#ef4444", width=2, dash="dash"),
                layer="above",
            )
            fig_gantt.add_annotation(
                x=eod_x, y=-0.5,
                text="End of Day",
                showarrow=False,
                font=dict(color="#ef4444", size=11),
                yanchor="top",
                xanchor="center",
            )

        fig_gantt.update_layout(
            barmode="overlay",
            title="Projected OR Timeline",
            xaxis=dict(title="Time of Day", tickvals=tick_vals,
                       ticktext=tick_text, tickangle=0,
                       tickfont=dict(size=12)),
            yaxis=dict(autorange="reversed", title=""),
            height=max(360, len(cases) * 80 + 130),
            plot_bgcolor="#f8fafc", paper_bgcolor="#f8fafc",
            margin=dict(l=10, r=10, t=54, b=60),
            legend=dict(orientation="h", y=-0.25),
        )
        st.plotly_chart(fig_gantt, use_container_width=True,
                        config={"displayModeBar": False})
        st.caption(
            "Each bar represents one case. Colour indicates risk level. "
            "Grey blocks are room turnover time. Red dashed line marks 5:00 PM end of day. "
            "Hover over any bar for details."
        )

        # Case list
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        st.markdown("#### Case List")

        st.markdown('<span class="table-header-marker"></span>', unsafe_allow_html=True)
        hcols = st.columns([2, 1.2, 1.2, 1.5, 1.5, 1.5, 1.2, 1.0])
        for col, hdr in zip(hcols, ["Label", "Physician", "Start", "Extra Proc", "Est Duration", "Risk", "Source", ""]):
            col.markdown(f"**{hdr}**")

        badge_colors = {"Low": GREEN, "Medium": ORANGE, "High": RED}
        for i, (c, t) in enumerate(zip(cases, timeline)):
            row_cls = "row-even-marker" if i % 2 == 0 else "row-odd-marker"
            st.markdown(f'<span class="{row_cls}"></span>', unsafe_allow_html=True)
            rc = st.columns([2, 1.2, 1.2, 1.5, 1.5, 1.5, 1.2, 1.0])
            rc[0].write(c["label"])
            rc[1].write(c["physician"])
            rc[2].write(t["start"].strftime("%I:%M %p"))
            rc[3].write(c["extra_proc"].split(" — ")[0])
            rc[4].write(f"{c['lo']:.0f}–{c['hi']:.0f} min")
            badge_clr = badge_colors[c["risk"]]
            rc[5].markdown(
                f"<span style='background:{badge_clr};color:white;padding:3px 10px;"
                f"border-radius:12px;font-size:12px;font-weight:600'>{c['risk']}</span>",
                unsafe_allow_html=True,
            )
            source_lbl = "Schedule tab" if c.get("quick_add") is not None else "Risk tab"
            source_clr = BLUE
            rc[6].markdown(
                f"<span style='font-size:11px;color:{source_clr};font-weight:500'>{source_lbl}</span>",
                unsafe_allow_html=True,
            )
            rc[7].markdown('<span class="del-btn-marker"></span>', unsafe_allow_html=True)
            if rc[7].button("✕", key=f"del_{i}"):
                st.session_state.schedule.pop(i)
                st.rerun()

        high_cases = [c for c in cases if c["risk"] == "High"]
        if high_cases:
            names = ", ".join(c["label"] for c in high_cases)
            st.markdown(
                f"<div class='box-red' style='margin-top:12px'>"
                f"<b>High-risk cases:</b> {names}. "
                f"Use Optimize to move these to the morning slot."
                f"</div>",
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — POST-CASE DEBRIEF
# ══════════════════════════════════════════════════════════════════════════════
with tab_debrief:
    st.markdown("<div class='page-title'>Post-Case Debrief</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>"
        "After a procedure, enter the actual time for each step. The system benchmarks each step "
        "against that physician's historical averages, shows what percentile each step fell in, "
        "and flags steps that drove a long case with likely root causes."
        "</div>",
        unsafe_allow_html=True,
    )

    col_in, col_out = st.columns([1, 1.1], gap="large")

    with col_in:
        st.markdown("### Case Details")

        db_label     = st.text_input("Case label / patient",
                                     placeholder="e.g. Pt 001 — links to risk score history",
                                     key="db_label",
                                     help="Enter the same label used in the Pre-Case Risk Score tab to link this debrief to the pre-case prediction.")
        db_physician = st.selectbox("Physician", ["Dr. A", "Dr. B", "Dr. C"], key="db_phys")
        db_case_type = st.radio("Case type", ["Standard PVI", "Extra Procedure"],
                                horizontal=True, key="db_type")

        # Pull matching risk prediction from history if label matches
        matched_prediction = None
        if db_label.strip() and st.session_state.calc_history:
            for h in st.session_state.calc_history:
                if h.get("Label", "").strip().lower() == db_label.strip().lower():
                    matched_prediction = h
                    break
        if matched_prediction:
            pred_lo  = matched_prediction.get("Duration", "—").split("–")[0] if "–" in matched_prediction.get("Duration","") else "—"
            pred_hi  = matched_prediction.get("Duration", "—").split("–")[-1].replace(" min","") if "–" in matched_prediction.get("Duration","") else "—"
            pred_risk = matched_prediction.get("Sched. Risk", matched_prediction.get("Risk", "—"))
            st.markdown(
                f"<div style='background:#eff6ff;border-left:4px solid #1a56db;"
                f"border-radius:0 6px 6px 0;padding:10px 14px;margin-bottom:10px'>"
                f"<div style='font-size:11px;font-weight:700;color:#6b7280;"
                f"text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px'>"
                f"Linked pre-case prediction</div>"
                f"<div style='font-size:13px;color:#1c1917'>"
                f"Predicted duration: <b>{pred_lo}–{pred_hi} min</b> · "
                f"Risk: <b>{pred_risk}</b> · "
                f"Physician: <b>{matched_prediction.get('Physician','—')}</b></div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        elif db_label.strip():
            st.markdown(
                "<div style='background:#fffbeb;border-left:4px solid #f59e0b;"
                "border-radius:0 6px 6px 0;padding:8px 14px;margin-bottom:10px;"
                "font-size:12px;color:#374151'>"
                "No matching pre-case calculation found for this label. "
                "Run the risk score first and use the same label to link them.</div>",
                unsafe_allow_html=True,
            )

        phys_step_bmk = BMK["physician_steps"][db_physician]
        phys_n_cases  = BMK["physician"][db_physician]["n"]

        st.markdown(
            f"<p style='font-size:12px;color:{GREY};margin-bottom:10px'>"
            f"Benchmarked against {phys_n_cases} historical {db_physician} standard PVI cases. "
            f"Steps with fewer than 5 physician cases fall back to the global average.</p>",
            unsafe_allow_html=True,
        )
        st.markdown("**Enter actual step durations (minutes):**")

        step_inputs = {}
        for col_s, lbl in zip(STEP_COLS, STEP_LABELS):
            avg = phys_step_bmk[col_s]["mean"]
            step_inputs[col_s] = st.number_input(
                f"{lbl}  ({db_physician} avg {avg:.0f} min)",
                min_value=0.0, max_value=120.0,
                value=float(round(avg)), step=0.5,
                key=f"db_{col_s}",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Delay Flags**")
        st.markdown(
            "<p style='font-size:12px;color:#6b7280;margin-top:-8px;margin-bottom:8px'>"
            "Check any that occurred during this case.</p>",
            unsafe_allow_html=True,
        )

        DELAY_FLAGS = [
            "Equipment wait (supply not staged in advance)",
            "Cable management issue",
            "ACT check pause mid-procedure",
            "Communication repeat or miscommunication",
            "Patient repositioning disruption",
            "Mapping system issue (CARTO)",
            "Sterile field disruption",
            "Other unexpected delay",
        ]
        df_col1, df_col2 = st.columns(2)
        delay_checked = []
        for j, flag in enumerate(DELAY_FLAGS):
            col_target = df_col1 if j % 2 == 0 else df_col2
            if col_target.checkbox(flag, key=f"delay_{j}"):
                delay_checked.append(flag)

        db_notes = st.text_area(
            "Notes on this case (optional)",
            placeholder="e.g. Difficult TSP due to thick septum...", height=80,
        )
        analyze = st.button("Analyze This Case", type="primary", use_container_width=True)

    with col_out:
        st.markdown("### Debrief Report")

        if not analyze:
            st.markdown(
                "<div style='text-align:center;padding:60px 20px;color:#9ca3af'>"
                "<div style='font-size:15px;margin-top:14px'>"
                "Enter the actual step times and click <b>Analyze This Case</b>.</div>"
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            actuals      = [step_inputs[c] for c in STEP_COLS]
            actual_total = sum(actuals)
            phys_avgs    = [phys_step_bmk[c]["mean"]  for c in STEP_COLS]
            phys_p90s    = [phys_step_bmk[c]["p90"]   for c in STEP_COLS]
            phys_vals    = [phys_step_bmk[c]["values"] for c in STEP_COLS]
            phys_avg_total = sum(phys_avgs)
            total_delta    = actual_total - phys_avg_total

            phys_sub = df[
                (df["CASE_TYPE"] == "Standard PVI") &
                (df["PHYSICIAN"] == db_physician)
            ]["PT_IN_OUT"].dropna()
            ref_vals    = phys_sub if len(phys_sub) >= 5 else df[df["CASE_TYPE"] == "Standard PVI"]["PT_IN_OUT"].dropna()
            overall_pct = float((ref_vals < actual_total).mean() * 100)

            if overall_pct <= 33:
                o_cls, o_lbl = "box-green",  "Faster than usual"
            elif overall_pct <= 66:
                o_cls, o_lbl = "box-yellow", "About average"
            else:
                o_cls, o_lbl = "box-red",    "Longer than usual"

            st.markdown(
                f"<div class='{o_cls}'>"
                f"<b>{o_lbl}</b> — Total: <b>{actual_total:.0f} min</b> "
                f"({'+ ' if total_delta >= 0 else ''}{total_delta:.0f} min vs "
                f"{db_physician} avg) | "
                f"Faster than <b>{100 - overall_pct:.0f}%</b> of {db_physician} cases"
                f"</div>",
                unsafe_allow_html=True,
            )

            # Predicted vs actual panel (only shown if label matched a calculation)
            if matched_prediction:
                try:
                    dur_str  = matched_prediction.get("Duration", "")
                    p_lo_val = float(dur_str.split("–")[0]) if "–" in dur_str else None
                    p_hi_val = float(dur_str.split("–")[-1].replace(" min","")) if "–" in dur_str else None
                    p_mid    = (p_lo_val + p_hi_val) / 2 if p_lo_val and p_hi_val else None
                    if p_mid:
                        diff     = actual_total - p_mid
                        in_range = p_lo_val <= actual_total <= p_hi_val if p_lo_val and p_hi_val else False
                        diff_cls = "box-green" if in_range else ("box-yellow" if abs(diff) <= 15 else "box-red")
                        diff_lbl = "Within predicted range" if in_range else ("Close to predicted range" if abs(diff) <= 15 else "Outside predicted range")
                        st.markdown(
                            f"<div class='{diff_cls}'>"
                            f"<b>Model accuracy — {diff_lbl}</b><br>"
                            f"Predicted: {p_lo_val:.0f}–{p_hi_val:.0f} min · "
                            f"Actual: {actual_total:.0f} min · "
                            f"Difference vs midpoint: {'+' if diff >= 0 else ''}{diff:.0f} min"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                except Exception:
                    pass

            st.markdown("<br>", unsafe_allow_html=True)

            # Comparison chart
            bar_colors = []
            for a, avg_v, p90 in zip(actuals, phys_avgs, phys_p90s):
                bar_colors.append(GREEN if a <= avg_v else (ORANGE if a <= p90 else RED))

            fig_db = go.Figure()
            fig_db.add_trace(go.Bar(
                x=STEP_LABELS, y=phys_avgs, name=f"{db_physician} Avg",
                marker_color="#e5e7eb",
                hovertemplate=f"<b>%{{x}}</b><br>{db_physician} Avg: %{{y:.1f}} min<extra></extra>",
            ))
            fig_db.add_trace(go.Bar(
                x=STEP_LABELS, y=actuals, name="This Case",
                marker_color=bar_colors,
                text=[f"{a:.0f}" for a in actuals], textposition="outside",
                hovertemplate="<b>%{x}</b><br>Actual: %{y:.1f} min<extra></extra>",
            ))
            fig_db.update_layout(
                barmode="overlay",
                title=f"Step Duration: This Case vs {db_physician} Historical Average",
                yaxis_title="Minutes", height=300,
                plot_bgcolor="white", paper_bgcolor="white",
                margin=dict(l=10, r=10, t=54, b=20),
                legend=dict(orientation="h", y=-0.22),
            )
            st.plotly_chart(fig_db, use_container_width=True)

            # Per-step table
            table_rows = []
            flagged    = []
            for col_s, lbl, actual, avg, vals, delta in zip(
                STEP_COLS, STEP_LABELS, actuals, phys_avgs, phys_vals,
                [a - b for a, b in zip(actuals, phys_avgs)]
            ):
                pct         = float((vals < actual).mean() * 100)
                is_fallback = phys_step_bmk[col_s].get("fallback", False)
                note        = " *" if is_fallback else ""

                if pct <= 33:   verdict = "Fast"
                elif pct <= 66: verdict = "Average"
                elif pct <= 90: verdict = "Slow"
                else:
                    verdict = "Very Slow"
                    flagged.append((lbl, actual, avg, pct))

                table_rows.append({
                    "Step":                    lbl + note,
                    "Actual":                  f"{actual:.0f} min",
                    f"{db_physician} Avg":     f"{avg:.0f} min",
                    "Delta vs Avg":            f"{'+ ' if delta >= 0 else ''}{delta:.0f} min",
                    "Percentile":              f"{pct:.0f}th",
                    "Verdict":                 verdict,
                })

            st.dataframe(pd.DataFrame(table_rows), hide_index=True, use_container_width=True)

            fallback_cols = [lbl for col_s, lbl in zip(STEP_COLS, STEP_LABELS)
                             if phys_step_bmk[col_s].get("fallback", False)]
            if fallback_cols:
                st.markdown(
                    f"<p style='font-size:11px;color:{GREY}'>* Global average used for: "
                    f"{', '.join(fallback_cols)} — insufficient {db_physician} cases.</p>",
                    unsafe_allow_html=True,
                )

            ROOT_CAUSES = {
                "TSP":            "Likely driven by patient anatomy (thick or calcified septum, or prior ablation scar).",
                "Pre-Map":        "Possible causes: poor signal quality, patient movement, or complex left atrial anatomy.",
                "Ablation":       "More ablation sites or extra catheter repositioning time than usual.",
                "Pt Prep":        "Consider reviewing intubation workflow or room setup checklist.",
                "Vascular Access":"May indicate difficult venous access — flag for pre-procedure ultrasound.",
                "Post Care":      "Check for extended recovery monitoring or documentation delays.",
            }

            if flagged:
                flag_lines = [
                    f"<b>{lbl}</b> {actual:.0f} min (avg {avg:.0f} min, {pct:.0f}th percentile) — "
                    f"{ROOT_CAUSES.get(lbl, 'Review procedure notes.')}"
                    for lbl, actual, avg, pct in flagged
                ]
                st.markdown(
                    "<div class='box-red'><b>Steps above 90th percentile:</b><br>"
                    + "<br>".join(flag_lines) + "</div>",
                    unsafe_allow_html=True,
                )
            else:
                slow_lbls = [r["Step"].rstrip("*").strip() for r in table_rows
                             if float(r["Percentile"].replace("th", "")) > 66]
                if slow_lbls:
                    st.markdown(
                        "<div class='box-yellow'><b>Steps above average but within normal range:</b> "
                        + ", ".join(slow_lbls)
                        + ". No action required — monitor trend over multiple cases.</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<div class='box-green'><b>No outlier steps.</b> "
                        "All steps within normal range for this physician.</div>",
                        unsafe_allow_html=True,
                    )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                "<div style='font-size:12px;font-weight:600;color:#374151;margin-bottom:8px'>"
                "Delay flags recorded this case</div>",
                unsafe_allow_html=True,
            )
            if delay_checked:
                badges = " ".join(
                    f"<span style='background:#fef2f2;color:#dc2626;border:1px solid #fca5a5;"
                    f"padding:4px 12px;border-radius:12px;font-size:12px;font-weight:500;"
                    f"display:inline-block;margin:3px 4px 3px 0'>{flag}</span>"
                    for flag in delay_checked
                )
                st.markdown(badges, unsafe_allow_html=True)

                # Save to running tally in session state
                if "delay_tally" not in st.session_state:
                    st.session_state.delay_tally = {}
                for flag in delay_checked:
                    st.session_state.delay_tally[flag] = st.session_state.delay_tally.get(flag, 0) + 1
            else:
                st.markdown(
                    "<div class='box-green'>No delays reported for this case.</div>",
                    unsafe_allow_html=True,
                )

            # Running delay tally across all debriefs this session
            if st.session_state.get("delay_tally"):
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    "<div style='font-size:12px;font-weight:600;color:#374151;margin-bottom:8px'>"
                    "Delay frequency — all cases this session</div>",
                    unsafe_allow_html=True,
                )
                tally = st.session_state.delay_tally
                max_count = max(tally.values())
                for flag, count in sorted(tally.items(), key=lambda x: -x[1]):
                    bar_w = max(4, round(count / max_count * 100))
                    st.markdown(
                        f"<div style='display:flex;align-items:center;gap:10px;"
                        f"margin-bottom:6px;font-size:12px'>"
                        f"<span style='min-width:280px;color:#374151'>{flag}</span>"
                        f"<div style='flex:1;background:#e5e7eb;border-radius:3px;"
                        f"height:8px;overflow:hidden'>"
                        f"<div style='background:#ef4444;width:{bar_w}%;height:100%'></div></div>"
                        f"<span style='min-width:24px;text-align:right;font-family:monospace;"
                        f"font-size:12px;font-weight:600;color:#374151'>{count}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                if st.button("Reset delay tally", key="reset_tally"):
                    st.session_state.delay_tally = {}
                    st.rerun()

            if db_notes.strip():
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='box-blue'><b>Case Notes:</b> {db_notes}</div>",
                    unsafe_allow_html=True,
                )


