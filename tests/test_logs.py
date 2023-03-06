import unittest

import pandas as pd

from src.enums import ApiParams, Const
from src.logs import Logs, TopicOperator


class TestLogs(unittest.TestCase):
    def setUp(self) -> None:
        self.logs = Logs()

    @unittest.skip
    def test_get_evt_logs_by_addr(self):
        resp = self.logs.get_evt_logs_by_addr(
            address="0xbd3531da5cf5857e7cfaa92426877b022e612cf8",
            from_block=12878196,
            to_block=12878196,
            limit=50,
        )
        print(pd.read_json(resp.json()).info())
        self.assertIsNotNone(resp)

    def test_get_evt_logs_by_addr_filter_by_topics(self):
        resp = self.logs.get_evt_logs_by_addr_filtered_by_topic(
            # address="0xbd3531da5cf5857e7cfaa92426877b022e612cf8",
            from_block=12878196,
            to_block=12878196,
            topics={
                ApiParams.TOPIC_0: "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                ApiParams.TOPIC_2: "0x000000000000000000000000c45a4b3b698f21f88687548e7f5a80df8b99d93d",
                ApiParams.TOPIC_3: "0x00000000000000000000000000000000000000000000000000000000000000b6",
            },
            operators=[
                TopicOperator(
                    topic_a=ApiParams.TOPIC_0,
                    topic_b=ApiParams.TOPIC_2,
                    operator=Const.OPERATOR_AND,
                ),
                TopicOperator(
                    topic_a=ApiParams.TOPIC_2,
                    topic_b=ApiParams.TOPIC_3,
                    operator=Const.OPERATOR_OR,
                ),
                TopicOperator(
                    topic_a=ApiParams.TOPIC_2,
                    topic_b=ApiParams.TOPIC_3,
                    operator=Const.OPERATOR_AND,
                ),
            ],
            limit=50,
        )
        print(pd.read_json(resp.json()).info())
        self.assertIsNotNone(resp)
