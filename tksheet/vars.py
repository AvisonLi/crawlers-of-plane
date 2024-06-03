from __future__ import annotations

from platform import system as get_os

USER_OS: str = f"{get_os()}".lower()
ctrl_key: str = "Command" if USER_OS == "darwin" else "Control"
rc_binding: str = "<2>" if USER_OS == "darwin" else "<3>"
symbols_set: set[str] = set("""!#$%&'()*+,-./:;"@[]^_`{|}~>?= \\""")
nonelike: set[object] = {None, "none", ""}
truthy: set[object] = {True, "true", "t", "yes", "y", "on", "1", 1, 1.0}
falsy: set[object] = {False, "false", "f", "no", "n", "off", "0", 0, 0.0}
val_modifying_options: set[str, str, str] = {"checkbox", "format", "dropdown"}
named_span_types = (
    "format",
    "highlight",
    "dropdown",
    "checkbox",
    "readonly",
    "align",
)
emitted_events: set[str] = {
    "<<SheetModified>>",
    "<<SheetRedrawn>>",
    "<<SheetSelect>>",
}
backwards_compatibility_keys: dict[str, str] = {
    "font": "table_font",
}
scrollbar_options_keys: set[str] = {
    "vertical_scroll_background",
    "horizontal_scroll_background",
    "vertical_scroll_troughcolor",
    "horizontal_scroll_troughcolor",
    "vertical_scroll_lightcolor",
    "horizontal_scroll_lightcolor",
    "vertical_scroll_darkcolor",
    "horizontal_scroll_darkcolor",
    "vertical_scroll_relief",
    "horizontal_scroll_relief",
    "vertical_scroll_troughrelief",
    "horizontal_scroll_troughrelief",
    "vertical_scroll_bordercolor",
    "horizontal_scroll_bordercolor",
    "vertical_scroll_borderwidth",
    "horizontal_scroll_borderwidth",
    "vertical_scroll_gripcount",
    "horizontal_scroll_gripcount",
    "vertical_scroll_arrowsize",
    "horizontal_scroll_arrowsize",
    "vertical_scroll_active_bg",
    "horizontal_scroll_active_bg",
    "vertical_scroll_not_active_bg",
    "horizontal_scroll_not_active_bg",
    "vertical_scroll_pressed_bg",
    "horizontal_scroll_pressed_bg",
    "vertical_scroll_active_fg",
    "horizontal_scroll_active_fg",
    "vertical_scroll_not_active_fg",
    "horizontal_scroll_not_active_fg",
    "vertical_scroll_pressed_fg",
    "horizontal_scroll_pressed_fg",
}
