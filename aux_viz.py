import pandas as pd
import plotly.express as px


def plot_time_series(df, agg_period="D", mode="agg"):
  if mode == "agg":
    df['date'] = pd.to_datetime(df['date'])
    df = df[["date", "views"]]
    df_temp = df.set_index("date")
    grouped = df_temp.groupby(
      [
      pd.Grouper(level="date", freq=agg_period)
      ]
    ).agg(
      views = pd.NamedAgg(column = "views", aggfunc="sum")
    )
    df_plot = grouped.reset_index()
    fig = px.line(df_plot, x="date", y="views", title="Views for selected ADMIN1-regions",
                  labels={"date": "Time Period", "views": "Views"})
  elif mode == "compare" or mode == "stacked":
    df['date'] = pd.to_datetime(df['date'])
    df = df[["article", "date", "views"]]
    df_temp = df.set_index(["article", "date"])
    grouped = df_temp.groupby(
      [
        pd.Grouper(level="article"),
        pd.Grouper(level="date", freq=agg_period)
      ]
    ).agg(
      views=pd.NamedAgg(column="views", aggfunc="sum")
    )
    df_plot = grouped.reset_index()
    if mode == "compare":
      fig = px.line(df_plot, x="date", y="views", color = "article", title="Views for selected ADMIN1-regions",
                  labels={"date": "Time Period", "views": "Views"})
    elif mode == "stacked":
      fig = px.area(df_plot, x="date", y="views", color = "article", title="Views for selected ADMIN1-regions",
                  labels={"date": "Time Period", "views": "Views"})
  return fig

