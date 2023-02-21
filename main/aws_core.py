import os.path

import main.security # test 패키지의 동작을 위해서 main패키지 안에 있지만 이렇게 할 수 밖에 없다.
import boto3
from main import security


def s3_getclient():
    s3 = s3 = boto3.client(
        service_name=security.service_name,
        region_name=security.region_name,  # 자신이 설정한 bucket region
        aws_access_key_id=security.aws_access_key_id,
        aws_secret_access_key=security.aws_secret_access_key,
    )
    return s3


def get_url(s3, s3_path):

    """
    :param s3: s3 client 객체 
    :param s3_path: 확장자를 포함한 객체
    :return: 
    """
    assert '.' in s3_path, 's3_path는 확장자를 포함한 객체여야합니다.'

    # base, ext = os.path.splitext(path)
    location = s3.get_bucket_location(Bucket=security.bucket_name)[
        "LocationConstraint"]  # ap-northeast-2이다. 고정인듯? -2는 고정 아닐 수도 있다.
    filename = s3_path
    url = f"https://{security.bucket_name}.s3.{location}.amazonaws.com/{filename}"  # 이 형식으로 url을 만들 수 있다.
    return url
