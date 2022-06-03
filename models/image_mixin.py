import logging
from odoo import api, fields, models, api, tools, _

RATIO_LIMIT_LANDSCAPE = 0.85
RATIO_LIMIT_PORTRAIT = 1.15

class ImageMixinJT(models.AbstractModel):
    _inherit = 'image.mixin'

    image_ratio = fields.Float(compute='_compute_image_ratio')
    
    @api.depends('image_128')
    def _compute_image_ratio(self):
        for record in self:
            if(record.image_128):
                image = tools.base64_to_image(record.image_128)
                width = image.width
                height = image.height
                ratio = height / width
                record.image_ratio = ratio
            else :
                record.image_ratio = 0

    is_image_square = fields.Boolean(compute='_compute_is_image_square')
    is_image_landscape = fields.Boolean(compute='_compute_is_image_landscape')
    is_image_portrait = fields.Boolean(compute='_compute_is_image_portrait')

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