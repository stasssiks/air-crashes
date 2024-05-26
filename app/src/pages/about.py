from dash import html, register_page

register_page(
    __name__,
    name='Hypothesis',
    top_nav=True,
    path='/about'
)

bullet_points = [
    {
        "title": "There are fewer crashes now due to technological advancements.",
        "description": "With the rapid development of technology, safety measures and systems in vehicles and "
                       "infrastructure have greatly improved. This includes advancements in automotive engineering, "
                       "better road designs, and the implementation of traffic management systems that reduce the "
                       "likelihood of accidents. "
    },
    {
        "title": "The peak was during World War II.",
        "description": "The period of World War II saw a significant increase in crashes. This was due to the high "
                       "volume of military vehicles and aircraft in use, often in hazardous conditions and with "
                       "limited safety protocols in place. The urgency and scale of wartime operations also "
                       "contributed to this peak. "
    },
    {
        "title": "There are more crashes in autumn and winter due to weather conditions.",
        "description": "The colder months bring adverse weather conditions such as rain, snow, and ice, which make "
                       "driving and flying more dangerous. Reduced visibility and slippery surfaces are major "
                       "contributing factors to the higher incidence of crashes during these seasons. "
    }
]


def layout():
    page_layout = html.Div([
        html.Ul([
            html.Li([
                html.H2(point["title"], style={'font-size': '32px', 'padding-top': '10px', 'padding-bottom': '10px'}),
                html.P(point["description"], style={'font-size': '24px', 'padding': '10px 20px'})
            ]) for point in bullet_points
        ], style={'padding': '20px'})
    ], style={'padding': '20px'})
    return page_layout
