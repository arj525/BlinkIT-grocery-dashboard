# import pandas as pd
# import plotly.express as px
# import dash
# from dash import html, dcc, Input, Output
# import dash_bootstrap_components as dbc

# # Load and clean the data
# df = pd.read_excel("BlinkIT Grocery Data Excel.xlsx")
# df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
# df = df.rename(columns={
#     'sales': 'total_sales',
#     'rating': 'avg_ratings',
#     'item_visibility': 'item_visibility',
#     'item_type': 'item_type',
#     'outlet_size': 'outlet_size',
#     'outlet_location_type': 'outlet_location',
#     'outlet_type': 'outlet_type',
#     'outlet_establishment_year': 'year_established',
#     'item_fat_content': 'fat_content'
# })

# # Add derived columns
# df['avg_sales'] = df['total_sales']
# df['no_of_items'] = 1

# # Initialize the app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# # Helper to create KPI card
# def generate_kpi_card(title, value, color="#ffc107"):
#     return dbc.Card([
#         dbc.CardBody([
#             html.H5(title, className="card-title text-muted"),
#             html.H3(value, className="card-text")
#         ])
#     ], className="m-2 text-center shadow-sm rounded", style={
#         "backgroundColor": "#f9f9f9", "borderLeft": f"6px solid {color}"
#     })


# # Layout structure
# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             html.Div([
#                 html.H2("blink it", style={"color": "#84C225", "fontWeight": "bold", "fontSize": "40px"}),
#                 html.H6("India's Last Minute App", className="mb-4 text-muted"),

#                 html.Label("Outlet Location Type"),
#                 dcc.Dropdown(['All'] + sorted(df['outlet_location'].unique()), 'All', id='location-filter'),

#                 html.Label("Outlet Size", className="mt-3"),
#                 dcc.Dropdown(['All'] + sorted(df['outlet_size'].unique()), 'All', id='size-filter'),

#                 html.Label("Outlet Type", className="mt-3"),
#                 dcc.Dropdown(['All'] + sorted(df['outlet_type'].unique()), 'All', id='type-filter'),

#                 html.Button("Reset", id='reset-button', style={'marginTop': '20px'})
#             ], style={"backgroundColor": "#ffeb3b", "padding": "20px", "borderRadius": "10px", "height": "100vh"})
#         ], width=2),

#         dbc.Col([
#             # KPI Cards
#             dbc.Row([
#                 dbc.Col(generate_kpi_card("Total Sales", f"${df['total_sales'].sum() / 1e6:.2f}M"), width=3),
#                 dbc.Col(generate_kpi_card("Avg Sales", f"${df['avg_sales'].mean():.0f}"), width=3),
#                 dbc.Col(generate_kpi_card("No. of Items", f"{df['no_of_items'].sum()}"), width=3),
#                 dbc.Col(generate_kpi_card("Avg Ratings", f"{df['avg_ratings'].mean():.1f}"), width=3),
#             ], className="mb-4"),

#             # Tabs for dynamic bar chart
#             dbc.Row([
#                 dcc.Tabs(id="tabs", value='avg_sales', children=[
#                     dcc.Tab(label='Avg Sales', value='avg_sales'),
#                     dcc.Tab(label='Avg Ratings', value='avg_ratings'),
#                     dcc.Tab(label='No. of Items', value='no_of_items'),
#                     dcc.Tab(label='Total Sales', value='total_sales'),
#                 ]),
#                 dcc.Graph(id='bar-chart'),
#             ]),
            
            

#             # Charts Section
#             dbc.Row([
#                 dbc.Col(dcc.Graph(id='fat-pie'), width=6),
#                 dbc.Col(dcc.Graph(id='size-pie'), width=6),
#             ]),

#             dbc.Row([
#                 dbc.Col(dcc.Graph(id='sales-by-item'), width=6),
#                 dbc.Col(dcc.Graph(id='establishment-trend'), width=6),
#             ]),

#             dbc.Row([
#                 dbc.Col(dcc.Graph(id='location-bar'), width=6),
#                 dbc.Col(dcc.Graph(id='outlet-type-table'), width=6),
#             ])
#         ], width=10)
#     ])
# ], fluid=True)

# # Callback to update all charts
# @app.callback(
#     [Output('fat-pie', 'figure'),
#      Output('size-pie', 'figure'),
#      Output('sales-by-item', 'figure'),
#      Output('establishment-trend', 'figure'),
#      Output('location-bar', 'figure'),
#      Output('outlet-type-table', 'figure'),
#      Output('bar-chart', 'figure')],
#     [Input('location-filter', 'value'),
#      Input('size-filter', 'value'),
#      Input('type-filter', 'value'),
#      Input('tabs', 'value')]
# )
# def update_charts(location, size, otype, tab):
#     dff = df.copy()
#     if location != 'All':
#         dff = dff[dff['outlet_location'] == location]
#     if size != 'All':
#         dff = dff[dff['outlet_size'] == size]
#     if otype != 'All':
#         dff = dff[dff['outlet_type'] == otype]

#     # Pie Charts
#     fat_fig = px.pie(dff, values='total_sales', names='fat_content', hole=0.4, title="Fat Content")
#     size_fig = px.pie(dff, values='total_sales', names='outlet_size', hole=0.4, title="Outlet Size")

#     # Bar Charts
#     item_fig = px.bar(dff.groupby('item_type')['total_sales'].sum().nlargest(10).reset_index(),
#                       x='total_sales', y='item_type', orientation='h', title="Top Item Types")

#     est_fig = px.line(dff.groupby('year_established')['total_sales'].sum().reset_index(),
#                       x='year_established', y='total_sales', title="Outlet Establishment Trend")

#     loc_fig = px.bar(dff.groupby('outlet_location')['total_sales'].sum().reset_index(),
#                      x='outlet_location', y='total_sales', title="Sales by Location")

#     outlet_summary = dff.groupby('outlet_type').agg({
#         'total_sales': 'sum',
#         'no_of_items': 'sum',
#         'avg_sales': 'mean',
#         'avg_ratings': 'mean',
#         'item_visibility': 'mean'
#     }).reset_index()

#     outlet_fig = px.bar(outlet_summary, x='total_sales', y='outlet_type', orientation='h',
#                         color='avg_ratings', title="Outlet Type Performance")

#     # Tab-based Bar Chart
#     y_col = tab if tab in dff.columns else 'total_sales'
#     color = '#e53935' if tab in ['avg_sales', 'avg_ratings', 'no_of_items'] else '#90caf9'
#     bar_fig = px.bar(dff, x='outlet_type', y=y_col, color_discrete_sequence=[color], title=f"{tab.replace('_', ' ').title()} by Outlet Type")

#     return fat_fig, size_fig, item_fig, est_fig, loc_fig, outlet_fig, bar_fig

# # Run server
# if __name__ == '__main__':
#     # app.run_server(debug=True)
#      app.run(debug=True)






















# import pandas as pd
# import plotly.express as px
# import dash
# from dash import html, dcc, Input, Output
# import dash_bootstrap_components as dbc
# import plotly.graph_objects as go

# # Load and clean the data
# df = pd.read_excel("BlinkIT Grocery Data Excel.xlsx")
# df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
# df = df.rename(columns={
#     'sales': 'total_sales',
#     'rating': 'avg_ratings',
#     'item_visibility': 'item_visibility',
#     'item_type': 'item_type',
#     'outlet_size': 'outlet_size',
#     'outlet_location_type': 'outlet_location',
#     'outlet_type': 'outlet_type',
#     'outlet_establishment_year': 'year_established',
#     'item_fat_content': 'fat_content'
# })

# # Add derived columns
# df['avg_sales'] = df['total_sales']
# df['no_of_items'] = 1

# # Initialize the app with a modern theme (LUX for a clean, professional look)
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap"])

# # Define custom color palette
# COLORS = {
#     'primary': '#84C225',  # BlinkIT Green
#     'secondary': '#FFEB3B',  # BlinkIT Yellow
#     'accent1': '#26A69A',  # Teal
#     'accent2': '#FF7043',  # Coral
#     'background': '#F5F7FA',  # Light Gray
#     'text': '#2D3748',  # Dark Gray
# }

# # Helper to create KPI card with icons and animations
# def generate_kpi_card(title, value, color=COLORS['accent1'], icon="fas fa-dollar-sign"):
#     return dbc.Card(
#         [
#             dbc.CardBody(
#                 [
#                     html.Div(
#                         [
#                             html.I(className=icon, style={"fontSize": "24px", "color": color}),
#                             html.H5(title, className="card-title text-muted mt-2"),
#                             html.H3(value, className="card-text", style={"color": COLORS['text'], "fontWeight": "600"}),
#                         ],
#                         className="d-flex align-items-center justify-content-center"
#                     )
#                 ],
#                 style={"transition": "transform 0.3s ease-in-out"}
#             )
#         ],
#         className="m-2 text-center shadow-lg rounded-lg",
#         style={
#             "background": f"linear-gradient(135deg, {COLORS['background']} 0%, #FFFFFF 100%)",
#             "borderLeft": f"6px solid {color}",
#             ":hover": {"transform": "scale(1.05)"}
#         }
#     )

# # Layout structure with enhanced styling
# app.layout = dbc.Container(
#     [
#         # Header
#         html.Div(
#             [
#                 html.H1(
#                     "BlinkIT Dashboard",
#                     style={
#                         "color": COLORS['primary'],
#                         "fontWeight": "600",
#                         "fontSize": "48px",
#                         "textAlign": "center",
#                         "marginBottom": "10px",
#                         "fontFamily": "'Poppins', sans-serif"
#                     }
#                 ),
#                 html.H6(
#                     "India's Last Minute App - Powered by xAI",
#                     style={
#                         "color": COLORS['text'],
#                         "textAlign": "center",
#                         "marginBottom": "30px",
#                         "fontFamily": "'Poppins', sans-serif"
#                     }
#                 ),
#             ]
#         ),

#         dbc.Row(
#             [
#                 # Sidebar
#                 dbc.Col(
#                     [
#                         html.Div(
#                             [
#                                 html.Label("Outlet Location Type", style={"fontWeight": "500", "color": COLORS['text']}),
#                                 dcc.Dropdown(
#                                     ['All'] + sorted(df['outlet_location'].unique()),
#                                     'All',
#                                     id='location-filter',
#                                     style={
#                                         "borderRadius": "8px",
#                                         "border": f"1px solid {COLORS['primary']}",
#                                         "fontFamily": "'Poppins', sans-serif"
#                                     }
#                                 ),

#                                 html.Label("Outlet Size", style={"fontWeight": "500", "color": COLORS['text'], "marginTop": "20px"}),
#                                 dcc.Dropdown(
#                                     ['All'] + sorted(df['outlet_size'].unique()),
#                                     'All',
#                                     id='size-filter',
#                                     style={
#                                         "borderRadius": "8px",
#                                         "border": f"1px solid {COLORS['primary']}",
#                                         "fontFamily": "'Poppins', sans-serif"
#                                     }
#                                 ),

#                                 html.Label("Outlet Type", style={"fontWeight": "500", "color": COLORS['text'], "marginTop": "20px"}),
#                                 dcc.Dropdown(
#                                     ['All'] + sorted(df['outlet_type'].unique()),
#                                     'All',
#                                     id='type-filter',
#                                     style={
#                                         "borderRadius": "8px",
#                                         "border": f"1px solid {COLORS['primary']}",
#                                         "fontFamily": "'Poppins', sans-serif"
#                                     }
#                                 ),

#                                 html.Button(
#                                     "Reset Filters",
#                                     id='reset-button',
#                                     className="btn btn-outline-primary mt-4 w-100",
#                                     style={
#                                         "borderRadius": "8px",
#                                         "border": f"2px solid {COLORS['accent2']}",
#                                         "color": COLORS['accent2'],
#                                         "fontFamily": "'Poppins', sans-serif",
#                                         "transition": "all 0.3s ease-in-out",
#                                         ":hover": {"backgroundColor": COLORS['accent2'], "color": "#FFFFFF"}
#                                     }
#                                 ),
#                             ],
#                             style={
#                                 "background": f"linear-gradient(180deg, {COLORS['secondary']} 0%, {COLORS['primary']} 100%)",
#                                 "padding": "30px",
#                                 "borderRadius": "15px",
#                                 "boxShadow": "0 4px 15px rgba(0,0,0,0.1)",
#                                 "position": "sticky",
#                                 "top": "20px",
#                                 "height": "fit-content"
#                             }
#                         )
#                     ],
#                     width=2,
#                     style={"padding": "20px"}
#                 ),

#                 # Main Content
#                 dbc.Col(
#                     [
#                         # KPI Cards
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     generate_kpi_card("Total Sales", f"${df['total_sales'].sum() / 1e6:.2f}M", COLORS['primary'], "fas fa-dollar-sign"),
#                                     width=3
#                                 ),
#                                 dbc.Col(
#                                     generate_kpi_card("Avg Sales", f"${df['avg_sales'].mean():.0f}", COLORS['accent1'], "fas fa-chart-line"),
#                                     width=3
#                                 ),
#                                 dbc.Col(
#                                     generate_kpi_card("No. of Items", f"{df['no_of_items'].sum()}", COLORS['accent2'], "fas fa-boxes"),
#                                     width=3
#                                 ),
#                                 dbc.Col(
#                                     generate_kpi_card("Avg Ratings", f"{df['avg_ratings'].mean():.1f}", COLORS['secondary'], "fas fa-star"),
#                                     width=3
#                                 ),
#                             ],
#                             className="mb-4"
#                         ),

#                         # Tabs for dynamic bar chart
#                         dbc.Row(
#                             [
#                                 dcc.Tabs(
#                                     id="tabs",
#                                     value='avg_sales',
#                                     children=[
#                                         dcc.Tab(
#                                             label='Avg Sales',
#                                             value='avg_sales',
#                                             style={"fontFamily": "'Poppins', sans-serif", "color": COLORS['text']},
#                                             selected_style={"backgroundColor": COLORS['primary'], "color": "#FFFFFF"}
#                                         ),
#                                         dcc.Tab(
#                                             label='Avg Ratings',
#                                             value='avg_ratings',
#                                             style={"fontFamily": "'Poppins', sans-serif", "color": COLORS['text']},
#                                             selected_style={"backgroundColor": COLORS['primary'], "color": "#FFFFFF"}
#                                         ),
#                                         dcc.Tab(
#                                             label='No. of Items',
#                                             value='no_of_items',
#                                             style={"fontFamily": "'Poppins', sans-serif", "color": COLORS['text']},
#                                             selected_style={"backgroundColor": COLORS['primary'], "color": "#FFFFFF"}
#                                         ),
#                                         dcc.Tab(
#                                             label='Total Sales',
#                                             value='total_sales',
#                                             style={"fontFamily": "'Poppins', sans-serif", "color": COLORS['text']},
#                                             selected_style={"backgroundColor": COLORS['primary'], "color": "#FFFFFF"}
#                                         ),
#                                     ],
#                                     style={"fontFamily": "'Poppins', sans-serif"}
#                                 ),
#                                 dcc.Graph(id='bar-chart', style={"backgroundColor": "#FFFFFF", "borderRadius": "10px", "padding": "10px"}),
#                             ],
#                             className="mb-4"
#                         ),

#                         # Charts Section
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     dcc.Graph(id='fat-pie'),
#                                     width=6,
#                                     style={"backgroundColor": "#FFFFFF", "borderRadius": "10px", "padding": "10px"}
#                                 ),
#                                 dbc.Col(
#                                     dcc.Graph(id='size-pie'),
#                                     width=6,
#                                     style={"backgroundColor": "#FFFFFF", "borderRadius": "10px", "padding": "10px"}
#                                 ),
#                             ],
#                             className="mb-4"
#                         ),

#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     dcc.Graph(id='sales-by-item'),
#                                     width=6,
#                                     style={"backgroundColor": "#FFFFFF", "borderRadius": "10px", "padding": "10px"}
#                                 ),
#                                 dbc.Col(
#                                     dcc.Graph(id='establishment-trend'),
#                                     width=6,
#                                     style={"backgroundColor": "#FFFFFF", "borderRadius": "10px", "padding": "10px"}
#                                 ),
#                             ],
#                             className="mb-4"
#                         ),

#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     dcc.Graph(id='location-bar'),
#                                     width=6,
#                                     style={"backgroundColor": "#FFFFFF", "borderRadius": "10px", "padding": "10px"}
#                                 ),
#                                 dbc.Col(
#                                     dcc.Graph(id='outlet-type-table'),
#                                     width=6,
#                                     style={"backgroundColor": "#FFFFFF", "borderRadius": "10px", "padding": "10px"}
#                                 ),
#                             ]
#                         )
#                     ],
#                     width=10
#                 )
#             ]
#         )
#     ],
#     fluid=True,
#     style={
#         "backgroundColor": COLORS['background'],
#         "padding": "40px",
#         "fontFamily": "'Poppins', sans-serif"
#     }
# )

# # Callback to reset filters
# @app.callback(
#     [Output('location-filter', 'value'),
#      Output('size-filter', 'value'),
#      Output('type-filter', 'value')],
#     Input('reset-button', 'n_clicks')
# )
# def reset_filters(n_clicks):
#     return 'All', 'All', 'All'

# # Callback to update all charts
# @app.callback(
#     [Output('fat-pie', 'figure'),
#      Output('size-pie', 'figure'),
#      Output('sales-by-item', 'figure'),
#      Output('establishment-trend', 'figure'),
#      Output('location-bar', 'figure'),
#      Output('outlet-type-table', 'figure'),
#      Output('bar-chart', 'figure')],
#     [Input('location-filter', 'value'),
#      Input('size-filter', 'value'),
#      Input('type-filter', 'value'),
#      Input('tabs', 'value')]
# )
# def update_charts(location, size, otype, tab):
#     dff = df.copy()
#     if location != 'All':
#         dff = dff[dff['outlet_location'] == location]
#     if size != 'All':
#         dff = dff[dff['outlet_size'] == size]
#     if otype != 'All':
#         dff = dff[dff['outlet_type'] == otype]

#     # Define custom color sequence
#     color_sequence = [COLORS['primary'], COLORS['secondary'], COLORS['accent1'], COLORS['accent2']]

#     # Pie Charts
#     fat_fig = px.pie(
#         dff,
#         values='total_sales',
#         names='fat_content',
#         hole=0.5,
#         title="Sales by Fat Content",
#         color_discrete_sequence=color_sequence
#     ).update_traces(
#         textinfo='percent+label',
#         hovertemplate='%{label}: %{value:,.0f} (%{percent})',
#         marker=dict(line=dict(color='#FFFFFF', width=2))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         showlegend=True,
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     size_fig = px.pie(
#         dff,
#         values='total_sales',
#         names='outlet_size',
#         hole=0.5,
#         title="Sales by Outlet Size",
#         color_discrete_sequence=color_sequence
#     ).update_traces(
#         textinfo='percent+label',
#         hovertemplate='%{label}: %{value:,.0f} (%{percent})',
#         marker=dict(line=dict(color='#FFFFFF', width=2))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         showlegend=True,
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     # Bar Charts
#     item_fig = px.bar(
#         dff.groupby('item_type')['total_sales'].sum().nlargest(10).reset_index(),
#         x='total_sales',
#         y='item_type',
#         orientation='h',
#         title="Top 10 Item Types by Sales",
#         color_discrete_sequence=[COLORS['accent1']]
#     ).update_traces(
#         hovertemplate='%{y}: %{x:,.0f}',
#         marker=dict(line=dict(color='#FFFFFF', width=1))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         xaxis_title="Total Sales",
#         yaxis_title="Item Type",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     est_fig = px.line(
#         dff.groupby('year_established')['total_sales'].sum().reset_index(),
#         x='year_established',
#         y='total_sales',
#         title="Sales Trend by Establishment Year",
#         color_discrete_sequence=[COLORS['primary']],
#         markers=True
#     ).update_traces(
#         hovertemplate='Year: %{x}<br>Sales: %{y:,.0f}',
#         line=dict(width=3),
#         marker=dict(size=8)
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         xaxis_title="Year Established",
#         yaxis_title="Total Sales",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     loc_fig = px.bar(
#         dff.groupby('outlet_location')['total_sales'].sum().reset_index(),
#         x='outlet_location',
#         y='total_sales',
#         title="Sales by Outlet Location",
#         color_discrete_sequence=[COLORS['accent2']]
#     ).update_traces(
#         hovertemplate='%{x}: %{y:,.0f}',
#         marker=dict(line=dict(color='#FFFFFF', width=1))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         xaxis_title="Outlet Location",
#         yaxis_title="Total Sales",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     outlet_summary = dff.groupby('outlet_type').agg({
#         'total_sales': 'sum',
#         'no_of_items': 'sum',
#         'avg_sales': 'mean',
#         'avg_ratings': 'mean',
#         'item_visibility': 'mean'
#     }).reset_index()

#     outlet_fig = px.bar(
#         outlet_summary,
#         x='total_sales',
#         y='outlet_type',
#         orientation='h',
#         title="Outlet Type Performance",
#         color='avg_ratings',
#         color_continuous_scale=[COLORS['secondary'], COLORS['primary']]
#     ).update_traces(
#         hovertemplate='%{y}: Sales=%{x:,.0f}<br>Avg Rating=%{marker.color:.1f}',
#         marker=dict(line=dict(color='#FFFFFF', width=1))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         xaxis_title="Total Sales",
#         yaxis_title="Outlet Type",
#         coloraxis_colorbar_title="Avg Ratings",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     # Tab-based Bar Chart
#     y_col = tab if tab in dff.columns else 'total_sales'
#     color = COLORS['accent1'] if tab in ['avg_sales', 'avg_ratings', 'no_of_items'] else COLORS['primary']
#     bar_fig = px.bar(
#         dff,
#         x='outlet_type',
#         y=y_col,
#         title=f"{tab.replace('_', ' ').title()} by Outlet Type",
#         color_discrete_sequence=[color]
#     ).update_traces(
#         hovertemplate='%{x}: %{y:,.2f}',
#         marker=dict(line=dict(color='#FFFFFF', width=1))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         xaxis_title="Outlet Type",
#         yaxis_title=tab.replace('_', ' ').title(),
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     return fat_fig, size_fig, item_fig, est_fig, loc_fig, outlet_fig, bar_fig

# # Run server
# if __name__ == '__main__':
#     app.run(debug=True)
# @app.callback(
#     [Output('fat-pie', 'figure'),
#      Output('size-pie', 'figure'),
#      Output('sales-by-item', 'figure'),
#      Output('establishment-trend', 'figure'),
#      Output('location-bar', 'figure'),
#      Output('outlet-type-table', 'figure'),
#      Output('bar-chart', 'figure')],
#     [Input('location-filter', 'value'),
#      Input('size-filter', 'value'),
#      Input('type-filter', 'value'),
#      Input('tabs', 'value')]
# )
# def update_charts(location, size, otype, tab):
#     dff = df.copy()
#     if location != 'All':
#         dff = dff[dff['outlet_location'] == location]
#     if size != 'All':
#         dff = dff[dff['outlet_size'] == size]
#     if otype != 'All':
#         dff = dff[dff['outlet_type'] == otype]

#     # Handle empty dataframe
#     if dff.empty:
#         empty_fig = go.Figure().update_layout(
#             title="No Data Available",
#             annotations=[dict(text="No data matches the selected filters.", x=0.5, y=0.5, showarrow=False)],
#             title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#             font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#             paper_bgcolor='rgba(0,0,0,0)',
#             plot_bgcolor='rgba(0,0,0,0)'
#         )
#         return (empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig)

#     # Define custom color sequence
#     color_sequence = [COLORS['primary'], COLORS['secondary'], COLORS['accent1'], COLORS['accent2']]

#     # Pie Charts (unchanged)
#     fat_fig = px.pie(
#         dff,
#         values='total_sales',
#         names='fat_content',
#         hole=0.5,
#         title="Sales by Fat Content",
#         color_discrete_sequence=color_sequence
#     ).update_traces(
#         textinfo='percent+label',
#         hovertemplate='%{label}: %{value:,.0f} (%{percent})',
#         marker=dict(line=dict(color='#FFFFFF', width=2))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         showlegend=True,
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     size_fig = px.pie(
#         dff,
#         values='total_sales',
#         names='outlet_size',
#         hole=0.5,
#         title="Sales by Outlet Size",
#         color_discrete_sequence=color_sequence
#     ).update_traces(
#         textinfo='percent+label',
#         hovertemplate='%{label}: %{value:,.0f} (%{percent})',
#         marker=dict(line=dict(color='#FFFFFF', width=2))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         showlegend=True,
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     # Other charts (unchanged for brevity)
#     item_fig = px.bar(
#         dff.groupby('item_type')['total_sales'].sum().nlargest(10).reset_index(),
#         x='total_sales',
#         y='item_type',
#         orientation='h',
#         title="Top 10 Item Types by Sales",
#         color_discrete_sequence=[COLORS['accent1']]
#     ).update_traces(
#         hovertemplate='%{y}: %{x:,.0f}',
#         marker=dict(line=dict(color='#FFFFFF', width=1))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         xaxis_title="Total Sales",
#         yaxis_title="Item Type",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     est_fig = px.line(
#         dff.groupby('year_established')['total_sales'].sum().reset_index(),
#         x='year_established',
#         y='total_sales',
#         title="Sales Trend by Establishment Year",
#         color_discrete_sequence=[COLORS['primary']],
#         markers=True
#     ).update_traces(
#         hovertemplate='Year: %{x}<br>Sales: %{y:,.0f}',
#         line=dict(width=3),
#         marker=dict(size=8)
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         xaxis_title="Year Established",
#         yaxis_title="Total Sales",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     loc_fig = px.bar(
#         dff.groupby('outlet_location')['total_sales'].sum().reset_index(),
#         x='outlet_location',
#         y='total_sales',
#         title="Sales by Outlet Location",
#         color_discrete_sequence=[COLORS['accent2']]
#     ).update_traces(
#         hovertemplate='%{x}: %{y:,.0f}',
#         marker=dict(line=dict(color='#FFFFFF', width=1))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         xaxis_title="Outlet Location",
#         yaxis_title="Total Sales",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     outlet_summary = dff.groupby('outlet_type').agg({
#         'total_sales': 'sum',
#         'no_of_items': 'sum',
#         'avg_sales': 'mean',
#         'avg_ratings': 'mean',
#         'item_visibility': 'mean'
#     }).reset_index()

#     outlet_fig = px.bar(
#         outlet_summary,
#         x='total_sales',
#         y='outlet_type',
#         orientation='h',
#         title="Outlet Type Performance",
#         color='avg_ratings',
#         color_continuous_scale=[COLORS['secondary'], COLORS['primary']]
#     ).update_traces(
#         hovertemplate='%{y}: Sales=%{x:,.0f}<br>Avg Rating=%{marker.color:.1f}',
#         marker=dict(line=dict(color='#FFFFFF', width=1))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         xaxis_title="Total Sales",
#         yaxis_title="Outlet Type",
#         coloraxis_colorbar_title="Avg Ratings",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     # Updated Bar Chart Logic
#     y_col = tab if tab in dff.columns else 'total_sales'
#     color = COLORS['accent1'] if tab in ['avg_sales', 'avg_ratings', 'no_of_items'] else COLORS['primary']

#     # Aggregate data for bar chart to avoid rendering issues
#     agg_dict = {
#         'total_sales': 'sum',
#         'avg_sales': 'mean',
#         'avg_ratings': 'mean',
#         'no_of_items': 'sum'
#     }
#     bar_data = dff.groupby('outlet_type')[y_col].agg(agg_dict.get(y_col, 'sum')).reset_index()

#     bar_fig = px.bar(
#         bar_data,
#         x='outlet_type',
#         y=y_col,
#         title=f"{y_col.replace('_', ' ').title()} by Outlet Type",
#         color_discrete_sequence=[color]
#     ).update_traces(
#         hovertemplate='%{x}: %{y:,.2f}',
#         marker=dict(line=dict(color='#FFFFFF', width=1))
#     ).update_layout(
#         title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
#         font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
#         xaxis_title="Outlet Type",
#         yaxis_title=y_col.replace('_', ' ').title(),
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(t=50, b=50, l=50, r=50),
#         height=400,  # Explicitly set height for better visibility
#         xaxis_tickangle=45  # Rotate x-axis labels for readability
#     )

#     return fat_fig, size_fig, item_fig, est_fig, loc_fig, outlet_fig, bar_fig







import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Load and clean the data (unchanged)
df = pd.read_excel("BlinkIT Grocery Data Excel.xlsx")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df = df.rename(columns={
    'sales': 'total_sales',
    'rating': 'avg_ratings',
    'item_visibility': 'item_visibility',
    'item_type': 'item_type',
    'outlet_size': 'outlet_size',
    'outlet_location_type': 'outlet_location',
    'outlet_type': 'outlet_type',
    'outlet_establishment_year': 'year_established',
    'item_fat_content': 'fat_content'
})

df['avg_sales'] = df['total_sales']
df['no_of_items'] = 1

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap"])

# Define custom color palette (unchanged)
COLORS = {
    'primary': '#84C225',  # BlinkIT Green
    'secondary': '#FFEB3B',  # BlinkIT Yellow
    'accent1': '#26A69A',  # Teal
    'accent2': '#FF7043',  # Coral
    'background': '#F5F7FA',  # Light Gray
    'text': '#2D3748',  # Dark Gray
}

# Helper to create KPI card
def generate_kpi_card(title, value, color=COLORS['accent1'], icon="fas fa-dollar-sign"):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.I(className=icon, style={"fontSize": "24px", "color": color}),
                            html.H5(title, className="card-title text-muted mt-2"),
                            html.H3(value, className="card-text", style={"color": COLORS['text'], "fontWeight": "600"}),
                        ],
                        className="d-flex align-items-center justify-content-center"
                    )
                ],
                style={"transition": "transform 0.3s ease-in-out, background 0.3s ease-in-out"}
            )
        ],
        className="m-2 text-center shadow-lg rounded-lg",
        style={
            "background": f"linear-gradient(145deg, {COLORS['background']} 30%, #E8ECEF 100%)",  # Softer gradient
            "borderLeft": f"6px solid {color}",
            ":hover": {
                "transform": "scale(1.05)",
                "background": f"linear-gradient(145deg, {color}20 30%, #FFFFFF 100%)"  # Dynamic hover
            }
        }
    )

# Layout structure
app.layout = dbc.Container(
    [
        # Header (unchanged)
        html.Div(
            [
                html.H1(
                    "BlinkIT Dashboard",
                    style={
                        "color": COLORS['primary'],
                        "fontWeight": "600",
                        "fontSize": "48px",
                        "textAlign": "center",
                        "marginBottom": "10px",
                        "fontFamily": "'Poppins', sans-serif"
                    }
                ),
                html.H6(
                    "India's Last Minute App - Powered by xAI",
                    style={
                        "color": COLORS['text'],
                        "textAlign": "center",
                        "marginBottom": "30px",
                        "fontFamily": "'Poppins', sans-serif"
                    }
                ),
            ]
        ),

        dbc.Row(
            [
                # Sidebar
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Label("Outlet Location Type", style={"fontWeight": "500", "color": COLORS['text']}),
                                dcc.Dropdown(
                                    ['All'] + sorted(df['outlet_location'].unique()),
                                    'All',
                                    id='location-filter',
                                    style={
                                        "borderRadius": "8px",
                                        "border": f"1px solid {COLORS['primary']}",
                                        "fontFamily": "'Poppins', sans-serif"
                                    }
                                ),

                                html.Label("Outlet Size", style={"fontWeight": "500", "color": COLORS['text'], "marginTop": "20px"}),
                                dcc.Dropdown(
                                    ['All'] + sorted(df['outlet_size'].unique()),
                                    'All',
                                    id='size-filter',
                                    style={
                                        "borderRadius": "8px",
                                        "border": f"1px solid {COLORS['primary']}",
                                        "fontFamily": "'Poppins', sans-serif"
                                    }
                                ),

                                html.Label("Outlet Type", style={"fontWeight": "500", "color": COLORS['text'], "marginTop": "20px"}),
                                dcc.Dropdown(
                                    ['All'] + sorted(df['outlet_type'].unique()),
                                    'All',
                                    id='type-filter',
                                    style={
                                        "borderRadius": "8px",
                                        "border": f"1px solid {COLORS['primary']}",
                                        "fontFamily": "'Poppins', sans-serif"
                                    }
                                ),

                                html.Button(
                                    "Reset Filters",
                                    id='reset-button',
                                    className="btn btn-outline-primary mt-4 w-100",
                                    style={
                                        "borderRadius": "8px",
                                        "border": f"2px solid {COLORS['accent2']}",
                                        "color": COLORS['accent2'],
                                        "fontFamily": "'Poppins', sans-serif",
                                        "transition": "all 0.3s ease-in-out",
                                        ":hover": {"backgroundColor": COLORS['accent2'], "color": "#FFFFFF"}
                                    }
                                ),
                            ],
                            style={
                                "background": f"linear-gradient(180deg, {COLORS['secondary']}20 0%, {COLORS['primary']}20 100%)",  # Softer gradient
                                "padding": "30px",
                                "borderRadius": "15px",
                                "boxShadow": "0 4px 15px rgba(0,0,0,0.1)",
                                "position": "sticky",
                                "top": "20px",
                                "height": "fit-content"
                            }
                        )
                    ],
                    width=2,
                    style={"padding": "20px"}
                ),

                # Main Content
                dbc.Col(
                    [
                        # KPI Cards
                        dbc.Row(
                            [
                                dbc.Col(
                                    generate_kpi_card("Total Sales", f"${df['total_sales'].sum() / 1e6:.2f}M", COLORS['primary'], "fas fa-dollar-sign"),
                                    width=3
                                ),
                                dbc.Col(
                                    generate_kpi_card("Avg Sales", f"${df['avg_sales'].mean():.0f}", COLORS['accent1'], "fas fa-chart-line"),
                                    width=3
                                ),
                                dbc.Col(
                                    generate_kpi_card("No. of Items", f"{df['no_of_items'].sum()}", COLORS['accent2'], "fas fa-boxes"),
                                    width=3
                                ),
                                dbc.Col(
                                    generate_kpi_card("Avg Ratings", f"{df['avg_ratings'].mean():.1f}", COLORS['secondary'], "fas fa-star"),
                                    width=3
                                ),
                            ],
                            className="mb-4"
                        ),

                        # Tabs for dynamic bar chart (unchanged)
                        dbc.Row(
                            [
                                dcc.Tabs(
                                    id="tabs",
                                    value='avg_sales',
                                    children=[
                                        dcc.Tab(
                                            label='Avg Sales',
                                            value='avg_sales',
                                            style={"fontFamily": "'Poppins', sans-serif", "color": COLORS['text']},
                                            selected_style={"backgroundColor": COLORS['primary'], "color": "#FFFFFF"}
                                        ),
                                        dcc.Tab(
                                            label='Avg Ratings',
                                            value='avg_ratings',
                                            style={"fontFamily": "'Poppins', sans-serif", "color": COLORS['text']},
                                            selected_style={"backgroundColor": COLORS['primary'], "color": "#FFFFFF"}
                                        ),
                                        dcc.Tab(
                                            label='No. of Items',
                                            value='no_of_items',
                                            style={"fontFamily": "'Poppins', sans-serif", "color": COLORS['text']},
                                            selected_style={"backgroundColor": COLORS['primary'], "color": "#FFFFFF"}
                                        ),
                                        dcc.Tab(
                                            label='Total Sales',
                                            value='total_sales',
                                            style={"fontFamily": "'Poppins', sans-serif", "color": COLORS['text']},
                                            selected_style={"backgroundColor": COLORS['primary'], "color": "#FFFFFF"}
                                        ),
                                    ],
                                    style={"fontFamily": "'Poppins', sans-serif"}
                                ),
                                dcc.Graph(id='bar-chart', style={"backgroundColor": "#F9FAFB", "borderRadius": "10px", "padding": "10px"}),
                            ],
                            className="mb-4"
                        ),

                        # Charts Section
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(id='fat-pie'),
                                    width=6,
                                    style={"backgroundColor": "#F9FAFB", "borderRadius": "10px", "padding": "10px"}
                                ),
                                dbc.Col(
                                    dcc.Graph(id='size-pie'),
                                    width=6,
                                    style={"backgroundColor": "#F9FAFB", "borderRadius": "10px", "padding": "10px"}
                                ),
                            ],
                            className="mb-4"
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(id='sales-by-item'),
                                    width=6,
                                    style={"backgroundColor": "#F9FAFB", "borderRadius": "10px", "padding": "10px"}
                                ),
                                dbc.Col(
                                    dcc.Graph(id='establishment-trend'),
                                    width=6,
                                    style={"backgroundColor": "#F9FAFB", "borderRadius": "10px", "padding": "10px"}
                                ),
                            ],
                            className="mb-4"
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(id='location-bar'),
                                    width=6,
                                    style={"backgroundColor": "#F9FAFB", "borderRadius": "10px", "padding": "10px"}
                                ),
                                dbc.Col(
                                    dcc.Graph(id='outlet-type-table'),
                                    width=6,
                                    style={"backgroundColor": "#F9FAFB", "borderRadius": "10px", "padding": "10px"}
                                ),
                            ]
                        )
                    ],
                    width=10
                )
            ]
        )
    ],
    fluid=True,
    style={
        "background": f"linear-gradient(180deg, {COLORS['background']} 0%, #E8ECEF 100%)",  # Subtle gradient
        "padding": "40px",
        "fontFamily": "'Poppins', sans-serif"
    }
)

# Callback to reset filters (unchanged)
@app.callback(
    [Output('location-filter', 'value'),
     Output('size-filter', 'value'),
     Output('type-filter', 'value')],
    Input('reset-button', 'n_clicks')
)
def reset_filters(n_clicks):
    return 'All', 'All', 'All'

# Callback to update all charts
@app.callback(
    [Output('fat-pie', 'figure'),
     Output('size-pie', 'figure'),
     Output('sales-by-item', 'figure'),
     Output('establishment-trend', 'figure'),
     Output('location-bar', 'figure'),
     Output('outlet-type-table', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('location-filter', 'value'),
     Input('size-filter', 'value'),
     Input('type-filter', 'value'),
     Input('tabs', 'value')]
)
def update_charts(location, size, otype, tab):
    dff = df.copy()
    if location != 'All':
        dff = dff[dff['outlet_location'] == location]
    if size != 'All':
        dff = dff[dff['outlet_size'] == size]
    if otype != 'All':
        dff = dff[dff['outlet_type'] == otype]

    # Handle empty dataframe
    if dff.empty:
        empty_fig = go.Figure().update_layout(
            title="No Data Available",
            annotations=[dict(text="No data matches the selected filters.", x=0.5, y=0.5, showarrow=False)],
            title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
            font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
            paper_bgcolor='#F9FAFB',  # Match chart background
            plot_bgcolor='#F9FAFB'
        )
        return (empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig)

    # Define custom color sequence
    color_sequence = [COLORS['primary'], COLORS['secondary'], COLORS['accent1'], COLORS['accent2']]

    # Pie Charts
    fat_fig = px.pie(
        dff,
        values='total_sales',
        names='fat_content',
        hole=0.5,
        title="Sales by Fat Content",
        color_discrete_sequence=color_sequence
    ).update_traces(
        textinfo='percent+label',
        hovertemplate='%{label}: %{value:,.0f} (%{percent})',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    ).update_layout(
        title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
        font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
        paper_bgcolor='#F9FAFB',
        plot_bgcolor='#F9FAFB',
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50)
    )

    size_fig = px.pie(
        dff,
        values='total_sales',
        names='outlet_size',
        hole=0.5,
        title="Sales by Outlet Size",
        color_discrete_sequence=color_sequence
    ).update_traces(
        textinfo='percent+label',
        hovertemplate='%{label}: %{value:,.0f} (%{percent})',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    ).update_layout(
        title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
        font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
        paper_bgcolor='#F9FAFB',
        plot_bgcolor='#F9FAFB',
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50)
    )

    # Bar Charts
    item_fig = px.bar(
        dff.groupby('item_type')['total_sales'].sum().nlargest(10).reset_index(),
        x='total_sales',
        y='item_type',
        orientation='h',
        title="Top 10 Item Types by Sales",
        color_discrete_sequence=[COLORS['accent1']]
    ).update_traces(
        hovertemplate='%{y}: %{x:,.0f}',
        marker=dict(line=dict(color='#FFFFFF', width=1))
    ).update_layout(
        title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
        font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
        xaxis_title="Total Sales",
        yaxis_title="Item Type",
        paper_bgcolor='#F9FAFB',
        plot_bgcolor='#F9FAFB',
        margin=dict(t=50, b=50, l=50, r=50)
    )

    est_fig = px.line(
        dff.groupby('year_established')['total_sales'].sum().reset_index(),
        x='year_established',
        y='total_sales',
        title="Sales Trend by Establishment Year",
        color_discrete_sequence=[COLORS['primary']],
        markers=True
    ).update_traces(
        hovertemplate='Year: %{x}<br>Sales: %{y:,.0f}',
        line=dict(width=3),
        marker=dict(size=8)
    ).update_layout(
        title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
        font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
        xaxis_title="Year Established",
        yaxis_title="Total Sales",
        paper_bgcolor='#F9FAFB',
        plot_bgcolor='#F9FAFB',
        margin=dict(t=50, b=50, l=50, r=50)
    )

    loc_fig = px.bar(
        dff.groupby('outlet_location')['total_sales'].sum().reset_index(),
        x='outlet_location',
        y='total_sales',
        title="Sales by Outlet Location",
        color_discrete_sequence=[COLORS['accent2']]
    ).update_traces(
        hovertemplate='%{x}: %{y:,.0f}',
        marker=dict(line=dict(color='#FFFFFF', width=1))
    ).update_layout(
        title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
        font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
        xaxis_title="Outlet Location",
        yaxis_title="Total Sales",
        paper_bgcolor='#F9FAFB',
        plot_bgcolor='#F9FAFB',
        margin=dict(t=50, b=50, l=50, r=50)
    )

    outlet_summary = dff.groupby('outlet_type').agg({
        'total_sales': 'sum',
        'no_of_items': 'sum',
        'avg_sales': 'mean',
        'avg_ratings': 'mean',
        'item_visibility': 'mean'
    }).reset_index()

    outlet_fig = px.bar(
        outlet_summary,
        x='total_sales',
        y='outlet_type',
        orientation='h',
        title="Outlet Type Performance",
        color='avg_ratings',
        color_continuous_scale=[COLORS['secondary'], COLORS['primary']]
    ).update_traces(
        hovertemplate='%{y}: Sales=%{x:,.0f}<br>Avg Rating=%{marker.color:.1f}',
        marker=dict(line=dict(color='#FFFFFF', width=1))
    ).update_layout(
        title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
        font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
        xaxis_title="Total Sales",
        yaxis_title="Outlet Type",
        coloraxis_colorbar_title="Avg Ratings",
        paper_bgcolor='#F9FAFB',
        plot_bgcolor='#F9FAFB',
        margin=dict(t=50, b=50, l=50, r=50)
    )

    # Tab-based Bar Chart
    y_col = tab if tab in dff.columns else 'total_sales'
    color = COLORS['accent1'] if tab in ['avg_sales', 'avg_ratings', 'no_of_items'] else COLORS['primary']
    agg_dict = {
        'total_sales': 'sum',
        'avg_sales': 'mean',
        'avg_ratings': 'mean',
        'no_of_items': 'sum'
    }
    bar_data = dff.groupby('outlet_type')[y_col].agg(agg_dict.get(y_col, 'sum')).reset_index()

    bar_fig = px.bar(
        bar_data,
        x='outlet_type',
        y=y_col,
        title=f"{y_col.replace('_', ' ').title()} by Outlet Type",
        color_discrete_sequence=[color]
    ).update_traces(
        hovertemplate='%{x}: %{y:,.2f}',
        marker=dict(line=dict(color='#FFFFFF', width=1))
    ).update_layout(
        title_font=dict(size=20, family="'Poppins', sans-serif", color=COLORS['text']),
        font=dict(family="'Poppins', sans-serif", color=COLORS['text']),
        xaxis_title="Outlet Type",
        yaxis_title=y_col.replace('_', ' ').title(),
        paper_bgcolor='#F9FAFB',
        plot_bgcolor='#F9FAFB',
        margin=dict(t=50, b=50, l=50, r=50),
        height=400,
        xaxis_tickangle=45
    )

    return fat_fig, size_fig, item_fig, est_fig, loc_fig, outlet_fig, bar_fig


# Run server
if __name__ == '__main__':
    app.run(debug=True)