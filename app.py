## Imports----------------------------------------------------------------
from tkinter import font
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit import markdown as md

## Defaulting Streamlit App to Wide Mode---------------------------------
st.set_page_config(
    page_title="The FIFA Men's World Cup - Team Performance", layout="wide"
)

## Pandas Data Wrangling-------------------------------------------------
# List of Years the World Cup Took Place______________________________
year_list = [y for y in range(2022, 1949, -4)] + [y for y in range(1938, 1929, -4)]

# Reading CSV Files into Pandas Dataframes_______________________________
df_ogs = pd.read_csv(
    "./datasets/fifa-football-world-cup-dataset/FIFA - World Cup Summary.csv"
)

# concatenated dataframe containing all data
fifa_wc_data = pd.concat(
    [
        pd.read_csv(
            f"./datasets/fifa-football-world-cup-dataset/FIFA - {year}.csv"
        ).assign(Year=year)
        for year in year_list
    ]
)

fifa_wc_data.rename(
    columns={"Goals For": "Goals Scored", "Goals Against": "Goals Conceded"},
    inplace=True,
)

# List of Total Goals Scored per World Cup_____________________________
goals_per_wc = (
    fifa_wc_data.groupby("Year")["Goals Scored"].sum().sort_index(ascending=False)
)

# List of Number of Participating Teams per World Cup___________________
num_teams_per_wc = (
    fifa_wc_data.groupby("Year")["Team"].count().sort_index(ascending=False)
)

# List of Number of Matches Played per World Cup________________________
num_matches_list = list(df_ogs["MATCHES PLAYED"])
num_matches_list.reverse()

# List of World Cup Hosts________________________________________________
hosts_list = list(df_ogs["HOST"])
hosts_list.reverse()

# List of World Cup Champions____________________________________________
champions_list = list(df_ogs["CHAMPION"])
champions_list.reverse()

# List of World Cup Runner-Ups___________________________________________
runner_ups_list = list(df_ogs["RUNNER UP"])
runner_ups_list.reverse()

# List of World Cup Third Place Teams____________________________________
third_place_list = list(df_ogs["THIRD PLACE"])
third_place_list.reverse()

# Creating a new FIFA World Cup Summary Dataframe_______________________
df_summary = pd.DataFrame(year_list, columns=["Year"])
df_summary["Host(s)"] = list(reversed(df_ogs["HOST"].to_list()))
df_summary["Champion"] = list(reversed(df_ogs["CHAMPION"].to_list()))
df_summary["Runner-Up"] = list(reversed(df_ogs["RUNNER UP"].to_list()))
df_summary["Third Place"] = list(reversed(df_ogs["THIRD PLACE"].to_list()))
df_summary["Number of Teams"] = num_teams_per_wc.values
df_summary["Matches Played"] = list(reversed(df_ogs["MATCHES PLAYED"].to_list()))
df_summary["Total Goals Scored"] = goals_per_wc.values
df_summary["Avg Goals per Game"] = round(
    (df_summary["Total Goals Scored"] / df_summary["Matches Played"]), 1
)
df_summary_i = df_summary.set_index("Year")
df_summary_i.columns.name = df_summary_i.index.name
df_summary_i.index.name = None

# All winners in FIFA World Cup history_________________________________
df_summary_n = df_summary.copy()
df_summary_n["Champion"] = df_summary_n["Champion"].replace(
    ["West Germany", "Germany"], "Germany *"
)
wc_champions_dict = dict(df_summary_n["Champion"].value_counts())
df_champions = pd.DataFrame(
    list(wc_champions_dict.items()), columns=["Team", "Number of Titles"]
)

# Average Number of Goals per Number of World Cup Participants Dataframe__
avg_goals_per_num_teams_dict = dict(
    [
        (
            x,
            round(
                df_summary.loc[
                    df_summary["Number of Teams"] == x, "Total Goals Scored"
                ].mean(),
                2,
            ),
        )
        for x in df_summary.loc[:, "Number of Teams"]
    ]
)
df_agnt = pd.DataFrame.from_dict(avg_goals_per_num_teams_dict.items())
df_agnt.columns = ["Number of Teams", "Average Number of Goals"]
df_agnt.sort_values("Number of Teams", ascending=False, inplace=True)

## Creating Plots/Charts--------------------------------------------------
# Plot of World Cup winners in the history of the competition______________
df_champions["Number of Titles"] = df_champions["Number of Titles"].astype(str)
fig_champions = px.bar(
    df_champions,
    x="Team",
    y="Number of Titles",
    height=550,
    text="Number of Titles",
)
fig_champions.update_xaxes(tickfont_size=14)
fig_champions.update_yaxes(tickfont_size=16)
fig_champions.update_layout(yaxis=dict(visible=False, showticklabels=False))
fig_champions.update_traces(
    textposition="outside",
    textfont=dict(size=16),
    marker=dict(
        color=[
            "#0082d9" if i == df_champions["Number of Titles"].idxmax() else "#7ccbfd"
            for i in df_champions.index
        ]
    ),
)

# Plot of Total Goals Scored per World Cup________________________________
df_summary_2 = df_summary.copy().sort_values("Number of Teams", ascending=False)
df_summary_2["Number of Teams"] = df_summary_2["Number of Teams"].astype(str)
fig_tg = px.bar(
    df_summary_2,
    x="Year",
    y="Total Goals Scored",
    color="Number of Teams",
    title="Total Goals Scored in each World Cup (1930-2018)",
    hover_data=["Matches Played"],
    height=600,
)
fig_tg.update_xaxes(type="category", categoryorder="category ascending", tickangle=-60)

# Plot of Average Goals Scored per World Cup Game_______________________
df_summary_2["Year"] = df_summary_2["Year"].astype(str)
fig_ag = px.line(
    df_summary.sort_values("Year", ascending=True),
    x="Year",
    y="Avg Goals per Game",
    title="Average Number of Goals Scored per Game in each World Cup",
    hover_data=["Number of Teams", "Total Goals Scored", "Matches Played"],
    height=550,
)
fig_ag.update_xaxes(type="category", categoryorder="category ascending")
fig_ag.update_traces(mode="markers+lines")

# Plot of Average Number of Goals per Number of World Cup Participants___
df_agnt["Number of Teams"] = df_agnt["Number of Teams"].astype(str)
fig_agnt = px.bar(
    df_agnt,
    x="Number of Teams",
    y="Average Number of Goals",
    color="Number of Teams",
    text="Average Number of Goals",
    title="Average Number of Goals Scored per Number of Participating Teams",
    height=550,
)
fig_agnt.update_layout(
    legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=0.7)
)
fig_agnt.update_xaxes(type="category", categoryorder="category ascending")
fig_agnt.update_yaxes(gridcolor="#848884")
fig_agnt.update_traces(textposition="outside")

## App Layout------------------------------------------------------------
# Page Header
col1, col2, col3 = st.columns([1.1, 1.5, 1])
with col2:
    st.title("The FIFA Men's World Cup")

# Summary Table_________________________________________________________
# Header
st.header("FIFA World Cup Tournament Summary")

## World Cup Summary Plots_____________________________________________
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "World Cup Champions",
        "📈 Total Goals Scored per World Cup",
        "📈 Average Goals Scored per Game in each World Cup",
        "📈 Average Goals Scored per Number of World Cup Participants",
        "🗃 Data",
    ]
)
# Plot of world cup champions_________________________________________
df_champions_i = df_champions.set_index("Team")
df_champions_i.columns.name = df_champions_i.index.name
df_champions_i.index.name = None
tab1_text = "- &#42; 3 titles won as **West Germany** (1954, 1974, 1990) and 1 as unified Germany (2014)."

with tab1:
    options = st.selectbox(
        "Choose how you want the data presented: Chart or Table", ("Chart", "Table")
    )
    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        md("#### All FIFA World Cup Champions and Number of Titles")
    if options == "Table":
        col1, col2, col3 = st.columns([2, 3, 3])
        with col2:
            st.write(df_champions_i.to_html(), unsafe_allow_html=True)
        with col3:
            md(tab1_text)
    elif options == "Chart":
        col1, col2, col3 = st.columns([1, 7, 3])
        with col2:
            st.plotly_chart(fig_champions, use_container_width=True)
        with col3:
            st.write("")
            st.write("")
            st.write("")
            md(tab1_text)
    else:
        st.error("You can only select Chart or Table.")

# Plot of Total Goals Scored per World Cup_____________________________
with tab2:
    col1, col2 = st.columns([9, 3])
    with col1:
        st.plotly_chart(fig_tg, use_container_width=True)
    with col2:
        md(
            """
           - The **1954** and **1958** World Cup editions had many more goals scored compared to other editions that had 16 participating teams (**1934, 1954-1978**).
           - The **1990** World Cup oddly had significantly fewer goals scored compared to other editions of the tournament with 24 participants (**1982-1994**), but was nonetheless one embroiled in drama.
           - The **2006** edition and especially the **2010** World Cup had numerous complaints about the behaviour of the matchball used in the tournament, which may partially explain why fewer goals were scored compared to other editions with 32 participants (**1998-present**).
           """
        )
# Plot of Average Goals Scored per Game in each World Cup______________
with tab3:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(fig_ag, use_container_width=True)
    with col2:
        md(
            """
- The earliest World Cup Editions (**1930-1958**) in general had on average higher number of goals scored per game (**over 3.5**), while subsequent editions had comparably lower numbers (**under 3**).

- Interestingly, the **1954** World Cup while having the most goals scored (**140**) amongst all the editions in which 16 teams participated (**1934, 1954-1978**), had the second fewest matches played (**26**).
    - Hence the highest average goals scored per game (**5.4**) in World Cup history.
- The **1990** World Cup in contrast, has the lowest average goals scored per game (**2.2**) in the tournament's history.
    """
        )
# Plot of Average Number of Goals per Number of World Cup Participants_
with tab4:
    col1, col2 = st.columns([8, 3])
    with col1:
        st.plotly_chart(fig_agnt, use_container_width=True)
    with col2:
        md(
            """
            - Generally, the higher the number of participants, the higher the number of goals scored in the World Cup. Though that isn't necessarily the case for every edition of the World Cup.
           """
        )
# Dataframe Table______________________________________________________
with tab5:
    st.write(df_summary_i.to_html(), unsafe_allow_html=True)


## World Cup Team Perfomances-----------------------------------------
# Dynamically create and display team performance bar chart
def create_fifa_bar_chart(year):
    try:
        year_data = fifa_wc_data[fifa_wc_data["Year"] == year]
        fig = px.bar(
            year_data.sort_index(ascending=False),
            x=["Goals Conceded", "Goals Scored"],
            y="Team",
            title=f"{year} World Cup Team Perfomance - Goals Scored and Conceded",
            barmode="group",
            labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
            width=652,
            height=920,
            color_discrete_map={"Goals Scored": "#0082d9", "Goals Conceded": "#c68555"},
        )

        fig.update_traces(hovertemplate="Team: %{y}<br>Goals: %{x}")

        fig.update_layout(
            legend=dict(
                orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=0.5
            )
        )

        return fig

    except:
        print(
            f"Data not found for {year}.\nPlease input a valid FIFA World Cup year up to {max(year_list)}!"
        )


# Dynamically create and render dataframe for selected year
def render_fifa_df(year):
    try:
        return fifa_wc_data[fifa_wc_data["Year"] == year].to_html()

    except:
        print(
            f"Data not found for {year}.\nPlease input a valid FIFA World Cup year up to 2018!"
        )


## Team Performance per World Cup--------------------------------------
# Header
st.header("Team Performance in each World Cup")
# Section Layout
selected_year = st.selectbox(
    "Choose the World Cup edition you wish to display", (year_list)
)

try:
    tab1, tab2 = st.tabs(["📈 Team Performace Chart", "🗃 Team Performance Data"])
    with tab1:
        col1, col2, col3 = st.columns([1, 14, 1])
        with col2:
            st.plotly_chart(
                create_fifa_bar_chart(selected_year), use_container_width=True
            )
    with tab2:
        st.write(
            render_fifa_df(selected_year),
            unsafe_allow_html=True,
        )
except:
    st.error(
        "This plot/information is currently unavailable. Please, contact [@Binyoh](https://github.com/Binyoh1) to have it resolved"
    )

# Footer
md(
    """Dataset Source: [Kaggle](https://www.kaggle.com/datasets/iamsouravbanerjee/fifa-football-world-cup-dataset)"""
)
