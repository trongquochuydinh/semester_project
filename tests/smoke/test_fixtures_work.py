
# Successfully created a company, linked a user and an item to that company
def test_fixtures_work(company, admin, item):
    assert company.id is not None
    assert admin.company_id == company.id
    assert item.company_id == company.id
    assert item.quantity == 10