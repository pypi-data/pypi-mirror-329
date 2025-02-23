#!/usr/bin/python3
# @Time    : 2025-02-22
# @Author  : Kevin Kong (kfx2007@163.com)

from re import S
from unittest import TestCase
import unittest
from aliyun_sms.signature import Signature
from aliyun_sms.sms import Sms

class TestSign(TestCase):
    def setUp(self) -> None:
        self.sig = Signature(
            "LTAI5t7D7W9qZJUgtnkZZp2F",
            "th8HG0Swqm5EGopGExwanxHDl1QOPT"
        )
        self.sms = Sms(
            "LTAI5t7D7W9qZJUgtnkZZp2F",
            "th8HG0Swqm5EGopGExwanxHDl1QOPT"
        )
        
    def test_sendSms(self):
        res =  self.sms.sendSms(
            "18561363632",
            "浙江矫马同步带有限公司",
            "SMS_478575841",
            {"consignee": "李玮峰", "phone": "+86 18561363632"}
        )
        self.assertEqual(res["Code"], "OK", res)
            
    
    # def test_getSiginatureList(self):
    #     res = self.sig.getSiginatureList()
    #     self.assertEqual(res["Code"], "OK", res)

    
if __name__ == "__main__":
    unittest.main()