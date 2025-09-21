import logging
import base64
import struct
from odoo import api, fields, models, tools, _
from odoo.tools.image import base64_to_image

RATIO_LIMIT_LANDSCAPE = 0.85
RATIO_LIMIT_PORTRAIT = 1.15

_logger = logging.getLogger(__name__)

class ImageMixinJT(models.AbstractModel):
    _inherit = 'image.mixin'

    image_ratio = fields.Float(compute='_compute_image_ratio', store=True, groups='base.group_user')
    
    def _get_webp_dimensions_from_header(self, img_data):
        """Extract dimensions from WebP header without decoding the image"""
        try:
            raw = base64.b64decode(img_data)
            if raw[:4] == b'RIFF' and raw[8:12] == b'WEBP':
                chunk_type = raw[12:16]
                if chunk_type == b'VP8X':
                    # VP8X format - dimensions at specific offsets
                    width = struct.unpack('<I', raw[24:27] + b'\x00')[0] + 1
                    height = struct.unpack('<I', raw[27:30] + b'\x00')[0] + 1
                    return width, height
                elif chunk_type == b'VP8 ':
                    # VP8 lossy format
                    width = struct.unpack('<H', raw[26:28])[0] & 0x3FFF
                    height = struct.unpack('<H', raw[28:30])[0] & 0x3FFF
                    return width, height
                elif chunk_type == b'VP8L':
                    # VP8L lossless format
                    bits = struct.unpack('<I', raw[21:25])[0]
                    width = (bits & 0x3FFF) + 1
                    height = ((bits >> 14) & 0x3FFF) + 1
                    return width, height
        except Exception as e:
            _logger.debug(f"Failed to read WebP header: {e}")
        return None, None
    
    @api.depends('image_128')
    def _compute_image_ratio(self):
        for record in self:
            img = record.image_128
            if img:
                try:
                    # Try Odoo's standard method first
                    image = base64_to_image(img)
                    width = image.width
                    height = image.height
                    ratio = height / width
                    record.image_ratio = ratio
                except Exception as e:
                    # Fallback to WebP header reading if PIL fails
                    _logger.debug(f"PIL decode failed: {e}, trying WebP header")
                    width, height = record._get_webp_dimensions_from_header(img)
                    if width and height:
                        record.image_ratio = height / width
                    else:
                        record.image_ratio = 0
            else:
                record.image_ratio = 0

    is_image_square = fields.Boolean(compute='_compute_is_image_square', store=True, groups='base.group_user')
    is_image_landscape = fields.Boolean(compute='_compute_is_image_landscape', store=True, groups='base.group_user')
    is_image_portrait = fields.Boolean(compute='_compute_is_image_portrait', store=True, groups='base.group_user')

    @api.depends('image_ratio')
    def _compute_is_image_square(self):
        for record in self:
            if RATIO_LIMIT_LANDSCAPE <= record.image_ratio <= RATIO_LIMIT_PORTRAIT:
                record.is_image_square = True
            else:
                record.is_image_square = False

    @api.depends('image_ratio')
    def _compute_is_image_landscape(self):
        for record in self:
            if record.image_ratio < RATIO_LIMIT_LANDSCAPE:
                record.is_image_landscape = True
            else:
                record.is_image_landscape = False

    @api.depends('image_ratio')
    def _compute_is_image_portrait(self):
        for record in self:
            if record.image_ratio > RATIO_LIMIT_PORTRAIT:
                record.is_image_portrait = True
            else:
                record.is_image_portrait = False