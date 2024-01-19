import pytest

from hindex_stats.db import MemoryDatabase


@pytest.fixture()
def db():
    return MemoryDatabase()


@pytest.fixture()
def data_banach():
    return {
        "name": "Stefan Banach",
        "interests": ["functional analysis"],
        "affiliation": "University of Lwów",
    }


@pytest.fixture()
def data_hilbert():
    return {
        "name": "David Hilbert",
        "interests": [
            "functional analysis",
            "invariant theory",
            "commutative algebra",
            "spectral theory",
        ],
        "affiliation": "Göttingen University",
    }


def test_can_read_written_object(db, data_banach):
    id = db.write(data_banach)
    assert db.read(id) == data_banach


def test_can_write_and_read_multiple_objects(db, data_banach, data_hilbert):
    id_banach = db.write(data_banach)
    id_hilbert = db.write(data_hilbert)

    assert db.read(id_banach) == data_banach
    assert db.read(id_hilbert) == data_hilbert


def test_reading_nonexistent_object_fails(db, data_banach):
    id = db.write(data_banach)

    with pytest.raises(KeyError):
        db.read(id + "asdf")


def test_can_read_written_reference(db):
    key = "1234abcdef"
    ref = "confs/iccs-2023"
    db.write_ref(ref, key)

    assert db.read_ref(ref) == key


def test_reading_nonexistent_reference_fails(db):
    db.write_ref("confs/iccs-2023", "1234abcdef")

    with pytest.raises(KeyError):
        db.read_ref("confs/iccs-2022")


def test_reading_removed_reference_fails(db):
    ref = "confs/iccs-2023"
    db.write_ref(ref, "1234abcdef")

    db.delete_ref(ref)

    with pytest.raises(KeyError):
        db.read_ref(ref)


def test_deleting_nonexistent_reference_fails(db):
    db.write_ref("confs/iccs-2023", "1234abcdef")

    with pytest.raises(KeyError):
        db.delete_ref("confs/iccs-2022")
