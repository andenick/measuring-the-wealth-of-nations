"""
RMWND Dash — Chart Builder
Plotly chart construction with view modes, recession bands, splice markers,
and dual-axis support. Feature-parallel with the R Shiny chart_builder.R.
"""

import plotly.graph_objects as go

RECESSIONS_NBER = [
    (1948, 1949), (1953, 1954), (1957, 1958), (1960, 1961),
    (1969, 1970), (1973, 1975), (1980, 1980), (1981, 1982),
    (1990, 1991), (2001, 2001), (2007, 2009), (2020, 2020),
]

SPLICE_YEAR = 1989

SERIES_COLORS = [
    "#ffcc00", "#00ccff", "#ff7f0e", "#2ca02c",
    "#d62728", "#9467bd", "#e377c2", "#8c564b",
    "#17becf", "#bcbd22", "#7f7f7f", "#1f77b4",
    "#98df8a", "#ff9896", "#c5b0d5", "#ffbb78",
]

FONT_FAMILY = "Inter, system-ui, -apple-system, sans-serif"


def get_chart_theme(dark: bool = False) -> dict:
    if dark:
        return {
            "paper_bgcolor": "#16213e",
            "plot_bgcolor": "#16213e",
            "font_color": "#e8e8e8",
            "grid_color": "#333333",
            "zeroline_color": "#555555",
            "legend_bgcolor": "rgba(22,33,62,0.85)",
        }
    return {
        "paper_bgcolor": "#ffffff",
        "plot_bgcolor": "#ffffff",
        "font_color": "#333333",
        "grid_color": "#e8e8e8",
        "zeroline_color": "#cccccc",
        "legend_bgcolor": "rgba(255,255,255,0.85)",
    }


def apply_layout(fig: go.Figure, title: str, y_label: str,
                 subtitle: str = None, dark: bool = False) -> go.Figure:
    theme = get_chart_theme(dark)
    title_text = f"{title}<br><sup>{subtitle}</sup>" if subtitle else title

    fig.update_layout(
        title=dict(text=title_text, font=dict(size=14, color=theme["font_color"])),
        xaxis=dict(
            title=dict(text="Year", font=dict(color=theme["font_color"])),
            dtick=5, gridcolor=theme["grid_color"],
            zerolinecolor=theme["zeroline_color"],
            tickfont=dict(color=theme["font_color"]),
        ),
        yaxis=dict(
            title=dict(text=y_label, font=dict(color=theme["font_color"])),
            gridcolor=theme["grid_color"],
            zerolinecolor=theme["zeroline_color"],
            tickfont=dict(color=theme["font_color"]),
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.18,
            xanchor="center", x=0.5,
            bgcolor=theme["legend_bgcolor"],
            font=dict(color=theme["font_color"]),
        ),
        plot_bgcolor=theme["plot_bgcolor"],
        paper_bgcolor=theme["paper_bgcolor"],
        margin=dict(l=70, r=50, t=60, b=80),
        font=dict(family=FONT_FAMILY, color=theme["font_color"]),
        height=480,
    )
    return fig


def add_recession_bands(fig: go.Figure, year_range: tuple) -> go.Figure:
    shapes = []
    for start, end in RECESSIONS_NBER:
        if end < year_range[0] or start > year_range[1]:
            continue
        shapes.append(dict(
            type="rect", fillcolor="rgba(200,200,200,0.2)",
            line=dict(width=0),
            x0=start, x1=end, y0=0, y1=1, yref="paper", layer="below",
        ))
    if shapes:
        fig.update_layout(shapes=shapes)
    return fig


def add_splice_marker(fig: go.Figure, splice_year: int = SPLICE_YEAR) -> go.Figure:
    fig.add_shape(
        type="line", x0=splice_year, x1=splice_year,
        y0=0, y1=1, yref="paper",
        line=dict(color="#605ca8", dash="dash", width=1.5),
    )
    fig.add_annotation(
        x=splice_year, y=1, yref="paper",
        text="Book | Extension", showarrow=False,
        font=dict(size=9, color="#605ca8"), yanchor="bottom",
    )
    return fig


def build_series_chart(entry: dict, view_mode: str, year_range: tuple,
                       selected_subsources: list = None,
                       dual_axis: bool = False,
                       dark: bool = False) -> go.Figure:
    sid = entry["series_id"]
    name = entry.get("name", sid)
    df = entry.get("data")

    if df is None or df.empty:
        fig = go.Figure()
        fig.update_layout(title=f"No data for {sid}")
        return fig

    df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])].copy()
    if df.empty:
        fig = go.Figure()
        fig.update_layout(title=f"No data in range for {sid}")
        return fig

    numeric_cols = [c for c in df.columns if c != "year" and df[c].dtype in ("float64", "int64")]
    if not numeric_cols:
        fig = go.Figure()
        fig.update_layout(title=f"No numeric columns for {sid}")
        return fig

    fig = go.Figure()

    if view_mode == "final_series":
        col = sid if sid in numeric_cols else numeric_cols[0]
        fig.add_trace(go.Scatter(
            x=df["year"], y=df[col], mode="lines+markers",
            name=name, line=dict(color="#543c8a", width=2),
            marker=dict(size=4),
        ))

    elif view_mode == "author_construction":
        book = df[df["year"] <= SPLICE_YEAR]
        if not book.empty:
            col = sid if sid in numeric_cols else numeric_cols[0]
            fig.add_trace(go.Scatter(
                x=book["year"], y=book[col], mode="lines+markers",
                name=f"{name} (Book)", line=dict(color="#3c8dbc", width=2),
                marker=dict(size=4),
            ))

    elif view_mode == "final_extension":
        ext = df[df["year"] >= SPLICE_YEAR]
        if not ext.empty:
            col = sid if sid in numeric_cols else numeric_cols[0]
            fig.add_trace(go.Scatter(
                x=ext["year"], y=ext[col], mode="lines+markers",
                name=f"{name} (Extension)",
                line=dict(color="#f39c12", width=2, dash="dot"),
                marker=dict(size=3),
            ))

    elif view_mode == "select_individual" and selected_subsources:
        cols = [c for c in selected_subsources if c in numeric_cols]
        for i, col in enumerate(cols):
            color = SERIES_COLORS[i % len(SERIES_COLORS)]
            fig.add_trace(go.Scatter(
                x=df["year"], y=df[col], mode="lines",
                name=col, line=dict(color=color, width=2),
            ))

    else:
        # all_sources / show_components
        for i, col in enumerate(numeric_cols):
            color = SERIES_COLORS[i % len(SERIES_COLORS)]
            yaxis = "y"
            if dual_axis and i > 0:
                yaxis = "y2"
            fig.add_trace(go.Scatter(
                x=df["year"], y=df[col], mode="lines",
                name=col, line=dict(color=color, width=2),
                yaxis=yaxis,
            ))

    units_label = entry.get("units", "Value") or "Value"
    subtitle = f"{sid} \u00b7 {name}"
    fig = apply_layout(fig, name, units_label, subtitle=subtitle, dark=dark)

    if dual_axis:
        theme = get_chart_theme(dark)
        fig.update_layout(yaxis2=dict(
            title="Secondary Axis", overlaying="y", side="right",
            gridcolor=theme["grid_color"],
            tickfont=dict(color=theme["font_color"]),
        ))

    fig = add_recession_bands(fig, year_range)

    has_book = any(df["year"] <= SPLICE_YEAR)
    has_ext = any(df["year"] > SPLICE_YEAR)
    if has_book and has_ext and view_mode in ("all_sources", "final_series"):
        fig = add_splice_marker(fig)

    return fig


def build_multi_series_chart(entries: list, year_range: tuple,
                             dark: bool = False) -> go.Figure:
    fig = go.Figure()
    for i, entry in enumerate(entries):
        df = entry.get("data")
        if df is None or df.empty:
            continue
        df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
        if df.empty:
            continue
        sid = entry["series_id"]
        numeric_cols = [c for c in df.columns if c != "year" and df[c].dtype in ("float64", "int64")]
        col = sid if sid in numeric_cols else (numeric_cols[0] if numeric_cols else None)
        if col is None:
            continue
        color = SERIES_COLORS[i % len(SERIES_COLORS)]
        fig.add_trace(go.Scatter(
            x=df["year"], y=df[col], mode="lines",
            name=entry.get("name", sid), line=dict(color=color, width=1.5),
        ))

    fig = apply_layout(fig, "Multi-Series Overlay", "Value", dark=dark)
    fig = add_recession_bands(fig, year_range)
    return fig
