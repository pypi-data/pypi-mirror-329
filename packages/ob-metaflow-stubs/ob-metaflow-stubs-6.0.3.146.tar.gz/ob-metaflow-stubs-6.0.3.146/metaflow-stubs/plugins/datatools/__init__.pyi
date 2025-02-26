######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.0.1+obcheckpoint(0.1.8);ob(v1)                                                    #
# Generated on 2025-02-25T21:49:22.561383                                                            #
######################################################################################################

from __future__ import annotations


from . import local as local
from .local import MetaflowLocalNotFound as MetaflowLocalNotFound
from .local import MetaflowLocalURLException as MetaflowLocalURLException
from .local import Local as Local
from . import s3 as s3
from .s3.s3 import MetaflowS3Exception as MetaflowS3Exception
from .s3.s3 import S3 as S3

def read_in_chunks(dst, src, src_sz, max_chunk_size):
    ...

