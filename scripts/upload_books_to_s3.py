"""
upload_books_to_s3.py

YOUR TASK: fill in the parts marked with TODO. Comments explain what each
step needs to do and why -- the actual code is up to you.

Goal: upload the 3 dataset CSVs (books_enriched.csv, ratings.csv,
book_tags.csv) from your local data/raw/ folder to S3, under a
raw/books/ prefix.

Run it like:
  python upload_books_to_s3.py --bucket aws-eur-roxana-bucket
"""

import boto3
import argparse
import os
from botocore.exceptions import ClientError

def upload_files(local_dir: str, filenames: list, bucket: str, prefix: str = "raw"):
    """
    Uploads each file in `filenames` (found inside `local_dir`) to S3,
    under the given `prefix`.

    Steps to implement:
    1. Create an S3 client. (Hint: one line, boto3 has a function for this.
       No credentials go in this file -- boto3 finds them automatically
       from the aws configure setup you already did.)
   
    2. Loop over each filename in `filenames`.

    3. For each one, build the two things you need:
       - the full local path (local_dir + filename)
       - the destination "key" in S3 (prefix + "/" + filename)
       (Hint: os.path.join() is the safe way to combine path pieces --
       avoids bugs with missing/extra slashes on different operating systems.)

    4. Try to upload it. The S3 client object has a method for uploading
       a local file directly -- look up "upload_file" in boto3's S3 client
       docs if you're not sure of the exact method name and argument order.

    5. If it works, print a success message showing local path -> s3 path.
       If it fails, catch the error (don't let one bad file crash the
       whole loop) and print what went wrong, then continue to the next file.
    """
    # TODO: implement the steps above
    s3 = boto3.client("s3")
    filenames = ["books_enriched.csv", "ratings.csv", "book_tags.csv"]
    for filename in filenames:
      local_path = os.path.join(local_dir, filename)
      s3_key = f"{prefix}/{filename}"
      s3.upload_file(local_path, bucket, s3_key)
      print(f"Uploaded {local_path} -> s3://{bucket}/{s3_key}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True, help="Target S3 bucket name")
    args = parser.parse_args()

    # TODO: build this list from the actual filenames sitting in your
    # data/raw/ folder right now
    filenames = []

    local_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

    upload_files(local_dir, filenames, args.bucket)
