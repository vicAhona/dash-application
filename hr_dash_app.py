import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

hr_df = pd.read_csv('hr_data.csv')

hr_dash_df = hr_df.copy()

app = Dash(__name__)
app.title = 'HR Analytics Dashboard'

app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f5f7fa',
        'padding': '20px'
    },
    children=[
        html.H1('HR Analytics Dashboard', style={'textAlign': 'center', 'color': '#333333'}),
        html.P('Explore employee distribution and salary patterns by department, job title, and county.',
               style={'textAlign': 'center', 'color': '#555555'}),

        html.Div(
            style={'display': 'flex', 'gap': '20px', 'marginTop': '20px'},
            children=[
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#ffffff', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'},
                    children=[
                        html.Label('Select Department', style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='dept-filter',
                            options=[{'label': d, 'value': d} for d in sorted(hr_dash_df['department'].unique())],
                            value=None,
                            placeholder='All departments',
                            multi=True
                        )
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#ffffff', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'},
                    children=[
                        html.Label('Select County', style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='county-filter',
                            options=[{'label': c, 'value': c} for c in sorted(hr_dash_df['county'].unique())],
                            value=None,
                            placeholder='All counties',
                            multi=True
                        )
                    ]
                )
            ]
        ),

        html.Div(
            style={'display': 'flex', 'gap': '20px', 'marginTop': '20px'},
            children=[
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#ffffff', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'},
                    children=[
                        html.H3('Average Salary by Department', style={'textAlign': 'center'}),
                        dcc.Graph(id='avg-salary-dept')
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#ffffff', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'},
                    children=[
                        html.H3('Salary vs Years of Experience', style={'textAlign': 'center'}),
                        dcc.Graph(id='salary-vs-exp')
                    ]
                )
            ]
        ),

        html.Div(
            style={'marginTop': '20px', 'backgroundColor': '#ffffff', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'},
            children=[
                html.H3('Employee Count by Job Title', style={'textAlign': 'center'}),
                dcc.Graph(id='count-job-title')
            ]
        )
    ]
)


@app.callback(
    Output('avg-salary-dept', 'figure'),
    Output('salary-vs-exp', 'figure'),
    Output('count-job-title', 'figure'),
    Input('dept-filter', 'value'),
    Input('county-filter', 'value')
)
def update_charts(selected_depts, selected_counties):
    dff = hr_dash_df.copy()

    if selected_depts:
        if isinstance(selected_depts, list):
            dff = dff[dff['department'].isin(selected_depts)]
        else:
            dff = dff[dff['department'] == selected_depts]

    if selected_counties:
        if isinstance(selected_counties, list):
            dff = dff[dff['county'].isin(selected_counties)]
        else:
            dff = dff[dff['county'] == selected_counties]

    dept_summary = dff.groupby('department', as_index=False)['salary'].mean()
    fig_dept = px.bar(
        dept_summary,
        x='department',
        y='salary',
        color='department',
        title='Average Salary by Department',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_dept.update_layout(
        showlegend=False,
        xaxis_title='Department',
        yaxis_title='Average Salary',
        plot_bgcolor='#f9fafb',
        paper_bgcolor='#ffffff'
    )

    fig_scatter = px.scatter(
        dff,
        x='years_of_experience',
        y='salary',
        color='gender',
        hover_data=['job_title', 'department', 'county'],
        title='Salary vs Years of Experience',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_scatter.update_layout(
        xaxis_title='Years of Experience',
        yaxis_title='Salary',
        plot_bgcolor='#f9fafb',
        paper_bgcolor='#ffffff'
    )

    job_counts = dff['job_title'].value_counts().reset_index()
    job_counts.columns = ['job_title', 'count']
    fig_jobs = px.bar(
        job_counts,
        x='job_title',
        y='count',
        title='Employee Count by Job Title',
        color='count',
        color_continuous_scale='Blues'
    )
    fig_jobs.update_layout(
        xaxis_title='Job Title',
        yaxis_title='Number of Employees',
        plot_bgcolor='#f9fafb',
        paper_bgcolor='#ffffff'
    )

    return fig_dept, fig_scatter, fig_jobs


if __name__ == '__main__':
    app.run_server(debug=True)
