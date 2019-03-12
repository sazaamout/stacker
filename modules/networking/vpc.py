#!/usr/bin/env python

"""Module with VPC resources."""

from __future__ import print_function

from troposphere import (
    Ref, Output, ec2, GetAtt
)

from stacker.blueprints.base import Blueprint

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOGICAL RESOURCES NAMES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
VPC_NAME = 'VPC'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RESOURCES IDs
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
VPC_ID = Ref(VPC_NAME)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OUTPUT VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OUTPUT_VPC_ID = 'VpcId'


AWS_TEMPLATE_VERSION = '2010-09-09'


class VPC(Blueprint):
    """Stacker blueprint for creating a Basic VPC."""

    VARIABLES = {
        'VpcCidr': {
            'type': str,
            'description': 'CIDR block range for VPC ip space',
        },

        'VpcName': {
            'type': str,
            'description': 'The Name of the deployed VPC',
            'Default': 'myVPC'
        },
        'UseInternetGW': {
            'type': bool,
            'description': 'toggle the creation of internetGW on/off',
            'default': False
        }
    }

    def create_vpc(self):
        """Create the VPC resources."""
        template = self.template
        variables = self.get_variables()
        self.template.add_version(AWS_TEMPLATE_VERSION)
        self.template.add_description('Create a VPC')

        vpc = ec2.VPC(
            VPC_NAME,
            CidrBlock=variables['VpcCidr'],
            EnableDnsSupport=True,
            EnableDnsHostnames=True,
            Tags=[ec2.Tag('Name', variables['VpcName'] + '-LATESTREPO')]
        )

        template.add_resource(vpc)

        template.add_output(
            Output(
                OUTPUT_VPC_ID,
                Value=VPC_ID
            )
        )

        # create the internet gateway if needed
        if variables["UseInternetGW"]:
            template.add_resource(ec2.InternetGateway('InternetGatway'))
            template.add_resource(
            ec2.VPCGatewayAttachment(
                'GatewayAttach',
                VpcId=Ref(VPC_NAME),
                InternetGatewayId=Ref('InternetGatway')
            )
        )

    def create_template(self):
        """Create template (main function called by Stacker)."""
        self.create_vpc()

