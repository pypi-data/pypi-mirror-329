import boto3
import logging


def update_dns(hosted_zone, name, ip) -> bool:
    client = boto3.client('route53')

    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone,
        ChangeBatch={
            "Comment": "Automatic record update",
            "Changes": [{
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": name,
                    "Type": "A",
                    "TTL": 300,
                    "ResourceRecords": [{
                        "Value": ip
                    }]
                }
            }]
        }
    )

    logging.debug(response)

    return True