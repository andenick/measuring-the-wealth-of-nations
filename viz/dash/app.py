"""
RMWND Dash — Interactive Data Explorer
Shaikh & Tonak (1994) — Measuring the Wealth of Nations Replication
Plotly Dash + dash-bootstrap-components with light/dark theme toggle.
Feature-parallel with the R Shiny app.
"""

import dash
from dash import Dash, html, dcc, callback, Input, Output, State, dash_table, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

from data_loader import (
    load_config, load_viz_style, build_catalog, get_tab_series,
    get_loaded_count, BASE_DIR, VIZ_DIR,
)
from chart_builder import build_series_chart, build_multi_series_chart
from validate_data import validate_app_data, print_validation_results
from logger import get_file_logger, log_structured

log = get_file_logger()

# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------
CONFIG = load_config()
STYLE = load_viz_style()
CATALOG = build_catalog(CONFIG)
TABS = CONFIG.get("tabs", {})
DEFAULT_TAB = CONFIG.get("default_tab", "ch5")
YEAR_RANGE = CONFIG.get("year_range", [1925, 2025])
DEFAULT_YEAR_RANGE = CONFIG.get("default_year_range", [1929, 2025])
LOADED_COUNT = get_loaded_count(CATALOG)
TOTAL_COUNT = len(CATALOG)

log.info("[RMWND Dash] Catalog: %d series, %d with data", TOTAL_COUNT, LOADED_COUNT)

# Resolve canonical paths for validation
_viz_dir = VIZ_DIR.resolve()
_registry_path = (_viz_dir / CONFIG["registry_path"]).resolve()
_subsource_path = _viz_dir / "data" / "catalogs" / "SUBSOURCE_METADATA.json"
_linkage_path = _viz_dir / "data" / "catalogs" / "SERIES_SOURCE_LINKAGE.json"
_catalog_path = _viz_dir / "data" / "catalogs" / "DEFINITIVE_SERIES_CATALOG.json"
_manifest_path = _viz_dir / "data" / "DATA_MANIFEST.json"

VALIDATION_PATHS = {
    "registry": str(_registry_path),
    "config": str((_viz_dir / "config" / "app_config.json").resolve()),
    "catalog": str(_catalog_path),
    "subsource_metadata": str(_subsource_path),
    "series_linkage": str(_linkage_path),
    "style": str((_viz_dir / "viz_style.json").resolve()),
    "manifest": str(_manifest_path),
}

_subsource_meta = None
if _subsource_path.exists():
    import json as _json
    with open(_subsource_path, encoding="utf-8") as _f:
        _subsource_meta = _json.load(_f)

from data_loader import load_registry
_raw_registry = load_registry(CONFIG)
VALIDATION_RESULTS = validate_app_data(
    VALIDATION_PATHS, _raw_registry, CATALOG, _subsource_meta,
)
print_validation_results(VALIDATION_RESULTS)
log_structured("startup_validation",
               gate=VALIDATION_RESULTS["gate"],
               errors=VALIDATION_RESULTS["error_count"],
               warnings=VALIDATION_RESULTS["warning_count"])

# ---------------------------------------------------------------------------
# App init
# ---------------------------------------------------------------------------
app = Dash(
    __name__,
    title=CONFIG.get("app_title", "RMWND Explorer"),
    update_title="Loading…",
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.FLATLY,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    ],
)


def make_tab_options():
    return [{"label": t.get("label", k), "value": k} for k, t in TABS.items()]


def make_series_options(tab_id):
    tab_cfg = TABS.get(tab_id, {})
    ids = tab_cfg.get("series_ids", [])
    opts = []
    for sid in ids:
        entry = CATALOG.get(sid)
        if entry:
            name = entry["name"]
            label = f"{sid}: {name[:40]}{'...' if len(name) > 40 else ''}"
            opts.append({"label": label, "value": sid})
    return opts


VIEW_MODES = [
    {"label": "All Sources", "value": "all_sources"},
    {"label": "Final Series", "value": "final_series"},
    {"label": "Author Construction", "value": "author_construction"},
    {"label": "Final Extension", "value": "final_extension"},
    {"label": "Select Individual", "value": "select_individual"},
    {"label": "Show Components", "value": "show_components"},
]

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
sidebar = html.Div(
    id="sidebar",
    children=[
        html.Div([
            html.H4([html.I(className="fas fa-chart-line me-2"), "RMWND Explorer"],
                     className="mb-1"),
            html.P("Shaikh & Tonak (1994)", className="text-muted small mb-0"),
        ], className="mb-3 pb-3", style={"borderBottom": "1px solid var(--border-color)"}),

        dbc.Label("Chapter Tab"),
        dcc.Dropdown(id="tab-selector", options=make_tab_options(),
                     value=DEFAULT_TAB, clearable=False, className="mb-3"),

        dbc.Label("Select Series"),
        dcc.Dropdown(id="series-selector", clearable=False, className="mb-3"),

        dbc.Label("Year Range"),
        dcc.RangeSlider(
            id="year-slider",
            min=YEAR_RANGE[0], max=YEAR_RANGE[1], step=1,
            value=DEFAULT_YEAR_RANGE,
            marks={y: str(y) for y in range(YEAR_RANGE[0], YEAR_RANGE[1] + 1, 10)},
            tooltip={"placement": "bottom", "always_visible": False},
            className="mb-3",
        ),

        dbc.Label("View Mode"),
        dbc.RadioItems(
            id="view-mode",
            options=VIEW_MODES,
            value="all_sources",
            className="mb-3",
        ),

        html.Div(id="subsource-selector-container"),

        dbc.Checkbox(id="dual-axis", label="Dual Y-Axis", value=False, className="mb-3"),

        html.Hr(),

        html.Div(id="sidebar-stats", className="small text-muted"),
    ],
)

main_content = html.Div([
    html.Div(id="series-header"),

    dbc.Card([
        dbc.CardBody([
            dcc.Graph(id="main-chart", config={"displayModeBar": True,
                                                 "displaylogo": False}),
        ])
    ], className="mb-3 chart-container"),

    dbc.Tabs(id="detail-tabs", active_tab="methodology", children=[
        dbc.Tab(label="Methodology", tab_id="methodology",
                children=[html.Div(id="methodology-panel", className="p-3")]),
        dbc.Tab(label="Quotes", tab_id="quotes",
                children=[html.Div(id="quotes-panel", className="p-3")]),
        dbc.Tab(label="Extension", tab_id="extension",
                children=[html.Div(id="extension-panel", className="p-3")]),
        dbc.Tab(label="Data", tab_id="data",
                children=[html.Div(id="data-panel", className="p-3")]),
        dbc.Tab(label="Series Browser", tab_id="browser",
                children=[html.Div(id="browser-panel", className="p-3")]),
    ]),
])

app.layout = html.Div([
    dcc.Store(id="theme-store", data="light"),

    # Top nav bar
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand([
                html.I(className="fas fa-book-open me-2"),
                "RMWND — Measuring the Wealth of Nations",
            ]),
            dbc.Button(
                html.I(id="theme-icon", className="fas fa-moon"),
                id="theme-toggle", color="link",
                className="text-white ms-auto",
            ),
        ], fluid=True),
        color="#543c8a", dark=True, className="mb-0",
    ),

    # Body: sidebar + main
    dbc.Container([
        dbc.Row([
            dbc.Col(sidebar, width=3, className="sidebar-col"),
            dbc.Col(main_content, width=9),
        ])
    ], fluid=True, className="mt-3"),
])

# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

# Theme toggle + restore on load
app.clientside_callback(
    """
    function(n_clicks, current_theme) {
        // On initial load (no clicks), restore from localStorage
        if (!n_clicks || n_clicks === 0) {
            var saved = localStorage.getItem("rmwnd-theme");
            if (saved === "dark") {
                document.body.classList.add("dark-mode");
                return ["dark", "fas fa-sun"];
            }
            return ["light", "fas fa-moon"];
        }
        // On click, toggle
        var next = current_theme === "light" ? "dark" : "light";
        document.body.classList.toggle("dark-mode", next === "dark");
        localStorage.setItem("rmwnd-theme", next);
        return [next, next === "dark" ? "fas fa-sun" : "fas fa-moon"];
    }
    """,
    [Output("theme-store", "data"), Output("theme-icon", "className")],
    Input("theme-toggle", "n_clicks"),
    State("theme-store", "data"),
)


@callback(
    Output("series-selector", "options"),
    Output("series-selector", "value"),
    Input("tab-selector", "value"),
)
def update_series_options(tab_id):
    opts = make_series_options(tab_id)
    val = opts[0]["value"] if opts else None
    return opts, val


@callback(
    Output("subsource-selector-container", "children"),
    Input("view-mode", "value"),
    Input("series-selector", "value"),
)
def update_subsource_selector(view_mode, series_id):
    if view_mode != "select_individual" or not series_id:
        return []
    entry = CATALOG.get(series_id)
    if not entry or entry.get("data") is None:
        return []
    df = entry["data"]
    numeric_cols = [c for c in df.columns if c != "year" and df[c].dtype in ("float64", "int64")]
    if not numeric_cols:
        return []
    return [
        dbc.Label("Select Subsources"),
        dcc.Dropdown(
            id="subsource-selector",
            options=[{"label": c, "value": c} for c in numeric_cols],
            value=[numeric_cols[0]],
            multi=True, className="mb-3",
        ),
    ]


@callback(
    Output("sidebar-stats", "children"),
    Input("tab-selector", "value"),
)
def update_sidebar_stats(tab_id):
    tab_cfg = TABS.get(tab_id, {})
    tab_count = len(tab_cfg.get("series_ids", []))
    color = "var(--success)" if LOADED_COUNT >= 60 else "var(--warning)"
    return [
        html.Div(f"{LOADED_COUNT} / {TOTAL_COUNT} series loaded",
                 style={"fontWeight": "600", "color": color}),
        html.P(f"Tab series: {tab_count}", className="mb-0 mt-1"),
    ]


@callback(
    Output("series-header", "children"),
    Input("series-selector", "value"),
    Input("tab-selector", "value"),
)
def update_header(series_id, tab_id):
    if not series_id:
        return html.Div("Select a series", className="figure-header")
    entry = CATALOG.get(series_id, {})
    name = entry.get("name", series_id)
    status = entry.get("extension_status", "conceptual")
    chapter = entry.get("chapter", "?")
    start = entry.get("time_period_start")
    end = entry.get("time_period_end")
    period_str = f"{start} – {end}" if start and end else ""

    badge_colors = {
        "extended_2025": "success", "calculated": "warning",
        "conceptual": "secondary", "partial": "info",
        "needs_source": "danger", "verified": "success",
    }

    return html.Div(className="figure-header", children=[
        html.Div(f"Chapter {chapter} · {tab_id}", className="figure-chapter"),
        html.H3([
            f"{series_id}: {name} ",
            dbc.Badge(status, color=badge_colors.get(status, "secondary"),
                      className="ms-2"),
        ], className="figure-title"),
        html.Div([
            html.I(className="fas fa-calendar-alt me-1") if period_str else None,
            period_str,
        ], className="text-muted small") if period_str else None,
    ])


@callback(
    Output("main-chart", "figure"),
    Input("series-selector", "value"),
    Input("view-mode", "value"),
    Input("year-slider", "value"),
    Input("dual-axis", "value"),
    Input("theme-store", "data"),
    State("subsource-selector-container", "children"),
)
def update_chart(series_id, view_mode, year_range, dual_axis, theme, sub_container):
    if not series_id:
        return go.Figure().update_layout(title="Select a series")
    entry = CATALOG.get(series_id)
    if not entry:
        return go.Figure().update_layout(title=f"Series {series_id} not found")

    dark = theme == "dark"

    selected_subs = None
    if view_mode == "select_individual" and sub_container:
        for child in (sub_container or []):
            if isinstance(child, dict) and child.get("props", {}).get("id") == "subsource-selector":
                selected_subs = child["props"].get("value")

    try:
        fig = build_series_chart(
            entry, view_mode, tuple(year_range),
            selected_subsources=selected_subs,
            dual_axis=dual_axis, dark=dark,
        )
        return fig
    except Exception as e:
        import traceback
        traceback.print_exc()
        fig = go.Figure()
        fig.update_layout(title=dict(text=f"Chart Error: {e}", font=dict(size=12)))
        return fig


@callback(
    Output("methodology-panel", "children"),
    Input("series-selector", "value"),
)
def update_methodology(series_id):
    if not series_id:
        return html.P("Select a series")
    entry = CATALOG.get(series_id, {})

    items = [
        _info_row("Series ID", entry.get("series_id", "?")),
        _info_row("Units", entry.get("units", "")),
        _info_row("Time Period", f"{entry.get('time_period_start', '?')} – {entry.get('time_period_end', '?')}"),
        _info_row("Extension Status", entry.get("extension_status", "?")),
        _info_row("Subsources", str(entry.get("subsource_count", 0))),
    ]

    formula = entry.get("construction_formula", "")
    if formula:
        items.append(_section("Construction Formula", "warning"))
        items.append(html.Div(formula, className="formula-box"))

    note = entry.get("methodology_note", "")
    if note:
        items.append(_section("Methodology Note", "warning"))
        items.append(html.Div(note, className="info-panel"))

    disclosure = entry.get("viz_disclosure", "")
    if disclosure:
        items.append(_section("Disclosure", "danger"))
        items.append(html.Div(disclosure, className="info-panel"))

    apis = entry.get("api_sources", [])
    if apis:
        items.append(_section("API Sources", "info"))
        items.append(html.Ul([html.Li(a, style={"color": "var(--accent)"}) for a in apis]))

    subsources = entry.get("subsources", {})
    if subsources:
        items.append(_section("Subsource Details", "warning"))
        for ss_id, ss in subsources.items():
            if isinstance(ss, dict):
                items.append(html.Div(className="subsource-card", children=[
                    html.Strong(f"{ss_id}: {ss.get('source_name', 'Unknown')}",
                                style={"color": "var(--highlight)"}),
                    html.Div([
                        html.Span(f"Period: {ss.get('time_period_start', '?')}-{ss.get('time_period_end', '?')}",
                                  className="me-3", style={"color": "var(--accent)"}),
                        html.Span(f"API: {ss.get('api', '')}", style={"color": "var(--success)"})
                        if ss.get("api") else None,
                    ], className="small mt-1"),
                ]))

    return items


@callback(
    Output("quotes-panel", "children"),
    Input("series-selector", "value"),
)
def update_quotes(series_id):
    if not series_id:
        return html.P("Select a series")
    entry = CATALOG.get(series_id, {})
    quote = entry.get("shaikh_quote", "")
    page = entry.get("shaikh_quote_page", "")

    if quote and len(quote) > 5 and quote != "N/A - See related figures":
        return html.Div(className="book-quote", children=[
            html.Div(f'"{quote}"',
                     style={"fontStyle": "italic", "color": "var(--text-primary)", "lineHeight": "1.6"}),
            html.Div(f"— Shaikh & Tonak (1994), p. {page}",
                     className="text-muted small mt-2") if page else None,
        ])
    return html.P("No quote available for this series.", className="text-muted")


@callback(
    Output("extension-panel", "children"),
    Input("series-selector", "value"),
)
def update_extension(series_id):
    if not series_id:
        return html.P("Select a series")
    entry = CATALOG.get(series_id, {})
    status = entry.get("extension_status", "conceptual")

    badge_colors = {
        "extended_2025": "success", "calculated": "warning",
        "conceptual": "secondary",
    }

    items = [
        _section("Extension Status", "info"),
        html.Div(className="info-panel", children=[
            html.Div([
                html.Span("Status", className="info-label me-3"),
                dbc.Badge(status, color=badge_colors.get(status, "secondary")),
            ], className="d-flex justify-content-between align-items-center"),
            html.Div(
                html.P([html.I(className="fas fa-check-circle me-1"), " Extended through 2025"],
                       style={"color": "var(--success)"})
                if status == "extended_2025"
                else html.P("Extension methodology pending review", className="text-muted"),
                className="mt-2",
            ),
        ]),
    ]

    apis = entry.get("api_sources", [])
    if apis:
        items.append(_section("Extension API Sources", "info"))
        items.append(html.Ul([html.Li(a, style={"color": "var(--accent)"}) for a in apis]))

    return items


@callback(
    Output("data-panel", "children"),
    Input("series-selector", "value"),
    Input("year-slider", "value"),
)
def update_data_table(series_id, year_range):
    if not series_id:
        return html.P("Select a series")
    entry = CATALOG.get(series_id, {})
    df = entry.get("data")
    if df is None or df.empty:
        return html.P("No data available", className="text-muted")

    df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])].copy()
    numeric_cols = [c for c in df.columns if c != "year" and df[c].dtype in ("float64", "int64")]
    for c in numeric_cols:
        df[c] = df[c].round(4)

    return [
        dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": c, "id": c} for c in df.columns],
            page_size=20,
            sort_action="native",
            filter_action="native",
            export_format="csv",
            style_table={"overflowX": "auto"},
            style_header={
                "backgroundColor": "var(--bg-panel)",
                "color": "var(--text-primary)",
                "fontWeight": "bold",
            },
            style_cell={
                "backgroundColor": "var(--bg-primary)",
                "color": "var(--text-primary)",
                "border": "1px solid var(--border-color)",
                "fontFamily": "Inter, system-ui, sans-serif",
                "fontSize": "13px",
            },
        ),
    ]


@callback(
    Output("browser-panel", "children"),
    Input("tab-selector", "value"),
)
def update_browser(tab_id):
    tab_cfg = TABS.get(tab_id, {})
    tab_label = tab_cfg.get("label", tab_id)
    entries = get_tab_series(CATALOG, tab_cfg)

    cards = []
    for entry in entries:
        sid = entry["series_id"]
        status = entry.get("extension_status", "conceptual")
        badge_colors = {
            "extended_2025": "success", "calculated": "warning", "conceptual": "secondary",
        }
        has_data = entry.get("has_data", False)

        cards.append(html.Div(className="series-card", children=[
            html.Div(className="d-flex justify-content-between align-items-center", children=[
                html.Div([
                    html.Strong(sid, style={"color": "var(--accent)", "fontSize": "1.1em"}),
                    html.Span(f" {entry.get('name', '')}", className="text-secondary ms-2"),
                ]),
                dbc.Badge(status, color=badge_colors.get(status, "secondary")),
            ]),
            html.Div([
                html.Span(f"Subsources: {entry.get('subsource_count', 0)}", className="text-muted small me-3"),
                html.Span([html.I(className="fas fa-check me-1"), "Data loaded"],
                          className="small", style={"color": "var(--success)"})
                if has_data else
                html.Span([html.I(className="fas fa-times me-1"), "No data"],
                          className="small", style={"color": "var(--danger)"}),
            ], className="mt-1"),
        ]))

    extended_count = sum(1 for e in CATALOG.values() if e.get("extension_status") == "extended_2025")

    return [
        _section(f"Series — {tab_label}", "primary"),
        html.P(f"Showing {len(entries)} series in tab. Total catalog: {TOTAL_COUNT}",
               className="text-muted small"),
        html.Div(cards, style={"maxHeight": "500px", "overflowY": "auto"}),
        _section("Catalog Statistics", "info"),
        html.Div(className="info-panel d-flex gap-4 flex-wrap", children=[
            _stat_box("Total Series", TOTAL_COUNT, "var(--accent)"),
            _stat_box("With Data", LOADED_COUNT, "var(--success)"),
            _stat_box("Extended", extended_count, "var(--info)"),
        ]),
    ]


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------
def _section(title, color_type="info"):
    colors = {"success": "#28a745", "warning": "#ffc107", "info": "#543c8a",
              "danger": "#dc3545", "primary": "#543c8a"}
    c = colors.get(color_type, "#543c8a")
    return html.Div(title, style={
        "borderLeft": f"4px solid {c}", "padding": "8px 12px",
        "margin": "15px 0 10px 0", "fontWeight": "bold",
        "color": "var(--text-primary)", "fontSize": "14px",
    })


def _info_row(label, value):
    return html.Div(className="methodology-item", children=[
        html.Span(label, className="info-label"),
        html.Div(str(value), className="info-value"),
    ])


def _stat_box(label, value, color):
    return html.Div([
        html.Div(label, className="text-muted small"),
        html.Div(str(value), style={"color": color, "fontSize": "1.5em", "fontWeight": "bold"}),
    ])


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(
        host=CONFIG.get("host", "127.0.0.1"),
        port=CONFIG.get("port_dash", 8050),
        debug=CONFIG.get("debug", False),
    )
