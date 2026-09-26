======================
S3 Attachment Manager
======================

This module provides integration with Amazon S3 for storing file attachments in Odoo.

Features
--------

* Store file attachments in Amazon S3 instead of the local filesystem.
* Automatically retry on failure with exponential backoff and jitter.
* Fallback to local filesystem storage (optional).

Installation
------------

1. Install the ``boto3`` Python package:

   ::

      pip install boto3

2. Install this module in your Odoo instance.

Configuration
-------------

1. Go to **Settings** -> **Technical** -> **System Parameters** in Odoo.
2. Create the following parameters:

::

   s3_attachment_manager.bucket            <your-s3-bucket-name>
   s3_attachment_manager.access_key_id        <your-aws-access-key-id>
   s3_attachment_manager.secret_access_key    <your-aws-secret-access-key>

.. note::
   If you are testing locally with **MinIO** or a custom S3-compatible service, also add:
   
   - **Key:** ``s3_attachment_manager.endpoint_url``
   - **Value:** ``http://minio:9000`` (or your custom URL)

   For **production on AWS S3**, do NOT add ``s3_attachment_manager.endpoint_url``.

Environment Variables (Optional Fallback)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, you can set the following environment variables in local Docker environments:

::

   S3_ATTACHMENT_MANAGER_BUCKET=<your-s3-bucket-name>
   S3_ATTACHMENT_MANAGER_ACCESS_KEY_ID=<your-aws-access-key-id>
   S3_ATTACHMENT_MANAGER_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
   S3_ATTACHMENT_MANAGER_ENDPOINT_URL=<your-endpoint-url>

Migration Script
----------------

To migrate existing local filestore attachments to S3/MinIO, run the migration script in Odoo Shell:

1. Access the Odoo shell:

   ::

      odoo shell -r <db_user> -w <db_password> --db_host <db_host> -d <db_name>

2. Run the script:

   ::

      exec(open('/path/to/migrate_to_s3.py').read())
      migrate_attachments_to_s3(self.env, limit=500)

License
-------

This module is licensed under the AGPL-3 License.
