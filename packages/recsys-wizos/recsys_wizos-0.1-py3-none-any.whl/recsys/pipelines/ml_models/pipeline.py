from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    get_cart_model_input,
    get_popular_model_input,
    get_similar_model_input,
)

base_ml_models_pipeline = pipeline(
    [
        node(
            get_cart_model_input,
            inputs={
                "produtos": "03_primary.produtos",
                "storesStock": "03_primary.storesStockSnapshot",
                "transactions": "03_primary.transactions",
                "params": "params:cart",
            },
            outputs=[
                "05_model_input.cart.produtos",
                "05_model_input.cart.stores_products",
                "05_model_input.cart.rules",
            ],
        ),
        node(
            get_popular_model_input,
            inputs={
                "produtos": "03_primary.produtos",
                "storesStock": "03_primary.storesStockSnapshot",
                "transactions": "03_primary.transactions",
                "params": "params:popular",
            },
            outputs=[
                "05_model_input.popular.produtos",
                "05_model_input.popular.store_stock",
                "05_model_input.popular.master_product_rank",
            ],
        ),
        node(
            get_similar_model_input,
            inputs={
                "produtos": "03_primary.produtos",
                "storesStock": "03_primary.storesStockSnapshot",
                "params": "params:similar",
            },
            outputs=[
                "05_model_input.similar.produtos",
                "05_model_input.similar.stores_products",
                "05_model_input.similar.produtosMestre_matrixIndices_mapping",
                "05_model_input.similar.tfidf_matrix",
            ],
        ),
    ]
)


def create_pipeline(**kwargs) -> Pipeline:
    ds_pipe = pipeline(
        base_ml_models_pipeline,
        namespace="ds",
    )

    averara_pipe = pipeline(
        base_ml_models_pipeline,
        namespace="averara",
    )

    return ds_pipe + averara_pipe
