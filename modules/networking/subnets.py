#!/usr/bin/env python

"""Module with SUBNET resources."""

from __future__ import print_function

from troposphere import (
    Ref, Output, ec2, GetAtt
)

from stacker.blueprints.base import Blueprint

AWS_TEMPLATE_VERSION = '2010-09-09'

class SUBNETS(Blueprint):
    """Stacker blueprint for creating a Basic Subnets."""

    VARIABLES = {
        'VpcId': {
            'type': str,
        },
        'PublicSubnet1': {
            'type': str,
            'description': 'des'
        },
        'PublicSubnet1_cidr': {
            'type': str,
            'description': 'des'
        },
        'PrivateSubnet1': {
            'type': str,
            'description': 'des'
        },
        'PrivateSubnet1_cidr': {
            'type': str,
            'description': 'des'
        },
        'zone': {
            'type': str,
        }
    }

    def create_subnet(self):
        """Create the Subnets resources."""
        template = self.template
        variables = self.get_variables()
        self.template.add_version(AWS_TEMPLATE_VERSION)
        self.template.add_description('Create a Subnets')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # create the Public Subnet(s)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        template.add_resource (
            ec2.Subnet(
                "PublicSubnet1",
                AvailabilityZone=variables['zone'],
                VpcId=variables['VpcId'],
                CidrBlock=variables['PublicSubnet1_cidr'],
                Tags=[ec2.Tag('Name', variables['PublicSubnet1'])]
            )
        )
        # add the output var
        template.add_output(
            Output(
                'PublicSubnet1Id',
                Value=Ref('PublicSubnet1')
            )
        )

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # create the Private Subnet(s)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        template.add_resource (
            ec2.Subnet(
                "PrivateSubnet1",
                AvailabilityZone=variables['zone'],
                VpcId=variables['VpcId'],
                CidrBlock=variables['PrivateSubnet1_cidr'],
                Tags=[ec2.Tag('Name', variables['PrivateSubnet1'])]
            )
        )
        # add the output var
        template.add_output(
            Output(
                'PrivateSubnet1Id',
                Value=Ref('privateSubnet1')
            )
        )




    def create_template(self):
        """Create template (main function called by Stacker)."""
        self.create_subnet()

