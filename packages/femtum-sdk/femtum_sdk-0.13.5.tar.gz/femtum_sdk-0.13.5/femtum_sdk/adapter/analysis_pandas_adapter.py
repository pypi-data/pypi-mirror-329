from femtum_sdk.adapter.tags_adapter import ApplyTagsToDataframe
import pandas as pd
from femtum_sdk.core.result_pb2 import (
    SpectrumResult,
)


def SweepResulToDataframe(
    item: SpectrumResult,
    with_tags: bool = False,
) -> pd.DataFrame:
    dataframeDict = {
        "Powers": list(map(float, item.PowersArray)),
        "Wavelengths": list(map(float, item.WavelengthsArray)),
    }

    dataframe = pd.DataFrame(dataframeDict)

    if with_tags is True:
        dataframe = ApplyTagsToDataframe(dataframe, item.Tags)

    return dataframe
