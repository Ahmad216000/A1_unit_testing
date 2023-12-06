import bibtex
import pytest
@pytest.fixture()

def setup_data():
    return{
        'simple_author_1':"Smith",
        'simple_author_2':"Jones",
        'author_1': "Jones Smith",
        'author_2': "Bob Jones",
        'author_3':"Justin Kenneth Pearson",
        'surname_first_1':"Pearson, Justin Kenneth",
        'surname_first_2':"Van Hentenryck, Pascal",
        "multiple_authors_1":"Pearson, Justin and Jones, Bob"
    }
def test_author_1(setup_data):
    #test only surname
    (Surename,FirstNames)=bibtex.extract_author(setup_data['simple_author_1'])
    assert (Surename,FirstNames)==('Smith','')

    (Surename, FirstNames) = bibtex.extract_author(setup_data['simple_author_2'])
    assert (Surename, FirstNames) == ('Jones', '')
#
def test_author_2(setup_data):
    (Surename, FirstNames) = bibtex.extract_author(setup_data['author_1'])
    assert (Surename, FirstNames) ==  ("Smith" , "Jones")
    (Surename, FirstNames) = bibtex.extract_author(setup_data['author_2'])
    assert (Surename, FirstNames) == ("Jones" , "Bob")

def test_author_3(setup_data):
    (Surename, FirstNames) = bibtex.extract_author(setup_data['author_3'])
    assert (Surename, FirstNames) ==  ("Pearson" , "Justin Kenneth")

def test_surname_first (setup_data) :
    (Surename, FirstNames) = bibtex.extract_author(setup_data['surname_first_1'])
    assert (Surename, FirstNames) == ("Pearson", "Justin Kenneth")
    (Surename, FirstNames) = bibtex.extract_author(setup_data['surname_first_2'])
    assert (Surename, FirstNames) == ("Van Hentenryck", "Pascal")
def test_multiple_authors_1 (setup_data) :
    Authors = bibtex.extract_authors(setup_data['multiple_authors_1'])
    assert Authors[0] == ("Pearson", "Justin")
    assert Authors[1] == ("Jones", "Bob")