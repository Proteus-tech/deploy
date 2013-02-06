from proteus.update_aws_info import select_aws_name, split_detail
from unittest import TestCase

class TestUpdateAWSInfo(TestCase):
    def test_select_aws_name(self):
        aws_string = "ec2-204-236-159-62.us-west-1.compute.amazonaws.com"
        " -- running (ip-10-252-78-148) [ssh, http] {}\nr-61c55234"
        " -- stopped (singapore) [longevity] {u'Name': u'demo-back-service'}"
        expected = ["ec2-204-236-159-62.us-west-1.compute.amazonaws.com"]
        aws_name_list = select_aws_name(aws_string)
        self.assertEqual(expected, aws_name_list)

    def test_split_detail(self):
        aws_list = ["ec2-204-236-159-62.us-west-1.compute.amazonaws.com"
        " -- running (ip-10-252-78-148) [ssh, http] {}"
        ,"ec2-54-252-61-234.ap-southeast-2.compute.amazonaws.com"
        " -- running (cartoonmed) [ssh, http] "
        "{u'master': u'ready', u'mta': u'exim4', u'slave': u'ready',"
        " u'Name': u'testserver-playable_admin_service',"
        " u'buildbot': u'combo-playable_admin_service'}"]
        expected = ["{'status': 'running', 'pub_ip': '204-236-159-62', "
        "'dns': 'ec2-204-236-159-62.us-west-1.compute.amazonaws.com'}"
        ,"{'status': 'running', 'pub_ip': '54-252-61-234', "
        "'dns': 'ec2-54-252-61-234.ap-southeast-2.compute.amazonaws.com'}"]
        aws_dict = split_detail(aws_list)
        self.assertEqual(expected, aws_dict)
