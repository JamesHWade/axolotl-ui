from shiny import ui
import yaml


# https://icons.getbootstrap.com/icons/question-circle-fill/
def question_circle_fill() -> str:
    ui.HTML(
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-question-circle-fill mb-1" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.496 6.033h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286a.237.237 0 0 0 .241.247zm2.325 6.443c.61 0 1.029-.394 1.029-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94 0 .533.425.927 1.01.927z"/></svg>'
    )


def background_img(url: str, opacity: float) -> str:
    """
    Generate CSS style for setting a somewhat transparent background image.

    Parameters
    ----------
    url : str
        URL of the image to be used as a background.
    opacity : float
        Opacity level of the background image (0.0 to 1.0).

    Returns
    -------
    str
        A CSS style string to set the somewhat transparent background image.
    """
    return f"""
    <style>
    body, html {{
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
    }}
    body::before {{
        content: "";
        position: fixed; /* Cover the entire page */
        left: 0;
        right: 0;
        z-index: -1; /* Ensure the image stays in the background */
        display: block;
        background-image: url('{url}');
        background-size: cover; /* Cover the entire page */
        background-position: center; /* Center the background image */
        opacity: {opacity}; /* Set the opacity for the image */
        width: 100%;
        height: 100%;
    }}
    </style>
    """


def read_markdown_file(path):
    with open(path, "r") as file:
        lines = file.readlines()

    # Find the start and end of the YAML header
    yaml_delimiters = [i for i, line in enumerate(lines) if line.strip() == "---"]

    # Skip the YAML header if it exists (assuming there are two delimiters)
    if len(yaml_delimiters) == 2:
        content_start = yaml_delimiters[1] + 1
        return "".join(lines[content_start:])
    else:
        # No YAML header found, return the entire content
        return "".join(lines)


def read_yaml(path: str) -> dict:
    with open(path, "r") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line and not line.startswith("#")]
    return yaml.safe_load("\n".join(lines))


def create_accordion_from_config(
    config: dict, section_name: str = "Config", open: bool = False
) -> str:
    """
    Create a user interface from a configuration dictionary.

    This function generates a sidebar with input fields for each key-value pair in the configuration dictionary.
    The type of input field depends on the type of the value:
    - If the value is a boolean, it creates radio buttons with options for True and False.
    - If the value is a number (int or float), it creates a numeric input field.
    - For other types of values, it creates a text input field.

    Parameters:
    config (dict): The configuration dictionary.
    section_name (str): The name of the section.
    open (bool): Whether the section should be open by default.

    Returns:
    str: A string representing the user interface.
    """
    # Create a list of UI elements
    ui_elements = []
    for key, value in config.items():
        # Check the type of the value
        if isinstance(value, bool):
            # If it's a boolean, create radio buttons
            input_element = ui.input_radio_buttons(
                id=key,
                label=key,
                choices=[True, False],
                selected=value,
            )
        elif isinstance(value, (int, float)):
            # If it's a number, create a numeric input
            input_element = ui.input_numeric(
                id=key,
                label=key,
                min=0,  # You may want to adjust this
                max=100,  # You may want to adjust this
                step=1,  # You may want to adjust this
                value=value,
                width=400,
            )
        else:
            # Otherwise, create an input text field
            input_element = ui.input_text(
                id=key,
                label=key,
                placeholder=str(value),
            )
        ui_elements.append(input_element)

    # Create accordion with the UI elements
    return ui.accordion(
        ui.accordion_panel(section_name, *ui_elements, width=400), open=open
    )
