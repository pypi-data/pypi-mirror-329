"""Pydantic models for the input parameters of the model."""

import logging
from typing import Dict, Union

from pydantic import BaseModel, Field, conlist, field_validator
from pyproj import CRS
from pyproj.exceptions import CRSError

logger = logging.getLogger(__name__)


def pprint_pydantic_validation_error(validation_error):
    """Pretty print a Pydantic validation error."""
    errors = validation_error.errors()
    full_message = ""
    for error in errors:
        loc = " -> ".join(map(str, error["loc"]))
        msg = error["msg"]
        error_type = error["type"]
        full_message += f"Error in {loc}: {msg} (type={error_type})\n"

    return full_message


def check_projection_format(v):
    """Check that the projection starts with EPSG.

    If you ever want to include non euclidean coordinate systems, beware of the
    downstream concequences. This includes but is not limited in the time of writing
    DataStreamer.create_size().
    The function is used as a field validator in the InputParameters class and for a
    validator in the html form in the cosmopolitan web service.
    """
    if v is None:
        return v

    if not v.startswith("EPSG"):
        raise ValueError("Projection must start with EPSG")

    try:
        crs = CRS.from_user_input(v)
    except CRSError as e:
        raise ValueError(f"Invalid projection: {e}")

    if not crs.is_projected:
        raise ValueError("CRS must be an euclidean coordinate system")
    return v


class PredictorInformation(BaseModel):
    """Data model for the predictor data."""

    file_path: Union[str, None] = Field(
        ..., description="The path to the csv file with the predictor data."
    )
    unit: str = Field(
        ..., description="Unit of the predictor (can be an empty string)."
    )
    std_deviation: bool = Field(
        ...,
        description="Whether the csv has an addiational column with the standard deviation. If std_deviation is True and constant is False, the standard deviation will be assumed in the fourth column.",  # noqa
    )
    constant: bool = Field(
        ...,
        description="Whether the csv has no addiational column with the time. If std_deviation is True and constant is False, the standard deviation will be assumed in the fourth coclumn.",  # noqa
    )
    nan_value: str = Field(
        ...,
        description="The value that represents NaN in the csv file (can be an empty string).",  # noqa
    )


class PredictorInformationHeader(PredictorInformation):
    """Data model for the predictor data provide by the header."""

    predictor_name: str = Field(
        ..., description="The name of the predictor (e.g. 'elevation')."
    )


class WhatToPlot(BaseModel):
    """List of which plotting functions should be used."""

    # TODO - Add descriptions to the fields
    alldays_predictor_importance: bool
    day_measurements: bool
    day_prediction_map: bool
    day_predictor_importance: bool
    pred_correlation: bool
    predictors: bool
    prediction_distance: bool


class InputParameters(BaseModel):
    """Data model for the input parameters."""

    geometry: conlist(float, min_length=5, max_length=5) = Field(
        ...,
        description="A list of five numbers representing the bounding box. [xmin, xmax, ymin, ymax, resolution].",  # noqa
    )
    projection: Union[str, None] = Field(
        ...,
        description="The projection of the bounding box e.g. EPSG:25832",
    )
    soil_moisture_data: str = Field(
        ...,
        description="The path to the soil moisture data.",
    )
    predictors: Dict[str, Union[PredictorInformation, None]] = Field(
        ...,
        description="A dictionary of predictors. Either provide one of the predefined predictors (e.g. 'corine') with None or provide a predictor information model.",  # noqa
    )
    monte_carlo_soil_moisture: bool = Field(
        ...,
        description="Whether to use a Monte Carlo Simulation to predict uncertainty for soil moisture.",  # noqa
    )
    monte_carlo_predictors: bool = Field(
        ...,
        description="Whether to use a Monte Carlo Simulation to predict uncertainty for the predictors.",  # noqa
    )
    monte_carlo_iterations: int = Field(
        ..., description="Number of iterations for the Monte Carlo Simulation."
    )
    allow_nan_in_training: bool = Field(
        ...,
        description="Whether to allow NaN values in the training data.",
    )
    predictor_qmc_sampling: bool = Field(
        ...,
        description="Whether to use Quasi-Monte Carlo sampling for the predictors.",
    )
    compute_slope: bool = Field(
        ...,
        description="Whether to compute the slope from elevation and use as predictor.",
    )
    compute_aspect: bool = Field(
        ...,
        description="Whether to compute the aspect from elevation and use as predictor.",  # noqa
    )
    past_prediction_as_feature: bool = Field(
        ..., description="Whether to use the past prediction as a feature."
    )
    what_to_plot: WhatToPlot = Field(
        ..., description="List of which plotting functions should be used."
    )  # noqa
    save_results: bool = Field(
        ...,
        description="Dump random forest model. Reload it and use it for predictions.",
    )
    save_input_data: bool = Field(
        ..., description="Dump input data. Quicker to reload the data."
    )

    @field_validator("projection")
    def check_projection_format(cls, v):
        """Check that the projection starts with EPSG."""
        return check_projection_format(v)
