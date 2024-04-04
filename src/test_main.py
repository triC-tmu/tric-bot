import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, call, patch

from main import ac_alert


class TestMain(IsolatedAsyncioTestCase):
    @patch("main.client.run", new_callable=MagicMock)
    @patch("main.get_members_ac")
    @patch("main.get_problems_difficulty")
    @patch("main.send_message")
    async def test_ac_alert(
        self,
        mock_send_message,
        mock_get_problems_difficulty,
        mock_get_members_ac,
        mock_client_run,
    ):
        # Mock data
        ac_submissions = [
            [
                {
                    "user_id": "user1",
                    "problem_id": "abc138_a",
                    "result": "AC",
                    "id": "12345",
                    "contest_id": "abc138",
                }
            ],
            [
                {
                    "user_id": "user2",
                    "problem_id": "abc138_a",
                    "result": "AC",
                    "id": "12345",
                    "contest_id": "abc138",
                },
                {
                    "user_id": "user2",
                    "problem_id": "abc138_d",
                    "result": "AC",
                    "id": "67890",
                    "contest_id": "abc138",
                },
            ],
        ]
        ac_submissions_difficulty = {"abc138_a": 18, "abc138_d": 920}

        # Mock function return values
        mock_get_members_ac.return_value = ac_submissions
        mock_get_problems_difficulty.return_value = ac_submissions_difficulty

        # Call the function
        await ac_alert()

        expected_calls = [
            call(
                "user1が:hai:abc138_aをACしました。\n https://atcoder.jp/contests/abc138/submissions/12345\n"
            ),
            call(
                "user2が:hai:abc138_aをACしました。\n https://atcoder.jp/contests/abc138/submissions/12345\nuser2が:midori:abc138_dをACしました。\n https://atcoder.jp/contests/abc138/submissions/67890\n"
            ),
        ]

        # Assert the function calls
        mock_get_members_ac.assert_called_once()
        mock_get_problems_difficulty.assert_called_once()
        mock_send_message.assert_has_calls(expected_calls)


if __name__ == "__main__":
    unittest.main()
