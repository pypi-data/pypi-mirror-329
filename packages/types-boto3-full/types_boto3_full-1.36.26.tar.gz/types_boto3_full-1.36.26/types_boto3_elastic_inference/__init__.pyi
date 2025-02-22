"""
Main interface for elastic-inference service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elastic_inference/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_elastic_inference import (
        Client,
        DescribeAcceleratorsPaginator,
        ElasticInferenceClient,
    )

    session = Session()
    client: ElasticInferenceClient = session.client("elastic-inference")

    describe_accelerators_paginator: DescribeAcceleratorsPaginator = client.get_paginator("describe_accelerators")
    ```
"""

from .client import ElasticInferenceClient
from .paginator import DescribeAcceleratorsPaginator

Client = ElasticInferenceClient

__all__ = ("Client", "DescribeAcceleratorsPaginator", "ElasticInferenceClient")
