import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

import base64
from pathlib import Path


MIN_YEAR = 2010
PRE_YEARS = 1
POST_YEARS = 1

# We highlight these, but we load ALL data for the global charts
COUNTRIES_OF_INTEREST = [
    "United States", "United Kingdom", "Germany",
    "France", "Japan", "Israel", "Canada",
    "Russia", "Ukraine", "China", "Argentina", "Brazil", "Ghana", "India"
]

# URLs / Paths
LIFE_URL = "life.csv"
HAPPINESS_PATH = "happiness.csv"
MACRO_PATH = "macro.csv"

#events
EVENTS = pd.DataFrame([
    {"event": "The Election of Donald Trump", "start_year": 2016, "end_year": 2017, "scope": "Global", "type": "Political","sideA":"United States","sideB":"Israel", "bio":"The election of a 'Washington outsider' as the 45th President of the United States marked a pivot toward 'America First' policies"},
    {"event": "US–China trade tensions", "start_year": 2018, "end_year": 2020, "scope": "Global", "type": "Economic","sideA":"Israel","sideB":"Israel", "bio": "An economic conflict between China and the United States has been ongoing since January 2018, when U.S. president Donald Trump began imposing tariffs and other trade barriers on China "},
    {"event": "Israel Political Crisis", "start_year": 2019, "end_year": 2022, "scope": "Israel", "type": "Political","sideA":"Israel","sideB":"Israel", "bio": "a period of political instability in Israel, in which five Knesset elections were held in a span of over three years"},
    {"event": "The U.S.–North Korea Summits", "start_year": 2018, "end_year": 2020, "scope": "Global", "type": "Political","sideA":"United States","sideB":"North Korea","bio":"Beginning with the Singapore Summit in June 2018, Donald Trump became the first sitting U.S. president to meet with a North Korean leader, Kim Jong-un. While the meetings did not result in full denuclearization, they represented a historic shift from the 'fire and fury' rhetoric of 2017."},
    {"event": "The Abraham Accords", "start_year": 2019, "end_year": 2020, "scope": "Global","type": "Political", "sideA": "United Arab Emirates", "sideB": "Israel","bio":"In a major shift for Middle Eastern geopolitics, the United Arab Emirates and Bahrain signed agreements to normalize diplomatic relations with Israel."},
])

EVENTS_WARS = pd.DataFrame([
    {"event": "Syrian Civil War (Peak)", "start_year": 2015, "end_year": 2018, "scope": "Syria", "type": "War","sideA":"Israel","sideB":"Syria","bio":"The conflict involved a dizzying array of actors, including Turkey, Iran, the U.S., and various rebel and Kurdish factions, leading to one of the worst humanitarian disasters of the 21st century."},
    {"event": "The Shayrat Missile Strike", "start_year": 2016, "end_year": 2017, "scope": "Global", "type": "War","sideA":"United States","sideB":"Syria","bio":"In a swift, one-night engagement, the United States launched 59 Tomahawk cruise missiles from the Mediterranean Sea at a Syrian government airbase."},
    {"event": "The 2016 Four-Day War", "start_year": 2016, "end_year": 2016, "scope": "Global", "type": "War","sideA":"Armenia","sideB":"Azerbaijan","bio":"A short but bloody eruption of the frozen conflict between Armenia and Azerbaijan. While not a Western war, it took place on the European periphery and was characterized by the first major use of suicide drones"},
    {"event": "The Turkey-Greece Border Standoff", "start_year": 2019, "end_year": 2020, "scope": "Global", "type": "Conflict","sideA":"Turkey","sideB":"Greece", "bio":"Tensions boiled over when Turkey announced it would no longer stop refugees from entering the EU. Greece responded by deploying the military to the Evros border. This led to weeks of border skirmishes involving tear gas, water cannons, and reports of live fire."},
    {"event": "The 2016 Montenegro Coup Attempt", "start_year": 2015, "end_year": 2016, "scope": "Global", "type": "Conflict","sideA":"Serbia","sideB":"Montenegro","bio":"In October 2016, Montenegrin authorities arrested a group of Serbian and Russian nationalists who were allegedly planning to storm the Parliament and assassinate the Prime Minister to stop the country from joining NATO."},
])

EVENTS_PANDEMICS = pd.DataFrame([
    {"event": "COVID-19 pandemic", "start_year": 2019, "end_year": 2022, "scope": "Global", "type": "Pandemic","bio":"Emerging in late 2019, this became the most significant global health event in a century. Beyond the millions of deaths, it caused the total restructuring of global politics, economics, and daily life. It led to the fastest vaccine development in history and a permanent shift in remote work and digital infrastructure."},
    {"event": "Ebola outbreak (West Africa)", "start_year": 2014, "end_year": 2016, "scope": "West Africa","type": "Epidemic","bio":"This was the largest and most complex Ebola outbreak since the virus was first discovered in 1976. Concentrated in Guinea, Liberia, and Sierra Leone, it resulted in over 11,000 deaths"},
    {"event": "The Zika Virus Epidemic", "start_year": 2014, "end_year": 2017, "scope": "West Africa","type": "Epidemic","bio":"Spreading rapidly through the Americas, particularly Brazil, Zika was declared a Public Health Emergency of International Concern (PHEIC). This led to unprecedented travel warnings and public health debates ahead of the 2016 Rio Olympics."},
    {"event": "The Yemen Cholera Outbreak", "start_year": 2016, "end_year": 2022, "scope": "Global", "type": "Pandemic","bio":"Linked directly to the civil war, this became the worst cholera outbreak in recorded history. Over 2.5 million cases were reported as the country’s water and sanitation infrastructure collapsed. At its peak, nearly 80% of the population lacked access to clean water."},
    {"event": "The 2019 Dengue Fever Surge", "start_year": 2018, "end_year": 2019, "scope": "Global", "type": "Pandemic","bio":"2019 was one of the worst years for dengue on record. Millions of cases were reported in countries like the Philippines, Vietnam, and Bangladesh. In the Americas, Brazil alone reported over 2 million cases."},
])


# ----------------------------
# BACKGROUND (Overview only)
# ----------------------------
def set_overview_background(image_path: str):
    """
    Sets a full-page background image and adds a semi-transparent
    white container to keep text readable.
    Works best when called ONLY in the Overview tab.
    """
    try:
        img_bytes = Path(image_path).read_bytes()
    except Exception as e:
        st.warning(f"Could not load background image: {e}")
        return

    b64 = base64.b64encode(img_bytes).decode()

    st.markdown(
        f"""
        <style>
        /* Page background */
        [data-testid="stAppViewContainer"] {{
            background: url("data:image/jpg;base64,{b64}") no-repeat center center fixed;
            background-size: cover;
        }}

        /* Make content readable */
        [data-testid="stAppViewContainer"] .block-container {{
            background: rgba(255, 255, 255, 0.82);
            border-radius: 18px;
            padding: 2rem;
            margin-top: 1.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        }}

        /* Transparent header */
        header[data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


#data loaders
@st.cache_data(show_spinner=False)
def load_life_expectancy():
    try:
        df = pd.read_csv(LIFE_URL)
        # Handle "Entity" vs "country"
        if "Entity" in df.columns:
            df = df.rename(columns={"Entity": "country", "Code": "iso_code", "Year": "year"})

        # Find the value column
        value_col = [c for c in df.columns if c not in ["country", "iso_code", "year", "Code"]][0]
        df = df.rename(columns={value_col: "life_expectancy"})

        df["year"] = pd.to_numeric(df["year"], errors="coerce")
        df = df[df["year"] >= MIN_YEAR]
        return df[["country", "year", "life_expectancy"]]
    except Exception as e:
        st.error(f"Error loading Life Expectancy data: {e}")
        return pd.DataFrame(columns=["country", "year", "life_expectancy"])


@st.cache_data(show_spinner=False)
def load_happiness():

    # Normalizing column names
    df = pd.read_csv(HAPPINESS_PATH)
    col_map = {
        "Country name": "country",
        "Country": "country",
        "Year": "year",
        "Life evaluation (3-year average)": "happiness_score",
        "happiness_score": "happiness_score",
        "Explained by: Log GDP per capita": "log_gdp_per_capita",
    }
    df = df.rename(columns=col_map)

    # check required columns exist
    if "happiness_score" not in df.columns:
        st.error("Happiness file missing 'happiness_score' column.")
        return pd.DataFrame()

    # Create proxy for GDP if not present (using Log GDP)
    if "log_gdp_per_capita" in df.columns:
        df["gdp_per_capita"] = df["log_gdp_per_capita"]
    else:
        df["gdp_per_capita"] = 0

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df[df["year"] >= MIN_YEAR]
    return df[["country", "year", "happiness_score", "gdp_per_capita"]]


@st.cache_data(show_spinner=False)
def load_macro():

    df = pd.read_csv(MACRO_PATH)
    df = df.rename(columns={"countryname": "country", "rGDP_pc": "gdp_pc"})

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df[df["year"] >= MIN_YEAR]
    return df[["country", "year", "gdp_pc"]]


@st.cache_data(show_spinner=False)
def build_panel():

    macro = load_macro()
    happiness = load_happiness()
    life = load_life_expectancy()

    # Merge
    panel = pd.merge(macro, happiness, on=["country", "year"], how="outer")
    panel = pd.merge(panel, life, on=["country", "year"], how="outer")

    return panel


METRIC_MAP = {
    "gdp_pc": "Real GDP per Capita",
    "happiness_score": "Happiness Score (0-10)",
    "life_expectancy": "Life Expectancy (Years)",
}


def plot_resilience_dumbbell(panel, event_row, metric):

    start = event_row["start_year"]
    end = event_row["end_year"]

    #filter
    df_filtered = panel[panel["year"].isin([start, end])].copy()

    #pivot
    df_pivot = df_filtered.pivot(index="country", columns="year", values=metric)

    #keep only countries that have both data points
    if start not in df_pivot.columns or end not in df_pivot.columns:
        st.warning("Insufficient data for this time range.")
        return

    df_pivot = df_pivot.dropna(subset=[start, end])
    df_pivot["change"] = df_pivot[end] - df_pivot[start]

    plot_df = df_pivot.loc[df_pivot.index.isin(COUNTRIES_OF_INTEREST)].sort_values("change")
    fig = go.Figure()

    # Draw the lines connecting start and end
    for country in plot_df.index:
        start_val = plot_df.loc[country, start]
        end_val = plot_df.loc[country, end]
        color = "#3c9de7" if end_val >= start_val else "#e7973c"  # green good, red bad

        fig.add_trace(go.Scatter(
            x=[start_val, end_val],
            y=[country, country],
            mode="lines",
            line=dict(color=color, width=2),
            showlegend=False,
            hoverinfo="skip"
        ))

    # Add markers for Start Year
    fig.add_trace(go.Scatter(
        x=plot_df[start],
        y=plot_df.index,
        mode="markers",
        marker=dict(color="white", size=10),
        name=str(start)
    ))

    # Add markers for End Year
    fig.add_trace(go.Scatter(
        x=plot_df[end],
        y=plot_df.index,
        mode="markers",
        marker=dict(color=plot_df["change"].apply(lambda x: "#2e9acc" if x >= 0 else "#cc802e"), size=10),
        name=str(end)
    ))

    fig.update_layout(
        title=f"Winners & Losers: Change in {METRIC_MAP.get(metric, metric)} ({start}-{end})",
        xaxis_title=METRIC_MAP.get(metric, metric),
        yaxis_title="Country",
        height=max(400, len(plot_df) * 25),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_head_to_head(panel, event_row):

    #get Countries
    try:
        c1_name = event_row["sideA"]
        c2_name = event_row["sideB"]
    except KeyError:
        st.error("Event data missing 'sideA' or 'sideB' keys.")
        return

    #Naming Aliases
    aliases = {
        "Russia": "Russian Federation",
        "UK": "United Kingdom",
        "USA": "United States",
        "UAE": "United Arab Emirates"
    }
    c1_real = aliases.get(c1_name, c1_name)
    c2_real = aliases.get(c2_name, c2_name)

    start = event_row["start_year"]
    end = event_row["end_year"]
    y_min = start - 2
    y_max = end + 2

    #filter
    df = panel[
        (panel["country"].isin([c1_real, c2_real])) &
        (panel["year"] >= y_min) &
        (panel["year"] <= y_max)
        ].sort_values("year")

    if df.empty:
        st.warning(f"No data available for {c1_name} or {c2_name}.")
        return

    #subplots
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Economy (GDP)", "Happiness Score", "Life Expectancy"),
        horizontal_spacing=0.1
    )

    fig.add_trace(go.Bar(
        x=[None], y=[None],
        name="Conflict Period",
        marker_color="red",
        opacity=0.2,
        showlegend=True
    ), row=1, col=1)

    #add traces - helper
    def add_metric_trace(metric_col, row, col, show_legend):
        c1_data = df[df["country"] == c1_real]
        fig.add_trace(go.Scatter(
            x=c1_data["year"], y=c1_data[metric_col],
            mode='lines+markers',
            name=c1_name,
            line=dict(color='#1f77b4', width=3),  # Blue
            legendgroup=c1_name,
            showlegend=show_legend
        ), row=row, col=col)

        c2_data = df[df["country"] == c2_real]
        fig.add_trace(go.Scatter(
            x=c2_data["year"], y=c2_data[metric_col],
            mode='lines+markers',
            name=c2_name,
            line=dict(color='#ff7f0e', width=3),  # Orange
            legendgroup=c2_name,
            showlegend=show_legend
        ), row=row, col=col)

    # Add traces
    add_metric_trace("gdp_pc", 1, 1, True)
    add_metric_trace("happiness_score", 1, 2, False)
    add_metric_trace("life_expectancy", 1, 3, False)

    # highlight the Event
    for col in [1, 2, 3]:
        fig.add_vrect(
            x0=start, x1=end,
            fillcolor="grey", opacity=0.1,
            layer="below", line_width=0,
            row=1, col=col
        )

    #Legend Layout
    fig.update_layout(
        title_text=f"Head-to-Head: {c1_name} vs {c2_name}",
        height=450,
        margin=dict(l=20, r=20, t=80, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.05,
            xanchor="center", x=0.5
        ),
        template="plotly_white",
        hovermode="x unified"
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='whitesmoke')

    st.plotly_chart(fig, use_container_width=True)


def plot_conflict_path(panel, country_name, event_row):

    start = event_row["start_year"]
    end = event_row["end_year"]

    #Country Name Mismatches
    if country_name not in panel["country"].values:
        aliases = {"Russia": "Russian Federation", "UK": "United Kingdom", "USA": "United States"}
        country_name = aliases.get(country_name, country_name)

    #filter
    y_min = int(start - 1)
    y_max = int(end + 3)

    df_country = panel[(panel["country"] == country_name) &
                       (panel["year"] >= y_min) &
                       (panel["year"] <= y_max)].sort_values("year")

    if df_country.empty:
        st.warning(f"No data available for {country_name}.")
        return

    # set baseline
    base_row = df_country[df_country["year"] == start]

    if base_row.empty:
        #use the first available year if exact start year is missing
        base_row = df_country.iloc[[0]]
        st.caption(f"Note: Baseline set to {base_row['year'].values[0]} (Start year data missing)")

    # Calculate Index: (Value / Base_Value) * 100
    metrics = {
        "gdp_pc": "Economy (GDP)",
        "happiness_score": "Happiness",
        "life_expectancy": "Life Expectancy"
    }

    df_plot = df_country.copy()

    for col, label in metrics.items():
        base_val = base_row[col].values[0]
        if pd.notna(base_val) and base_val != 0:
            df_plot[label] = (df_plot[col] / base_val) * 100
        else:
            df_plot[label] = None

    #melt
    df_melted = df_plot.melt(
        id_vars=["year"],
        value_vars=list(metrics.values()),
        var_name="Metric",
        value_name="Index"
    )

    #build chart
    fig = px.line(
        df_melted,
        x="year",
        y="Index",
        color="Metric",
        markers=True,
        title=f"Relative Impact: {country_name} (Baseline {start} = 100)",
        color_discrete_map={
            "Economy (GDP)": "#1f77b4",  # Blue
            "Happiness": "#ff7f0e",  # Orange
            "Life Expectancy": "#2ca02c"  # Green
        }
    )

    #Add "Baseline" and "Crisis Zone"
    fig.add_hline(y=100, line_dash="dash", line_color="gray", opacity=0.7, annotation_text="Baseline (100)")

    # Highlight conflict
    fig.add_vrect(
        x0=start, x1=end,
        fillcolor="red", opacity=0.05,
        layer="below", line_width=0,
        annotation_text="CONFLICT PERIOD", annotation_position="top left"
    )

    #calculate final % change for the end year to show
    final_row = df_plot[df_plot["year"] == end]
    if not final_row.empty:
        for col, label in metrics.items():
            if label in df_plot.columns:
                val = final_row[label].values[0]
                if pd.notna(val):
                    pct_change = val - 100
                    symbol = "▲" if pct_change >= 0 else "▼"
                    fig.add_annotation(
                        x=end, y=val,
                        text=f"{symbol} {pct_change:.1f}%",
                        showarrow=True, arrowhead=1,
                        ax=20, ay=-20 if pct_change > 0 else 20,
                        font=dict(color="black", size=10),
                        bgcolor="white", bordercolor="black", opacity=0.8
                    )

    fig.update_layout(
        yaxis=dict(title="Change relative to Start (100 = No Change)"),
        xaxis=dict(title="Year"),
        hovermode="x unified",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_health_wealth_tradeoff(panel, event_row):

    start = event_row["start_year"]
    end = event_row["end_year"]

    #filter Data
    df_filtered = panel[
        (panel["year"].isin([start, end])) &
        (panel["country"].isin(COUNTRIES_OF_INTEREST))
    ].copy()

    if df_filtered.empty:
        st.warning("Insufficient data.")
        return

    #pivot
    pivot_life = df_filtered.pivot(index="country", columns="year", values="life_expectancy")
    pivot_gdp = df_filtered.pivot(index="country", columns="year", values="gdp_pc")

    if start not in pivot_life.columns or end not in pivot_life.columns:
        st.warning("Insufficient data for the selected years.")
        return

    # delta
    df_delta = pd.DataFrame(index=pivot_life.index)
    df_delta["delta_life"] = pivot_life[end] - pivot_life[start]
    df_delta["delta_gdp_pct"] = (pivot_gdp[end] - pivot_gdp[start]) / pivot_gdp[start] * 100

    df_delta = df_delta.dropna()

    #Classify - helper
    def classify(row):
        if row["delta_life"] > 0 and row["delta_gdp_pct"] > 0:
            return "Resilient (Health+ Wealth+)"
        if row["delta_life"] < 0 and row["delta_gdp_pct"] < 0:
            return "Crisis (Health- Wealth-)"
        return "Trade-off"

    df_delta["Status"] = df_delta.apply(classify, axis=1)
    df_delta["country"] = df_delta.index

    color_map = {
        "Resilient (Health+ Wealth+)": "#2e6dcc",  # Blue
        "Crisis (Health- Wealth-)":    "#cc6b2e",  # Orange
        "Trade-off":                   "#95a5a6"   # Gray
    }

    fig = px.scatter(
        df_delta,
        x="delta_life",
        y="delta_gdp_pct",
        color="Status",
        hover_name="country",
        title=f"Health vs. Wealth Trade-off ({start}-{end})",
        labels={"delta_life": "Change in Life Expectancy (Years)", "delta_gdp_pct": "GDP Growth (%)"},
        color_discrete_map=color_map
    )

    #quadrant lines and size
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.add_vline(x=0, line_dash="dash", line_color="gray")
    fig.update_traces(marker_size=15)
    st.plotly_chart(fig, use_container_width=True)


def plot_delta_map(panel, event_row, metric):

    #same as all functions
    start = event_row["start_year"]
    end = event_row["end_year"]

    df_filtered = panel[panel["year"].isin([start, end])].copy()
    df_pivot = df_filtered.pivot(index="country", columns="year", values=metric)

    if start not in df_pivot.columns or end not in df_pivot.columns:
        st.warning("No data for map.")
        return

    df_pivot["delta"] = df_pivot[end] - df_pivot[start]
    df_pivot = df_pivot.reset_index()

    fig = px.choropleth(
        df_pivot,
        locations="country",
        locationmode="country names",
        color="delta",
        color_continuous_scale="RdBu",  # Red for negative, Blue for positive
        color_continuous_midpoint=0,
        title=f"Global Change in {METRIC_MAP.get(metric, metric)} ({start}-{end})",
        hover_name="country"
    )

    fig.update_geos(projection_type="natural earth")
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    st.plotly_chart(fig, use_container_width=True)


# dashboards
def render_Overview():
    st.title("📊 Global Crisis Dashboard: User Guide")

    st.markdown("""
    ### Welcome
    This dashboard analyzes how major global shocks in the world of **Political, Military, and Biological** impact the well-being of nations.

    We focus on **Top 15 Strategic Nations**, while also including specific countries which certain events focuses on.

    ---

    ### How to Use This Dashboard

    **1. Political Events Tab**
    * **Focus:** Political events.
    * **Key Visual:** *The Dumbbell Chart*. It shows you the "Before" and "After" of a crisis. 
        * **Green Line:** The country improved despite the shock.
        * **Red Line:** The country declined.
    * **Use Case:** choose an event and a metric and see how each top 15 country was affected.

    **2. Wars Tab**
    * **Focus:** The correlation of destruction.
    * **Key Visual:** relative impact based on a baseline, and a head-to-head chart according to the war/conflict
    * **Use Case:** choose an event and a country and see how each top 15 country was affected, and also a matchup between the 2 countries mainly envolved.

    **3. Epidemics Tab**
    * **Focus:** The "Health vs. Wealth" dilemma.
    * **Key Visual:** *The Trade-off Scatter*.
    * **Use Case:** choose an event and see how each country preformed
    """)

    st.info("👈 Select a dashboard from the sidebar to begin.")


def render_Politics_dashboard(panel):
    st.header("Political Events")
    metric_dict = {"GDP":"gdp_pc", "Happiness Score":"happiness_score", "Life Expectancy":"life_expectancy"}

    #selectors
    col1, col2 = st.columns(2)
    with col1:
        event_name = st.selectbox("Select Event", EVENTS["event"].tolist(), key="pol_event")
    with col2:
        metric = st.selectbox("Metric to Compare", ["Happiness Score", "GDP", "Life Expectancy"], key="pol_metric")

    event_row = EVENTS[EVENTS["event"] == event_name].iloc[0]
    metric = metric_dict[metric]

    #dumbell plot
    st.subheader("Who Won and Who Lost?")
    st.markdown("This chart compares the metric *before* and *after* the event. Green lines indicate improvement.")
    st.markdown(event_row["bio"])
    plot_resilience_dumbbell(panel, event_row, metric)

    st.divider()

    #delta map
    st.subheader("Global Impact Map")
    plot_delta_map(panel, event_row, metric)


def render_Wars_dashboard(panel):
    st.header("The Cost of Conflict")

    col1, col2 = st.columns(2)
    with col1:
        event_name = st.selectbox("Select Conflict", EVENTS_WARS["event"].tolist(), key="war_event")
    with col2:
        event_row = EVENTS_WARS[EVENTS_WARS["event"] == event_name].iloc[0]
        default_scope = event_row["scope"].split(" / ")[0]  # heuristic

        all_countries = COUNTRIES_OF_INTEREST
        try:
            default_idx = all_countries.index(default_scope)
        except:
            default_idx = 0

        country = st.selectbox("Focus Country", all_countries, index=default_idx, key="war_country")

    #connected scatter
    st.subheader(f"Trajectory of {country}")
    st.markdown(event_row["bio"])
    plot_conflict_path(panel, country, event_row)

    st.divider()

    #head2head
    st.subheader("Head-to-Head Comparison")
    plot_head_to_head(panel, event_row)


def render_Epidemics_dashboard(panel):
    st.header("Epidemics: Health vs. Wealth")

    event_name = st.selectbox("Select Epidemic", EVENTS_PANDEMICS["event"].tolist(), key="epi_event")
    event_row = EVENTS_PANDEMICS[EVENTS_PANDEMICS["event"] == event_name].iloc[0]

    #trade-off scatter
    st.subheader("The Trade-off")
    st.markdown("Did saving lives cost the economy?")
    st.markdown(event_row["bio"])
    plot_health_wealth_tradeoff(panel, event_row)

    # decided to give up on this map plot
    ##st.divider()

    #map plot
    ##st.subheader("Global Health Impact")
    ##plot_delta_map(panel, event_row, "life_expectancy")


def main():
    st.set_page_config(page_title="Global Crisis Dashboard", layout="wide")

    st.sidebar.title("Navigation")
    tab = st.sidebar.radio("Go to:", ["Overview", "Political Events", "Wars", "Epidemics"])

    with st.spinner("Loading Data..."):
        panel = build_panel()

    if panel.empty:
        st.error("Data could not be loaded. Please check file paths.")
        return

    if tab == "Overview":
        # ✅ Background ONLY on Overview
        set_overview_background("overview_bg.jpg")  # <-- put the image next to app.py with this name
        render_Overview()
    elif tab == "Political Events":
        render_Politics_dashboard(panel)
    elif tab == "Wars":
        render_Wars_dashboard(panel)
    elif tab == "Epidemics":
        render_Epidemics_dashboard(panel)


if __name__ == "__main__":
    main()






