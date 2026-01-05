import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="My Data Story",
    page_icon="📊",
    layout="wide",
)

# ---------- SIDEBAR ----------
st.sidebar.title("Controls")
st.sidebar.write("Adjust the settings to explore the data.")

points = st.sidebar.slider("Number of points", 50, 500, 200)
noise_level = st.sidebar.slider("Noise level", 0.0, 1.0, 0.3)

# ---------- DATA ----------
np.random.seed(0)
x = np.linspace(0, 10, points)
y = np.sin(x) + noise_level * np.random.randn(points)

df = pd.DataFrame({"x": x, "y": y})

# ---------- HERO SECTION ----------
st.markdown(
    """
    # 📊 My Interactive Data Story  

    This page shows an example of an **aesthetic, single-page** Streamlit app that combines:
    - Clean layout  
    - Interactive visuals  
    - Explanatory text
    """,
)

st.markdown("---")

# ---------- METRICS ROW ----------
col1, col2, col3 = st.columns(3)

col1.metric("Data points", f"{points}")
col2.metric("Noise level", f"{noise_level:.2f}")
col3.metric("Y mean", f"{df['y'].mean():.2f}")

st.markdown("")

# ---------- MAIN SECTION: VISUAL + TEXT ----------
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Trend over time")

    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("x", title="X axis"),
            y=alt.Y("y", title="Y value"),
            tooltip=["x", "y"],
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

with right_col:
    st.subheader("What are we looking at?")
    st.write(
        """
        This chart shows a **noisy sine wave**.  
        Use the controls in the sidebar to:
        - Increase the number of points
        - Adjust how noisy the line is  

        As you move the sliders:
        - The line becomes smoother or more jagged  
        - Summary metrics above update automatically  
        """
    )

st.markdown("---")

# ---------- SECOND VISUAL / SECTION ----------
st.subheader("Distribution of values")

import altair as alt
import pandas as pd
import numpy as np

# Clean lung_cancer labels
df_clean = df.copy()
df_clean['lung_cancer'] = df_clean['lung_cancer'].map({
    1: "Positive",
    0: "Negative",
    "yes": "Positive",
    "no": "Negative",
    "Yes": "Positive",
    "No": "Negative"
})

df_clean = df_clean.dropna(subset=['lung_cancer', 'pack_years'])

# ----------------------------
# Bin pack_years for a cleaner baseline visualization
# ----------------------------
bins = [0, 10, 20, 40, df_clean['pack_years'].max() + 1]
labels = ["0–10", "10–20", "20–40", "40+"]

df_clean['pack_bin'] = pd.cut(df_clean['pack_years'], bins=bins, labels=labels, include_lowest=True)

# ----------------------------
# Stacked relative-frequency bar chart
# ----------------------------
baseline_packyears = (
    alt.Chart(df_clean)
    .transform_aggregate(
        count='count()',
        groupby=['pack_bin', 'lung_cancer']
    )
    .transform_joinaggregate(
        total='sum(count)',
        groupby=['pack_bin']
    )
    .transform_calculate(
        proportion="datum.count / datum.total"
    )
    .mark_bar()
    .encode(
        x=alt.X('pack_bin:N', title="Pack Year Category"),
        y=alt.Y('proportion:Q',
                title="Relative Frequency",
                stack="normalize",
                axis=alt.Axis(format="%")),
        color=alt.Color(
            'lung_cancer:N',
            scale=alt.Scale(
                domain=["Positive", "Negative"],
                range=["firebrick", "steelblue"]
            ),
            title="Lung Cancer Status"
        ),
        tooltip=[
            alt.Tooltip('pack_bin:N', title='Pack Years'),
            alt.Tooltip('lung_cancer:N', title='Status'),
            alt.Tooltip('proportion:Q', title='Relative Frequency', format='.1%'),
            alt.Tooltip('count:Q', title='Raw Count')
        ]
    )
    .properties(
        width=700,
        height=400,
        title="Baseline: Lung Cancer Relative Frequency Across Pack Year Categories"
    )
)

baseline_packyears


st.altair_chart(hist, use_container_width=True)

st.markdown(
    """
    This histogram shows how the **values of _y_** are distributed.  
    With low noise, the values cluster tightly around the sine curve.  
    With higher noise, the distribution spreads out.
    """
)

# ---------- RAW DATA IN EXPANDER ----------
with st.expander("See raw data"):
    st.dataframe(df)

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built with ❤️ in Streamlit")
