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
def compute_risk(prior_ablation, anatomy, extra_proc, physician, time_of_day) -> dict:
    md = MODEL_DATA

    tsp_base = {"Simple": BMK["tsp_p25"], "Moderate": BMK["tsp_med"], "Complex": BMK["tsp_p75"]}[anatomy]
    tsp_est  = tsp_base + (8.0 if prior_ablation == "Yes" else 0.0)
    tsp_est  = min(tsp_est, BMK["steps"]["TSP"]["max"])

    phys_fm  = BMK["physician_feature_means"][physician]
    n_abl    = phys_fm["N_ABL"]
    pt_prep  = phys_fm["PT_PREP"]

    extra_flag = 0.0 if extra_proc == "None — Standard PVI Only" else 1.0
    phys_enc   = float(PHYS_MAP[physician])

    x_vec     = np.array([1.0, n_abl, tsp_est, phys_enc, pt_prep, extra_flag])
    predicted = float(np.dot(md["coeffs"], x_vec))
    predicted = max(40.0, predicted)

    lo = max(40.0, predicted - md["residual_std"])
    hi = predicted + md["residual_std"]

    risk = "Low" if predicted < BMK["p50"] else ("Medium" if predicted < BMK["p75"] else "High")

    score   = 0
    drivers = []

    if prior_ablation == "Yes":
        score += 1
        drivers.append(f"Prior ablation — estimated TSP raised to {tsp_est:.0f} min (scar tissue effect).")

    if anatomy == "Moderate":
        score += 1
        drivers.append(f"Moderate anatomy — TSP estimated at {tsp_est:.0f} min (historical median).")
    elif anatomy == "Complex":
        score += 2
        drivers.append(f"Complex anatomy — TSP estimated at {tsp_est:.0f} min (historical 75th percentile).")

    extra_scores = {"CTI Ablation": 1, "BOX Isolation": 2, "SVC Isolation": 2, "Multiple Extra Procedures": 3}
    if extra_proc in extra_scores:
        score += extra_scores[extra_proc]
        drivers.append(f"{extra_proc} flagged — increases predicted time via extra procedure coefficient.")

    if physician == "Dr. C":
        drivers.append(f"Dr. C has only {BMK['physician']['Dr. C']['n']} cases — prediction uncertainty is higher.")

    if time_of_day == "Afternoon":
        score += 1
        drivers.append("Afternoon slot — elevated overrun risk regardless of predicted duration.")

    tsp_s = {"Simple": 0, "Moderate": 1, "Complex": 2}[anatomy] + (1 if prior_ablation == "Yes" else 0)
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
        "score": score, "risk": risk, "lo": lo, "hi": hi, "center": predicted,
        "tsp_label": tsp_label, "tsp_est": tsp_est, "sched_rec": sched_rec,
        "drivers": drivers, "r2": md["r2"],
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
        "Enter patient and procedure details before a case begins. Duration is predicted using "
        "a linear regression model trained on the EP Lab dataset. Risk level is determined by "
        "where the predicted duration falls in the historical distribution of case times."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<hr style='border:none;border-top:1.5px solid #0d1b2a;margin:0 0 22px 0'>",
        unsafe_allow_html=True,
    )

    col_form, col_result = st.columns([1, 1.2], gap="large")

    with col_form:
        st.markdown("<div class='step-label'>Step 1 — Enter Case Details</div>", unsafe_allow_html=True)
        with st.container(border=True):
            prior_ablation = st.radio("Prior ablation?", ["No", "Yes"], horizontal=True, key="risk_prior")
            anatomy        = st.select_slider(
                "Heart anatomy complexity (from imaging)",
                options=["Simple", "Moderate", "Complex"], value="Moderate", key="risk_anatomy",
            )
            extra_proc = st.selectbox(
                "Extra procedure planned?",
                ["None — Standard PVI Only", "CTI Ablation", "BOX Isolation",
                 "SVC Isolation", "Multiple Extra Procedures"],
                key="risk_extra",
            )
            physician   = st.selectbox("Performing physician", ["Dr. A", "Dr. B", "Dr. C"], key="risk_phys")
            time_of_day = st.radio("Time of day", ["Morning", "Afternoon"], horizontal=True, key="risk_tod")
            patient_label = st.text_input("Patient or case label (optional)", placeholder="e.g. Pt 001", key="risk_label")

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

    # Compute only on button click; persist result in session state
    if calc_clicked:
        result = compute_risk(prior_ablation, anatomy, extra_proc, physician, time_of_day)
        st.session_state.risk_result = result
        st.session_state.risk_inputs = {
            "physician": physician, "anatomy": anatomy, "extra_proc": extra_proc,
            "prior": prior_ablation, "time_of_day": time_of_day,
        }
        lbl = patient_label.strip() or f"Calculation {len(st.session_state.calc_history) + 1}"
        st.session_state.calc_history.append({
            "Label":      lbl,
            "Physician":  physician,
            "Anatomy":    anatomy,
            "Extra Proc": extra_proc.replace("None — Standard PVI Only", "Standard PVI"),
            "Prior Abl.": prior_ablation,
            "Risk":       result["risk"],
            "Duration":   f"{result['lo']:.0f}–{result['hi']:.0f} min",
        })

    r = st.session_state.risk_result

    with col_result:
        st.markdown("<div class='step-label'>Step 2 — Review Assessment</div>", unsafe_allow_html=True)
        with st.container(border=True):
            if r is None:
                st.markdown(
                    "<div style='display:flex;align-items:center;justify-content:center;"
                    "min-height:420px;text-align:center;color:#9ca3af;'>"
                    "<div style='font-size:15px;line-height:1.7'>"
                    "Complete the form and click <b>Calculate Risk</b><br>to see the prediction."
                    "</div></div>",
                    unsafe_allow_html=True,
                )
            else:
                # ── Risk badge ──
                risk_color = RISK_COLORS[r["risk"]]
                st.markdown(
                    f"<div class='risk-{r['risk'].lower()}'>"
                    f"<div style='font-size:26px;font-weight:700;color:{risk_color}'>{r['risk']} Risk</div>"
                    f"<div style='font-size:13px;color:#374151;margin-top:4px'>"
                    f"Predicted duration is "
                    f"{'below the historical median' if r['risk'] == 'Low' else 'between the 50th and 75th percentile' if r['risk'] == 'Medium' else 'above the 75th percentile'}"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )

                # ── Duration gauge ──
                st.markdown("<div class='result-spacer'></div>", unsafe_allow_html=True)
                st.markdown("**Predicted Duration vs Historical Distribution**")
                st.plotly_chart(
                    duration_gauge(r["center"], r["lo"], r["hi"]),
                    use_container_width=True, config={"displayModeBar": False},
                )

                # ── KPI cards ──
                st.markdown("<div class='result-spacer'></div>", unsafe_allow_html=True)
                m1, m2 = st.columns(2)
                m1.markdown(kpi_card("Predicted Duration", f"{r['lo']:.0f}–{r['hi']:.0f} min", BLUE),
                            unsafe_allow_html=True)
                m2.markdown(kpi_card("TSP Difficulty", r["tsp_label"], BLUE),
                            unsafe_allow_html=True)

                # ── Scheduling recommendation ──
                st.markdown("<div class='result-spacer'></div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='box-yellow'><b>Scheduling recommendation:</b> {r['sched_rec']}</div>",
                    unsafe_allow_html=True,
                )

                # ── Risk drivers ──
                st.markdown("<div class='result-spacer'></div>", unsafe_allow_html=True)
                st.markdown("**Risk Drivers**")
                if r["drivers"]:
                    for d in r["drivers"]:
                        st.markdown(f"- {d}")
                else:
                    st.markdown(
                        "<div class='box-green'>No significant risk factors identified.</div>",
                        unsafe_allow_html=True,
                    )

                # ── Model expander ──
                st.markdown("<div class='result-spacer'></div>", unsafe_allow_html=True)
                with st.expander("How this prediction works"):
                    md   = MODEL_DATA
                    coef = md["coefs"]
                    intc = md["intercept"]
                    r2_val = md["r2"]
                    st.markdown(
                        f"<p style='font-size:12px;color:{GREY};margin:0 0 10px'>"
                        f"R\u00b2 = {r2_val:.3f} \u2014 the model explains {r2_val*100:.0f}% of case time variance. "
                        f"Remaining variance is driven by unobserved factors like patient anatomy and team coordination."
                        f" | Trained on {md['n_train']} cases.</p>",
                        unsafe_allow_html=True,
                    )
                    signs = [("+" if c >= 0 else "\u2212") for c in coef]
                    terms = "  ".join(
                        f"{s} {abs(c):.2f}\u00d7({n})"
                        for s, c, n in zip(signs, coef, md["feat_display"])
                    )
                    eq = f"Predicted PT_IN_OUT = {intc:.1f}  {terms}"
                    st.markdown(f"<div class='eq-box'>{eq}</div>", unsafe_allow_html=True)
                    st.markdown("**What each coefficient means:**")
                    for exp in [
                        f"Ablation Sites ({coef[0]:+.2f} min/site): each additional site adds {abs(coef[0]):.2f} min.",
                        f"TSP Duration ({coef[1]:+.2f} min/min): each extra minute in TSP flows through to total time — the largest source of variability.",
                        f"Physician ({coef[2]:+.2f} min/unit): encodes Dr. A=0, Dr. B=1, Dr. C=2; reflects case mix differences, not performance.",
                        f"Patient Prep ({coef[3]:+.2f} min/min): extra prep time cascades into overall duration.",
                        f"Extra Procedure ({coef[4]:+.2f} min): having any extra procedure adds an average of {abs(coef[4]):.0f} min.",
                    ]:
                        st.markdown(f"- {exp}")
                    st.markdown(
                        f"<div class='box-orange' style='font-size:12px'>"
                        f"This model is trained on {md['n_train']} cases from a single EP Lab centre. "
                        f"For planning guidance only — not for clinical decision-making."
                        f"</div>",
                        unsafe_allow_html=True,
                    )

    # Handle Add to Day Schedule — use the inputs that produced the stored result
    if add_sched and r is not None:
        # Fall back to current widget values if risk_inputs was not stored
        inp = st.session_state.risk_inputs or {
            "physician": physician, "anatomy": anatomy, "extra_proc": extra_proc,
            "prior": prior_ablation, "time_of_day": time_of_day,
        }
        label = patient_label.strip() if patient_label.strip() else f"Case {len(st.session_state.schedule) + 1}"
        st.session_state.schedule.append({
            "label":        label,
            "physician":    inp["physician"],
            "extra_proc":   inp["extra_proc"],
            "anatomy":      inp["anatomy"],
            "prior":        inp["prior"],
            "time_of_day":  inp["time_of_day"],
            "risk":         r["risk"],
            "duration_est": r["center"],
            "lo":           r["lo"],
            "hi":           r["hi"],
        })
        st.toast(f"'{label}' added — switch to OR Day Schedule Builder to view.")
        st.rerun()

    # ── Calculation History ──
    if st.session_state.calc_history:
        st.divider()
        h_col1, h_col2 = st.columns([6, 1])
        h_col1.markdown("#### Calculation History")
        if h_col2.button("Clear", key="clear_history"):
            st.session_state.calc_history = []
            st.rerun()
        hist_df = pd.DataFrame(st.session_state.calc_history)
        st.dataframe(hist_df, hide_index=True, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div class='box-red' style='font-size:12px'>"
        "<b>Disclaimer:</b> Predictions are based on a small single-centre dataset. "
        "For educational and planning purposes only — not for clinical decision-making."
        "</div>",
        unsafe_allow_html=True,
    )


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

    # ── Section 2: Add a Case ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Add a Case</div>", unsafe_allow_html=True)
    st.divider()
    with st.expander("Add a Case to Today's Schedule",
                     expanded=len(st.session_state.schedule) == 0):
        fa1, fa2, fa3 = st.columns(3)
        with fa1:
            add_label   = st.text_input("Patient or case label", placeholder="e.g. Pt 004", key="add_lbl")
            add_phys    = st.selectbox("Physician", ["Dr. A", "Dr. B", "Dr. C"], key="add_phys")
        with fa2:
            add_prior   = st.radio("Prior ablation?", ["No", "Yes"], horizontal=True, key="add_prior")
            add_anatomy = st.select_slider("Anatomy complexity",
                                           options=["Simple", "Moderate", "Complex"],
                                           value="Moderate", key="add_anat")
        with fa3:
            add_extra   = st.selectbox("Extra procedure?",
                                       ["None — Standard PVI Only", "CTI Ablation",
                                        "BOX Isolation", "SVC Isolation",
                                        "Multiple Extra Procedures"], key="add_extra")
            add_tod     = st.radio("Time of day", ["Morning", "Afternoon"],
                                   horizontal=True, key="add_tod")

        if st.button("Add Case", type="primary"):
            r_add = compute_risk(add_prior, add_anatomy, add_extra, add_phys, add_tod)
            lbl   = add_label.strip() if add_label.strip() else f"Case {len(st.session_state.schedule) + 1}"
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
            })
            st.rerun()

    if not st.session_state.schedule:
        st.markdown(
            "<div style='text-align:center;padding:60px 20px;color:#9ca3af'>"
            "<div style='font-size:15px;margin-top:14px'>"
            "No cases scheduled yet. Add cases above or send them from the "
            "Pre-Case Risk Score tab.</div></div>",
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
        hcols = st.columns([2, 1.5, 1.5, 2, 1.5, 1.5, 1.1])
        for col, hdr in zip(hcols, ["Label", "Physician", "Anatomy", "Extra Proc", "Est Duration", "Risk", ""]):
            col.markdown(f"**{hdr}**")

        badge_colors = {"Low": GREEN, "Medium": ORANGE, "High": RED}
        for i, c in enumerate(cases):
            row_cls = "row-even-marker" if i % 2 == 0 else "row-odd-marker"
            st.markdown(f'<span class="{row_cls}"></span>', unsafe_allow_html=True)
            rc = st.columns([2, 1.5, 1.5, 2, 1.5, 1.5, 1.1])
            rc[0].write(c["label"])
            rc[1].write(c["physician"])
            rc[2].write(c["anatomy"])
            rc[3].write(c["extra_proc"].split(" — ")[0])
            rc[4].write(f"{c['lo']:.0f}–{c['hi']:.0f} min")
            badge_clr = badge_colors[c["risk"]]
            rc[5].markdown(
                f"<span style='background:{badge_clr};color:white;padding:3px 10px;"
                f"border-radius:12px;font-size:12px;font-weight:600'>{c['risk']}</span>",
                unsafe_allow_html=True,
            )
            rc[6].markdown('<span class="del-btn-marker"></span>', unsafe_allow_html=True)
            if rc[6].button("Remove", key=f"del_{i}"):
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
        st.markdown("### Actual Case Times")

        db_physician = st.selectbox("Physician", ["Dr. A", "Dr. B", "Dr. C"], key="db_phys")
        db_case_type = st.radio("Case type", ["Standard PVI", "Extra Procedure"],
                                horizontal=True, key="db_type")

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
            st.markdown("**Flagged Delays**")
            if delay_checked:
                badges = " ".join(
                    f"<span style='background:#ef4444;color:white;padding:3px 10px;"
                    f"border-radius:12px;font-size:12px;font-weight:500;"
                    f"display:inline-block;margin:3px 4px 3px 0'>{flag}</span>"
                    for flag in delay_checked
                )
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.markdown(
                    "<div class='box-green'>No delays reported for this case.</div>",
                    unsafe_allow_html=True,
                )

            if db_notes.strip():
                st.markdown(
                    f"<div class='box-blue'><b>Case Notes:</b> {db_notes}</div>",
                    unsafe_allow_html=True,
                )
