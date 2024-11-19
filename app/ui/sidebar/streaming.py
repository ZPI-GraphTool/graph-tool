import faicons as fa
from shiny import ui


def streaming() -> tuple:
    return (
        ui.row(
            ui.column(10, "Streaming algorithm", class_="selectize-label"),
            ui.column(
                2,
                ui.input_action_button(
                    "refresh_streaming_list",
                    label=None,
                    icon=fa.icon_svg("rotate"),
                    class_="refresh-button",
                ),
            ),
            class_="selectize-row",
        ),
        ui.output_ui("streaming_selectize"),
        ui.input_action_button("edit_streaming", "Edit streaming algorithm"),
    )
