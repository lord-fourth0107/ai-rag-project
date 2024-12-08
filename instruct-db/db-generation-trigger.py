import sys
import os

# Add the parent directory of 'models' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import query_feature_store,create_prompts, push_to_huggingface
from query_feature_store import query_feature_store
from generate_instruction_dataset import generate_intruction_dataset
from generate_preference_dataset import generate_preference_dataset
from create_prompts import create_prompts
from models.instruct_db.dataset import DatasetType
# @ step
def generate_datasets(
    dataset_type: DatasetType = DatasetType.INSTRUCTION,
    test_split_size: float = 0.1,
    push_to_hf: bool = False,
    dataset_id: str | None = None,
    mock: bool = False,
    wait_for: str | list[str] | None = None,
) -> None:
    cleaned_documents = query_feature_store()
    prompts = create_prompts(documents=cleaned_documents, dataset_type=dataset_type)
    if dataset_type == DatasetType.INSTRUCTION:
        dataset = generate_intruction_dataset(prompts=prompts, test_split_size=test_split_size, mock=mock)
    elif dataset_type == DatasetType.PREFERENCE:
        dataset = generate_preference_dataset(prompts=prompts, test_split_size=test_split_size, mock=mock)
    else:
        raise ValueError(f"Invalid dataset type: {dataset_type}")

    if push_to_hf:
        push_to_huggingface.push_to_huggingface(dataset=dataset, dataset_id=dataset_id)

generate_datasets(push_to_hf=True,dataset_id="nsh22/ai-rag-ros-instruction-dataset")