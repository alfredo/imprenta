# Imprenta

An AWS lambda that generates PDF files from HTML using pdfkit and wkhtmltopdf.

This package will:

- Read context variables from the API payload.
- Render context varialbes with the `vendor/templates/base.html`.
- Pass the rendered HTML to wkhtmltopdf to generate the PDF
- Upload the PDF file to S3.
- Return a signed URL of the PDF and the key.

This package is not feature complete. It is intended to be the starting point for a PDF generator as the HTML template will need to be coded, the context variables handled and authentication added.

[Chalice](https://github.com/aws/chalice) microframework is used to do the aws configuration heavylifting.

## Requirements

- Docker
- virtualenv (recommended).
- GNU make
- [awscli](https://pypi.python.org/pypi/awscli) python package installed and configured.

## Bootstrapping

A bootstrap script has been created for convenience. Make sure the project virtualenv is activated before running this command.

```
$ make build
```

This command will:

- Download and install wkhtmltopdf
- Build docker and install amazon-linux specific dependencies.
- Install package dependencies in the active python environment.
- Prepare the chalice initial configuration.

After this command has been run the environment variables in `pdf/.chalice/conf.json` must be added. These AWS credentials must match the


## Deploy

A command has been created to deploy the application

```
$ make deploy
```

## Running it local

The lambda can be run locally, but the wkhtmltopdf binary won't run since it is using the linux binary at the moment.


```
$ make local
```
