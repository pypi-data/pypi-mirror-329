from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)

_xml_ids_renames = [
    (
        "somconnexio.CompartidesFibra1Gb2mobils",
        "somconnexio.CompartidesFibra1Gb2mobils50GB",
    ),
    (
        "somconnexio.CompartidesFibra1Gb3mobils",
        "somconnexio.CompartidesFibra1Gb3mobils50GB",
    ),
    (
        "somconnexio.CompartidesFibra600Mb2mobils",
        "somconnexio.CompartidesFibra600Mb2mobils50GB",
    ),
    (
        "somconnexio.CompartidesFibra600Mb3mobils",
        "somconnexio.CompartidesFibra600Mb3mobils50GB",
    ),
    (
        "somconnexio.CompartidesFibra300MbSF2mobils",
        "somconnexio.CompartidesFibra300MbSF2mobils50GB",
    ),
    (
        "somconnexio.CompartidesFibra300MbSF3mobils",
        "somconnexio.CompartidesFibra300MbSF3mobils50GB",
    ),
    (
        "somconnexio.CompartidesFibra300Mb2mobils",
        "somconnexio.CompartidesFibra300Mb2mobils50GB",
    ),
    (
        "somconnexio.CompartidesFibra300Mb3mobils",
        "somconnexio.CompartidesFibra300Mb3mobils50GB",
    ),
    (
        "somconnexio.IsCompanyExclusive",
        "somconnexio.SalesCategory",
    ),
    (
        "somconnexio.SharingDataBond",
        "somconnexio.NumMobilesInPack",
    ),
    (
        "somconnexio.Sharing2Mobiles",
        "somconnexio.Pack2Mobiles",
    ),
    (
        "somconnexio.Sharing3Mobiles",
        "somconnexio.Pack3Mobiles",
    ),
]

_xml_ids_new_names = [
    (
        "somconnexio.SalesCategory",
        "Sales category",
    ),
    (
        "somconnexio.CompanyExclusive",
        "Company",
    ),
    (
        "somconnexio.NumMobilesInPack",
        "Number of mobiles in pack",
    ),
    (
        "somconnexio.Pack2Mobiles",
        "Pack 2 mobiles",
    ),
    (
        "somconnexio.Pack3Mobiles",
        "Pack 3 mobiles",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, _xml_ids_renames)

    # Update name field for product attributes and values instances
    for xml_id, new_name in _xml_ids_new_names:
        instance = env.ref(xml_id)
        instance.write({"name": new_name})

    _logger.info("XML IDs renamed")

    # Remove previous packs
    product_pack_lines = env["product.pack.line"].search([])
    for line in product_pack_lines:
        line.unlink()
