"""Read local FITS headers without accessing image arrays."""

from dataclasses import dataclass, field
from pathlib import Path
import warnings

from astropy.io import fits


@dataclass
class HeaderInfo:
    kind: str
    header: fits.Header


@dataclass
class Inspection:
    path: str
    status: str = "NOT COMPLETED"
    size: int | None = None
    hdus: list[HeaderInfo] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)


class UnsupportedInput(Exception):
    """Input is outside the supported local, uncompressed FITS scope."""


def inspect_fits(path: str) -> Inspection:
    result = Inspection(path=path)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            source = Path(path)
            if not source.is_file():
                raise UnsupportedInput("Input is not an accessible regular file. Check the path and permissions.")
            with source.open("rb") as stream:
                stream.seek(0, 2)
                result.size = stream.tell()
                stream.seek(0)
                magic = stream.read(8)
                if magic.startswith((b"\x1f\x8b", b"BZh", b"PK\x03\x04", b"\xfd7zXZ\x00")):
                    raise UnsupportedInput("Compressed input is unsupported. Supply an uncompressed FITS file.")
                if magic != b"SIMPLE  ":
                    raise ValueError("Missing primary FITS SIMPLE card.")
                if result.size % 2880:
                    raise ValueError("File size is not a multiple of the FITS 2880-byte block size.")
                stream.seek(0)
                with fits.open(
                    stream, mode="readonly", memmap=False, lazy_load_hdus=False,
                    do_not_scale_image_data=True, disable_image_compression=True,
                    checksum=False, ignore_missing_simple=False, ignore_missing_end=False,
                ) as hdus:
                    hdus.verify("exception")
                    if hdus[0].header.get("SIMPLE") is not True:
                        raise ValueError("The primary header does not declare SIMPLE = T.")
                    end = 0
                    for hdu in hdus:
                        if hdu.header.get("ZIMAGE", False):
                            raise UnsupportedInput("Tile-compressed images are unsupported. Supply uncompressed FITS.")
                        for card in hdu.header.cards:
                            card.verify("exception")
                        info = hdu.fileinfo()
                        if info is None or info["hdrLoc"] != end:
                            raise ValueError("HDU layout could not be verified.")
                        end = info["datLoc"] + info["datSpan"]
                        if end > result.size:
                            raise ValueError("File is truncated: a declared HDU data span extends beyond the file.")
                        result.hdus.append(HeaderInfo(type(hdu).__name__, hdu.header.copy()))
                    if end != result.size:
                        raise ValueError("Unaccounted bytes follow the final HDU.")
                    result.status = "PASSED"
        except UnsupportedInput as exc:
            result.issues.append(str(exc))
        except OSError as exc:
            if exc.errno is None:
                result.status = "FAILED"
                result.issues.append(f"Invalid FITS structure: {exc}")
            else:
                result.issues.append(f"Unable to read the input: {exc}. Check access permissions and storage.")
        except (ValueError, TypeError, KeyError, IndexError, OverflowError, fits.verify.VerifyError) as exc:
            result.status = "FAILED"
            result.issues.append(f"Invalid FITS structure: {exc}")
        for warning in caught:
            result.issues.append(f"Parser warning: {warning.message}")
        if caught and result.status == "PASSED":
            result.status = "NOT COMPLETED"
    return result
