## Imports----------------------------------------------------------------
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit import markdown as md

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

# Goals and Participating Teams Dataframe________________________________
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
# Plot of Total Goals Scored per World Cup________________________________
df_summary_2 = df_summary.copy().sort_values("Number of Teams", ascending=False)
df_summary_2["Number of Teams"] = df_summary_2["Number of Teams"].astype(str)
fig_tg = px.bar(
    df_summary_2,
    x="Year",
    y="Total Goals Scored",
    color="Number of Teams",
    title="Total Goals Scored in each World Cup (1930-2018)",
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
)
fig_ag.update_xaxes(type="category", categoryorder="category ascending", tickangle=-90)

# Plot of Average Number of Goals per Number of Wordl Cup Participants___
df_agnt["Number of Teams"] = df_agnt["Number of Teams"].astype(str)
fig_agnt = px.bar(
    df_agnt,
    x="Number of Teams",
    y="Average Number of Goals",
    color="Number of Teams",
    text="Average Number of Goals",
    title="Average Number of Goals Scored per Number of Participating Teams",
    width=800,
)
fig_agnt.update_xaxes(type="category", categoryorder="category ascending")

## App Layout------------------------------------------------------------
# Page Header
md("<h1 style='text-align: center;'>The FIFA World Cup</h1>", unsafe_allow_html=True)

# Summary Table_________________________________________________________
# Header
st.header("FIFA World Cup Tournament Summary")

## World Cup Summary Plots_____________________________________________
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Total Goals Scored per World Cup",
        "📈 Average Goals Scored per Game in each World Cup",
        "📈 Average Goals Scored per Number of World Cup Participants",
        "🗃 Data",
    ]
)
# Plot of Total Goals Scored per World Cup_____________________________
with tab1:
    st.plotly_chart(fig_tg)
# Plot of Average Goals Scored per Game in each World Cup______________
with tab2:
    st.plotly_chart(fig_ag)
# Plot of Average Number of Goals per Number of World Cup Participants_
with tab3:
    st.plotly_chart(fig_agnt)
# Dataframe Table______________________________________________________
with tab4:
    df_summary

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
fig_2018.update_xaxes(tickangle=-85)
fig_2018.update_yaxes(dtick=4)

# WC 2014 Team performance_____________________________________________
fig_2014 = px.bar(
    df_2014,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 2014 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)
fig_2014.update_xaxes(tickangle=-85)
fig_2014.update_yaxes(dtick=4)

# WC 2010 Team performance_____________________________________________
fig_2010 = px.bar(
    df_2010,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 2010 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)
fig_2010.update_xaxes(tickangle=-85)
fig_2010.update_yaxes(dtick=4)

# WC 2006 Team performance_____________________________________________
fig_2006 = px.bar(
    df_2006,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 2006 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)
fig_2006.update_xaxes(tickangle=-85)
fig_2006.update_yaxes(dtick=4)

# WC 2002 Team performance_____________________________________________
fig_2002 = px.bar(
    df_2002,
    x="Team",
    y=["Goals For", "Goals Against"],
    title="Goals Scored & Conceded per Nation - 2002 World Cup",
    barmode="group",
    labels={"Team": "Team", "value": "Number of Goals", "variable": ""},
)
fig_2002.update_xaxes(tickangle=-85)
fig_2002.update_yaxes(dtick=4)

## Team Performance per World Cup--------------------------------------
# Header
st.header("Team Performance in each World Cup")
# Section Layout
option = st.selectbox("Choose the World Cup Edition(s) you wish to view", (year_list))


# Footer
md(
    """Dataset Source: [Kaggle](https://www.kaggle.com/datasets/iamsouravbanerjee/fifa-football-world-cup-dataset)"""
)
