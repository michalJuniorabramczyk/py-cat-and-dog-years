import pytest
import app.main as main


# --- Testy z przykładów w zadaniu ---
@pytest.mark.parametrize(
    "cat,dog,expected",
    [
        (0, 0, [0, 0]),
        (14, 14, [0, 0]),
        (15, 15, [1, 1]),
        (23, 23, [1, 1]),
        (24, 24, [2, 2]),
        (27, 27, [2, 2]),
        (28, 28, [3, 2]),  # kot +1 co 4 lata, pies dopiero co 5 lat
        (100, 100, [21, 17]),
    ],
)
def test_examples_from_spec(cat: int, dog: int, expected: list[int]) -> None:
    assert main.get_human_age(cat, dog) == expected


# --- Granice przedziałów dla kota ---
@pytest.mark.parametrize(
    "age,expected",
    [
        (0, 0),   # < 15
        (14, 0),
        (15, 1),  # 15..23
        (23, 1),
        (24, 2),  # 24..27
        (27, 2),
        (28, 3),  # start kolejnego kroku (co 4 lata)
        (31, 3),
    ],
)
def test_cat_age_boundaries(age: int, expected: int) -> None:
    cat, dog = main.get_human_age(age, 0)
    assert cat == expected
    assert dog == 0  # kontrolnie — druga wartość bez wpływu


# --- Granice przedziałów dla psa ---
@pytest.mark.parametrize(
    "age,expected",
    [
        (0, 0),   # < 15
        (14, 0),
        (15, 1),  # 15..23
        (23, 1),
        (24, 2),  # 24..28
        (28, 2),
        (29, 3),  # start kolejnego kroku (co 5 lat)
        (33, 3),
    ],
)
def test_dog_age_boundaries(age: int, expected: int) -> None:
    cat, dog = main.get_human_age(0, age)
    assert dog == expected
    assert cat == 0  # kontrolnie — pierwsza wartość bez wpływu


# --- Ucinanie części ułamkowej (floor) ---
def test_discard_remainder_rules() -> None:
    # kot: po 24, dopiero co 4 lata +1 (25..27 wciąż 2)
    assert main.get_human_age(25, 0)[0] == 2
    assert main.get_human_age(26, 0)[0] == 2
    assert main.get_human_age(27, 0)[0] == 2
    assert main.get_human_age(28, 0)[0] == 3

    # pies: po 24, dopiero co 5 lat +1 (25..28 wciąż 2)
    assert main.get_human_age(0, 25)[1] == 2
    assert main.get_human_age(0, 28)[1] == 2
    assert main.get_human_age(0, 29)[1] == 3
