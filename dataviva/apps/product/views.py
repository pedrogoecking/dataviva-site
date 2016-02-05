# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.secex.services import Product as SecexProductService
from dataviva.api.secex.services import ProductTradePartners as SecexProductTradePartnersService
from dataviva.api.secex.services import ProductMunicipalities as SecexProductMunicipalitiesService
#from dataviva.api.secex.services import ProductByLocation as SecexProductByLocationService


mod = Blueprint('product', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/product',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<product_id>')
def index(product_id):

    bra_id = request.args.get('bra_id')

    #None database fields must be treated (/05?bra_id=2ce020008)
    #and templates with no data shall be omitted...

    #Vars to do tests:
    #section (depth == 2)
    #positon (depth == 6)
    #brazil (bra_id == None)
    #product_id = #05 #052601
    #bra_id = #None #4mg #4mg01 #4mg0000 #4mg010206 #2ce020008

    context = {
        'background_image':'static/img/bg-profile-location.jpg',
        'portrait':'static/img/mineric_product.jpg',
        'desc_general': 'Sample Text',
        'desc_international_trade': 'Sample Text',
        'desc_economic_opp': 'Sample Text'
    }

    context['bra_id'] = bra_id
    if bra_id:
        context['bra_id_len'] = len(bra_id)
    context['depth'] = len(product_id)

    header = {}
    body = {}

    if bra_id:
        secex_product_service = SecexProductByLocationService(bra_id=bra_id, product_id=product_id)

        #body['dest_name_export'] = secex_product_service.destination_with_more_exports()
        #body['dest_export_value'] = secex_product_service.highest_export_value_by_destination()
        #body['src_name_import'] =  secex_product_service.origin_with_more_imports()
        #body['src_import_value'] =  secex_product_service.highest_import_value_by_origin()

        if len(product_id) == 6:
            pass
            #header['pci'] = secex_product_service.product_complexity()
            #header['rca_wld'] = secex_product_service.rca_wld()
            #header['distance_wld'] = secex_product_service.distance_wld()
            #header['opp_gain_wld'] = secex_product_service.opp_gain_wld()

        if len(bra_id) != 9:
            pass
            #body['municipality_name_export'] = secex_product_service.municipality_with_more_exports()
            #body['municipality_export_value'] = secex_product_service.highest_export_value_by_municipality()
            #body['municipality_name_import'] = secex_product_service.municipality_with_more_imports()
            #body['municipality_import_value'] = secex_product_service.highest_import_value_by_municipality()

    else:
        secex_product_service = SecexProductService(product_id=product_id)
        secex_product_trade_service = SecexProductTradePartnersService(product_id=product_id)
        secex_product_munic_service = SecexProductMunicipalitiesService(product_id=product_id)

        body['municipality_name_export'] = secex_product_munic_service.municipality_with_more_exports()
        body['municipality_export_value'] = secex_product_munic_service.highest_export_value()
        body['municipality_name_import'] = secex_product_munic_service.municipality_with_more_imports()
        body['municipality_import_value'] = secex_product_munic_service.highest_import_value()
        body['dest_name_export'] = secex_product_trade_service.destination_with_more_exports()
        body['dest_export_value'] = secex_product_trade_service.highest_export_value()
        body['src_name_import'] = secex_product_trade_service.origin_with_more_imports()
        body['src_import_value'] = secex_product_trade_service.highest_import_value()


    header['name'] = secex_product_service.product_name()
    header['year'] = secex_product_service.product_name()
    header['trade_balance'] = secex_product_service.trade_balance()
    header['export_val'] = secex_product_service.total_exported()
    header['export_net_weight'] = secex_product_service.unity_weight_export_price()
    header['import_val'] = secex_product_service.total_imported()
    header['import_net_weight'] = secex_product_service.unity_weight_import_price()

    return render_template('product/index.html', body_class='perfil-estado', header=header, body=body, context=context)