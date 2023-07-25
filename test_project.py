from project import yes_or_no_answer, screen_clear, download_picture


def test_screen_clear():
    assert screen_clear() == True


def test_download_picture():
    assert download_picture("louay", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfps4Dz393uuISs0azkN6vr7jlOROQU10bMnUsmjqP&s") == True


def test_yes_or_no_answer_with_y(monkeypatch):
    # Define the input value you want to test
    input_value = "y"
    # Monkeypatch the input function to return the defined input value
    monkeypatch.setattr('builtins.input', lambda _: input_value)
    # Call the function with the expected input value
    result = yes_or_no_answer("Enter something: ")
    # The expected result is True
    expected_result =  True
    # Assert the result
    assert result == expected_result


def test_yes_or_no_answer_with_n(monkeypatch):
    # Define the input value you want to test
    input_value = "n"
    # Monkeypatch the input function to return the defined input value
    monkeypatch.setattr('builtins.input', lambda _: input_value)
    # Call the function with the expected input value
    result = yes_or_no_answer("Enter something: ")
    # The expected result is True
    expected_result = False
    # Assert the result
    assert result == expected_result
