import faicons as fa
from shiny import ui


def preprocessing() -> tuple:
    return (
        ui.panel_conditional(
            "input.with_preprocessing == true",
            ui.row(
                ui.column(8, "Preprocessing function", class_="selectize-label"),
                ui.column(
                    3,
                    ui.input_action_button(
                        "refresh_preprocessing_list",
                        label="",
                        icon=fa.icon_svg("rotate"),
                        class_="refresh-button",
                    ),
                ),
                class_="selectize-row",
            ),
            ui.output_ui("preprocessing_selectize"),
            ui.input_action_button("edit_preprocessing", "Edit preprocessing function"),
        ),
    )
