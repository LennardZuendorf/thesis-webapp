"""gr.HTML() component."""

from __future__ import annotations

from typing import Any, Callable

from gradio_client.documentation import document, set_documentation_group

from gradio.components.base import Component
from gradio.events import Events

set_documentation_group("component")


@document()
class iFrame(Component):
    """
    Used to display abitrary html output.
    Preprocessing: this component does *not* accept input.
    Postprocessing: expects a valid HTML {str}.

    Demos: text_analysis
    Guides: key-features
    """

    EVENTS = [Events.change]

    def __init__(
        self,
        value: str | Callable = "",
        *,
        label: str | None = None,
        every: float | None = None,
        show_label: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        height: str | None = None,
        width: str | None = None,
    ):
        """
        Parameters:
            value: Default value. If callable, the function will be called whenever the app loads to set the initial value of the component.
            label: The label for this component. Is used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.
            every: If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. Queue must be enabled. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            show_label: This parameter has no effect.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the iFrame DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the iFrame DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            height: The height of the iFrame in valid css (i.e "10px). If None, the height will be automatically set to 100%
        """
        super().__init__(
            label=label,
            every=every,
            show_label=show_label,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            value=value,
        )

        # updating component to take custom height and width values
        self.height = height
        self.width = width

    def example_inputs(self) -> Any:
        # setting a custom example
        return """<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ?si=QfHLpHZsI98oZT1G" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>"""

    def preprocess(self, payload: str | None) -> str | None:
        return payload

    def postprocess(self, value: str | None) -> str | None:
        return value

    def api_info(self) -> dict[str, Any]:
        return {"type": "string"}
