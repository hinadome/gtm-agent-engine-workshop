import os
import unittest
from unittest.mock import patch

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent.gtm_agent import send_prospect_email


class SendProspectEmailTests(unittest.TestCase):
    def test_disqualified_lead_is_blocked_without_message_id(self):
        prospect = {
            "prospect_id": "LEAD-50001",
            "name": "Priya Nair",
            "email": "priya.nair@brightwaveapps.com",
        }

        with patch(
            "gtm_agent.gtm_agent.data_service.get_prospect_record",
            return_value={"disqualified": True},
        ), patch("gtm_agent.gtm_agent.uuid.uuid4") as uuid4:
            result = send_prospect_email.func(
                prospect=prospect,
                subject="Invitation to Book a Demo",
                body="Please book a demo.",
                runtime=None,
                from_rep={"name": "Marco Rossi", "email": "marco.rossi@northpoint.com"},
            )

        self.assertEqual(
            result,
            {
                "status": "blocked",
                "reason": "Prospect is disqualified; outbound email not sent.",
                "prospect_id": "LEAD-50001",
            },
        )
        self.assertNotIn("message_id", result)
        uuid4.assert_not_called()


if __name__ == "__main__":
    unittest.main()
