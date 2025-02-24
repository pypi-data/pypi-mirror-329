This is a Python package for VDC: Versatile Data Cleanser Based on Semantic Inconsistency.

## Installation

```bash
pip install vdc
```

## Usage

```python
from vdc.cleanser import DataCleanser
from vdc.utils.config import VDCConfig

config = VDCConfig(
    llm_base_url="https://api.openai.com/v1/",
    llm_api_key="sk-xxx",
    mllm_base_url="https://api.openai.com/v1/",
    mllm_api_key="sk-xxx",
)

cleanser = DataCleanser(
    config=config, llm_model="gpt-4o-mini", mllm_model="gpt-4o-mini"
)

res = cleanser.process_image_text_pair(
    img_path="test.jpeg",
    text="A black cat is sitting on a wooden table.",
    num_questions=5,
)

consistency_score = res.consistency_score   
is_consistent = res.is_consistent

print(res)
```