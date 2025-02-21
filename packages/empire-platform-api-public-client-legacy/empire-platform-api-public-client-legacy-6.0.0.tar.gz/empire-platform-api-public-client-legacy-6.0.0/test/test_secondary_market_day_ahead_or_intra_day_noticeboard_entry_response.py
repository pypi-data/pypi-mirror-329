# coding: utf-8

"""
    Platform API

    _OpenAPI specification for the **Platform API** of **Empire**, the allocation and nomination platform of BritNed_  ---  Additional documentation available in the API's [GitHub repository](https://github.com/britned/empire-platform-api) 

    The version of the OpenAPI document: 6.0.0
    Contact: britned.info@britned.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from empire_platform_api_public_client_legacy.models.secondary_market_day_ahead_or_intra_day_noticeboard_entry_response import SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse  # noqa: E501

class TestSecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse(unittest.TestCase):
    """SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse:
        """Test SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse`
        """
        model = SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse()  # noqa: E501
        if include_optional:
            return SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse(
                mtus = [
                    empire_platform_api_public_client_legacy.models.secondary_market_day_ahead_or_intra_day_noticeboard_entry_response_mtus.SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        response_capacity = 56, 
                        response_price = 1.337, )
                    ],
                contact_name = '',
                phone_number = '+480728880015',
                email = '2@MDTMv2D2ylmgd10Z3UB6UkJSISSB512iz2DiJykO4IVP7YNsKQHh9BsaMPOiOuo3_QLOpkB.KIPOf2Flbsh1TpRS00PDvgoKGNXgxLHoPJE._eVrdJNcY9CLxYxBbcfSJXXZGSCF7dC-lSY-7ZlQJLW1_GNchKk5EBLDz1ctzsIY4oI.cl12VtuaSfjvmymTJfYkic17VJpcq1X6tjkH36lFYtIUw23vATP5cgpgctxW3q4fsZS5Uz-fvg2bA4.I-r1orbd3s4Kdu4Q19mfvL0A7Rpn3Av26g7OJWsQ0WBkWv3CuuRrMkJf5gzLvv2wY.NPqhvoybcy8QU.0_1u6BhIo-27B5JIFoxlv9-BJxhRRelW6lINX6.1Elv8Z4qYvYNwb3t4awGG-6yh0-gMEzQ8uhi90kNEaHx.5LWBoOt62fDnfouEM59JJWYHa1Ya1DpwFCTpIA0Gnqa9PQ0lvjCR3UYpt1vrS1p.R1OzxrQfgrgcyvfHmHL7bSaRv9kZ_K.NGkIi19s7KrTBx8qCkWG3nkJgXYUf-2g1bLoF4Q2SDvsQvki_Gv.3xSglBiD_kTqWft7LgtQq8DkTxH9-GEgnhdskTUa-JGB99tBTH1m8LyVjqKCRWp6XS1rwkzrnn.h0XoK7cYVKPWx4kXAhG_GEdV9fi1LUY2eBXIK-aaNx-IAoUxtYKQpsS2HM0cvxv.88aJmQRbOi5pM9K4SWNKj0UeVyhnBjVWguY2vNQIw3D_aRMF2Tm7SelZBdyPOLRs2IImu0zJ-sEvqrLoPmgi.JrQNmT_4QLVs0oSHjB6pC-1mwGXNIZ-mK8w9K1xfp9OikxJ6eiOUAchnVGrwqvIGWHJ7Z1.eTeQr7h2GhDiufc8pTDOUcgYQwyEct13aGy9ShDDH49uy_cuS1qDT5br69Zb9J7ztaciXoL3UMxQsS4RhgPVNkMuBNIrWv_v.6kENTnbd0jYevK4Igno2LdfSDI1Cs6huybGb1zEpVJcz_sYPOWoI5540Y2OLcYufJVmh2PNuin04QumvvjetJ2wYXn.2W6zwIrDKlbs9CPExuzXJjOmov9hu5QjJ_xMDMiy-rwLYYugfVA0tbOL0.zdgU9sGpVxk.V0XsgBCaMb6w.WmQk2AHCmB9lVwewmjj04um-gQsMcYoZx6RzkDL1MAzcQRnYq9jshsHLjup_Xq1.S5JIFlA8s7VLbfJ8CdU1--K_bbEzgXW.tGc11HJjfPh9aPBMPn9vOOHdKkQ6_InnGXC1663IOeomDvz9sa4XpvFxFUjA2Vr.PYqBpPgKYJXJXx50oGq47BDC1bkGeAny7jvr.nVoFMKNnHvQ4AYmlmF-v4iCmrtetgOVivKk30FKcbp2YLd7pV.yS_oco2NX0KaIUr6IkqdrU12DLntCJlzZRgbiwPbeBEaozEh0SiWTzo35ic3_fxCN.JH7Ifx4drCfHNmicDnRnqH2lvbFg3LEqe7XaJ9kbxYSX1C_Lr7dDE3pdI47Y5OdDPkSvjK_RoQMDG8YTqdvQky1k.bXOyxDLVceMTPn2f1D8joDAWMEOKR7TA5Mr5sJj8HnYiNQw3dMfL85GQOI.PdtmSOAEKxeS.nf5zlDYDcZtAn2y3pBKKrVM3EsaoUBgV8gy30aITJ7uhAIMDUKTawsf6HUR.vzPAZ5l09xshFyzZ.iL2KN6CGlaHkPX2BJeFuAvdHCCkQfzG8UQdfdhrt6srAn0F.isE9LinMVcxjk_gX1iQ6En890DUqRq1QMsZdFRNoDtaPmlYuZyzIuPbP9BoKeUzcKrabe3xXH.Opr6PVcnpJXO1EjjhcsqEiC9dTSNBWTV28hLq4QrTzI9GtnaVV7h1gY.lMPOz0JlrLFiDe3KOjXDRBF9hN72JekIfNuG9Pqe8.sbStaCVPDJlO5QnMT8K8jKE9fe7M-6-c8yP711SfHIbsPGUzHQRu0X7ALLvsoFkc22LM5RF.KXIeel20-8t0dHGD.TMbINi8qq1WxwuHJ8xdW47netlfTR8n_uO18chNXvsqeiN.fhIlF4_xFhy.LI2a',
                comment = '',
                responded_at = '2022-01-04T00:00:00.000Z'
            )
        else:
            return SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse(
                mtus = [
                    empire_platform_api_public_client_legacy.models.secondary_market_day_ahead_or_intra_day_noticeboard_entry_response_mtus.SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        response_capacity = 56, 
                        response_price = 1.337, )
                    ],
                contact_name = '',
                phone_number = '+480728880015',
                email = '2@MDTMv2D2ylmgd10Z3UB6UkJSISSB512iz2DiJykO4IVP7YNsKQHh9BsaMPOiOuo3_QLOpkB.KIPOf2Flbsh1TpRS00PDvgoKGNXgxLHoPJE._eVrdJNcY9CLxYxBbcfSJXXZGSCF7dC-lSY-7ZlQJLW1_GNchKk5EBLDz1ctzsIY4oI.cl12VtuaSfjvmymTJfYkic17VJpcq1X6tjkH36lFYtIUw23vATP5cgpgctxW3q4fsZS5Uz-fvg2bA4.I-r1orbd3s4Kdu4Q19mfvL0A7Rpn3Av26g7OJWsQ0WBkWv3CuuRrMkJf5gzLvv2wY.NPqhvoybcy8QU.0_1u6BhIo-27B5JIFoxlv9-BJxhRRelW6lINX6.1Elv8Z4qYvYNwb3t4awGG-6yh0-gMEzQ8uhi90kNEaHx.5LWBoOt62fDnfouEM59JJWYHa1Ya1DpwFCTpIA0Gnqa9PQ0lvjCR3UYpt1vrS1p.R1OzxrQfgrgcyvfHmHL7bSaRv9kZ_K.NGkIi19s7KrTBx8qCkWG3nkJgXYUf-2g1bLoF4Q2SDvsQvki_Gv.3xSglBiD_kTqWft7LgtQq8DkTxH9-GEgnhdskTUa-JGB99tBTH1m8LyVjqKCRWp6XS1rwkzrnn.h0XoK7cYVKPWx4kXAhG_GEdV9fi1LUY2eBXIK-aaNx-IAoUxtYKQpsS2HM0cvxv.88aJmQRbOi5pM9K4SWNKj0UeVyhnBjVWguY2vNQIw3D_aRMF2Tm7SelZBdyPOLRs2IImu0zJ-sEvqrLoPmgi.JrQNmT_4QLVs0oSHjB6pC-1mwGXNIZ-mK8w9K1xfp9OikxJ6eiOUAchnVGrwqvIGWHJ7Z1.eTeQr7h2GhDiufc8pTDOUcgYQwyEct13aGy9ShDDH49uy_cuS1qDT5br69Zb9J7ztaciXoL3UMxQsS4RhgPVNkMuBNIrWv_v.6kENTnbd0jYevK4Igno2LdfSDI1Cs6huybGb1zEpVJcz_sYPOWoI5540Y2OLcYufJVmh2PNuin04QumvvjetJ2wYXn.2W6zwIrDKlbs9CPExuzXJjOmov9hu5QjJ_xMDMiy-rwLYYugfVA0tbOL0.zdgU9sGpVxk.V0XsgBCaMb6w.WmQk2AHCmB9lVwewmjj04um-gQsMcYoZx6RzkDL1MAzcQRnYq9jshsHLjup_Xq1.S5JIFlA8s7VLbfJ8CdU1--K_bbEzgXW.tGc11HJjfPh9aPBMPn9vOOHdKkQ6_InnGXC1663IOeomDvz9sa4XpvFxFUjA2Vr.PYqBpPgKYJXJXx50oGq47BDC1bkGeAny7jvr.nVoFMKNnHvQ4AYmlmF-v4iCmrtetgOVivKk30FKcbp2YLd7pV.yS_oco2NX0KaIUr6IkqdrU12DLntCJlzZRgbiwPbeBEaozEh0SiWTzo35ic3_fxCN.JH7Ifx4drCfHNmicDnRnqH2lvbFg3LEqe7XaJ9kbxYSX1C_Lr7dDE3pdI47Y5OdDPkSvjK_RoQMDG8YTqdvQky1k.bXOyxDLVceMTPn2f1D8joDAWMEOKR7TA5Mr5sJj8HnYiNQw3dMfL85GQOI.PdtmSOAEKxeS.nf5zlDYDcZtAn2y3pBKKrVM3EsaoUBgV8gy30aITJ7uhAIMDUKTawsf6HUR.vzPAZ5l09xshFyzZ.iL2KN6CGlaHkPX2BJeFuAvdHCCkQfzG8UQdfdhrt6srAn0F.isE9LinMVcxjk_gX1iQ6En890DUqRq1QMsZdFRNoDtaPmlYuZyzIuPbP9BoKeUzcKrabe3xXH.Opr6PVcnpJXO1EjjhcsqEiC9dTSNBWTV28hLq4QrTzI9GtnaVV7h1gY.lMPOz0JlrLFiDe3KOjXDRBF9hN72JekIfNuG9Pqe8.sbStaCVPDJlO5QnMT8K8jKE9fe7M-6-c8yP711SfHIbsPGUzHQRu0X7ALLvsoFkc22LM5RF.KXIeel20-8t0dHGD.TMbINi8qq1WxwuHJ8xdW47netlfTR8n_uO18chNXvsqeiN.fhIlF4_xFhy.LI2a',
                responded_at = '2022-01-04T00:00:00.000Z',
        )
        """

    def testSecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse(self):
        """Test SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
