from api.services.company_service import paginate_companies

def test_paginate_companies_basic(db, company, company2):
    result = paginate_companies(
        db=db,
        limit=1,
        offset=0,
        filters={},
    )

    assert result["total"] >= 2
    assert len(result["data"]) == 1

def test_paginate_companies_filter_by_name(db, company):
    result = paginate_companies(
        db=db,
        limit=10,
        offset=0,
        filters={"name": company.name},
    )

    assert result["total"] == 1
    assert result["data"][0]["name"] == company.name
