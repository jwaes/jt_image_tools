# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Recompute image ratio fields after adding WebP header reading support.
    
    This migration recalculates all image-related computed fields that were
    previously returning 0 due to PIL's inability to decode WebP images.
    """
    _logger.info("Starting migration for jt_image_tools 18.0.1.2.0")
    
    # Get the environment
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Recompute product.image fields
    product_images = env['product.image'].search([])
    if product_images:
        _logger.info(f"Recomputing image fields for {len(product_images)} product.image records")
        
        # Invalidate cache for stored fields
        product_images.invalidate_recordset([
            'image_ratio', 
            'is_image_square', 
            'is_image_landscape', 
            'is_image_portrait'
        ])
        
        # Force recomputation
        product_images._compute_image_ratio()
        product_images._compute_is_image_square()
        product_images._compute_is_image_landscape()
        product_images._compute_is_image_portrait()
        
        _logger.info("Completed recomputation for product.image records")
    
    # Recompute product.template fields
    product_templates = env['product.template'].search([])
    if product_templates:
        _logger.info(f"Recomputing image fields for {len(product_templates)} product.template records")
        
        # Invalidate cache for stored fields
        product_templates.invalidate_recordset([
            'image_ratio',
            'is_image_square',
            'is_image_landscape', 
            'is_image_portrait'
        ])
        
        # Force recomputation
        product_templates._compute_image_ratio()
        product_templates._compute_is_image_square()
        product_templates._compute_is_image_landscape()
        product_templates._compute_is_image_portrait()
        
        _logger.info("Completed recomputation for product.template records")
    
    # Commit changes
    cr.commit()
    
    _logger.info("Migration for jt_image_tools 18.0.1.2.0 completed successfully")