from dash import html, register_page

register_page(
    __name__,
    name='Conclusion',
    top_nav=True,
    path='/conclusion'
)

conclusion = [
    {
        "title": "The number of crashes each year is decreasing.",
        "description": "Thanks to improvements in vehicle safety, better infrastructure, and more rigorous traffic "
                       "regulations, the annual number of crashes has been on a downward trend. Technological "
                       "innovations such as advanced driver-assistance systems (ADAS) also contribute to this "
                       "decrease. "
    },
    {
        "title": "Most crashes occur in winter and summer, but the difference is not significant.",
        "description": "While there is a slight increase in crashes during the extreme weather conditions of winter "
                       "and summer, the overall distribution of crashes throughout the year shows that these seasons "
                       "do not differ significantly from each other. Factors like weather and holiday travel periods "
                       "contribute to this pattern. "
    },
    {
        "title": "The majority of crashes and casualties are caused by human error.",
        "description": "Human factors such as distracted driving, speeding, and impaired driving are the leading "
                       "causes of crashes. Despite advances in vehicle safety technology, human error remains a "
                       "significant factor, highlighting the need for continued education and enforcement of safe "
                       "driving practices. "
    },
    {
        "title": "Weather-related crashes are most frequent in summer and winter.",
        "description": "Adverse weather conditions, such as ice and snow in winter and heavy rain or fog in summer, "
                       "lead to an increased number of weather-related crashes. These conditions can impair "
                       "visibility and vehicle handling, emphasizing the need for caution during these seasons. "
    }
]


def layout():
    page_layout = html.Div([
        html.Ul([
            html.Li([
                html.H2(point["title"], style={'font-size': '32px', 'padding-top': '10px', 'padding-bottom': '10px'}),
                html.P(point["description"], style={'font-size': '24px', 'padding': '10px 20px'})
            ]) for point in conclusion
        ], style={'padding': '20px'})
    ], style={'padding': '20px'})
    return page_layout
