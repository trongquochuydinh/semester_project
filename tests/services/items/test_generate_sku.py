from api.services.item_service import generate_sku

def test_generate_sku_format():
    sku = generate_sku("Test Item 123")

    assert "-" in sku
    assert len(sku.split("-")[1]) == 6
