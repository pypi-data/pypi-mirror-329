import os

from blue_objects import file, README

from blue_cemetery import NAME, VERSION, ICON, REPO_NAME


items = README.Items(
    [
        {
            "name": "sagesemseg",
            "description": "A SemSeg (Semantic Segmenter) trained and deployed on AWS Sagemaker.",
            "url": "./blue_sandbox/sagesemseg/README.md",
            "marquee": "https://github.com/kamangir/assets/blob/main/blue-sandbox/sagesemseg-predict.png?raw=true",
        },
        {
            "name": "@damages",
            "description": "Satellite imagery damage assessment workflow",
            "url": "./blue_sandbox/microsoft_building_damage_assessment/README.md",
            "marquee": "https://github.com/kamangir/assets/raw/main/blue-sandbox/Maui-Hawaii-fires-Aug-23-ingest-2025-01-10-qqJqhm.png?raw=true",
        },
        {
            "name": "VisuaLyze",
            "description": 'How about calling it "VisuaLyze"? ... - OpenAI',
            "url": "./blue_sandbox/VisuaLyze",
            "marquee": "https://github.com/kamangir/openai-commands/assets/1007567/7c0ed5f7-6941-451c-a17e-504c6adab23f",
        },
        {
            "name": "gpt",
            "description": "co-authored with ChapGPT.",
            "url": "./blue_sandbox/cemetery/gpt",
        },
        {
            "name": "code generation",
            "marquee": "https://github.com/kamangir/openai-commands/blob/main/assets/completion_i2i_function.png?raw=true",
            "url": "./blue_sandbox/cemetery/code_generation",
        },
        {
            "name": "scripts",
            "description": "legacy mechanisms replaced with `@docker eval - <command>` and `@batch eval - <command>`.",
            "marquee": "https://github.com/kamangir/assets/blob/main/nbs/3x4.jpg?raw=true",
            "url": "./scripts",
        },
    ]
)


def build():
    return README.build(
        items=items,
        path=os.path.join(file.path(__file__), ".."),
        ICON=ICON,
        NAME=NAME,
        VERSION=VERSION,
        REPO_NAME=REPO_NAME,
    )
