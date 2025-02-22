from _typeshed import Incomplete
from virtualitics_sdk.assets.dataset import DataEncoding as DataEncoding, Dataset as Dataset
from virtualitics_sdk.assets.explainer import Explainer as Explainer, ExplanationTypes as ExplanationTypes
from virtualitics_sdk.assets.model import Model as Model
from virtualitics_sdk.elements.element import Element as Element, ElementType as ElementType
from virtualitics_sdk.elements.xai_button import XAIButton as XAIButton

class XAIDashboard(Element):
    '''An XAI Dashboard to show the Scenario Planning Tool which allows users to interact with their data an 
    explore scenarios that may have not been included in the original dataset. Using an existing
    :class:`~virtualitics_sdk.assets.model.Model` and :class:`~virtualitics_sdk.assets.dataset.Dataset`
    users can create potential new scenarios and use XAI to analyze the model\'s prediction for these new inputs. 
    
    :param model: The model that is performing predictions on the data points.
    :param explainer: The explainer to use for the model.
    :param plot_data: The data to show on the plot.
    :param x_axis_key: The key for the X-axis on this plot.
    :param y_axis_key: The key for the Y-axis on this plot.
    :param pred_column: The column in the data the prediction lies on.
    :param title: The title of the element, defaults to \'\'.
    :param description: The element\'s description, defaults to \'\'.
    :param bounds: An optional Dict of the bounds for the data. The keys will be
                    column names and the values will be list that represent the domain, defaults to None.
    :param waterfall_positive_color: The color of positive plots in the waterfall plot, defaults to None.
    :param waterfall_negative_color: The color of negative plots in the waterfall plot, defaults to None.
    :param expected_title: The expected title to show for the :class:`~virtualitics_sdk.elements.waterfall_plot.WaterfallPlot`s generated from this dashboard, defaults to "Expected Value".
    :param predicted_title: The predited title to show for the :class:`~virtualitics_sdk.elements.waterfall_plot.WaterfallPlot`s generated from this dashboard, defaults to "Final Prediction".
    :param top_n: Show only the top N values for the waterfall plot, defaults to None.
    :param train_data: Optionally pass in a separate training :class:`~virtualitics_sdk.assets.dataset.Dataset` to use for the explainer, defaults to None
    :param encoding: The encoding of the categorical values in the dataset, Attempts to auto-determine if categorical variables are still found.
    :param color_by_category: Whether to color the scatterplot by category.
    :param show_title: whether to show the title on the page when rendered, defaults to True.
    :param show_description: whether to show the description to the page when rendered, defaults to True.

    **EXAMPLE:** 

       .. code-block:: python
           
           # Imports 
           from virtualitics_sdk import XAIDashboard
           . . .
           # Example usage
           class ExampleStep(Step):
             def run(self, flow_metadata):
               . . . 
               dash = XAIDashboard(
                    xgb,
                    explainer,
                    prediction_dataset,
                    "LandContour",
                    "PredictedPrice",
                    "PredictedPrice",
                    title="",
                    bounds=bounds,
                    description=XAIDashboard.xai_dashboard_description(),
                    train_data=explain_dataset,
                    expected_title="Avg. Listed Price",
                    predicted_title="Predicted Price",
                    encoding=DataEncoding.ONE_HOT,
                )
    '''
    bounds: Incomplete
    plot: Incomplete
    explainer_persistence: Incomplete
    pred_column: Incomplete
    title: Incomplete
    description: Incomplete
    latest_user_input: Incomplete
    content: Incomplete
    params: Incomplete
    button: Incomplete
    def __init__(self, model: Model, explainer: Explainer, plot_data: Dataset, x_axis_key: str, y_axis_key: str, pred_column: str, title: str = '', description: str = '', bounds: dict[str, list[str | int | float]] | None = None, waterfall_positive_color: str | None = None, waterfall_negative_color: str | None = None, expected_title: str | None = None, predicted_title: str | None = None, top_n: int | None = None, train_data: Dataset | None = None, encoding: DataEncoding | None = None, color_by_category: bool = False, show_title: bool = True, show_description: bool = True) -> None: ...
    @staticmethod
    def xai_dashboard_description(): ...
    def get_value(self):
        """Get the value of an element. If the user has interacted with the value, the default
           will be updated.
        """
