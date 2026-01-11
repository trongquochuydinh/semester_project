from api.services.company_service import list_companies


def test_superadmin_can_list_all_companies(
    db, superadmin, company, company2
):
    response = list_companies(db=db, current_user=superadmin)

    ids = {c.id for c in response.companies}

    assert company.id in ids
    assert company2.id in ids

def test_admin_sees_only_own_company(
    db, admin, company, company2
):
    response = list_companies(db=db, current_user=admin)

    ids = {c.id for c in response.companies}

    assert ids == {company.id}


