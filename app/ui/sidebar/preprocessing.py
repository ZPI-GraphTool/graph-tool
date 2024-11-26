import faicons as fa
from htmltools import Tag
from shiny import ui


def preprocessing() -> tuple[Tag, ...]:
    return (
        ui.panel_conditional(
            "input.with_preprocessing == true",
            ui.row(
                ui.column(10, "Preprocessing function", class_="selectize-label"),
                ui.column(
                    2,
                    ui.input_action_button(
                        "refresh_preprocessing_list",
                        label=None,
                        icon=fa.icon_svg("rotate"),
                        class_="refresh-button",
                    ),
                ),
                class_="selectize-row",
            ),
            ui.output_ui("preprocessing_selectize"),
            ui.input_action_button(
                "edit_preprocessing",
                "Edit preprocessing function",
                icon=fa.icon_svg("code"),
            ),
        ),
    )
