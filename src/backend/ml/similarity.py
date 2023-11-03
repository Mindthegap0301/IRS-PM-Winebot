import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from scipy import spatial
from pathlib import Path

# Load task word embeddings
path = Path(__file__).parent / "embeddings.pkl"
embeddings_df = pd.read_pickle(path)

# Load model
# model = SentenceTransformer('./output/simcse-distileroberta-base-pca-128')
model_path = str(Path(__file__).parent) + "/simcse-distileroberta-base-pca-128"
model = SentenceTransformer(model_path)

csv_path = str(Path(__file__).parent) + "/merged_product_info_list_embedding.csv"


class SimilarityCalculator:
    def __init__(
        self,
        product,
        description_input,
        taste_exp_input,
        variety_input,
        pairing_input,
        price_input,
        priority="general",
    ):
        self.product = product
        self.description_input = description_input
        self.taste_exp_input = taste_exp_input
        self.variety_input = variety_input
        self.pairing_input = pairing_input
        self.price_input = price_input

        self.priority_weights = (
            {
                "description": 0.6,
                "taste_exp": 0.6,
                "variety": 0.2,
                "pairing": 0.1,
                "price": 0.1,
            }
            if priority == "flavour"
            else {
                "description": 0.4,
                "taste_exp": 0.8,
                "variety": 0.2,
                "pairing": 0.1,
                "price": 0.1,
            }
            if priority == "on_budget"
            else {
                "description": 0.4,
                "taste_exp": 0.4,
                "variety": 0.1,
                "pairing": 0.1,
                "price": 0.6,
            }
            if priority == "suitable_for_meal"
            else {
                "description": 0.4,
                "taste_exp": 0.4,
                "variety": 0.1,
                "pairing": 0.6,
                "price": 0.1,
            }
            if priority == "brand_first"
            else {
                "description": 0.4,
                "taste_exp": 0.4,
                "variety": 0.6,
                "pairing": 0.1,
                "price": 0.1,
            }
        )

        self.build_products_df()

    def build_products_df(self):
        # Build an products dataframe from `products` database table
        products_df = pd.read_csv(csv_path)

        # Merge sentence embeddings
        # products_df = products_df.merge(
        # embeddings_df, on="id", suffixes=("_df1", "_df2"), how="inner"
        # )

        self.products_df = products_df

    def calc_cosine_similarity(self, input, type, column_name="similarity"):
        data = pd.DataFrame(self.products_df).copy()
        input_vector = model.encode(input)
        if input_vector is None or len(input_vector) == 0:
            return None
        input_vector = input_vector.reshape(-1)
        embeddings = data[type + "_embedding"]
        if embeddings.isnull().values.any():
            data[column_name] = embeddings.apply(lambda x: 0)
        else:
            data[column_name] = embeddings.apply(
                lambda x: 1
                - spatial.distance.cosine(np.fromstring(x[1:-1], sep=" "), input_vector)
            )
        return data[["id", column_name]]

    def calc_euclidean_similarity(self, input_vector, column_name="similarity"):
        data = self.products_df.copy()
        columns = input_vector.keys()
        values = input_vector.values()

        def calc_distance(x):
            if x.isnull().any():
                return 0
            return 1 / (1 + spatial.distance.euclidean(list(values), x))

        data[column_name] = data[columns].agg(calc_distance, axis=1)
        return data[["id", column_name]]

    def calc_price_penalty(self, value, input):
        if value and input:
            # z = adjusted by Standard Deviations
            diff = (input - value) / 30.0

            if diff > 0:
                return 0
            elif diff < -1:
                return -1
            else:
                return diff
        else:
            return 0

    def calc_price_penalties(self, input, column_name="similarity"):
        data = self.products_df.copy()
        data[column_name] = data["product_price"].apply(
            lambda x: self.calc_price_penalty(x, input)
        )
        return data[["id", column_name]]

    def get_all_similar(self):
        description_similarity = self.calc_cosine_similarity(
            self.description_input, "average", "description_similarity"
        )
        taste_exp_similarity = self.calc_cosine_similarity(
            self.taste_exp_input, "taste_description", "taste_exp_similarity"
        )
        variety_similarity = self.calc_cosine_similarity(
            self.variety_input, "varietal_description", "variety_similarity"
        )
        pairing_similarity = self.calc_cosine_similarity(
            self.pairing_input, "pair", "pairing_similarity"
        )
        price_similarity = self.calc_price_penalties(
            self.price_input, "price_similarity"
        )

        return (
            description_similarity,
            taste_exp_similarity,
            variety_similarity,
            pairing_similarity,
            price_similarity,
        )

    def aggregate_similarity(self, row):
        return (
            self.priority_weights["description"] * row["description_similarity"]
            + self.priority_weights["taste_exp"] * row["taste_exp_similarity"]
            + self.priority_weights["variety"] * row["variety_similarity"]
            + self.priority_weights["pairing"] * row["pairing_similarity"]
            + self.priority_weights["price"] * row["price_similarity"]
        )

    def get_recommendation(self, n=10, as_dict=True):
        (
            description_similarity,
            taste_exp_similarity,
            variety_similarity,
            pairing_similarity,
            price_similarity,
        ) = self.get_all_similar()
        merge_df = (
            description_similarity.merge(
                taste_exp_similarity.merge(variety_similarity, on="id"), on="id"
            )
            .merge(pairing_similarity, on="id")
            .merge(price_similarity, on="id")
            .set_index("id")
        )
        merge_df["score"] = merge_df[
            [
                "description_similarity",
                "taste_exp_similarity",
                "variety_similarity",
                "pairing_similarity",
                "price_similarity",
            ]
        ].agg(self.aggregate_similarity, axis=1)
        merge_df = merge_df.sort_values("score", ascending=False)
        merge_df = merge_df.rename(index={"id": "product_id"})
        return merge_df[:n].to_dict(orient="index") if as_dict else merge_df[:n]
