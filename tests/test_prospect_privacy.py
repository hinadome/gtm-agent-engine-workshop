import json
import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ["LANGSMITH_TRACING"] = "false"

from gtm_agent import data_service, gtm_records
from gtm_agent.gtm_agent import build_prospect_profile, get_prospect


SENSITIVE_VALUES = ("billing_qualification", "tax_id", "card_on_file", "date_of_birth", "credit_check_ref")


def test_prospect_tools_exclude_billing_data_from_serialized_output():
    for prospect_id in gtm_records.PROSPECTS:
        data_service._PROFILES.clear()

        contact_output = get_prospect.invoke({"prospect_id": prospect_id})
        profile_output = build_prospect_profile.invoke({"prospect_id": prospect_id})

        for output in (contact_output, profile_output):
            serialized = json.dumps(output)
            assert all(value not in serialized for value in SENSITIVE_VALUES)
