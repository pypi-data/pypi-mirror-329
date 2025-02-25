from typing import Any

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from scipy.sparse import spmatrix
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.pt.stop_words import (
    STOP_WORDS as PT_STOP_WORDS,  # Stopwords para português
)


def _agg_as_list(
    df: pd.DataFrame, groupby_col: str, agg_col: str, return_df=False
) -> dict[Any, list[Any]]:
    df = df[[groupby_col, agg_col]].sort_values(groupby_col)
    keys = df[groupby_col].values
    values = df[agg_col].values
    ukeys, index = np.unique(keys, True)
    arrays = np.split(values, index[1:])
    if return_df:
        return pd.DataFrame({groupby_col: ukeys, agg_col: [list(a) for a in arrays]})
    return {k: np.unique(v) for k, v in zip(ukeys, arrays)}


def _select_features_from_dataset(df: pd.DataFrame, features: list[str]):
    return df[features]


def get_popular_model_input(
    produtos: pd.DataFrame,
    transactions: pd.DataFrame,
    storesStock: pd.DataFrame,
    params: dict[str, dict[str, list[str]]],
):
    def get_popular_store_stock(storesStock: pd.DataFrame):
        store_stock = {}
        store_stock["stores_master_products"] = _agg_as_list(
            storesStock, "Loja", "CodigoProdutoMestre"
        )
        store_stock["stores_products"] = _agg_as_list(
            storesStock, "Loja", "CodigoProduto"
        )
        return store_stock

    def get_master_product_rank(
        transactions: pd.DataFrame, produtos: pd.DataFrame
    ) -> pd.DataFrame:
        return (
            transactions.groupby("CodigoProdutoMestre", observed=True)[
                ["Quantidade", "Total"]
            ]
            .agg(
                **{
                    "QuantidadeTotal": ("Quantidade", "sum"),
                    "QuantidadeSessions": ("Quantidade", "count"),
                    "FaturamentoTotal": ("Total", "sum"),
                }
            )
            .sort_values(by="FaturamentoTotal", ascending=False)
        ).join(
            produtos.drop(columns=["Tamanho", "Cor"])
            .groupby("CodigoProdutoMestre", observed=False)
            .first()
        )

    # Selecting Features
    produtos = _select_features_from_dataset(produtos, params["produtos"]["features"])
    transactions = _select_features_from_dataset(
        transactions, params["transactions"]["features"]
    )
    storesStock = _select_features_from_dataset(
        storesStock, params["storesStock"]["features"]
    )

    # Generating and Saving Model's input
    store_stock = get_popular_store_stock(storesStock)
    master_product_rank = get_master_product_rank(transactions, produtos)

    return (produtos, store_stock, master_product_rank)


def get_similar_model_input(
    produtos: pd.DataFrame,
    storesStock: pd.DataFrame,
    params: dict[str, dict[str, list[str]]],
    only_stock=False,
):
    def get_produtos_pai(produtos: pd.DataFrame) -> pd.DataFrame:
        return (
            produtos[["CodigoProdutoMestre", "TAGS"]]
            .drop_duplicates(subset=["CodigoProdutoMestre", "TAGS"])
            .reset_index(drop=True)
        )

    def create_tfidf_matrix(artigo: pd.DataFrame) -> spmatrix:
        """Função para calcular a matriz TF-IDF"""
        # Criar um vetorizador TF-IDF
        tfidf_vectorizer = TfidfVectorizer(stop_words=list(PT_STOP_WORDS))

        # Aplicar TF-IDF às descrições dos itens
        tfidf_matrix_content = tfidf_vectorizer.fit_transform(artigo["TAGS"])

        # Retornar a matriz TF-IDF e o vetor TF-IDF
        return tfidf_matrix_content

    # Selecting Features
    produtos = _select_features_from_dataset(produtos, params["produtos"]["features"])
    storesStock = _select_features_from_dataset(
        storesStock, params["storesStock"]["features"]
    )

    # Generating and Saving Model's input
    stores_products = _agg_as_list(storesStock, "Loja", "CodigoProduto")

    produtos_pai = get_produtos_pai(produtos)
    produtosMestre_matrixIndices_mapping = {
        v: k for k, v in produtos_pai.CodigoProdutoMestre.to_dict().items()
    }
    tfidf_matrix = create_tfidf_matrix(produtos_pai)

    return produtos, stores_products, produtosMestre_matrixIndices_mapping, tfidf_matrix


def get_cart_model_input(
    produtos: pd.DataFrame,
    transactions: pd.DataFrame,
    storesStock: pd.DataFrame,
    params: dict[str, dict[str, list[str]]],
    # only_stock=False,
):
    def get_rules(transactions: pd.DataFrame) -> pd.DataFrame:
        atendimento_vitrines = _agg_as_list(
            transactions, "Atendimento_ID", "Vitrines", return_df=True
        )
        transactions_list = [
            [str(item) for item in sublist if pd.notnull(item)]
            for sublist in atendimento_vitrines["Vitrines"]
        ]
        # Converte a lista de listas para formato binário
        te = TransactionEncoder()
        te_array = te.fit(transactions_list).transform(transactions_list)
        df = pd.DataFrame(te_array, columns=te.columns_).astype(int)
        frequent_itemsets = apriori(
            df, min_support=0.001, use_colnames=True, max_len=2, low_memory=True
        )
        rules = association_rules(
            frequent_itemsets, metric="lift", min_threshold=1.0, num_itemsets=len(df)
        )
        return rules.sort_values("lift", ascending=False)

    # Selecting Features
    produtos = _select_features_from_dataset(produtos, params["produtos"]["features"])
    transactions = _select_features_from_dataset(
        transactions, params["transactions"]["features"]
    )
    storesStock = _select_features_from_dataset(
        storesStock, params["storesStock"]["features"]
    )

    # Generating and Saving Model's input
    stores_products = _agg_as_list(storesStock, "Loja", "CodigoProduto")

    rules = get_rules(transactions)

    return produtos, stores_products, rules
