from _typeshed import Incomplete
from virtualitics_sdk.app.flow_metadata import FlowMetadata as FlowMetadata
from virtualitics_sdk.assets.dataset import DataEncoding as DataEncoding
from virtualitics_sdk.assets.explainer import Explainer as Explainer
from virtualitics_sdk.elements.custom_event import CustomEvent as CustomEvent
from virtualitics_sdk.elements.infograph import InfographData as InfographData, InfographDataType as InfographDataType, Infographic as Infographic
from virtualitics_sdk.elements.plot import Plot as Plot
from virtualitics_sdk.elements.waterfall_plot import WaterfallPlot as WaterfallPlot
from virtualitics_sdk.elements.xai_dashboard import XAIDashboard as XAIDashboard

class XAIButton(CustomEvent):
    waterfall_positive: Incomplete
    waterfall_negative: Incomplete
    dashboard_id: Incomplete
    pred_column: Incomplete
    expected_title: Incomplete
    predicted_title: Incomplete
    encoding: Incomplete
    top_n: Incomplete
    titles: Incomplete
    def __init__(self, dashboard_title: str, dashboard_id: str, pred_column: str, encoding: str | DataEncoding | None = None, titles: list[str] | None = None, _id: str | None = None, waterfall_positive_color: str | None = None, waterfall_negative_color: str | None = None, expected_title: str | None = None, predicted_title: str | None = None, top_n: int | None = None) -> None: ...
    def out_of_range_info(self, feats: list[str], point: dict[str, int | float], bounds: dict[str, list[str | int]]) -> InfographData: ...
    def instance_exp_info(self, pred, spt_exp) -> InfographData: ...
    def estimate_diff_info(self, diff: int | float) -> InfographData: ...
    def data_likelihood_info(self, explainer: Explainer, instance) -> InfographData: ...
    def process_frontend_input(self, point: dict, categorical_names: list[str], dashboard: XAIDashboard) -> dict:
        """Preprocess frontend categorical inputs to be default one-hot
        """
    def postprocess_backend_output(self, point: dict, categorical_names: list[str], dashboard: XAIDashboard):
        """Postprocess backend one hot to be default verbose
        """
    def callback(self, flow_metadata: FlowMetadata, **step_clients) -> str | dict: ...
