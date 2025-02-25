from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    preprocess_produtos,
    preprocess_storesStockSnapshot,
    preprocess_transactions,
    process_produtos,
    process_storesStockSnapshot,
    process_transactions,
)

base_data_processing_pipeline = pipeline(
    [
        node(
            preprocess_produtos,
            inputs="01_raw.produtos",
            outputs="02_intermediate.produtos",
            namespace="intermediate_nodes",
        ),
        node(
            preprocess_storesStockSnapshot,
            inputs=["01_raw.storesStockSnapshot", "02_intermediate.produtos"],
            outputs="02_intermediate.storesStockSnapshot",
            namespace="intermediate_nodes",
        ),
        node(
            preprocess_transactions,
            inputs=["01_raw.transactions", "02_intermediate.produtos"],
            outputs="02_intermediate.transactions",
            namespace="intermediate_nodes",
        ),
        node(
            process_produtos,
            inputs=[
                "02_intermediate.produtos",
                "02_intermediate.transactions",
            ],
            outputs="03_primary.produtos",
            namespace="primary_nodes",
        ),
        node(
            process_storesStockSnapshot,
            inputs="02_intermediate.storesStockSnapshot",
            outputs="03_primary.storesStockSnapshot",
            namespace="primary_nodes",
        ),
        node(
            process_transactions,
            inputs=["02_intermediate.transactions", "03_primary.produtos"],
            outputs="03_primary.transactions",
            namespace="primary_nodes",
        ),
    ],
)


def create_pipeline(**kwargs) -> Pipeline:
    ds_pipe = pipeline(
        base_data_processing_pipeline,
        namespace="ds",
    )

    averara_pipe = pipeline(
        base_data_processing_pipeline,
        namespace="averara",
    )

    return ds_pipe + averara_pipe
