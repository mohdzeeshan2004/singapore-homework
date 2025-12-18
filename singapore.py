import streamlit as st
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Singapore Population Analysis",
    layout="wide"
)

st.title("🇸🇬 Singapore Population Data Analysis")
st.write("Analysis using Pandas & Streamlit")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Singapore_Residents.csv")

df = load_data()

st.subheader("📄 Raw Dataset")
st.dataframe(df)

# ======================================================
# 1️⃣ Total Population Every Year
# ======================================================
st.subheader("1️⃣ Total Population Every Year")

total_population_df = (
    df.groupby("Year")["Count"]
    .sum()
    .reset_index()
    .rename(columns={"Count": "Total_Population"})
)

st.dataframe(total_population_df)

st.line_chart(
    total_population_df.set_index("Year")
)

# ======================================================
# 2️⃣ Female to Male Ratio (3-Year Gap)
# ======================================================
st.subheader("2️⃣ Female to Male Ratio (Every 3 Years)")

years = [2000, 2003, 2006, 2009, 2012, 2015, 2018]

groups = {
    "Total": ("Total Male Residents", "Total Female Residents"),
    "Malays": ("Total Male Malays", "Total Female Malays"),
    "Chinese": ("Total Male Chinese", "Total Female Chinese"),
    "Indians": ("Total Male Indians", "Total Female Indians"),
    "Others": (
        "Other Ethnic Groups (Males)",
        "Other Ethnic Groups (Females)"
    )
}

ratio_data = []

for y in years:
    for g, (m, f) in groups.items():
        male = df[(df["Year"] == y) & (df["Residents"] == m)]["Count"].values[0]
        female = df[(df["Year"] == y) & (df["Residents"] == f)]["Count"].values[0]

        ratio_data.append({
            "Year": y,
            "Group": g,
            "Male": male,
            "Female": female,
            "Female_to_Male_Ratio": round(female / male, 4)
        })

ratio_df = pd.DataFrame(ratio_data)

st.dataframe(ratio_df)

# Filter option
selected_group = st.selectbox(
    "Select Group to Visualize",
    ratio_df["Group"].unique()
)

filtered_ratio = ratio_df[ratio_df["Group"] == selected_group]

st.line_chart(
    filtered_ratio.set_index("Year")["Female_to_Male_Ratio"]
)

# ======================================================
# 3️⃣ Population Growth (YoY & Running Total)
# ======================================================
st.subheader("3️⃣ Population Growth Analysis")

pop = df[df["Residents"] == "Total Residents"].sort_values("Year")

pop["Growth %"] = pop["Count"].pct_change() * 100
pop["Running Total %"] = (
    (pop["Count"] - pop["Count"].iloc[0]) /
    pop["Count"].iloc[0]
) * 100

growth_df = pop[["Year", "Count", "Growth %", "Running Total %"]]

st.dataframe(growth_df)

col1, col2 = st.columns(2)

with col1:
    st.write("📈 Year-on-Year Growth (%)")
    st.line_chart(growth_df.set_index("Year")["Growth %"])

with col2:
    st.write("📊 Running Total Growth (%)")
    st.line_chart(growth_df.set_index("Year")["Running Total %"])

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("👨‍💻 Built with **Python • Pandas • Streamlit**")
