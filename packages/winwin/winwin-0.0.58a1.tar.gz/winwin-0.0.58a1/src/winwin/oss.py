from typing import Optional, Union
from urllib.parse import urlparse

import oss2
import ossfs


class OssUri:
    def __init__(self, bucket: str, path: str):
        self.bucket = bucket
        self.path = path.lstrip("/")

    def __str__(self):
        return f"oss://{self.bucket}/{self.path}"

    @classmethod
    def from_path(cls, path: str, bucket: Optional[str] = None):
        if path.startswith("oss://"):
            result = urlparse(path)
            return cls(result.netloc, result.path)
        return cls(bucket, path)

    @property
    def full_path(self):
        return f"/{self.bucket}/{self.path}"


class OssFs:
    def __init__(self, conn: dict):
        self.oss = conn
        self.fs = ossfs.OSSFileSystem(
            endpoint=self.oss["endpoint"],
            key=self.oss["access_id"],
            secret=self.oss["access_key"],
        )

    @property
    def endpoint(self) -> str:
        return self.oss["endpoint"]

    @property
    def external_endpoint(self) -> str:
        return self.oss["endpoint"].replace("-internal.aliyuncs.com", ".aliyuncs.com")

    @property
    def bucket(self) -> oss2.Bucket:
        return self.bucket_for(self.oss["bucket"])

    def bucket_for(self, bucket_name: str, external: bool = False) -> oss2.Bucket:
        auth = oss2.Auth(self.oss["access_id"], self.oss["access_key"])
        return oss2.Bucket(
            auth, self.external_endpoint if external else self.endpoint, bucket_name
        )

    def _build_uri(self, path) -> OssUri:
        return OssUri.from_path(path, self.oss["bucket"])

    def _full_path(self, path) -> str:
        return self._build_uri(path).full_path

    def _replace_path(self, p):
        p["Key"] = p["name"] = "oss:/" + p["name"]
        return p

    def write(self, path, data):
        uri = self._build_uri(path)
        self.bucket_for(uri.bucket).put_object(uri.path, data)

    def open(self, path, mode):
        return self.fs.open(self._full_path(path), mode)

    def exists(self, path):
        return self.fs.exists(self._full_path(path))

    def isdir(self, path):
        return self.fs.isdir(self._full_path(path))

    def isfile(self, path):
        return self.fs.isfile(self._full_path(path))

    def copy(self, src, dst, recursive=False):
        self.fs.copy(self._full_path(src), self._full_path(dst), recursive)

    def listdir(self, path):
        return [self._replace_path(p) for p in self.fs.listdir(self._full_path(path))]

    def stat(self, path):
        return self._replace_path(self.fs.stat(self._full_path(path)))

    def rm(self, path: Union[str, list[str]], recursive=False, maxdepth=None):
        if type(path) is str:
            self.fs.rm(self._full_path(path), recursive, maxdepth)
        else:
            self.fs.rm([self._full_path(p) for p in path], recursive, maxdepth)

    def absolute_path(self, path) -> str:
        return str(self._build_uri(path))

    def sign_url(self, path, expires=864000):
        uri = self._build_uri(path)
        return self.bucket_for(uri.bucket, True).sign_url("GET", uri.path, expires)
