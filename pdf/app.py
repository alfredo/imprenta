import boto3
import os
import pdfkit

from chalice import Chalice
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
here = lambda *x: os.path.abspath(os.path.join(BASE_DIR, *x))

env = Environment(
    loader=FileSystemLoader(here('templates')),
    autoescape=select_autoescape(['html'])
)


binary_path = here('wkhtmltopdf')
configuration = pdfkit.configuration(wkhtmltopdf=binary_path)

app = Chalice(app_name='pdf')

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS')
AWS_SECRET_KEY = os.getenv('AWS_SECRET')
AWS_S3_BUCKET = os.getenv('AWS_BUCKET')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')


client = boto3.client(
    's3',
    region_name=AWS_REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY)


def release_id():
    return datetime.now().strftime('%Y%m%d-%H%M%S')


def upload_to_s3(file_object, key_name):
    result = client.put_object(
        Bucket=AWS_S3_BUCKET, Key=key_name, Body=file_object)
    return result


def get_s3_url(key_name):
    url = client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': AWS_S3_BUCKET,
            'Key': key_name,
        })
    return url


def render_template(file_name, context):
    template = env.get_template(file_name)
    return template.render(**context)


def render_pdf(params):
    name = params.get('name', 'Someone')
    contents = render_template('base.html', {
        'name': name,
    })
    pdf_file = pdfkit.from_string(contents, False, configuration=configuration)
    key_name = '%s.pdf' % release_id()
    result = upload_to_s3(pdf_file, key_name)
    print(result)
    return {
        'key': key_name,
        'url': get_s3_url(key_name),
    }


@app.route('/')
def index():
    params = app.current_request.query_params
    if params is None or 'name' not in params:
        return {
            'error': 'Missing param `name`',
        }
    try:
        return render_pdf(params)
    except Exception as e:
        return {
            'error': str(e),
        }
