import unittest

from gtm_agent.data_service import fetch_tech_stack, update_prospect_info


class UpdateProspectInfoTest(unittest.TestCase):
    def test_update_persists_technology(self):
        update_prospect_info("LEAD-39002", "Terraform")

        self.assertIn("Terraform", fetch_tech_stack("LEAD-39002"))


if __name__ == "__main__":
    unittest.main()
