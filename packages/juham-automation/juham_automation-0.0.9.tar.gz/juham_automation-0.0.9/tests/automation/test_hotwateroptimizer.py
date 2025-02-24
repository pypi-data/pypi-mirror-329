import unittest
from masterpiece import MqttMsg
from juham_automation.automation.hotwateroptimizer import HotWaterOptimizer


class TestHotWaterOptimizer(unittest.TestCase):

    def test_constructor(self) -> None:
        obj = HotWaterOptimizer(
            name="test_optimizer",
            temperature_sensor="test_sensor",
            start_hour=0,
            num_hours=4,
            spot_limit=0.1,
        )
        self.assertIsNotNone(obj)


if __name__ == "__main__":
    unittest.main()
