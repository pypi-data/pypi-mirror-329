from enum import Enum

from ai_clients.base.types import ExtendBaseModel


class CodestralModels(Enum):
    codestral_2501 = 'codestral-2501'
    codestral_mamba_2407 = 'codestral-mamba-2407'


class CompletionMessage(ExtendBaseModel):
    role: str
    content: str


class CompletionPrediction(ExtendBaseModel):
    content: str
    type: str = 'content'


class CompletionMessageRequest(ExtendBaseModel):
    messages: list[CompletionMessage]
    model: str = CodestralModels.codestral_2501.value
    prediction: CompletionPrediction | None = None
    temperature: int | None = None


class CompletionResponseUsage(ExtendBaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResponseChoiceMessage(ExtendBaseModel):
    content: str
    role: str
    prefix: bool | None = None
    tool_calls: list[dict] | None = None


class CompletionResponseChoice(ExtendBaseModel):
    index: int
    message: CompletionResponseChoiceMessage
    finish_reason: str


class CompletionResponse(ExtendBaseModel):
    id: str
    object: str
    model: str
    usage: CompletionResponseUsage
    created: int
    choices: list[CompletionResponseChoice]
