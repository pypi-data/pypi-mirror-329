from femtum_sdk.core.tag_pb2 import Tag
import pandas as pd


def ApplyTagsToDataframe(
    dataframe: pd.DataFrame,
    tags: list[Tag],
) -> pd.DataFrame:

    for tag in tags:
        dataframe[tag.Key] = tag.Value if tag.Value else True

    return dataframe
