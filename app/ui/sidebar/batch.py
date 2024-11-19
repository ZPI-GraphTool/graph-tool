import faicons as fa
from shiny import ui


def batch() -> tuple:
    return (
        ui.input_switch("with_batch", "With batch algorithm", False),
        ui.panel_conditional(
            "input.with_batch == true",
            ui.row(
                ui.column(10, "Batch algorithm", class_="selectize-label"),
                ui.column(
                    2,
                    ui.input_action_button(
                        "refresh_batch_list",
                        label=None,
                        icon=fa.icon_svg("rotate"),
                        class_="refresh-button",
                    ),
                ),
                class_="selectize-row",
            ),
            ui.output_ui("batch_selectize"),
            ui.input_action_button("edit_batch", "Edit batch algorithm"),
        ),
    )
