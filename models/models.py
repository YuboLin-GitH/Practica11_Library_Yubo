# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

# 1. Herencia del modelo: hereda del modelo existente de lector / partner 
class Member(models.Model):
    _inherit = 'res.partner'  # Cumple el requisito de herencia en algún modelo
    
    member_number = fields.Char(string='Número de Socio')

# 2. Modelo de Autor
class Author(models.Model):
    _name = 'library_yubo.author'
    _description = 'Autores de libros'

    name = fields.Char(string='Nombre', required=True)
    # Relación One2many: un autor puede tener varios libros 
    book_ids = fields.One2many('library_yubo.book', 'author_id', string='Libros')

# 3. Modelo de Libro (versión actualizada)
class Book(models.Model):
    _name = 'library_yubo.book'
    _description = 'Libros de la biblioteca'

    name = fields.Char(string='Título', required=True)
    # Relación Many2one: varios libros corresponden a un autor 
    author_id = fields.Many2one('library_yubo.author', string='Autor')
    # Relación Many2many: un libro puede pertenecer a varios géneros 
    genre_ids = fields.Many2many('library_yubo.genre', string='Géneros')
    
    state = fields.Selection([
        ('available', 'Disponible'), 
        ('borrowed', 'Prestado')
    ], string='Estado', default='available')

# 4. Modelo de Género de Libro
class Genre(models.Model):
    _name = 'library_yubo.genre'
    _description = 'Géneros de libros'
    
    name = fields.Char(string='Género', required=True)

# 5. Modelo de Préstamo (incluye lógica avanzada)
class Loan(models.Model):
    _name = 'library_yubo.loan'
    _description = 'Registro de préstamos'

    book_id = fields.Many2one('library_yubo.book', string='Libro', required=True)
    member_id = fields.Many2one('res.partner', string='Socio', required=True)
    
    # Uso de lambda para establecer el valor por defecto 
    loan_date = fields.Date(
        string='Fecha de Préstamo',
        default=lambda self: fields.Date.today()
    )
    return_date = fields.Date(string='Fecha de Devolución')
    
    # Campo calculado avanzado (almacenado en la base de datos) 
    duration = fields.Integer(
        string='Días de Préstamo',
        compute='_compute_duration',
        store=True  # <--- Significa que se almacena en una base de datos.
    )

    # Decorador @api.depends 
    @api.depends('loan_date', 'return_date')
    def _compute_duration(self):
        for record in self:
            if record.loan_date and record.return_date:
                record.duration = (record.return_date - record.loan_date).days
            else:
                record.duration = 0

    # Decorador @api.constrains (manejo de errores) 
    @api.constrains('return_date')
    def _check_return_date(self):
        for record in self:
            if record.return_date and record.return_date < record.loan_date:
                raise ValidationError(
                    'La fecha de devolución no puede ser anterior a la de préstamo.'
                )
