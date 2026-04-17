from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_PATH = Path("data") / "pink_morsels_sales.csv"
PRICE_INCREASE_DATE = pd.to_datetime("2021-01-15")

REGION_OPTIONS = ["all", "north", "east", "south", "west"]


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Sales"] = pd.to_numeric(df["Sales"])
    df["Region"] = df["Region"].astype(str).str.strip().str.lower()
    return df


df_all = load_data().sort_values("Date")

app = Dash(__name__)
app.title = "Soul Foods — Pink Morsel Sales Visualiser"


def make_figure(region: str):
    if region != "all":
        dff = df_all[df_all["Region"] == region].copy()
        title_region = region.title()
    else:
        dff = df_all.copy()
        title_region = "All regions"

    # Aggregate by day so the chart is clean and “before/after” is obvious
    dff = dff.groupby("Date", as_index=False)["Sales"].sum()

    fig = px.line(
        dff,
        x="Date",
        y="Sales",
        labels={"Date": "Date", "Sales": "Sales ($)"},
        title=f"Pink Morsel Sales Over Time — {title_region}",
    )

    fig.update_traces(line={"width": 3})

    # Vertical marker for the price increase date
    fig.add_vline(
        x=PRICE_INCREASE_DATE,
        line_width=2,
        line_dash="dash",
        line_color="#FF4D6D",
    )
    fig.add_annotation(
        x=PRICE_INCREASE_DATE,
        y=float(dff["Sales"].max()) if len(dff) else 0,
        text="Price increase (2021-01-15)",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-40,
    )

    fig.update_layout(
        margin={"l": 40, "r": 20, "t": 70, "b": 40},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="header",
            children=[
                html.H1("Soul Foods — Pink Morsel Sales Visualiser", className="title"),
                html.P(
                    className="subtitle",
                    children=(
                        "Use the controls below to explore Pink Morsel sales by region. "
                        "The dashed line marks the price increase on 2021-01-15."
                    ),
                ),
            ],
        ),
        html.Div(
            className="card controls",
            children=[
                html.Label("Filter by region", className="control-label"),
                dcc.RadioItems(
                    id="region-radio",
                    options=[{"label": r.title(), "value": r} for r in REGION_OPTIONS],
                    value="all",
                    inline=True,
                    className="radio",
                ),
            ],
        ),
        html.Div(
            className="card",
            children=[
                dcc.Graph(
                    id="sales-line-chart",
                    figure=make_figure("all"),
                    config={"displayModeBar": True},
                )
            ],
        ),
        html.Div(
            className="footer",
            children=[
                html.P(
                    "Business question: Were sales higher before or after the price increase?",
                    className="footer-text",
                )
            ],
        ),
    ],
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-radio", "value"),
)
def update_chart(selected_region: str):
    return make_figure(selected_region)


if __name__ == "__main__":
    app.run(debug=True)