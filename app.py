## Imports----------------------------------------------------------------
from tkinter import font
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit import markdown as md

## Defaulting Streamlit App to Wide Mode---------------------------------
st.set_page_config(layout="wide")

## Pandas Data Wrangling-------------------------------------------------
# Reading CSV Files into Pandas Dataframes_______________________________
df_ogs = pd.read_csv(
    "./datasets/fifa-football-world-cup-dataset/FIFA - World Cup Summary.csv"
)
df_2018 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 2018.csv")
df_2014 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 2014.csv")
df_2010 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 2010.csv")
df_2006 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 2006.csv")
df_2002 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 2002.csv")
df_1998 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1998.csv")
df_1994 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1994.csv")
df_1990 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1990.csv")
df_1986 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1986.csv")
df_1982 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1982.csv")
df_1978 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1978.csv")
df_1974 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1974.csv")
df_1970 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1970.csv")
df_1966 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1966.csv")
df_1962 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1962.csv")
df_1958 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1958.csv")
df_1954 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1954.csv")
df_1950 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1950.csv")
df_1938 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1938.csv")
df_1934 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1934.csv")
df_1930 = pd.read_csv("./datasets/fifa-football-world-cup-dataset/FIFA - 1930.csv")

# List of Dataframes_____________________________________________________
data_list = [
    df_2018,
    df_2014,
    df_2010,
    df_2006,
    df_2002,
    df_1998,
    df_1994,
    df_1990,
    df_1986,
    df_1982,
    df_1978,
    df_1974,
    df_1970,
    df_1966,
    df_1962,
    df_1958,
    df_1954,
    df_1950,
    df_1938,
    df_1934,
    df_1930,
]

# List of Years the World Cup Took Place______________________________
year_list = [x for x in range(1950, 2019, 4)]
year_list.sort(reverse=True)
year_list2 = [y for y in range(1930, 1939, 4)]
year_list2.sort(reverse=True)
year_list.extend(year_list2)

# List of Total Goals Scored per World Cup_____________________________
goals_list = [x["Goals For"].sum() for x in data_list]
goals_dict = dict(zip(year_list, goals_list))

# List of Number of Participating Teams per World Cup___________________
teams_list = [x["Team"].count() for x in data_list]
teams_dict = dict(zip(year_list, teams_list))

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
df_teams = pd.DataFrame(list(teams_dict.items()), columns=["Year", "Number of Teams"])
df_goals = pd.DataFrame(
    list(goals_dict.items()), columns=["Year", "Total Goals Scored"]
)
df_summary = (
    df_teams.set_index(["Year"]).join(df_goals.set_index(["Year"]))
).reset_index()
df_summary["Host(s)"] = hosts_list
df_summary["Champion"] = champions_list
df_summary["Runner-Up"] = runner_ups_list
df_summary["Third Place"] = third_place_list
df_summary["Matches Played"] = num_matches_list
df_summary["Avg Goals per Game"] = round(
    (df_summary["Total Goals Scored"] / df_summary["Matches Played"]), 2
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
# df_champions["Number of Titles"] = df_champions["Number of Titles"].astype(str)
fig_champions = px.bar(
    df_champions,
    x="Team",
    y="Number of Titles",
    color="Number of Titles",
    color_continuous_scale="Viridis",
    title="All FIFA World Cup Champions",
    height=550,
)
fig_champions.update_xaxes(tickfont_size=14)
fig_champions.update_yaxes(tickfont_size=16)

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
fig_ag = px.bar(
    df_summary_2,
    x="Year",
    y="Avg Goals per Game",
    color="Avg Goals per Game",
    title="Average Number of Goals Scored per Game in each World Cup",
    hover_data=["Number of Teams", "Total Goals Scored", "Matches Played"],
    height=550,
)
fig_ag.update_xaxes(type="category", categoryorder="category ascending", tickangle=-90)

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
fig_agnt.update_xaxes(type="category", categoryorder="category ascending")

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
with tab1:
    col1, col2 = st.columns([8, 3])
    with col1:
        st.plotly_chart(fig_champions, use_container_width=True)
    with col2:
        st.header("")
        md("**Champions Table**")
        st.write(
            df_champions_i.to_html(),
            unsafe_allow_html=True,
        )
        st.write("")
        md(
            "- __\*__ 3 titles won as **West Germany** (1954, 1974, 1990) and 1 as unified Germany (2014)."
        )
# Plot of Total Goals Scored per World Cup_____________________________
with tab2:
    col1, col2 = st.columns([9, 3])
    with col1:
        st.plotly_chart(fig_tg, use_container_width=True)
    with col2:
        md(
            """
           - The **1954** and **1958** World Cup editions had many more goals scored compared to other editions which had 16 participating teams (**1934, 1954-1978**).
           - The **1990** World Cup oddly had much fewer goals scored compared to other editions of the tournament with 24 participants (**1982-1994**), but was nonetheless one embroiled in drama.
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
- The earliest World Cup Editions (**1930-1958**) in general had higher average goals per game (**over 3.5**), while subsequent editions had comparably lower numbers (**under 3.0**).

- Interestingly, the **1954** World Cup while having the most goals scored (**140**) amongst all the editions in which 16 teams participated (**1934, 1954-1978**), it had the second fewest matches played (**26**).
    - Hence the highest average goals scored per game (**5.38**) in World Cup history.
- The **1990** World Cup in contrast, has the lowest average goals scored per game (**2.21**) in the tournament's history.
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
# WC 2018 Team performance_____________________________________________
fig_2018 = px.bar(
    df_2018,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 2018 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 2014 Team performance_____________________________________________
fig_2014 = px.bar(
    df_2014,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 2014 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 2010 Team performance_____________________________________________
fig_2010 = px.bar(
    df_2010,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 2010 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 2006 Team performance_____________________________________________
fig_2006 = px.bar(
    df_2006,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 2006 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 2002 Team performance_____________________________________________
fig_2002 = px.bar(
    df_2002,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 2002 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1998 Team performance_____________________________________________
fig_1998 = px.bar(
    df_1998,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1998 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1994 Team performance_____________________________________________
fig_1994 = px.bar(
    df_1994,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1994 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1990 Team performance_____________________________________________
fig_1990 = px.bar(
    df_1990,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1990 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1990 Team performance_____________________________________________
fig_1990 = px.bar(
    df_1990,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1990 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1986 Team performance_____________________________________________
fig_1986 = px.bar(
    df_1986,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1986 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1982 Team performance_____________________________________________
fig_1982 = px.bar(
    df_1982,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1982 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1982 Team performance_____________________________________________
fig_1982 = px.bar(
    df_1982,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1982 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1982 Team performance_____________________________________________
fig_1982 = px.bar(
    df_1982,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1982 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1978 Team performance_____________________________________________
fig_1978 = px.bar(
    df_1978,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1978 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1974 Team performance_____________________________________________
fig_1974 = px.bar(
    df_1974,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1974 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1970 Team performance_____________________________________________
fig_1970 = px.bar(
    df_1970,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1970 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1966 Team performance_____________________________________________
fig_1966 = px.bar(
    df_1966,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1966 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1962 Team performance_____________________________________________
fig_1962 = px.bar(
    df_1962,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1962 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1958 Team performance_____________________________________________
fig_1958 = px.bar(
    df_1958,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1958 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1958 Team performance_____________________________________________
fig_1958 = px.bar(
    df_1958,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1958 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1954 Team performance_____________________________________________
fig_1954 = px.bar(
    df_1954,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1954 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1950 Team performance_____________________________________________
fig_1950 = px.bar(
    df_1950,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1950 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1938 Team performance_____________________________________________
fig_1938 = px.bar(
    df_1938,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1938 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1934 Team performance_____________________________________________
fig_1934 = px.bar(
    df_1934,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1934 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# WC 1930 Team performance_____________________________________________
fig_1930 = px.bar(
    df_1930,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 1930 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)

# List of Plots________________________________________________________
fig_list = [
    fig_2018,
    fig_2014,
    fig_2010,
    fig_2006,
    fig_2002,
    fig_1998,
    fig_1994,
    fig_1990,
    fig_1986,
    fig_1982,
    fig_1978,
    fig_1974,
    fig_1970,
    fig_1966,
    fig_1962,
    fig_1958,
    fig_1954,
    fig_1950,
    fig_1938,
    fig_1934,
    fig_1930,
]

# Update Layout of all Plotly Figures
for fig in fig_list:
    fig.update_layout(height=650)
    fig.update_xaxes(tickangle=-85)
    fig.update_yaxes(dtick=2)

## Team Performance per World Cup--------------------------------------
# Header
st.header("Team Performance in each World Cup")
# Section Layout
selected_year = st.selectbox(
    "Choose the World Cup Edition you wish to display", (year_list)
)

try:
    tab1, tab2 = st.tabs(["📈 Team Performace Chart", "🗃 Team Performance Data"])
    with tab1:
        col1, col2, col3 = st.columns([1, 14, 1])
        with col2:
            st.plotly_chart(
                fig_list[year_list.index(selected_year)], use_container_width=True
            )
    with tab2:
        data_list[year_list.index(selected_year)]
except IndexError:
    st.error(
        "This plot/information is currently not available. Please, contact [@Binyoh](https://github.com/Binyoh1) to have it resolved"
    )

# Footer
md(
    """Dataset Source: [Kaggle](https://www.kaggle.com/datasets/iamsouravbanerjee/fifa-football-world-cup-dataset)"""
)
