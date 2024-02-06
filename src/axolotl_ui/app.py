from pathlib import Path

from shiny import App, Inputs, Outputs, Session, ui, reactive
import shinyswatch
from htmltools import HTML

from utils import background_img, question_circle_fill


www_dir = Path(__file__).parent.resolve() / "www"

project_config = ui.accordion_panel(
    "Project Config",
    *[
        ui.input_text(
            id="project_name",
            label=ui.tooltip(
                ui.span("Project Name ", question_circle_fill()), "Additional info"
            ),
            placeholder="Awesome Axolotl"
        ),
        ui.input_password(
            id="hf_token",
            label=ui.tooltip(
                ui.span("HuggingFace Token ", question_circle_fill()), "T"
            )
        ),
        ui.input_text(
            id="base_model",
            label=ui.tooltip(
                ui.span("Base Model ", question_circle_fill()),
                "This is the huggingface model that contains *.pt, *.safetensors, or *.bin files",
            ),
            placeholder="meta-llama/Llama-2-7b-chat-hf",
        ),
        ui.input_select(
            id="model_type",
            label=ui.tooltip(
                ui.span("Model Type ", question_circle_fill()),
                "If you want to specify the type of model to load, AutoModelForCausalLM is a good choice too.",
            ),
            choices=["AutoModelForCausalLM", "LlamaForCausalLM"],
            selected="AutoModelForCausalLM",
        ),
        ui.input_select(
            id="model_derivation",
            label=ui.tooltip(
                ui.span("Model Source ", question_circle_fill()),
                'Used to identify which the model is based on. Please note that if you set this to mistral, `padding_side` will be set to "left" by default',
            ),
            choices=["falcon", "llama", "mistra", "qwen"],
            selected="llama",
        ),
        ui.accordion(
            ui.accordion_panel(
                "Advanced Config",
                ui.input_text(id="test1", label="Test 2", placeholder="placeholder"),
            ),
            open=False,
        ),
    ]
)

dataset_config = ui.accordion_panel(
    "Datasets",
    *[
        ui.input_text(
            id="dataset_path",
            label=ui.tooltip(
                ui.span("Dataset Path ", question_circle_fill()), "A list of one or more paths to datasets to finetune the model with. HuggingFace dataset repo | s3://,gs:// path | \"json\" for local dataset, make sure to fill data_files"
            ),
            placeholder="vicgalle/alpaca-gpt4"
        ),
        ui.input_select(
            id="dataset_type",
            label=ui.tooltip(
                ui.span("Dataset Type ", question_circle_fill()), "The type of prompt to use for training. [alpaca, sharegpt, gpteacher, oasst, reflection]"
            ),
            choices=["alpaca", "sharegpt", "gpteacher", "oasst", "reflection"],
            selected="alpaca"
        )
    ]
)

app_ui = ui.page_fillable(
    shinyswatch.theme.minty(),
    ui.layout_sidebar(
        ui.sidebar(
            ui.h3("Axolotl Laucher 🚀"),
            ui.accordion(project_config, id="project_config"),
            ui.accordion(dataset_config, id="dataset_config", open=False),
            ui.input_action_button(
                "create_space",
                "Create HF Space",
            ),
            width=400,
            class_="opacity-75"
        ),
        HTML(background_img(url="https://github.com/OpenAccess-AI-Collective/axolotl/raw/main/image/axolotl.png",
                            opacity=0.1))
    )
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Effect
    @reactive.event(input.create_space)
    def _():
        ui.notification_show("This is not yet implemented.", type="warning")
    


app = App(
    app_ui,
    server,
    static_assets=str(www_dir),
)
