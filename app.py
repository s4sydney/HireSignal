import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page setup ───────────────────────────────────────────────────────────
st.set_page_config(page_title="HireSignal", page_icon="📊", layout="wide")

st.title("📊 HireSignal")
st.subheader("Decoding What UK Graduate Data Analyst Roles Really Demand")

st.markdown(
    "This project analyses **287 UK graduate Data Analyst job postings** "
    "and **42 real interview experience reviews** to uncover a 'visibility "
    "gap' — the difference between what candidates can see in a job posting "
    "and what is actually tested in the interview."
)

st.divider()

# ── Section 1: Skills tested in interviews ─────────────────────────────────
st.header("1. What Skills Are Actually Tested in Interviews?")

skills_df = pd.DataFrame({
    "Skill": ["SQL", "Python", "Excel", "Communication",
              "Data Visualisation", "Power BI", "VBA", "Statistics"],
    "Percentage": [47.6, 16.7, 14.3, 11.9, 9.5, 7.1, 2.4, 2.4]
})

fig1 = px.bar(
    skills_df.sort_values("Percentage"),
    x="Percentage", y="Skill", orientation="h",
    text="Percentage",
    labels={"Percentage": "% of interview reviews mentioning skill"},
    color_discrete_sequence=["#4C72B0"]
)
fig1.update_traces(texttemplate="%{text}%", textposition="outside")
fig1.update_layout(yaxis_title="", xaxis_range=[0, 55])

st.plotly_chart(fig1, use_container_width=True)
st.caption(
    "Based on 42 manually-collected Glassdoor interview reviews for UK "
    "Data Analyst roles. SQL appears in nearly half of all reviewed "
    "interview processes — by far the most commonly tested skill."
)

st.divider()

# ── Section 2: The Visibility Gap (interactive) ─────────────────────────────
st.header("2. The Visibility Gap")

st.markdown(
    "Job posting previews are limited to ~500 characters by the Adzuna API "
    "and are usually cut off **before** the skills section. The chart below "
    "compares how visible a skill is in the job posting preview versus how "
    "often it's actually tested in interviews."
)

gap_df = pd.DataFrame({
    "Skill": ["SQL", "Python", "Excel"],
    "Visible in job posting preview": [4.9, 1.0, 5.9],
    "Tested in interview": [47.6, 16.7, 14.3]
})

selected_skill = st.selectbox("Choose a skill to explore:", gap_df["Skill"])

row = gap_df[gap_df["Skill"] == selected_skill].iloc[0]
gap_value = row["Tested in interview"] - row["Visible in job posting preview"]

col1, col2 = st.columns([2, 1])

with col1:
    fig2 = go.Figure(data=[
        go.Bar(
            x=["Visible in job posting preview", "Tested in interview"],
            y=[row["Visible in job posting preview"], row["Tested in interview"]],
            marker_color=["#A8C5E2", "#C44E52"],
            text=[f"{row['Visible in job posting preview']}%",
                  f"{row['Tested in interview']}%"],
            textposition="outside"
        )
    ])
    fig2.update_layout(
        title=f"{selected_skill}: Preview vs Interview Reality",
        yaxis_title="Percentage (%)",
        yaxis_range=[0, 55],
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.metric(
        label=f"The {selected_skill} Gap",
        value=f"{gap_value:.1f} pts",
        help="Difference between % tested in interviews and % visible in job posting previews"
    )
    st.markdown(
        f"**{selected_skill}** appears in job posting previews "
        f"**{row['Visible in job posting preview']}%** of the time, but is "
        f"tested in **{row['Tested in interview']}%** of interviews."
    )
    if selected_skill == "SQL":
        st.markdown(
            "This is the project's central finding — candidates have almost "
            "no way to know SQL will be central to their interview just by "
            "reading the job ad."
        )

st.divider()

# ── Section 3: Salary ranges ─────────────────────────────────────────────────
st.header("3. Entry-Level Salary Ranges (UK)")

st.markdown(
    "For entry-level UK Data Analyst roles (graduate/junior/trainee, n=23), "
    "salary **minimums** cluster tightly between £28,000-£33,000. Salary "
    "**maximums** vary much more widely, from £30,000 up to £78,000."
)

try:
    st.image("outputs/chart2_salary_range.png",
             caption="Entry-Level Data Analyst Salary Range, UK (n=23)")
except Exception:
    st.info("Chart image not found — make sure outputs/chart2_salary_range.png "
            "is present in the repo.")

st.divider()

# ── Section 4: Sector breakdown ──────────────────────────────────────────────
st.header("4. Who Was Interviewed? Sector Breakdown")

sector_df = pd.DataFrame({
    "Sector": ["Banking", "Retail", "Finance/Tech", "Tech", "Public Sector",
               "Fintech", "Insurance", "Media", "Tech/Social Impact",
               "Healthcare", "Utilities", "Finance"],
    "Percentage": [26, 14, 12, 10, 10, 7, 7, 5, 2, 2, 2, 2]
})

fig4 = px.bar(
    sector_df.sort_values("Percentage"),
    x="Percentage", y="Sector", orientation="h",
    color_discrete_sequence=["#55A868"]
)
fig4.update_layout(yaxis_title="", xaxis_title="% of interview reviews (n=42)")

st.plotly_chart(fig4, use_container_width=True)
st.caption(
    "27 companies across 11 sectors. Banking is the most represented "
    "sector (26%), consistent with its prominence in UK graduate hiring."
)

st.divider()

# ── About / Methodology ──────────────────────────────────────────────────────
st.header("About This Project")

st.markdown("""
**Data Sources**
- 287 UK graduate Data Analyst job postings, collected via the Adzuna API
- 42 interview experience reviews, manually collected from Glassdoor (27 companies, 11 sectors)

**Key Limitation**
Job posting descriptions are truncated to ~500 characters by the Adzuna API,
consistently cutting off before the skills/requirements section. This is
why job postings show very low skill percentages — it reflects what's
*visible in the preview*, not what's actually required.

**Full project**: methodology, complete findings, limitations, and future
work are documented in the
[HireSignal GitHub repository](https://github.com/s4sydney/HireSignal).
""")

st.caption("Built by Sydney Ndabai) · MSc Data Analytics")
