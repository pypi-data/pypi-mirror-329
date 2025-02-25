from __future__ import annotations

import contextlib
import io
import mimetypes
import uuid
from collections.abc import Generator
from typing import Any

import fsspec
from pydantic import BaseModel
from pydantic.config import ConfigDict
from pydantic.fields import Field
from pydantic.functional_validators import model_validator
from typing_extensions import Self

from mosaico.integrations.base.adapters import Adapter
from mosaico.types import FilePath


class Media(BaseModel):
    """
    Represents a media object.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    """The unique identifier of the assets."""

    data: str | bytes | None = None
    """The content of the media."""

    path: FilePath | None = None
    """The path to the media."""

    mime_type: str | None = None
    """The MIME type of the media."""

    encoding: str = "utf-8"
    """The encoding of the media."""

    metadata: dict[str, Any] = Field(default_factory=dict)
    """The metadata of the media."""

    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True, extra="forbid")

    @property
    def description(self) -> str:
        """
        Returns a description of the media.
        """
        return self.metadata.get("description", "")

    @property
    def credit(self) -> str:
        """
        Returns the credits of the media.
        """
        return self.metadata.get("credit", "")

    @model_validator(mode="before")
    @classmethod
    def validate_media(cls, values: dict[str, Any]) -> Any:
        """
        Validates the content of the media.
        """
        if "data" not in values and "path" not in values:
            raise ValueError("Either data or path must be provided")

        return values

    @classmethod
    def from_path(
        cls,
        path: FilePath,
        *,
        encoding: str = "utf-8",
        mime_type: str | None = None,
        guess_mime_type: bool = True,
        metadata: dict | None = None,
        **kwargs: Any,
    ) -> Self:
        """
        Creates a media from a path.

        :param path: The path to the media.
        :param encoding: The encoding of the media.
        :param mime_type: The MIME type of the media.
        :param guess_mime_type: Whether to guess the MIME type.
        :param metadata: The metadata of the media.
        :param kwargs: Additional keyword arguments to the constructor.
        :return: The media.
        """
        if not mime_type and guess_mime_type:
            mime_type = mimetypes.guess_type(str(path))[0]

        return cls(
            data=None,
            path=path,
            metadata=metadata if metadata is not None else {},
            encoding=encoding,
            mime_type=mime_type,
            **kwargs,
        )

    @classmethod
    def from_data(
        cls,
        data: str | bytes,
        *,
        path: FilePath | None = None,
        metadata: dict | None = None,
        mime_type: str | None = None,
        **kwargs: Any,
    ) -> Self:
        """
        Creates a media from data.

        :param data: The data of the media.
        :param path: The path to the media.
        :param metadata: The metadata of the media.
        :param mime_type: The MIME type of the media.
        :param kwargs: Additional keyword arguments to the constructor.
        :return: The media.
        """
        return cls(
            data=data,
            path=path,
            metadata=metadata if metadata is not None else {},
            mime_type=mime_type,
            **{k: v for k, v in kwargs.items() if v is not None},
        )

    @classmethod
    def from_external(cls, adapter: Adapter[Media, Any], external: Any) -> Media:
        """
        Converts an external representation to a media.
        """
        if not isinstance(adapter, Adapter):
            raise TypeError("Adapter must be an instance of Adapter")
        return adapter.from_external(external)

    def to_external(self, adapter: Adapter[Media, Any]) -> Any:
        """
        Converts the media to an external representation.
        """
        if not isinstance(adapter, Adapter):
            raise TypeError("Adapter must be an instance of Adapter")
        return adapter.to_external(self)

    def to_string(self, *, storage_options: dict[str, Any] | None = None) -> str:
        """
        Returns the media as a string.
        """
        if isinstance(self.data, str):
            return self.data
        if isinstance(self.data, bytes):
            return self.data.decode(self.encoding)
        if self.data is None and self.path is not None:
            return _load_file(self.path, storage_options).decode(self.encoding)
        raise ValueError("Data is not a string or bytes")

    def to_bytes(self, *, storage_options: dict[str, Any] | None = None) -> bytes:
        """
        Returns the media as bytes.
        """
        if isinstance(self.data, bytes):
            return self.data
        if isinstance(self.data, str):
            return self.data.encode(self.encoding)
        if self.data is None and self.path is not None:
            return _load_file(self.path, storage_options)
        raise ValueError("Data is not a string or bytes")

    @contextlib.contextmanager
    def to_bytes_io(
        self, *, storage_options: dict[str, Any] | None = None
    ) -> Generator[io.BytesIO | io.BufferedReader]:
        """
        Read data as a byte stream.
        """
        if isinstance(self.data, bytes):
            yield io.BytesIO(self.data)
        elif self.data is None and self.path:
            yield from _yield_file(self.path, storage_options)
        else:
            raise NotImplementedError(f"Unable to convert blob {self}")


def _yield_file(path: FilePath, storage_options: dict[str, Any] | None = None) -> Generator[io.BufferedReader]:
    """
    Yields a file from a path.
    """
    fs, path_str = fsspec.core.url_to_fs(str(path), **(storage_options or {}))
    with fs.open(path_str, "rb") as f:
        yield f  # type: ignore


def _load_file(path: FilePath, storage_options: dict[str, Any] | None = None) -> bytes:
    """
    Loads a file from a path.
    """
    fs, path_str = fsspec.core.url_to_fs(str(path), **(storage_options or {}))
    with fs.open(path_str, "rb") as f:
        return f.read()
