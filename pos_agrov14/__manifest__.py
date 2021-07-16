# -*- coding: utf-8 -*-
{
    'name': "POS AGROMORALES",
    'summary': "Modificaciones al POS para Agromorales",
    'description': """Agregar botón para consultar las listas de precios del producto seleccionado,
    modificación al ticket """,
    'author': "KRA-FA SA DE CV",
    'website': "http://www.krafa.com.mx",
    'category': 'Point of Sale',
    'version': '14.0.1',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_assets.xml',
        'views/sequence_ff.xml',
        'views/pos_order_to_invoice.xml',
        'views/order.xml'
    ],
    'qweb': [
        'static/src/xml/pos_agro.xml',
    ]
}