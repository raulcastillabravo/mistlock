FROM public.ecr.aws/lambda/python:3.11

# Install dependencies to /asset
WORKDIR /
RUN pip install SQLAlchemy psycopg2-binary --target /asset
