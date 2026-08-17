import unittest

from kaa_rest_client.ecr_models import (
    EndpointConfiguration,
    SystemConfigurationInput,
    parse_config,
)


class EcrModelTests(unittest.TestCase):
    def test_parse_config_decodes_json_object(self):
        self.assertEqual(
            parse_config('{"active": true, "pushInterval": 5}'),
            {"active": True, "pushInterval": 5},
        )

    def test_parse_config_preserves_invalid_json_string(self):
        self.assertEqual(parse_config("not-json"), "not-json")

    def test_parse_config_preserves_already_decoded_values(self):
        value = {"emails": ["ops@example.com"]}
        self.assertIs(parse_config(value), value)

    def test_endpoint_configuration_uses_openapi_example_shape(self):
        result = EndpointConfiguration.from_dict({
            "configId": "231f1aae-a4be-11ea-bb37-0242ac130002",
            "name": "night-mode",
            "config": '{"active": true, "pushInterval": 5}',
            "createdDate": "2017-03-17T11:30:02.643Z",
            "updatedDate": "2017-03-17T11:30:02.643Z",
        })

        self.assertEqual(result.config_id, "231f1aae-a4be-11ea-bb37-0242ac130002")
        self.assertEqual(result.config, {"active": True, "pushInterval": 5})
        self.assertEqual(result.created_date, "2017-03-17T11:30:02.643Z")

    def test_system_configuration_input_serializes_structured_config(self):
        result = SystemConfigurationInput(
            name="alert-email-recipients",
            display_name="Alert email recipients",
            config={"emails": ["alert-monitor@acme.com"]},
        ).to_payload()

        self.assertEqual(result["name"], "alert-email-recipients")
        self.assertEqual(result["displayName"], "Alert email recipients")
        self.assertEqual(result["config"], '{"emails": ["alert-monitor@acme.com"]}')


if __name__ == "__main__":
    unittest.main()
