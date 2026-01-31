import pytest

class TestAccountRegistry:
    def test_add_account(self, registry, personal_account):
        registry.add_account(personal_account)
        assert registry.get_count() == 1
        
    def test_get_account_by_pesel(self, registry, personal_account):
        registry.add_account(personal_account)
        found = registry.get_account_by_pesel("12345678901")
        assert found == personal_account
        
    def test_get_account_by_pesel_not_found(self, registry):
        found = registry.get_account_by_pesel("00000000000")
        assert found is None

    def test_get_all_accounts(self, registry, personal_account):
        registry.add_account(personal_account)
        accounts = registry.get_all_accounts()
        assert len(accounts) == 1
        assert accounts[0] == personal_account