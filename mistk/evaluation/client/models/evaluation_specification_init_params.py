# coding: utf-8

"""
    Model Integration Software ToolKit - Metric Evaluation

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.4.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from mistk.evaluation.client.models.mistk_metric import MistkMetric  # noqa: F401,E501


class EvaluationSpecificationInitParams(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'assessment_type': 'str',
        'metrics': 'list[MistkMetric]',
        'input_data_path': 'str',
        'evaluation_input_format': 'str',
        'ground_truth_path': 'str',
        'evaluation_path': 'str',
        'properties': 'object'
    }

    attribute_map = {
        'assessment_type': 'assessment_type',
        'metrics': 'metrics',
        'input_data_path': 'input_data_path',
        'evaluation_input_format': 'evaluation_input_format',
        'ground_truth_path': 'ground_truth_path',
        'evaluation_path': 'evaluation_path',
        'properties': 'properties'
    }

    def __init__(self, assessment_type=None, metrics=None, input_data_path=None, evaluation_input_format=None, ground_truth_path=None, evaluation_path=None, properties=None):  # noqa: E501
        """EvaluationSpecificationInitParams - a model defined in Swagger"""  # noqa: E501

        self._assessment_type = None
        self._metrics = None
        self._input_data_path = None
        self._evaluation_input_format = None
        self._ground_truth_path = None
        self._evaluation_path = None
        self._properties = None
        self.discriminator = None

        self.assessment_type = assessment_type
        self.metrics = metrics
        self.input_data_path = input_data_path
        self.evaluation_input_format = evaluation_input_format
        self.ground_truth_path = ground_truth_path
        if evaluation_path is not None:
            self.evaluation_path = evaluation_path
        if properties is not None:
            self.properties = properties

    @property
    def assessment_type(self):
        """Gets the assessment_type of this EvaluationSpecificationInitParams.  # noqa: E501

        Assessment type to use for the evaluation  # noqa: E501

        :return: The assessment_type of this EvaluationSpecificationInitParams.  # noqa: E501
        :rtype: str
        """
        return self._assessment_type

    @assessment_type.setter
    def assessment_type(self, assessment_type):
        """Sets the assessment_type of this EvaluationSpecificationInitParams.

        Assessment type to use for the evaluation  # noqa: E501

        :param assessment_type: The assessment_type of this EvaluationSpecificationInitParams.  # noqa: E501
        :type: str
        """
        if assessment_type is None:
            raise ValueError("Invalid value for `assessment_type`, must not be `None`")  # noqa: E501

        self._assessment_type = assessment_type

    @property
    def metrics(self):
        """Gets the metrics of this EvaluationSpecificationInitParams.  # noqa: E501

        A list of metrics to use for the evaluation  # noqa: E501

        :return: The metrics of this EvaluationSpecificationInitParams.  # noqa: E501
        :rtype: list[MistkMetric]
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        """Sets the metrics of this EvaluationSpecificationInitParams.

        A list of metrics to use for the evaluation  # noqa: E501

        :param metrics: The metrics of this EvaluationSpecificationInitParams.  # noqa: E501
        :type: list[MistkMetric]
        """
        if metrics is None:
            raise ValueError("Invalid value for `metrics`, must not be `None`")  # noqa: E501

        self._metrics = metrics

    @property
    def input_data_path(self):
        """Gets the input_data_path of this EvaluationSpecificationInitParams.  # noqa: E501

        Path to input data for the evaluation  # noqa: E501

        :return: The input_data_path of this EvaluationSpecificationInitParams.  # noqa: E501
        :rtype: str
        """
        return self._input_data_path

    @input_data_path.setter
    def input_data_path(self, input_data_path):
        """Sets the input_data_path of this EvaluationSpecificationInitParams.

        Path to input data for the evaluation  # noqa: E501

        :param input_data_path: The input_data_path of this EvaluationSpecificationInitParams.  # noqa: E501
        :type: str
        """
        if input_data_path is None:
            raise ValueError("Invalid value for `input_data_path`, must not be `None`")  # noqa: E501

        self._input_data_path = input_data_path

    @property
    def evaluation_input_format(self):
        """Gets the evaluation_input_format of this EvaluationSpecificationInitParams.  # noqa: E501

        The format of the input data  # noqa: E501

        :return: The evaluation_input_format of this EvaluationSpecificationInitParams.  # noqa: E501
        :rtype: str
        """
        return self._evaluation_input_format

    @evaluation_input_format.setter
    def evaluation_input_format(self, evaluation_input_format):
        """Sets the evaluation_input_format of this EvaluationSpecificationInitParams.

        The format of the input data  # noqa: E501

        :param evaluation_input_format: The evaluation_input_format of this EvaluationSpecificationInitParams.  # noqa: E501
        :type: str
        """
        if evaluation_input_format is None:
            raise ValueError("Invalid value for `evaluation_input_format`, must not be `None`")  # noqa: E501
        allowed_values = ["predictions", "generations"]  # noqa: E501
        if evaluation_input_format not in allowed_values:
            raise ValueError(
                "Invalid value for `evaluation_input_format` ({0}), must be one of {1}"  # noqa: E501
                .format(evaluation_input_format, allowed_values)
            )

        self._evaluation_input_format = evaluation_input_format

    @property
    def ground_truth_path(self):
        """Gets the ground_truth_path of this EvaluationSpecificationInitParams.  # noqa: E501

        Path to ground_truth.csv file  # noqa: E501

        :return: The ground_truth_path of this EvaluationSpecificationInitParams.  # noqa: E501
        :rtype: str
        """
        return self._ground_truth_path

    @ground_truth_path.setter
    def ground_truth_path(self, ground_truth_path):
        """Sets the ground_truth_path of this EvaluationSpecificationInitParams.

        Path to ground_truth.csv file  # noqa: E501

        :param ground_truth_path: The ground_truth_path of this EvaluationSpecificationInitParams.  # noqa: E501
        :type: str
        """
        if ground_truth_path is None:
            raise ValueError("Invalid value for `ground_truth_path`, must not be `None`")  # noqa: E501

        self._ground_truth_path = ground_truth_path

    @property
    def evaluation_path(self):
        """Gets the evaluation_path of this EvaluationSpecificationInitParams.  # noqa: E501

        Path for evaluation output file  # noqa: E501

        :return: The evaluation_path of this EvaluationSpecificationInitParams.  # noqa: E501
        :rtype: str
        """
        return self._evaluation_path

    @evaluation_path.setter
    def evaluation_path(self, evaluation_path):
        """Sets the evaluation_path of this EvaluationSpecificationInitParams.

        Path for evaluation output file  # noqa: E501

        :param evaluation_path: The evaluation_path of this EvaluationSpecificationInitParams.  # noqa: E501
        :type: str
        """

        self._evaluation_path = evaluation_path

    @property
    def properties(self):
        """Gets the properties of this EvaluationSpecificationInitParams.  # noqa: E501

        A dictionary of key value pairs for evaluation plugin arguments.  # noqa: E501

        :return: The properties of this EvaluationSpecificationInitParams.  # noqa: E501
        :rtype: object
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this EvaluationSpecificationInitParams.

        A dictionary of key value pairs for evaluation plugin arguments.  # noqa: E501

        :param properties: The properties of this EvaluationSpecificationInitParams.  # noqa: E501
        :type: object
        """

        self._properties = properties

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(EvaluationSpecificationInitParams, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EvaluationSpecificationInitParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
