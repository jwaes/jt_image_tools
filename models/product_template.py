import logging
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    image_landscape = fields.Image(compute='_compute_image_landscape')
    image_portrait = fields.Image(compute='_compute_image_portrait')
    
    @api.depends('image_ratio')
    def _compute_image_landscape(self):
        for record in self:
            # _logger.info("Record is %s", record.name)
            if record.is_image_landscape:
                # _logger.info("Image is landscape")
                record.image_landscape = record.image_512
            else :
                # _logger.info("Image is not landscape")
                record.image_landscape = self._get_product_template_landscape_image(record)

    @api.depends('image_ratio')
    def _compute_image_portrait(self):
        for record in self:
            if record.is_image_portrait:
                record.image_portrait = record.image_512
            else :
                record.image_portrait = self._get_product_template_portrait_image(record)

    def _get_product_template_landscape_image(self, record):
        # _logger.info("Looping landscape photos for record %s", record.id)
        # _logger.info("number of images: %s", len(record.product_template_image_ids))
        for product_image in record.product_template_image_ids :
            # _logger.info("product image %s : %s", product_image.id, product_image.name)
            if product_image.is_image_landscape:
                return product_image.image_512

    def _get_product_template_portrait_image(self, record):
        # _logger.info("Looping portrait photos for record %s", record.id)
        for product_image in record.product_template_image_ids :
            if product_image.is_image_portrait:
                return product_image.image_512              

    def _get_square_images(self):
        self.ensure_one()
        images = self._get_images()
        filtered = []

        for image in images:
            _logger.info("TMPL ratio is %s", image.image_ratio)
            if image.is_image_square:
                filtered.append(image)
                
        return filtered                     