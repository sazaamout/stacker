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


class SUBNETS(Blueprint):
    """Stacker blueprint for creating a Basic VPC."""

    VARIABLES = {
        'VpcId': {
            'type': str,
        },
        'PublicSubnet1': {
            'type': str,
            'description': 'des'
        },
        'PublicSubnet2': {
            'type': str,
            'description': 'des'
        }
    }

    def create_subnet(self):
        """Create the Subnets resources."""
        template = self.template
        variables = self.get_variables()
        self.template.add_version(AWS_TEMPLATE_VERSION)
        self.template.add_description('Create a Subnets')

        template.add_resource (
            ec2.Subnet(
                "PublicSubnet1",
                AvailabilityZone="ca-central-1a",
                VpcId=variables['VpcId'],
                CidrBlock='10.0.0.0/24',
                Tags=[ec2.Tag('Name', "PublicSubnet1")]
            )
        )
        template.add_output(
            Output(
                'PublicSubnet1Id',
                Value=Ref('PublicSubnet1')
            )
        )


    def create_template(self):
        """Create template (main function called by Stacker)."""
        self.create_subnet()

