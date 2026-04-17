import app 


def test_header_present(dash_duo):
    dash_duo.start_server(app.app)

    dash_duo.wait_for_element("h1", timeout=10)
    assert "Soul Foods" in dash_duo.find_element("h1").text


def test_visualisation_present(dash_duo):
    dash_duo.start_server(app.app)

    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app.app)

    dash_duo.wait_for_element("#region-radio", timeout=10)
    picker = dash_duo.find_element("#region-radio")
    assert picker is not None