import unittest

from suger_sdk_python.api.api_api import ApiClient
from suger_sdk_python.api.offer_api import OfferApi
from suger_sdk_python.api.product_api import ProductApi
from suger_sdk_python.exceptions import ApiException
from suger_sdk_python.configuration import Configuration
from suger_sdk_python.api.entitlement_api import EntitlementApi


class TestSimpleTest(unittest.TestCase):

    def setUp(self) -> None:
        test_config = Configuration(
            host="https://api.dev.suger.cloud",
        )
        test_config.api_key[
            'APIKeyAuth'] = 'Key b277c95e5e92ff7a8e96e74baf6ee2fb080db3e6507977c0067791abc1f52da4220e866e2081117a1721788aa2e9dc6fe009f2a699f17a7bba23973af6954db4'
        api_client = ApiClient(test_config)
        self.api = api_client

    def test_get_offer(self) -> None:
        org_id = 'w43Vc6UfM'
        offer_id = '1Edc6L49p'
        try:
            result = OfferApi(self.api).get_offer(org_id, offer_id)
            print("The response of OfferApi:\n")
            print(result)
            self.assertEqual(result.id, offer_id)
            pass
        except ApiException as e:
            print("Exception when calling OfferApi->get_offer: %s\n" % e)
            assert False

    def test_get_product(self) -> None:
        org_id = 'w43Vc6UfM'
        product_id = 'uD4BR9VfM'
        try:
            result = ProductApi(self.api).get_product(org_id, product_id)
            print("The response of ProductApi:\n")
            print(result)
            self.assertEqual(result.id, product_id)
            pass
        except ApiException as e:
            print("Exception when calling ProductApi->get_product: %s\n" % e)
            assert False

    def test_get_entitlement(self) -> None:
        org_id = 'w43Vc6UfM'
        entitlement_id = 'rFofgFDS_'
        try:
            result = EntitlementApi(self.api).get_entitlement(org_id, entitlement_id)
            print("The response of EntitlementApi:\n")
            print(result)
            self.assertEqual(result.id, entitlement_id)
            pass
        except ApiException as e:
            print("Exception when calling EntitlementApi->get_entitlement: %s\n" % e)
            assert False


if __name__ == '__main__':
    unittest.main()
