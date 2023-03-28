import logging
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    image_landscape = fields.Image(compute='_compute_image_landscape')
    image_portrait = fields.Image(compute='_compute_image_portrait')
    
    def _is_square_image(self):
        self.ensure_one()
        image = tools.base64_to_image(self.image_variant_128)
        width = image.width
        height = image.height
        ratio = height / width
        return 1.0 == ratio

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
            

    @api.depends('image_variant_128')
    def _compute_image_ratio(self):
        for record in self:
            img = record.image_variant_128
            if(img):
                image = tools.base64_to_image(img)
                width = image.width
                height = image.height
                ratio = height / width
                record.image_ratio = ratio
            else :
                record.image_ratio = 0

    def _get_square_images(self):
        self.ensure_one()
        images = self._get_images()
        filtered = []

        for image in images:
            if 'product.product' == image._name:
                if image._is_square_image():
                    filtered.append(image)
            else:   
                if image.is_image_square:
                    filtered.append(image)
                
        return filtered
        