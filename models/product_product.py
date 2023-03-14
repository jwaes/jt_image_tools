import logging
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    image_landscape = fields.Image(compute='_compute_image_landscape')
    image_portrait = fields.Image(compute='_compute_image_portrait')
    
    @api.depends('image_ratio')
    def _compute_image_landscape(self):
        for record in self:
            if record.is_image_landscape:
                record.image_landscape = record.image_512
            else :
                record.image_landscape = self._get_product_variant_landscape_image(record)
                if not record.image_landscape:
                    record.image_landscape = record.product_tmpl_id._get_product_template_landscape_image(record)

    
    @api.depends('image_ratio')
    def _compute_image_portrait(self):
        for record in self:
            if record.is_image_portrait:
                record.image_portrait = record.image_512
            else :
                record.image_portrait = self._get_product_variant_portrait_image(record)
                if not record.image_portrait:
                    record.image_portrait = record.product_tmpl_id._get_product_template_portrait_image(record)


    def _get_product_variant_landscape_image(self, record):
        # _logger.info("Looping landscape photos for record %s", record.id)
        for product_image in record.product_variant_image_ids:
            if product_image.is_image_landscape:
                return product_image.image_512

    def _get_product_variant_portrait_image(self, record):
        # _logger.info("Looping portrait photos for record %s", record.id)
        for product_image in record.product_variant_image_ids:
            if product_image.is_image_portrait:
                return product_image.image_512                
            
    def _get_square_images(self):
        self.ensure_one()
        images = self._get_images()
        filtered = []

        for image in images:
            if image.is_image_square:
                filtered.append(image)
                
        return filtered
        