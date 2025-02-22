from _typeshed import Incomplete
from virtualitics_sdk.elements.element import ElementType as ElementType, InputElement as InputElement

class NumericRange(InputElement):
    '''A Numeric Range Input Element. 

    :param min_range: The minimum value for the range.
    :param max_range: The maximum value for the range.
    :param min_selection: The minimum selected value. Defaults to min_range value, defaults to None.
    :param max_selection: The maximum selected value. Defaults to max_range value, defaults to None.
                          For single sided sliders, this is the value to change to set defaults.
    :param include_nulls_visible: whether null values will be visible, defaults to True.
    :param include_nulls_value: whether to include null values, defaults to False.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param single: whether this range element is for a single sided slider, defaults to False.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.
    :param label: The label of the element, defaults to \'\'.
    :param placeholder: The placeholder of the element, defaults to \'\'.
    :param step_size: The size of default intervals between the min and max, defaults to None to automatically determine step size.

    **EXAMPLE:**
    
       .. code-block:: python

           # Imports 
           from virtualitics_sdk import NumericRange
           . . .
           # Example usage
           class ExampleStep(Step):
             def run(self, flow_metadata):
               . . . 
               num_range = NumericRange(0, 
                                        50, 
                                        max_selection=10, 
                                        single=True, 
                                        label="Slider Value",
                                        title="Single Numeric Range", 
                                        description="This is a single sided slider.",
                                        placeholder=\'Type a Number\', step_size=10)
               
    The above NumericRange will be displayed as: 

       .. image:: ../images/numeric_range_ex.png
          :align: center
          :scale: 75%
    '''
    single: Incomplete
    def __init__(self, min_range: int | float, max_range: int | float, min_selection: int | float | None = None, max_selection: int | float | None = None, include_nulls_visible: bool = True, include_nulls_value: bool = False, title: str = '', description: str = '', single: bool = False, show_title: bool = True, show_description: bool = True, label: str = '', placeholder: str = '', step_size: float | int | None = None) -> None: ...
    def get_value(self):
        """Get the value of an element. If the user has interacted with the value, the default
        will be updated.
        """
