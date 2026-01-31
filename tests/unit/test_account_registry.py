import pytest

from src.personal_account import PersonalAccount

class TestAccountRegistry:
    def test_add_account(self, registry, personal_account):
        registry.add_account(personal_account)
        assert registry.get_count() == 1
    
    def test_add_duplicate_account(self, registry, personal_account):
        registry.add_account(personal_account)
        
        duplicate_account = PersonalAccount("Jan", "Kowalski", personal_account.pesel)
        result = registry.add_account(duplicate_account)

        assert result is False
        assert registry.get_count() == 1
    
    def test_add_account_without_pesel(self, registry, company_account):
        result = registry.add_account(company_account)
        assert result is True
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
    
    def test_delete_account_success(self, registry, personal_account):
        registry.add_account(personal_account)
        result = registry.delete_account(personal_account.pesel)
        assert result is True
        assert registry.get_count() == 0

    def test_delete_account_fail(self, registry):
        result = registry.delete_account("00000000000")
        assert result is False