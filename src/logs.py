from __future__ import annotations

from typing import List, Optional, Union

import pydantic
from pydantic import BaseModel

import src.commons as com
from src.enums import ApiActions, ApiParams, Const, Modules


class TopicOperator(BaseModel):
    topic_a: ApiParams
    topic_b: ApiParams
    operator: Const

    @pydantic.root_validator()
    @classmethod
    def validate_input(cls, field_values):
        assert (
            field_values["topic_a"] != field_values["topic_b"]
        ), "topics must be different"
        assert (
            field_values["topic_a"]
            in [
                ApiParams.TOPIC_0,
                ApiParams.TOPIC_1,
                ApiParams.TOPIC_2,
                ApiParams.TOPIC_3,
            ]
        ) and (
            field_values["topic_b"]
            in [
                ApiParams.TOPIC_0,
                ApiParams.TOPIC_1,
                ApiParams.TOPIC_2,
                ApiParams.TOPIC_3,
            ]
        ), "Invalid topic"
        assert field_values["operator"] in [
            Const.OPERATOR_AND,
            Const.OPERATOR_OR,
        ], "Invalid operator"
        return field_values


class EventLogItem(BaseModel):
    address: str
    topics: List[str]
    data: str
    blockNumber: str
    timeStamp: str
    gasPrice: str
    gasUsed: str
    logIndex: str
    transactionHash: str
    transactionIndex: str


class EventLog(BaseModel):
    __root__: List[EventLogItem]


class Logs:
    def _generate_operator_params(
        self, topic_operators: list[TopicOperator]
    ) -> dict[str, str]:
        ret = {}
        for topic_operator in topic_operators:
            topic_a = topic_operator.topic_a.value
            topic_b = topic_operator.topic_b.value
            if topic_a == topic_b:
                raise ValueError("topics must be different")
            operator = topic_operator.operator.value
            ret[
                ApiParams.PARTIAL_PARAM_TOPIC.value
                + topic_a[-1]
                + Const.UNDERSCORE.value
                + topic_b[-1]
                + Const.UNDERSCORE.value
                + ApiParams.PARTIAL_PARAM_OPER.value
            ] = operator
        return ret

    def get_evt_logs_by_addr(
        self,
        address: str,
        from_block: int,
        to_block: int,
        page: int = 1,
        limit: int = Const.RESP_LENGTH_LIMIT_LOGS.value,
        all_pages: int = 1,
    ) -> Union[None, EventLog]:
        resp = com.get_transactions(
            address=address,
            module=Modules.LOGS,
            action=ApiActions.GETLOGS,
            fromBlock=from_block,
            toBlock=to_block,
            page=page,
            limit=limit,
            all_pages=all_pages,
        )
        return com.generate_model(resp, EventLog)

    def get_evt_logs_by_addr_filtered_by_topic(
        self,
        from_block: int,
        to_block: int,
        topics: dict[ApiParams, str],
        address: Optional[str] = None,
        operators: Optional[list[TopicOperator]] = None,
        page: Optional[int] = 1,
        limit: Optional[int] = Const.RESP_LENGTH_LIMIT_LOGS.value,
        all_pages: Optional[int] = 1,
    ):

        """
        operator

            caution:    please use combination of operators at your onw risk.
                        combining operators over multiple topics will result
                        in unexpected responses for example topic 0
                        and (topic 2 or 3) will yeild a different result
                        than topic 1 and (topic 3 or 2), so for some odd
                        reason the sequence also matters.
        """

        # self._validate_operator(operator)
        operator_params = {}
        input_topics_dict = {}
        if operators is not None:
            operator_params: dict[str, str] = self._generate_operator_params(
                operators
            )
        for key, value in topics.items():
            input_topics_dict[key.value] = value
        resp = com.get_transactions(
            module=Modules.LOGS,
            action=ApiActions.GETLOGS,
            fromBlock=from_block,
            toBlock=to_block,
            address=address,
            topic_operators=operator_params,
            topics=input_topics_dict,
            page=page,
            limit=limit,
            all_pages=all_pages,
        )
        return com.generate_model(resp, EventLog)
