from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

DATA_PATH = Path("data") / "pink_morsels_sales.csv"
PRICE_INCREASE_DATE = pd.to_datetime("2021-01-15")


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    # Ensure correct types
    df["Date"] = pd.to_datetime(df["Date"])
    df["Sales"] = pd.to_numeric(df["Sales"])

    # Sort by date as required
    df = df.sort_values("Date")

    return df


df = load_data()

fig = px.line(
    df,
    x="Date",
    y="Sales",
    labels={
        "Date": "Date",
        "Sales": "Sales ($)",
    },
    title="Pink Morsel Sales Over Time",
)

# Make the “before vs after 2021-01-15” comparison obvious
fig.add_vline(
    x=PRICE_INCREASE_DATE,
    line_width=2,
    line_dash="dash",
    line_color="red",
)
fig.add_annotation(
    x=PRICE_INCREASE_DATE,
    y=df["Sales"].max(),
    text="Price increase (2021-01-15)",
    showarrow=True,
    arrowhead=2,
    ax=40,
    ay=-40,
)

app = Dash(__name__)
app.title = "Soul Foods — Pink Morsel Sales Visualiser"

app.layout = html.Div(
    style={"maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1("Soul Foods — Pink Morsel Sales Visualiser"),
        html.P(
            "Question: Were sales higher before or after the Pink Morsel price increase on 2021-01-15?"
        ),
        dcc.Graph(
            id="sales-line-chart",
            figure=fig,
            config={"displayModeBar": True},
        ),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)