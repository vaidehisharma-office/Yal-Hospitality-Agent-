
import unittest
from unittest.mock import patch

from yal_agent.agent import handle_guest_request


class TestHotelAgent(unittest.TestCase):

    # ---------------------------------
    # 10 SUCCESSFUL ACTION TESTS
    # ---------------------------------

    @patch("yal_agent.agent.create_housekeeping_request")
    @patch("yal_agent.agent.classify")
    def test_01_send_towels(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "HOUSEKEEPING",
                "needs_clarification": False,
                "clarification_question": None
            }
        }
        mock_tool.return_value = {
            "success": True,
            "ticket_id": "HK-TEST001"
        }

        result = handle_guest_request("Send two towels", 402)

        self.assertTrue(result["success"])
        self.assertEqual(result["ticket_id"], "HK-TEST001")

    @patch("yal_agent.agent.create_housekeeping_request")
    @patch("yal_agent.agent.classify")
    def test_02_request_extra_pillow(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "HOUSEKEEPING",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": True,
            "ticket_id": "HK-TEST002"
        }

        result = handle_guest_request("Send an extra pillow", 403)

        self.assertTrue(result["success"])

    @patch("yal_agent.agent.create_housekeeping_request")
    @patch("yal_agent.agent.classify")
    def test_03_request_blanket(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "HOUSEKEEPING",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": True,
            "ticket_id": "HK-TEST003"
        }

        result = handle_guest_request("I need a blanket", 404)

        self.assertTrue(result["success"])

    @patch("yal_agent.agent.create_maintenance_request")
    @patch("yal_agent.agent.classify")
    def test_04_ac_not_cooling(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "MAINTENANCE",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": True,
            "ticket_id": "MT-TEST001"
        }

        result = handle_guest_request("AC is not cooling", 402)

        self.assertTrue(result["success"])

    @patch("yal_agent.agent.create_maintenance_request")
    @patch("yal_agent.agent.classify")
    def test_05_light_not_working(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "MAINTENANCE",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": True,
            "ticket_id": "MT-TEST002"
        }

        result = handle_guest_request("The light is not working", 405)

        self.assertTrue(result["success"])

    @patch("yal_agent.agent.create_maintenance_request")
    @patch("yal_agent.agent.classify")
    def test_06_wifi_not_working(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "MAINTENANCE",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": True,
            "ticket_id": "MT-TEST003"
        }

        result = handle_guest_request("Wi-Fi is not working", 406)

        self.assertTrue(result["success"])

    @patch("yal_agent.agent.contact_front_desk")
    @patch("yal_agent.agent.classify")
    def test_07_cleaning_complaint(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "COMPLAINT",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": True,
            "ticket_id": "FD-TEST001"
        }

        result = handle_guest_request(
            "My room was not cleaned properly", 402
        )

        self.assertTrue(result["success"])

    @patch("yal_agent.agent.contact_front_desk")
    @patch("yal_agent.agent.classify")
    def test_08_noise_complaint(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "COMPLAINT",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": True,
            "ticket_id": "FD-TEST002"
        }

        result = handle_guest_request("There is too much noise", 407)

        self.assertTrue(result["success"])

    @patch("yal_agent.agent.contact_front_desk")
    @patch("yal_agent.agent.classify")
    def test_09_staff_complaint(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "COMPLAINT",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": True,
            "ticket_id": "FD-TEST003"
        }

        result = handle_guest_request(
            "I want to report an issue with staff", 408
        )

        self.assertTrue(result["success"])

    @patch("yal_agent.agent.classify")
    def test_10_information_question(self, mock_classify):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "INFORMATION",
                "needs_clarification": False
            }
        }

        result = handle_guest_request("What time is breakfast?", 402)

        self.assertTrue(result["success"])
        self.assertFalse(result["action_taken"])

    # ---------------------------------
    # 10 FAILURE AND EDGE CASE TESTS
    # ---------------------------------

    @patch("yal_agent.agent.classify")
    def test_11_missing_room_number(self, mock_classify):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "HOUSEKEEPING",
                "needs_clarification": False
            }
        }

        result = handle_guest_request("Send towels")

        self.assertFalse(result["success"])
        self.assertIn("room number", result["response"].lower())

    @patch("yal_agent.agent.classify")
    def test_12_incomplete_complaint(self, mock_classify):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "COMPLAINT",
                "needs_clarification": True,
                "clarification_question": "Please explain your complaint."
            }
        }

        result = handle_guest_request("I have a complaint", 402)

        self.assertFalse(result["success"])
        self.assertIn("complaint", result["response"].lower())

    @patch("yal_agent.agent.classify")
    def test_13_classification_error(self, mock_classify):
        mock_classify.return_value = {
            "error": "api_error",
            "result": None
        }

        result = handle_guest_request("Send towels", 402)

        self.assertFalse(result["success"])

    @patch("yal_agent.agent.create_housekeeping_request")
    @patch("yal_agent.agent.classify")
    def test_14_housekeeping_tool_failure(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "HOUSEKEEPING",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": False,
            "message": "Service unavailable"
        }

        result = handle_guest_request("Send towels", 402)

        self.assertFalse(result["success"])

    @patch("yal_agent.agent.create_maintenance_request")
    @patch("yal_agent.agent.classify")
    def test_15_maintenance_tool_failure(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "MAINTENANCE",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": False,
            "message": "Maintenance unavailable"
        }

        result = handle_guest_request("Fix AC", 402)

        self.assertFalse(result["success"])

    @patch("yal_agent.agent.contact_front_desk")
    @patch("yal_agent.agent.classify")
    def test_16_front_desk_tool_failure(self, mock_classify, mock_tool):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "COMPLAINT",
                "needs_clarification": False
            }
        }
        mock_tool.return_value = {
            "success": False,
            "message": "Front desk unavailable"
        }

        result = handle_guest_request("Room complaint", 402)

        self.assertFalse(result["success"])

    @patch("yal_agent.agent.classify")
    def test_17_emergency_without_room_number(self, mock_classify):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "EMERGENCY",
                "needs_clarification": False
            }
        }

        result = handle_guest_request("Smoke from electrical socket")

        self.assertTrue(result["success"])
        self.assertFalse(result["action_taken"])
        self.assertIn("emergency", result["response"].lower())

    @patch("yal_agent.agent.classify")
    def test_18_information_without_room_number(self, mock_classify):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "INFORMATION",
                "needs_clarification": False
            }
        }

        result = handle_guest_request("What time is breakfast?")

        self.assertTrue(result["success"])
        self.assertFalse(result["action_taken"])

    @patch("yal_agent.agent.classify")
    def test_19_unknown_intent(self, mock_classify):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "UNKNOWN",
                "needs_clarification": False
            }
        }

        result = handle_guest_request("Something unusual", 402)

        self.assertFalse(result["success"])

    @patch("yal_agent.agent.classify")
    def test_20_emergency_needs_clarification(self, mock_classify):
        mock_classify.return_value = {
            "error": None,
            "result": {
                "intent": "EMERGENCY",
                "needs_clarification": True,
                "clarification_question": "Please explain."
            }
        }

        result = handle_guest_request("There may be smoke")

        self.assertTrue(result["success"])
        self.assertFalse(result["action_taken"])
        self.assertIn("emergency", result["response"].lower())


if __name__ == "__main__":
    unittest.main()
