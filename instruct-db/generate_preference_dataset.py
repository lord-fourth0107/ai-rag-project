from typing import Any

from typing_extensions import Annotated
# from zenml import ArtifactConfig, get_step_context, step

from models.instruct_db import generation
from models.instruct_db.dataset import DatasetType, PreferenceTrainTestSplit
from models.rag_base.prompt import GenerateDatasetSamplesPrompt
from models.dataCategory import DataCategory


# @step
def generate_preference_dataset(
    prompts: Annotated[dict[DataCategory, list[GenerateDatasetSamplesPrompt]], "prompts"],
    test_split_size: Annotated[float, "test_split_size"],
    mock: Annotated[bool, "mock_generation"] = False,
):
    dataset_generator = generation.get_dataset_generator(DatasetType.PREFERENCE)
    datasets = dataset_generator.generate(prompts, test_size=test_split_size, mock=mock)


    return datasets


def _get_metadata_preference_dataset(datasets: PreferenceTrainTestSplit) -> dict[str, Any]:
    instruct_dataset_categories = list(datasets.train.keys())
    train_num_samples = {
        category: instruct_dataset.num_samples for category, instruct_dataset in datasets.train.items()
    }
    test_num_samples = {category: instruct_dataset.num_samples for category, instruct_dataset in datasets.test.items()}

    return {
        "data_categories": instruct_dataset_categories,
        "test_split_size": datasets.test_split_size,
        "train_num_samples_per_category": train_num_samples,
        "test_num_samples_per_category": test_num_samples,
    }
