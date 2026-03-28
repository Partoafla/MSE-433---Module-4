# EP Lab — Smart Case Planning & Workflow Tracking System

A Streamlit web application built for MSE 433 (Module 4) at the University of Waterloo. This tool supports clinical workflow planning and post-case analysis for Electrophysiology (EP) Lab teams performing Atrial Fibrillation (AFib) ablation procedures using Pulse-Field Ablation (PFA).

---

## What This System Does

EP Labs face significant scheduling pressure — cases vary in complexity, physician performance varies, and late finishes create downstream problems for PACU staffing and patient safety. This dashboard helps OR coordinators and EP teams:

- **Predict case duration and risk before the day starts** using a regression model trained on historical case data
- **Build and visualize the full OR day schedule** with a projected timeline and constraint-aware warnings
- **Debrief after each case** by benchmarking actual step times against physician-specific historical averages

---

## Tabs

### Tab 1 — Pre-Case Risk Score

The user inputs patient and procedure details for an upcoming case. The system predicts how long the case will take and assigns a risk level (Low / Medium / High).

**Inputs:**
- Physician (Dr. A, Dr. B, Dr. C)
- Anatomy complexity (Simple / Moderate / Complex)
- Extra procedure (None, CTI, BOX lesion, SVC isolation, etc.)
- Prior ablation history (Yes / No)
- Time of day (Morning / Afternoon)
- Patient or case label

**How the prediction works:**

The model uses Ordinary Least Squares (OLS) regression fit on historical EP Lab case data from `MSE433_M4_Data.xlsx`. The features are:

- Physician identity (one-hot encoded)
- TSP difficulty score — derived from anatomy complexity (0/1/2) plus prior ablation (+1), mapped to Low / Moderate / High
- Extra procedure flag (binary: 0 or 1)
- Time of day (binary: 0 = morning, 1 = afternoon)

The regression is fit using `numpy.linalg.lstsq` — no external ML libraries required.

**Risk thresholds** are set at the 50th and 75th percentile of historical case durations:
- Below p50 → Low
- p50 to p75 → Medium
- Above p75 → High

**Output:**
- Risk badge (colour-coded)
- Predicted duration gauge (min / center / max)
- KPI cards: predicted duration, TSP difficulty, complexity category, percentile rank
- Scheduling recommendation (suggested time slot)
- Risk driver summary (which factors most increased predicted time)
- Calculation history table (tracks every run in the current session)

Clicking **Add to Day Schedule** sends the case directly to Tab 2.

---

### Tab 2 — OR Day Schedule Builder

Lets the coordinator build the full case list for the day and see a projected timeline before the OR opens.

**Controls:**
- OR start time (default 07:30)
- Turnover time between cases (default: historical average from data)
- **Optimize Case Order** — sorts cases so High-risk and longest cases run in the morning block, reducing afternoon overrun risk
- **Clear Schedule** — resets the full list

**How the timeline is built:**

Cases are laid out sequentially from OR start time. Each case uses its predicted duration (`center` from the regression). Turnover time is added between each case. The projected end time for each case is calculated exactly.

**PACU constraint (hard clinical rule):**

The last patient must leave the OR by **4:15 PM** because PACU requires 45 minutes of post-procedure care and PACU staff leave at 5:00 PM.

The latest allowable start time for the last case is calculated dynamically:

```
Latest Start = 4:15 PM − predicted duration of last case
```

Three status messages reflect the constraint:
- **Green** — last case finishes before 4:15 PM with >30 min buffer
- **Orange** — last case is within 30 minutes of the deadline (cutting close)
- **Red** — last case is projected to start after the latest safe start time (overrun risk)

**KPI cards:** Cases Today, Total OR Time, Est. Finish (colour reflects clearance status), High-Risk Cases, Medium-Risk Cases

**Gantt Chart:**
- Horizontal bar chart showing each case with risk-coloured bars
- Grey blocks show room turnover time
- Orange dashed vertical line at **4:15 PM** — OR Clearance Deadline
- Red dashed vertical line at **5:00 PM** — End of Day
- Hover tooltips show case label, physician, estimated duration, and risk level
- Plotly toolbar hidden for a cleaner interface

**Case List:**
- Navy header row
- Coloured risk badges per row
- Remove button to delete individual cases

---

### Tab 3 — Post-Case Debrief

After a procedure ends, the team enters the actual time for each step. The system benchmarks each step against that physician's historical performance and identifies what drove a long case.

**Steps tracked:** Patient Prep, Vascular Access, TSP, Pre-Map, Ablation Duration, Post Care

**How benchmarking works:**

For each step, the system compares the actual time entered against the physician's historical distribution for that step (mean, p90, all recorded values). If fewer than 5 physician-specific cases exist for a step, it falls back to the global average.

Verdicts per step:
- **Fast** — below 33rd percentile
- **Average** — 33rd to 66th percentile
- **Slow** — 66th to 90th percentile
- **Very Slow** — above 90th percentile (flagged with likely root cause)

Root cause suggestions are mapped per step (e.g. slow TSP → thick septum or prior ablation scar).

**Delay Flags:**

The user can check any delays that occurred during the case:
- Equipment wait
- Cable management issue
- ACT check pause mid-procedure
- Communication repeat or miscommunication
- Patient repositioning disruption
- Mapping system issue (CARTO)
- Sterile field disruption
- Other unexpected delay

Checked flags appear as red badges in the Debrief Report. If none are checked, a green confirmation is shown.

**Output:**
- Overall case verdict (faster than usual / about average / longer than usual)
- Step-by-step comparison bar chart vs physician average
- Per-step table with delta, percentile, and verdict
- Flagged outlier steps with root cause suggestions
- Flagged delay badges
- Free-text case notes

---

## Data

The app loads from `MSE433_M4_Data.xlsx`. The file must be present in the same directory as `app.py`.

Key columns used:

| Column | Description |
|---|---|
| `PHYSICIAN` | Treating physician |
| `CASE_TYPE` | Standard PVI or Extra Procedure |
| `PT_IN_OUT` | Total patient in-to-out time (minutes) |
| `TSP` | Transseptal puncture duration |
| `PRE_MAP`, `ABL_DURATION`, `POST_CARE`, etc. | Individual step durations |
| `AVG_TURNOVER` | Room turnover time between cases |
| `NOTE` | Free-text notes (used to detect extra procedure types) |

---

## How to Run

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Run the app**

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## Requirements

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
openpyxl>=3.1.0
```

No scikit-learn, scipy, or other ML libraries are required. The regression is implemented directly with NumPy.

---

## Project Structure

```
.
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── MSE433_M4_Data.xlsx           # Historical EP Lab case data
├── MSE433_M4_Definitions.docx    # Data dictionary and column definitions
├── .streamlit/
│   └── config.toml               # Forces light mode theme
└── chart*.png                    # Static analysis charts (exploratory)
```

---

## Disclaimer

This tool is built for educational and planning purposes as part of a university course project. Predictions are based on a small single-centre dataset. This system is **not** validated for clinical decision-making and should not be used as a substitute for professional clinical judgment.
