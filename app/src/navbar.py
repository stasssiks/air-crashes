import dash_bootstrap_components as dbc


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Hypothesis", href="/about")),
            dbc.NavItem(dbc.NavLink("Analysis", href="/analysis")),
            dbc.NavItem(dbc.NavLink("Conclusion", href="/conclusion")),
            dbc.NavItem(dbc.NavLink("Initial Data", href="/data"))
        ],
        brand="AIR CRASHES",
        brand_href="/",
        sticky="top",
        color="dark",
        dark=True,
    )

    return navbar
