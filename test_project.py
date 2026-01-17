import pytest
from unittest.mock import patch
from project import adding
from project import editing
from project import removing
from project import searching_name
from project import searching_password

def test_adding():
    with patch("project.users", ["someone"]): # Makes users just be a list containing only someone
        with patch("builtins.input", side_effect=["meb", "m", "hello"]):
            assert adding() == ("meb", "hello")

        with patch("builtins.input", side_effect=["brother","M", "anything"]):
            assert adding() == ("brother", "anything") # Capital choice input checking

        with patch("builtins.input", side_effect=["someone", "not_someone", "m", "anything_again"]):
            assert adding() == ("not_someone", "anything_again") # Because the username already exists

        with patch("builtins.input", side_effect=["", "none_empty", "m", "password"]):
            assert adding() == ("none_empty", "password") # Because the username can't be nothing

        with patch("builtins.input", side_effect=["greater_than_30_sandin2jwnjkadjkwjiawsandiniawniifbaidbi913wniw121j", "less_than_30", "m", "password"]):
            assert adding() == ("less_than_30", "password") # Because the username must not be greater than 30

        with patch("builtins.input", side_effect=["username", "m", "low", "greater_than_20"]):
            assert adding() == ("username", "greater_than_20") # Because the password must not be less than 4 digits

        with patch("builtins.input", side_effect=["username", "m", "very_high_asndjasnioasnxoionqwooqwdniooasdasw", "less_than_20"]):
            assert adding() == ("username", "less_than_20") # Because the password must not be greater than 20 digits

        with patch("builtins.input", side_effect=["hello", "m", "cs50 world", "Cs50"]):
            assert adding() == ("hello", "Cs50") # Checking input password with space in between

        with patch("builtins.input", side_effect=["hello world", "hi", "m", "anything"]):
            assert adding() == ("hi", "anything") # Checking input user with space in between

        with patch("builtins.input", side_effect=["abcd", "r"]), patch("project.pwo.generate", return_value="random_password"):
            assert adding() == ("abcd", "random_password") # Return the username and a randomly generated password

        with patch("builtins.input", side_effect=["AbCd", "r"]), patch("project.pwo.generate", return_value="Random_Password"):
            assert adding() == ("AbCd", "Random_Password") # Capital username input checking

        with patch("builtins.input", side_effect=["hellow", "R"]), patch("project.pwo.generate", return_value="random_password"):
            assert adding() == ("hellow", "random_password") # Capital choice input checking


def test_editing():
    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["u","someone", "someone_else"]):
            assert editing() == [{"username": "someone_else", "password": "anything"}, {"username": "me", "password": "12345"}]

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["U","someone", "someone_e"]):
            assert editing() == [{"username": "someone_e", "password": "anything"}, {"username": "me", "password": "12345"}] # Checking Capital choice input

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["invalid_choice","u", "someone", "someone_else"]):
            assert editing() == [{"username": "someone_else", "password": "anything"}, {"username": "me", "password": "12345"}] # Checking a non option choice

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["u","none_user", "someone", "someone_e"]):
            assert editing() == [{"username": "someone_e", "password": "anything"}, {"username": "me", "password": "12345"}] # Checking none existing user editing

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["u","someone", "me", "someone", "someone_else"]):
            assert editing() == [{"username": "someone_else", "password": "anything"}, {"username": "me", "password": "12345"}] # Trying to change to a user that already exists

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["u","someone", " BrUh  "]):
            assert editing() == [{"username": "BrUh", "password": "anything"}, {"username": "me", "password": "12345"}] # Checking Capital user change input and space inputs

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["p","someone", "anything_else"]):
            assert editing() == [{"username": "someone", "password": "anything_else"}, {"username": "me", "password": "12345"}]

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["P","someone", "abcd"]):
            assert editing() == [{"username": "someone", "password": "abcd"}, {"username": "me", "password": "12345"}] # Checking Capital choice

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["p","none_existing", "someone", "1234ab"]):
            assert editing() == [{"username": "someone", "password": "1234ab"}, {"username": "me", "password": "12345"}] # Checking none existing users password edit

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["p","someone", "  AbCDefgH    "]):
            assert editing() == [{"username": "someone", "password": "AbCDefgH"}, {"username": "me", "password": "12345"}] # Checking Capital password change and space inputs

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["p","someone", "  AbCDefgH    "]):
            assert editing() == [{"username": "someone", "password": "AbCDefgH"}, {"username": "me", "password": "12345"}] # Checking password input with spaces

    with patch("project.storage", [{"username": "someone", "password": "anything"}, {"username": "me", "password": "12345"}]), \
        patch("project.users", ["someone", "me"]), patch("project.passwords", ["anything", "12345"]):
        with patch("builtins.input", side_effect=["p","someone", "AbCD 123", "AbCDefgH"]):
            assert editing() == [{"username": "someone", "password": "AbCDefgH"}, {"username": "me", "password": "12345"}] # Checking password input with spaces in between


def test_removing():
    with patch("project.users", ["me", "me1", "someone"]):
        with patch("builtins.input", side_effect=["me1"]):
            assert removing() == "me1"
        with patch("builtins.input", side_effect=["someone_else","me"]):
            assert removing() == "me"
        with patch("builtins.input", side_effect=["1", "2", "3", "someone"]):
            assert removing() == "someone"


def test_searching_name():
    with patch("project.storage", [{"username": "me", "password": "12345"}, {"username": "me1", "password": "my_password"}, {"username": "someone", "password": "12345"}]), \
        patch("project.users", ["me", "me1", "someone"]):
        assert searching_name("me") == {"username": "me", "password": "12345"} # Test when inputed through terminal

        assert searching_name("me1") == {"username": "me1", "password": "my_password"} # When inputed through terminal

        with patch("builtins.input", side_effect=["me1"]):
            assert searching_name(True) == {"username": "me1", "password": "my_password"} # Test when inputed manually

        with patch("builtins.input", side_effect=["none"]):
            with pytest.raises(SystemExit):
                searching_name(True) # sys.exit when the user inputed doesn't exist and is inputted manually

        with pytest.raises(SystemExit):
            searching_name("me_none") # sys.exit when the user inputed doesn't exist and is inputted through terminal


def test_searching_password():
    with patch("project.storage", [{"username": "me", "password": "12345"}, {"username": "me1", "password": "my_password"}, {"username": "someone", "password": "12345"}]), \
        patch("project.passwords", ["12345", "my_password", "12345"]):
        assert searching_password("my_password") == [{"username": "me1", "password": "my_password"}] # Test when inputed through terminal

        assert searching_password("12345") == [{"username": "me", "password": "12345"}, {"username": "someone", "password": "12345"},] # Test when there are multiple passwords with same username

        with patch("builtins.input", side_effect=["my_password"]):
            assert searching_password(True) == [{"username": "me1", "password": "my_password"}] # Test when inputed manually

        with patch("builtins.input", side_effect=["12345"]):
            assert searching_password(True) == [{"username": "me", "password": "12345"}, {"username": "someone", "password": "12345"}] # Test when there are multiple passwords with same username

        with patch("builtins.input", side_effect=["not_password"]):
            with pytest.raises(SystemExit):
                searching_password(True) # sys.exit when the password inputed doesn't exist and is inputted manually

        with pytest.raises(SystemExit):
            searching_password("me_none") # sys.exit when the password inputed doesn't exist and is inputted through terminal

