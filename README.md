# FIFA World Cup Data Visualization and Observations (1930-2018)
This project aims to gain insights and visualize FIFA World Cup data since its inauguration in 1930 till the 2018 edition. Link to the notebook: [FIFA Data Viz Jupyter Notebook](notebook/fifa-world-cup-1930-2018.ipynb)

Link to the web app [here](https://binyoh1-fifa-world-cup-dataviz-app-wu31th.streamlitapp.com/)

You can download the datset [here](https://www.kaggle.com/datasets/iamsouravbanerjee/fifa-football-world-cup-dataset)

This project aims to gain the following insights:
- Build a dataset with World Cup host, winner and top scoring team for each edition of the World Cup (1930-2018)
- What is the probability of the top scoring team winning the World Cup.- What is the probability of the host nation's team winning the World Cup.
- Visualize data of total goals scored in every edition of the World Cup from 1930-2018 indicating the number of participating teams in each edition of the tournament.
- Visualize data of total goals scored and conceded by each nation in every edition of the World Cup from 1930-2018.
- Observe any noticeable trends and deviations from said trends across World Cup editions.
  - For any observable deviations, what were some interesting stories surrounding those particular World Cup editions.
- Finally, creating a web app that displays important/interesting visuals


### Current Task
- Updating web app visualizing interesting insights in plot and table format

I originally started creating the app layout using Plotly Dash, but came to the realization that creating the HTML & CSS properties would be very cumbersome (though I have some proficiency with both languages), the code also became extremely untidy (and that is before I start adding the data processing/wrangling).

As such, I went with the more beginner friendly Streamlit to build the web app.
