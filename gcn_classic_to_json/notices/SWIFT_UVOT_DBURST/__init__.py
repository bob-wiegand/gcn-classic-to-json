# from ...utils import load_attachments
from ... import utils
from ..SWIFT_UVOT_DBURST_PROC import parse_uvot_image


def parse(bin):
    bin[
        18
    ]  # Unused. According to Docs: 'useless by the time it reaches GCN distribution'

    bin[20:22]  # Spare. According to Docs: '8 bytes for the future'

    tmp = {
        **parse_uvot_image(bin),
        **utils.load_attachments([("uvot_raw_image.fits", "uvot_raw_image_fits")]),
    }

    return tmp
