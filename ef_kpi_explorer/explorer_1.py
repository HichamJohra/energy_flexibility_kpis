"""
Single-file Dash app to visualize a knowledge graph for methods in
`energy_flexibility_kpis.module_test_1`.

How it works
- Inspects the module for classes and classmethods named `calculate`.
- For each `calculate` method it extracts parameter names and types (from
  the signature) and the return annotation.
- Builds a directed graph where input parameters point to the method node,
  and the method node points to an output node (inferred from the return
  annotation). If the module exposes a `method_data_registry` and it
  contains recorded runtime outputs, these will be shown as additional
  information on the output node.

Run
$ python dash_kpi_knowledge_graph.py
Then open http://127.0.0.1:8050 in your browser.

Notes
- This script expects your package `energy_flexibility_kpis` to be importable
  (i.e. your project root on PYTHONPATH or installed in editable mode).
- Dependencies: dash, dash-cytoscape, networkx
  Install with: pip install dash dash-cytoscape networkx

"""

import inspect
import typing
from typing import get_type_hints
import importlib
import sys
import traceback

import networkx as nx

import dash
from dash import html, dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State


MODULE_NAME = "energy_flexibility_kpis.module_test_1"


def safe_import_module(name: str):
    try:
        mod = importlib.import_module(name)
        return mod, None
    except Exception as e:
        return None, traceback.format_exc()


STYLE = [
    {
        "selector": "node",
        "style": {
            "label": "data(label)",
            "text-valign": "center",
            "text-halign": "center",
            "width": "label",
            "height": "label",
            "padding": "8px",
            "background-color": "#BFD7B5",
            "border-width": 1,
            "border-color": "#6B8E23",
        },
    },
    {
        "selector": ".method",
        "style": {"background-color": "#FFCC5C", "shape": "round-rectangle"},
    },
    {"selector": ".input", "style": {"background-color": "#88C0D0"}},
    {"selector": ".output", "style": {"background-color": "#D87E7E"}},
    {"selector": "edge", "style": {"target-arrow-shape": "triangle", "curve-style": "bezier"}},
]


def annotation_to_str(ann):
    if ann is inspect._empty:
        return "Any"
    try:
        # for typing hints like List[float], etc.
        return str(ann).replace("typing.", "")
    except Exception:
        return getattr(ann, "__name__", str(ann))


def build_graph_from_module(mod):
    G = nx.DiGraph()
    # try to get registry if present
    method_data_registry = getattr(mod, "method_data_registry", {})

    for name, obj in inspect.getmembers(mod, inspect.isclass):
        # only consider classes defined in this module
        if obj.__module__ != mod.__name__:
            continue
        # look for classmethods named 'calculate' (or other callables)
        for attr_name, attr in inspect.getmembers(obj):
            if attr_name != "calculate":
                continue
            # attr might be function or function descriptor; resolve
            try:
                func = getattr(obj, attr_name)
            except Exception:
                func = attr

            sig = inspect.signature(func)
            params = [p for p in sig.parameters.values()]
            return_ann = sig.return_annotation

            method_node_id = f"{obj.__name__}.{attr_name}"
            G.add_node(method_node_id, label=method_node_id, type="method")

            # add parameter nodes (skip 'cls' or 'self')
            for p in params:
                if p.name in ("cls", "self"):
                    continue
                pid = f"{method_node_id}.param.{p.name}"
                ann = None
                if p.annotation is not inspect._empty:
                    ann = p.annotation
                G.add_node(pid, label=f"{p.name}: {annotation_to_str(p.annotation)}", type="input")
                G.add_edge(pid, method_node_id)

            # output node
            out_id = f"{method_node_id}.output"
            out_label = f"return: {annotation_to_str(return_ann)}"

            # if runtime output exists in registry, show summary
            reg_key = f"{obj.__name__}.{attr_name}"
            runtime_info = method_data_registry.get(reg_key)
            if runtime_info is not None:
                rt_out = runtime_info.get("output")
                try:
                    # small summary
                    out_summary = str(type(rt_out).__name__)
                    out_label += f"\n(runtime: {out_summary})"
                except Exception:
                    pass

            G.add_node(out_id, label=out_label, type="output")
            G.add_edge(method_node_id, out_id)

    return G


def nx_to_cytoscape_elements(G: nx.DiGraph):
    elements = []

    for n, data in G.nodes(data=True):
        node_type = data.get("type", "node")
        elem = {
            "data": {"id": n, "label": data.get("label", n)},
            "classes": node_type,
        }
        elements.append(elem)

    for u, v, data in G.edges(data=True):
        elements.append({"data": {"source": u, "target": v}})

    return elements


# Build app
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H3("KPI Module Knowledge Graph"),
        html.Div(id="status", style={"whiteSpace": "pre-wrap", "fontFamily": "monospace"}),
        html.Div(
            [
                cyto.Cytoscape(
                    id="cytoscape",
                    elements=[],
                    style={"width": "100%", "height": "600px"},
                    layout={"name": "breadthfirst"},
                    stylesheet=STYLE,
                )
            ]
        ),
        html.Div(
            [
                html.Button("Reload Module & Build Graph", id="reload", n_clicks=0),
                html.Span(" "),
                html.Button("Center Graph", id="center", n_clicks=0),
            ],
            style={"marginTop": "8px"},
        ),
        dcc.Store(id="last-elements"),
    ],
    style={"width": "95%", "margin": "auto"},
)


@app.callback(
    Output("status", "children"),
    Output("cytoscape", "elements"),
    Input("reload", "n_clicks"),
)
def reload_graph(n_clicks):
    mod, err = safe_import_module(MODULE_NAME)
    if err:
        status = f"Failed to import {MODULE_NAME}:\n{err}"
        return status, []

    G = build_graph_from_module(mod)
    elements = nx_to_cytoscape_elements(G)
    status = f"Module {MODULE_NAME} imported successfully.\nFound {len(G.nodes())} nodes and {len(G.edges())} edges.\nClick nodes to inspect labels."
    return status, elements


@app.callback(
    Output("cytoscape", "layout"),
    Input("center", "n_clicks"),
    State("cytoscape", "elements"),
)
def center_graph(n, elements):
    # toggling to a different layout to re-center
    return {"name": "cose"}


if __name__ == "__main__":
    app.run(debug=True)
