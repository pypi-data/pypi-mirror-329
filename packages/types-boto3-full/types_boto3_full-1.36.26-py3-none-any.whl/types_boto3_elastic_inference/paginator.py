"""
Type annotations for elastic-inference service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elastic_inference/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_elastic_inference.client import ElasticInferenceClient
    from types_boto3_elastic_inference.paginator import (
        DescribeAcceleratorsPaginator,
    )

    session = Session()
    client: ElasticInferenceClient = session.client("elastic-inference")

    describe_accelerators_paginator: DescribeAcceleratorsPaginator = client.get_paginator("describe_accelerators")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAcceleratorsRequestPaginateTypeDef,
    DescribeAcceleratorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeAcceleratorsPaginator",)


if TYPE_CHECKING:
    _DescribeAcceleratorsPaginatorBase = Paginator[DescribeAcceleratorsResponseTypeDef]
else:
    _DescribeAcceleratorsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeAcceleratorsPaginator(_DescribeAcceleratorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference/paginator/DescribeAccelerators.html#ElasticInference.Paginator.DescribeAccelerators)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elastic_inference/paginators/#describeacceleratorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAcceleratorsRequestPaginateTypeDef]
    ) -> PageIterator[DescribeAcceleratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference/paginator/DescribeAccelerators.html#ElasticInference.Paginator.DescribeAccelerators.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elastic_inference/paginators/#describeacceleratorspaginator)
        """
