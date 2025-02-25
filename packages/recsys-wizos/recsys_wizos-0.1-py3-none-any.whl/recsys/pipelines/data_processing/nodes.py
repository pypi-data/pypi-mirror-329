import re

import pandas as pd
from spacy.lang.pt.stop_words import (
    STOP_WORDS as PT_STOP_WORDS,  # Stopwords para português
)


def _optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if pd.api.types.is_integer_dtype(df[col]):
            df.loc[:, col] = pd.to_numeric(df[col], downcast="integer")
        elif pd.api.types.is_float_dtype(df[col]):
            df.loc[:, col] = pd.to_numeric(df[col], downcast="float")
        elif pd.api.types.is_object_dtype(df[col]):
            # Check wether mantain column type as obj or change to category
            num_unique_values = len(df[col].unique())
            num_total_values = len(df[col])
            if num_unique_values / num_total_values < 0.5:  # noqa: PLR2004
                df.loc[:, col] = df[col].astype("category")
    return df


def preprocess_produtos(produtos: pd.DataFrame) -> pd.DataFrame:
    def clean_colors(color):
        # Remover números e hífens, mantendo apenas letras e barras
        cleaned_color = re.sub(r"\d+|-", "", color)  # Remove números e hífens
        cleaned_color = re.sub(r"/{2,}", "/", cleaned_color)  # Remove barras duplicadas
        cleaned_color = (
            cleaned_color.strip()
        )  # Remove espaços em branco no início e no final
        return cleaned_color

    produtos = produtos[produtos.CodigoProdutoMestre.notna()]

    # Aplicar a função de limpeza
    produtos.loc[:, "Cor"] = produtos["Cor"].apply(clean_colors)
    produtos = _optimize_dtypes(produtos)

    return produtos


def preprocess_storesStockSnapshot(
    storesStock: pd.DataFrame, produtos: pd.DataFrame
) -> pd.DataFrame:
    storesStock = storesStock[storesStock.CodigoProduto.isin(produtos.CodigoProduto)]
    storesStock = _optimize_dtypes(storesStock)

    return storesStock


def preprocess_transactions(
    transactions: pd.DataFrame, produtos: pd.DataFrame
) -> pd.DataFrame:
    transactions = transactions[transactions.CodigoProduto.isin(produtos.CodigoProduto)]
    transactions = _optimize_dtypes(transactions)

    return transactions


def _cantor_pair(k1, k2, safe=True):
    """
    Cantor pairing function
    http://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function
    """
    z = 0.5 * (k1 + k2) * (k1 + k2 + 1) + k2
    if safe:
        try:
            if (k1, k2) != _cantor_depair(z):
                raise ValueError(f"{k1} and {k2} cannot be paired")
        except ValueError:
            t1, t2 = _cantor_depair(z)
            if not (k1.equals(t1) and k2.equals(t2)):
                raise ValueError(f"{k1} and {k2} cannot be paired")
    try:
        z = int(z)
    except TypeError:
        z = z.astype(int)

    return z


def _cantor_depair(z):
    """
    Inverse of Cantor pairing function
    http://en.wikipedia.org/wiki/Pairing_function#Inverting_the_Cantor_pairing_function
    """
    w = (((8 * z + 1) ** (1 / 2) - 1) / 2) // 1
    t = (w**2 + w) / 2
    try:
        y = int(z - t)
        x = int(w - y)
    except TypeError:
        y = (z - t).astype(int)
        x = (w - y).astype(int)

    # assert z != cantor_pairing(x, y, safe=False):
    return x, y


def _generate_tags(text):
    """Função para gerar TAGs mantendo o texto em maiúsculas"""
    if pd.isna(text):
        return ""
    words = re.findall(
        r"\b[A-Z]+\b", text
    )  # Extrair apenas palavras alfanuméricas em maiúsculas
    tags = [
        word for word in words if word.lower() not in PT_STOP_WORDS
    ]  # Remover stopwords (usando versão minúscula para comparar)
    return ", ".join(tags)


def _get_pop_products_7D(transactions: pd.DataFrame) -> pd.DataFrame:
    last_7D = pd.to_datetime("today").normalize() - pd.DateOffset(
        days=7, normalize=True
    )

    return (
        transactions.loc[transactions.Criacao >= last_7D]
        .groupby("CodigoProdutoMestre", observed=True)["Total"]
        .sum()
    )


def _transform_grendene_brand(x: pd.Series) -> pd.Series:
    return x.mask(
        x.str.contains("GRENDHA")
        | x.str.contains("ZAXY")
        | x.str.contains("RIDER")
        | x.str.contains("CARTAGO")
        | x.str.contains("IPANEMA")
        | x.str.contains("AZALEIA"),
        "GRENDENE",
    )


def process_produtos(
    produtos: pd.DataFrame, transactions: pd.DataFrame
) -> pd.DataFrame:
    produtos = produtos.set_index("CodigoProduto")

    def _get_vitrine(v: str) -> pd.Series:
        try:
            return produtos[v].cat.add_categories("").fillna("").astype(str)
        except AttributeError:
            return produtos[v].fillna("").astype(str)

    columns_to_extract_tags_from = ["Descricao", "Marca", "Vitrines"]

    v1, v2, v3, v4 = (
        _get_vitrine("Vitrine1"),
        _get_vitrine("Vitrine2"),
        _get_vitrine("Vitrine3"),
        _get_vitrine("Vitrine4"),
    )

    produtos["Vitrines"] = (v1 + " " + v2 + " " + v3 + " " + v4).str.strip()
    produtos["TAGS"] = (
        produtos[columns_to_extract_tags_from]
        .map(_generate_tags)
        .apply(lambda row: ", ".join(row), axis=1)
    )
    produtos["Marca"] = _transform_grendene_brand(produtos["Marca"])

    t = (
        _get_pop_products_7D(transactions)
        .reindex(produtos.CodigoProdutoMestre)
        .fillna(0)
        .reset_index()
    )
    t["CodigoProduto"] = produtos.index
    produtos = produtos.join(t.set_index("CodigoProduto")["Total"])

    return produtos


def process_transactions(
    transactions: pd.DataFrame, processed_produtos: pd.DataFrame
) -> pd.DataFrame:
    transactions = transactions.merge(
        processed_produtos[["Vitrines", "Tamanho", "Cor"]],
        how="left",
        left_on="CodigoProduto",
        right_index=True,
    )
    transactions["Atendimento_ID"] = _cantor_pair(
        transactions.Id, transactions.Loja_Codigo, safe=False
    )

    return transactions


def process_storesStockSnapshot(storesStock: pd.DataFrame) -> pd.DataFrame:
    return storesStock
