from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import List

from openai import OpenAI
from openai.types.chat import ParsedChatCompletion
from pydantic import BaseModel

from openaivec.log import observe
from openaivec.util import map_unique_minibatch_parallel

__ALL__ = ["VectorizedOpenAI"]

_logger: Logger = getLogger(__name__)


def vectorize_system_message(system_message: str) -> str:
    return f"""
<SystemMessage>
    <ElementInstructions>
        <Instruction>{system_message}</Instruction>
    </ElementInstructions>
    <BatchInstructions>
        <Instruction>
            You will receive multiple user messages at once.
            Please provide an appropriate response to each message individually.
        </Instruction>
    </BatchInstructions>
    <Examples>
        <Example>
            <Input>
                {{
                    "user_messages": [
                        {{
                            "id": 1,
                            "text": "{{user_message_1}}"
                        }},
                        {{
                            "id": 2,
                            "text": "{{user_message_2}}"
                        }}
                    ]
                }}
            </Input>
            <Output>
                {{
                    "assistant_messages": [
                        {{
                            "id": 1,
                            "text": "{{assistant_response_1}}"
                        }},
                        {{
                            "id": 2,
                            "text": "{{assistant_response_2}}"
                        }}
                    ]
                }}
            </Output>
        </Example>
    </Examples>
</SystemMessage>
"""


class Message(BaseModel):
    id: int
    text: str


class Request(BaseModel):
    user_messages: List[Message]


class Response(BaseModel):
    assistant_messages: List[Message]


class VectorizedLLM(metaclass=ABCMeta):

    @abstractmethod
    def predict(self, user_messages: List[str]) -> List[str]:
        pass

    @abstractmethod
    def predict_minibatch(self, user_messages: List[str], batch_size: int) -> List[str]:
        pass


@dataclass(frozen=True)
class VectorizedOpenAI(VectorizedLLM):
    client: OpenAI
    model_name: str  # it would be the name of deployment for Azure
    system_message: str
    temperature: float = 0.0
    top_p: float = 1.0
    _vectorized_system_message: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "_vectorized_system_message",
            vectorize_system_message(self.system_message),
        )

    @observe(_logger)
    def request(self, user_messages: List[Message]) -> ParsedChatCompletion[Response]:
        completion = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self._vectorized_system_message},
                {
                    "role": "user",
                    "content": Request(user_messages=user_messages).model_dump_json(),
                },
            ],
            temperature=self.temperature,
            top_p=self.top_p,
            response_format=Response,
        )
        return completion

    @observe(_logger)
    def predict(self, user_messages: List[str]) -> List[str]:
        messages = [Message(id=i, text=message) for i, message in enumerate(user_messages)]
        completion = self.request(messages)
        response_dict = {
            message.id: message.text for message in completion.choices[0].message.parsed.assistant_messages
        }
        sorted_responses = [response_dict.get(m.id, None) for m in messages]
        return sorted_responses

    @observe(_logger)
    def predict_minibatch(self, user_messages: List[str], batch_size: int) -> List[str]:
        return map_unique_minibatch_parallel(user_messages, batch_size, self.predict)
