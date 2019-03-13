import boto3


class AWSOutage(object):

    def __init__(self, region, az, duration):
        self.az = az
        self.region = region
        self.duration = duration
        self.session = boto3.Session()

    def __str__(self):
        return f'Outage of {self.az} in {self.region} for {self.duration}s'
