from api.domain.item import SkuGenerator


def test_generate_sku_format():
    sku = SkuGenerator.generate("Test Item 123")

    assert "-" in sku
    assert len(sku.split("-")[1]) == 6
