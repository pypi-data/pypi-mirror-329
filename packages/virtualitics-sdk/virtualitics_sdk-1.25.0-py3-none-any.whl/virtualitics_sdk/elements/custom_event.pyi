from _typeshed import Incomplete
from enum import Enum
from virtualitics_sdk.app.flow_metadata import FlowMetadata as FlowMetadata
from virtualitics_sdk.assets.asset import Asset as Asset
from virtualitics_sdk.elements.element import ElementType as ElementType, InputElement as InputElement

class CustomEventType(Enum):
    STANDARD: str
    ASSET_DOWNLOAD: str

class CustomEventPosition(Enum):
    LEFT: str
    CENTER: str
    RIGHT: str

class CustomEvent(InputElement):
    '''Creates a custom event element that calls the passed in function using flow_metadata when clicked.

    :param title: The title of the custom event element.
    :param description: A description to go with this element on the page.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param position: The position the event button should be placed, defaults to CustomEventPosition.RIGHT
    :param label: The label of the element, defaults to \'\'.
    :param placeholder: The placeholder of the element, defaults to \'\'.
    :param show_confirmation: Whether or not to display a confirmation modal after clicking the button, defaults to True.
        
    **EXAMPLE:** 

       .. code-block:: python

           # Imports 
           from virtualitics_sdk import CustomEvent
           . . .
           # Example usage
           # This creates a custom event for us to place in the step defined below
           class SimpleCustomEvent(CustomEvent):
              def __init__(self):
                 super().__init__(title="Kick-off", description="", show_description=False)
               def callback(self, flow_metadata) -> Union[str, dict]:
                 return "Done!"
           class ExampleStep(Step):
               def run(self, flow_metadata):
                . . . 
                event = SimpleCustomEvent()
                info = Infographic("", "", [], [recommendation], event=event)
                return info

    The above CustomEvent will be displayed as: 

       .. image:: ../images/custom_event_ex.png
          :align: center
          :scale: 25%
    '''
    def __init__(self, title: str, description: str, show_title: bool = True, show_description: bool = True, position: CustomEventPosition = ..., label: str = '', placeholder: str = '', show_confirmation: bool = True, **kwargs) -> None: ...
    def callback(self, flow_metadata: FlowMetadata, **step_clients: dict) -> str | dict: ...
    def get_value(self) -> None:
        """This function does nothing for Custom Events. Although they are input elements, getting their
        value will return None

        :return: None
        """

class AssetDownloadCustomEvent(CustomEvent):
    '''
    Creates a custom event that generates a download link to an Asset\'s data/object. The download link will return the
    bytes of the object if it is an instance of bytes, a text file if it is an instance of str or the dill pickled bytes
    of the python object.

    Adds some additional required parameters to the constructor.

    :param title: The title of the custom event element.
    :param asset: an Asset object with reference of the data/object to download.
    :param extension: A file extension of the resulting downloaded file.
    :param mime_type: Force the mimetype of the downloaded file (this determines how the client\'s browser
            encodes or writes the file being download.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    
    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from virtualitics_sdk import AssetDownloadCustomEvent
           . . .
           # Example usage 
           class DataShow(Step):
            def run(self, flow_metadata):
                . . . 
                acc = Model(label="linear-svc", model=LinearSVC().fit(X, y), name="Example")
                event = AssetDownloadCustomEvent("Download Linear SVC", acc, "pkl")
            
    The above AssetDownloadCustomEvent usage will be displayed as: 

       .. image:: ../images/asset_ce_ex.png
          :align: center
          :scale: 50%
    '''
    def __init__(self, title: str, asset: Asset, extension: str, mime_type: str | None = None, show_title: bool = True, show_description: bool = True) -> None: ...
    def callback(self, flow_metadata: FlowMetadata, **step_clients) -> str | dict: ...

class TriggerFlowCustomEvent(CustomEvent):
    '''
    Creates a custom event that triggers another app with optional pre-supplied input parameters.
    Then wait for the app to stop and return a redirect url to the last started step.
    
    :param title: The title of the custom event element.
    :param description: A description to go with this element on the page.
    :param flow_name: the Name of the App to be triggered
    :param input_parameters: an optional dictionary describing input parameters to be passed to the triggered app
    :param timeout: timeout in seconds, the amount of time to wait for the triggered app to stop [default = 30]
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param position: The position the event button should be placed, defaults to CustomEventPosition.RIGHT
    :param kwargs: 

    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from virtualitics_sdk import TriggerFlowCustomEvent
           . . . 
           # Example usage 
           class DataUpload(Step):
             def run(self, flow_metadata):
                . . .
                flow_input_parameters = {"steps": {
                    "DataUpload": {
                        "Dropdown One": {"value": "A", 
                                         "description": "", 
                                         "card_title": 
                                         "User Input Card"},
                        "Dropdown Two": {"value": "B", 
                                         "card_title": 
                                         "User Input Card"}}}}
                trigger = TriggerFlowCustomEvent(title="Trigger a Flow",
                                                description="",
                                                flow_name="TriggerFlowTest",
                                                input_parameters=flow_input_parameters)
            
    The above TriggerFlowCustomEvent will be displayed as: 

       .. image:: ../images/trigger_ce_ex.png
          :align: center
          :scale: 25%
    '''
    flow_name: Incomplete
    input_parameters: Incomplete
    timeout: Incomplete
    def __init__(self, title: str, description: str, flow_name: str, input_parameters: dict | None = None, timeout: int = 30, show_title: bool = True, show_description: bool = True, position: CustomEventPosition = ..., **kwargs) -> None: ...
    def callback(self, flow_metadata: FlowMetadata, **step_clients) -> str | dict: ...
