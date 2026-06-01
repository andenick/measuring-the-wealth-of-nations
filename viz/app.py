"""
RMWND Interactive Data Explorer
Plotly Dash application for Shaikh & Tonak (1994) replication data.
"""

import io
import json
from pathlib import Path

import dash
from dash import dcc, html, callback, Input, Output, State, ctx, no_update
import plotly.graph_objects as go
import pandas as pd

from data_loader import (
    load_config,
    build_catalog,
    load_chopped_csv,
    validate_data_availability,
    write_catalog_json,
)

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

CONFIG = load_config()
CATALOG = build_catalog(CONFIG)
TABS_CFG = CONFIG["tabs"]
PALETTE = CONFIG["color_palette"]
CHART = CONFIG["chart_defaults"]
SERIES_COLORS = PALETTE["series_colors"]

print("RMWND Dash — startup validation …")
avail = validate_data_availability(CONFIG)
print(f"  {len(avail['available'])} series available, "
      f"{len(avail['missing'])} missing, {len(avail['errors'])} errors")
write_catalog_json(CONFIG)
print("  Catalog written.")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _series_options(tab_id: str) -> list[dict]:
    """Dropdown options for a tab's series list."""
    sids = TABS_CFG.get(tab_id, {}).get("series_ids", [])
    opts = []
    for sid in sids:
        entry = CATALOG.get(sid)
        if entry and sid in avail["available"]:
            label = f"{sid}  —  {entry['name']}"
            opts.append({"label": label, "value": sid})
    return opts


def _year_bounds():
    return 1925, 2025


def _make_figure(series_ids: list[str], year_range: tuple[int, int]) -> go.Figure:
    """Build an overlaid line chart for the selected series."""
    fig = go.Figure()
    fig.update_layout(
        template=CHART["template"],
        height=CHART["height"],
        margin=CHART["margin"],
        font=dict(family=CHART["font_family"], size=CHART["font_size"]),
        paper_bgcolor=PALETTE["bg_card"],
        plot_bgcolor=PALETTE["bg_card"],
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0, font=dict(size=11),
        ),
        hovermode="x unified",
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.07)",
            title="Year",
            range=[year_range[0], year_range[1]],
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
    )
    if not series_ids:
        fig.add_annotation(
            text="Select one or more series to visualize",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False, font=dict(size=16, color=PALETTE["text_secondary"]),
        )
        return fig

    color_idx = 0
    units_set = set()
    for sid in series_ids:
        df = load_chopped_csv(sid)
        entry = CATALOG.get(sid, {})
        if df is None or df.empty:
            continue
        units_set.add(entry.get("units", ""))
        mask = (df.index >= year_range[0]) & (df.index <= year_range[1])
        df = df.loc[mask]
        for col in df.columns:
            series_data = df[col].dropna()
            if series_data.empty:
                continue
            color = SERIES_COLORS[color_idx % len(SERIES_COLORS)]
            color_idx += 1
            fig.add_trace(go.Scatter(
                x=series_data.index,
                y=series_data.values,
                mode="lines",
                name=col,
                line=dict(color=color, width=2),
                hovertemplate="%{y:.4g}<extra>%{fullData.name}</extra>",
            ))

    if len(units_set) == 1:
        fig.update_yaxes(title=units_set.pop())
    elif units_set:
        fig.update_yaxes(title=" / ".join(sorted(units_set)))

    return fig


def _methodology_text(series_ids: list[str]) -> str:
    """Assemble a methodology description from catalog entries."""
    if not series_ids:
        return "Select a series to see construction methodology."
    parts = []
    for sid in series_ids:
        entry = CATALOG.get(sid, {})
        lines = [f"### {sid} — {entry.get('name', '')}"]
        lines.append(f"**Units:** {entry.get('units', '—')}")
        lines.append(f"**Status:** {entry.get('status', '—')}")
        yr = entry.get("year_range")
        if yr:
            lines.append(f"**Year range:** {yr[0]}–{yr[1]}")
        tbl = entry.get("book_table", "")
        if tbl:
            lines.append(f"**Book table:** {tbl}")
        figs = entry.get("figures", [])
        if figs:
            lines.append(f"**Figures:** {', '.join(figs)}")
        for sub in entry.get("subseries", []):
            lines.append(
                f"- **{sub['id']}** ({sub.get('source', '')}) "
                f"[{sub.get('period', ['?','?'])[0]}–{sub.get('period', ['?','?'])[1]}] "
                f"*{sub.get('units', '')}*"
            )
        steps = entry.get("construction", [])
        if steps:
            lines.append("**Construction:**")
            for s in steps:
                op = s.get("op", "")
                formula = s.get("formula", "")
                desc = s.get("desc", "")
                detail = formula or desc or ""
                inputs = s.get("subseries", s.get("inputs", []))
                if inputs:
                    detail += f" ← {inputs}"
                lines.append(f"  {s.get('step', '?')}. `{op}` {detail}")
        parts.append("\n".join(lines))
    return "\n\n---\n\n".join(parts)


def _build_csv_download(series_ids: list[str], year_range: tuple[int, int]) -> str:
    """Merge selected series into a single CSV string."""
    frames = []
    for sid in series_ids:
        df = load_chopped_csv(sid)
        if df is not None:
            mask = (df.index >= year_range[0]) & (df.index <= year_range[1])
            frames.append(df.loc[mask])
    if not frames:
        return ""
    merged = pd.concat(frames, axis=1)
    merged.index.name = "Year"
    buf = io.StringIO()
    merged.to_csv(buf)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

app = dash.Dash(
    __name__,
    title=CONFIG["app_title"],
    update_title="Loading…",
    suppress_callback_exceptions=True,
)

SIDEBAR_STYLE = {
    "width": "340px",
    "minWidth": "300px",
    "backgroundColor": PALETTE["bg_secondary"],
    "padding": "20px",
    "overflowY": "auto",
    "borderRight": f"1px solid rgba(255,255,255,0.08)",
    "display": "flex",
    "flexDirection": "column",
    "gap": "14px",
}

MAIN_STYLE = {
    "flex": "1",
    "padding": "24px",
    "overflowY": "auto",
    "backgroundColor": PALETTE["bg_primary"],
}

tab_buttons = []
for tid, tcfg in TABS_CFG.items():
    tab_buttons.append(
        html.Button(
            tcfg["label"],
            id={"type": "tab-btn", "index": tid},
            n_clicks=0,
            className="tab-btn",
        )
    )

app.layout = html.Div(
    style={
        "display": "flex",
        "height": "100vh",
        "fontFamily": CHART["font_family"],
        "color": PALETTE["text_primary"],
        "backgroundColor": PALETTE["bg_primary"],
    },
    children=[
        # ---- Sidebar ----
        html.Div(
            style=SIDEBAR_STYLE,
            children=[
                html.H2(
                    "RMWND Explorer",
                    style={"margin": "0", "fontSize": "1.3rem", "fontWeight": "700"},
                ),
                html.P(
                    CONFIG["subtitle"],
                    style={"margin": "0", "fontSize": "0.78rem",
                           "color": PALETTE["text_secondary"]},
                ),
                html.Hr(style={"borderColor": "rgba(255,255,255,0.1)", "margin": "4px 0"}),

                # Tab buttons
                html.Div(
                    tab_buttons,
                    style={"display": "flex", "flexWrap": "wrap", "gap": "6px"},
                ),

                # Series selector
                html.Label("Series", style={"fontWeight": "600", "fontSize": "0.85rem"}),
                dcc.Dropdown(
                    id="series-dropdown",
                    multi=True,
                    placeholder="Pick series…",
                    style={"fontSize": "0.82rem"},
                    className="dash-dropdown",
                ),

                # Year range
                html.Label("Year range", style={"fontWeight": "600", "fontSize": "0.85rem"}),
                dcc.RangeSlider(
                    id="year-slider",
                    min=1925, max=2025, step=1,
                    value=[1929, 2025],
                    marks={y: str(y) for y in range(1930, 2030, 10)},
                    tooltip={"placement": "bottom", "always_visible": False},
                ),

                # Download
                html.Button(
                    "⬇  Download CSV",
                    id="download-btn",
                    n_clicks=0,
                    style={
                        "marginTop": "auto",
                        "padding": "8px 16px",
                        "border": "none",
                        "borderRadius": "6px",
                        "backgroundColor": PALETTE["accent"],
                        "color": "#fff",
                        "cursor": "pointer",
                        "fontWeight": "600",
                        "fontSize": "0.85rem",
                    },
                ),
                dcc.Download(id="csv-download"),

                # Validation summary
                html.Div(
                    id="validation-badge",
                    style={
                        "fontSize": "0.72rem",
                        "color": PALETTE["text_secondary"],
                        "textAlign": "center",
                    },
                    children=f"{len(avail['available'])} / {len(CATALOG)} series loaded",
                ),
            ],
        ),

        # ---- Main area ----
        html.Div(
            style=MAIN_STYLE,
            children=[
                # Hidden store for active tab
                dcc.Store(id="active-tab", data=CONFIG["default_tab"]),

                dcc.Graph(
                    id="main-chart",
                    config={
                        "displayModeBar": True,
                        "displaylogo": False,
                        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                    },
                    style={"marginBottom": "18px"},
                ),

                # Methodology panel
                html.Details(
                    open=False,
                    style={
                        "backgroundColor": PALETTE["bg_card"],
                        "borderRadius": "8px",
                        "padding": "14px 18px",
                    },
                    children=[
                        html.Summary(
                            "Methodology & Construction",
                            style={"cursor": "pointer", "fontWeight": "600",
                                   "fontSize": "0.95rem"},
                        ),
                        dcc.Markdown(
                            id="methodology-panel",
                            style={
                                "fontSize": "0.82rem",
                                "lineHeight": "1.55",
                                "color": PALETTE["text_secondary"],
                                "marginTop": "10px",
                            },
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Inline CSS for dropdown and tab styling (Dash doesn't support CSS files easily
# without assets folder, so we inject it)
app.index_string = '''<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
        * { box-sizing: border-box; }
        body { margin: 0; background: ''' + PALETTE["bg_primary"] + '''; }
        .tab-btn {
            padding: 6px 12px;
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 6px;
            background: transparent;
            color: ''' + PALETTE["text_secondary"] + ''';
            font-size: 0.78rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s;
        }
        .tab-btn:hover { background: rgba(99,110,250,0.15); color: #fff; }
        .tab-btn.active {
            background: ''' + PALETTE["accent"] + ''';
            color: #fff;
            border-color: ''' + PALETTE["accent"] + ''';
        }
        .Select-control, .Select-menu-outer {
            background: ''' + PALETTE["bg_card"] + ''' !important;
            color: ''' + PALETTE["text_primary"] + ''' !important;
        }
        .dash-dropdown .Select-value-label { color: ''' + PALETTE["text_primary"] + ''' !important; }
        .dash-dropdown .Select-placeholder { color: ''' + PALETTE["text_secondary"] + ''' !important; }
        /* Plotly dark overrides */
        .js-plotly-plot .plotly .modebar { background: transparent !important; }
        details summary::-webkit-details-marker { color: ''' + PALETTE["accent"] + '''; }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>'''


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@callback(
    Output("active-tab", "data"),
    [Input({"type": "tab-btn", "index": dash.ALL}, "n_clicks")],
    prevent_initial_call=True,
)
def switch_tab(n_clicks_list):
    triggered = ctx.triggered_id
    if triggered and isinstance(triggered, dict):
        return triggered["index"]
    return no_update


@callback(
    Output("series-dropdown", "options"),
    Output("series-dropdown", "value"),
    Input("active-tab", "data"),
)
def update_dropdown(tab_id):
    opts = _series_options(tab_id)
    default = [opts[0]["value"]] if opts else []
    return opts, default


@callback(
    Output("main-chart", "figure"),
    Output("methodology-panel", "children"),
    Input("series-dropdown", "value"),
    Input("year-slider", "value"),
)
def update_chart(selected_series, year_range):
    selected_series = selected_series or []
    yr = tuple(year_range) if year_range else (1929, 2025)
    fig = _make_figure(selected_series, yr)
    meth = _methodology_text(selected_series)
    return fig, meth


@callback(
    Output("csv-download", "data"),
    Input("download-btn", "n_clicks"),
    State("series-dropdown", "value"),
    State("year-slider", "value"),
    prevent_initial_call=True,
)
def download_csv(n_clicks, selected_series, year_range):
    if not selected_series:
        return no_update
    yr = tuple(year_range) if year_range else (1929, 2025)
    csv_str = _build_csv_download(selected_series, yr)
    if not csv_str:
        return no_update
    fname = f"rmwnd_{'_'.join(selected_series)}.csv"
    return dict(content=csv_str, filename=fname)


# Clientside callback to toggle active class on tab buttons
app.clientside_callback(
    """
    function(activeTab) {
        // Remove active from all, add to matching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            const id = JSON.parse(btn.id);
            if (id && id.index === activeTab) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        return window.dash_clientside.no_update;
    }
    """,
    Output("active-tab", "data", allow_duplicate=True),
    Input("active-tab", "data"),
    prevent_initial_call=True,
)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=CONFIG.get("debug", False),
        host=CONFIG.get("host", "127.0.0.1"),
        port=CONFIG.get("port", 8050),
    )
