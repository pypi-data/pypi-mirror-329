from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)

_xml_ids_to_unpublish = [
    "somconnexio.TrucadesIllimitades20GBPack",
    "somconnexio.CompartidesFibra1Gb3mobils50GB",
    "somconnexio.CompartidesFibra1Gb2mobils50GB",
    "somconnexio.CompartidesFibra600Mb3mobils50GB",
    "somconnexio.CompartidesFibra600Mb2mobils50GB",
    "somconnexio.CompartidesFibra300MbSF3mobils50GB",
    "somconnexio.CompartidesFibra300MbSF2mobils50GB",
    "somconnexio.CompartidesFibra300Mb3mobils50GB",
    "somconnexio.CompartidesFibra300Mb2mobils50GB",
    "somconnexio.PackSenseFixFibra300MbIL20GB",
    "somconnexio.PackFibra1GbIL20GB",
    "somconnexio.PackFibra600MbIL20GB",
    "somconnexio.PackFibra300MbIL20GB",
    "somconnexio.TrucadesIllimitades20GB",
    "somconnexio.TrucadesIllimitades150GB",
]

_xml_ids_to_publish = [
    "somconnexio.CompartidesFibra1Gb2mobils120GB",
    "somconnexio.CompartidesFibra1Gb2mobils120GBEiE",
    "somconnexio.CompartidesFibra1Gb3mobils120GB",
    "somconnexio.CompartidesFibra1Gb3mobils120GBEiE",
    "somconnexio.CompartidesFibra600Mb2mobils120GB",
    "somconnexio.CompartidesFibra600Mb2mobils120GBEiE",
    "somconnexio.CompartidesFibra600Mb3mobils120GB",
    "somconnexio.CompartidesFibra600Mb3mobils120GBEiE",
    "somconnexio.PackFibra1GbIL30GB",
    "somconnexio.PackFibra1GbIL30GBEiE",
    "somconnexio.PackFibra1GbIL50GBEiE",
    "somconnexio.PackFibra300Mb2mobils30GB",
    "somconnexio.PackFibra300Mb2mobils30GBEiE",
    "somconnexio.PackFibra300Mb3mobils30GB",
    "somconnexio.PackFibra300Mb3mobils30GBEiE",
    "somconnexio.PackFibra300MbIL30GB",
    "somconnexio.PackFibra300MbIL30GBEiE",
    "somconnexio.PackFibra300MbIL50GBEiE",
    "somconnexio.PackFibra300MbSF2mobils30GB",
    "somconnexio.PackFibra300MbSF2mobils30GBEiE",
    "somconnexio.PackFibra300MbSF3mobils30GB",
    "somconnexio.PackFibra300MbSF3mobils30GBEiE",
    "somconnexio.PackFibra600MbIL30GB",
    "somconnexio.PackFibra600MbIL30GBEiE",
    "somconnexio.PackFibra600MbIL50GBEiE",
    "somconnexio.PackSenseFixFibra300MbIL30GB",
    "somconnexio.PackSenseFixFibra300MbIL30GBEiE",
    "somconnexio.PackSenseFixFibra300MbIL50GBEiE",
    "somconnexio.TrucadesIllimitades17GB",
    "somconnexio.TrucadesIllimitades30GB",
    "somconnexio.TrucadesIllimitades90GB",
    "somconnexio.TrucadesIllimitades200GB",
    "somconnexio.SenseFixFibra300MbEiE",
    "somconnexio.Fibra300MbEiE",
    "somconnexio.Fibra600MbEiE",
    "somconnexio.Fibra1GbEiE",
]


@openupgrade.migrate()
def migrate(env, version):
    products_to_unpublish_ids = [
        env.ref(xml_id).id
        for xml_id in _xml_ids_to_unpublish
        if env.ref(xml_id, raise_if_not_found=False)
    ]
    products_to_publish_ids = [
        env.ref(xml_id).id
        for xml_id in _xml_ids_to_publish
        if env.ref(xml_id, raise_if_not_found=False)
    ]

    # Unpublish
    products_to_unpublish = env["product.product"].browse(products_to_unpublish_ids)
    products_to_unpublish.write({"public": False})
    _logger.info("Products unpublished: {}".format(products_to_unpublish_ids))

    # Publish
    products_to_publish = env["product.product"].browse(products_to_publish_ids)
    products_to_publish.write({"public": True})
    _logger.info("Products published: {}".format(products_to_publish_ids))
