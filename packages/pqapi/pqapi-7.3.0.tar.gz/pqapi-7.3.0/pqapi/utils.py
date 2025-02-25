import os
import random
from ast import literal_eval


def get_pqa_key() -> str:
    if "PQA_API_KEY" in os.environ:
        return os.environ["PQA_API_KEY"]
    if "PQA_API_TOKEN" in os.environ:
        return os.environ["PQA_API_TOKEN"]
    raise KeyError("PQA_API_KEY environment variable not set.")


def get_pqa_url() -> str:
    return os.environ.get("PQA_URL", "https://prod.api.paperqa.app")


# Special case for LitQA, when ideal == "null"
UNSURE_OPTION = "Insufficient information to answer this question"
_CAPITAL_A_INDEX = ord("A")


def make_mc_options(
    ideal: str, distractors: str | list[str], unsure_option: str | None = UNSURE_OPTION
) -> tuple[str, str, str | None]:
    """
    Return string of options (as letters) and correct answer.

    Source: https://github.com/Future-House/data-pipelines/blob/7f8d18b1f1a98c2bb370fbac138f4de2fa2bb02c/mae_platform/mae_platform/pqa_ops.py#L650
    """
    if isinstance(distractors, str):
        try:
            split_distractors = literal_eval(distractors)
            if not isinstance(split_distractors, list):
                raise TypeError("Need split_distractors to be a list.")  # noqa: TRY301
        except (ValueError, SyntaxError, TypeError):
            split_distractors = [d.strip("'[ ]\"") for d in distractors.split(",")]
        options: list[str] = split_distractors
    else:
        options = distractors

    if ideal == "null":
        if not unsure_option:
            raise ValueError(
                'Dataset configured for "unsure" options via '
                'ideal="null", please specify "unsure_option".'
            )
        correct_answer = unsure_option
    else:
        # add the answer to the options, only if not null
        options.append(ideal)
        correct_answer = ideal

    if unsure_option:
        options.append(unsure_option)

    random.shuffle(options)
    return (
        "\n".join([f"{_CAPITAL_A_INDEX + i:c}) {o}" for i, o in enumerate(options)]),
        chr(_CAPITAL_A_INDEX + options.index(correct_answer)),
        chr(_CAPITAL_A_INDEX + options.index(unsure_option)) if unsure_option else None,
    )
