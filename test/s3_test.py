import boto3
from main.security import * # 상수를 모두 저장해 놓음.
# TODO : git ignore 작성하기
s3 = s3 = boto3.client(
            service_name=service_name,
            region_name=region_name, # 자신이 설정한 bucket region
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

print(s3.list_buckets()) # s3 리스트 가져오기

s3.upload_file(
    "C:/Users/minkun/Downloads/이미지다운4.jpg",
    'my-shopping-img',
    'test3.jpg', # 확장자 까지 제대로 붙여야한다. 이 이름으로 버킷에 저장된다.
    ExtraArgs={'ContentType': "image/jpg", 'ACL': "public-read"} # content type을 설정해야 브라우저에서 올바르게 띄워준다.

)

location = s3.get_bucket_location(Bucket=bucket_name)["LocationConstraint"] # ap-northeast-2이다. 고정인듯? -2는 고정 아닐 수도 있다.
filename ='test3.jpg'


url =  f"https://{bucket_name}.s3.{location}.amazonaws.com/{filename}" # 이 형식으로 url을 만들 수 있다.

print(url)







