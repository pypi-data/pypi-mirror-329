# pylint: disable=C0302
"""Unit Tests of Drolta.

This test files does not use pytest fixtures because the database connection
needs to be closed at the end of each test. There is probably a more elegant
way to handle this (probably with a context manager). However, this works for
now.

"""

import sqlite3

import pytest

import drolta
import drolta.engine
from drolta.interpreter import has_alias_cycle


def initialize_test_data(db: sqlite3.Connection) -> None:
    """Initializes the provided data"""

    cursor = db.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS characters;
        DROP TABLE IF EXISTS houses;
        DROP TABLE IF EXISTS relations;

        CREATE TABLE characters (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT,
            house_id INTEGER,
            sex TEXT,
            life_stage TEXT,
            is_alive INTEGER,
            FOREIGN KEY (house_id) REFERENCES houses(id)
        ) STRICT;

        CREATE TABLE houses (
            id INTEGER NOT NULL PRIMARY KEY,
            name TEXT NOT NULL,
            reputation INT NOT NULL,
            is_noble INT NOT NULL
        ) STRICT;

        CREATE TABLE relations (
            from_id INTEGER NOT NULL,
            to_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            FOREIGN KEY (from_id) REFERENCES characters(id),
            FOREIGN KEY (to_id) REFERENCES characters(id)
        ) STRICT;
        """
    )

    cursor.executemany(
        """
        INSERT INTO
        characters (id, name, house_id, sex, life_stage, is_alive)
        VALUES
        (?, ?, ?, ?, ?, ?);
        """,
        [
            (1, "Rhaenyra", 1, "F", "Adult", 1),
            (2, "Laenor", 2, "M", "Adult", 1),
            (3, "Harwin", 3, "M", "Adult", 1),
            (4, "Jacaerys", 2, "M", "Teen", 1),
            (5, "Addam", None, "M", "Teen", 1),
            (6, "Corlys", 2, "M", "Adult", 1),
            (7, "Marilda", None, "F", "Adult", 0),
            (8, "Alyn", None, "M", "Adult", 1),
            (9, "Rhaenys", 1, "F", "Adult", 0),
            (10, "Laena", 2, "F", "Adult", 0),
            (11, "Daemon", 1, "M", "Adult", 1),
            (12, "Baela", 1, "F", "Teen", 1),
            (13, "Viserys", 1, "M", "Senior", 0),
            (14, "Alicent", 5, "F", "Adult", 1),
            (15, "Otto", 5, "M", "Senior", 1),
            (16, "Aegon", 1, "M", "Teen", 1),
            (17, "Cristen", 4, "M", "Adult", 1),
        ],
    )

    cursor.executemany(
        """
        INSERT INTO
            houses(id, name, reputation, is_noble)
        VALUES
            (?, ?, ?, ?);
        """,
        [
            (1, "Targaryen", 85, 1),
            (2, "Velaryon", 80, 1),
            (3, "Strong", 20, 0),
            (4, "Cole", -20, 0),
            (5, "Hightower", 50, 1),
        ],
    )

    cursor.executemany(
        """
        INSERT INTO
            relations (from_id, to_id, type)
        VALUES
            (?, ?, ?);
        """,
        [
            (4, 1, "Mother"),  # Jace -> Rhaenyra
            (4, 2, "Father"),  # Jace -> Laenor
            (4, 3, "BiologicalFather"),  # Jace -> Harwin
            (5, 6, "BiologicalFather"),  # Addam -> Corlys
            (2, 6, "BiologicalFather"),  # Laenor -> Corlys
            (2, 6, "Father"),  # Laenor -> Corlys
            (5, 7, "Mother"),  # Addam -> Marilda
            (8, 7, "Mother"),  # Alyn -> Marilda
            (8, 6, "BiologicalFather"),  # Alyn -> Corlys
            (2, 9, "Mother"),  # Laenor -> Rhaenys
            (10, 9, "Mother"),  # Laena -> Rhaenys
            (10, 6, "Father"),  # Laena -> Corlys
            (10, 6, "BiologicalFather"),  # Laena -> Corlys
            (6, 9, "Widower"),  # Corlys -> Rhaenys
            (6, 9, "FormerSpouse"),  # Corlys -> Rhaenys
            (9, 6, "FormerSpouse"),  # Rhaenys -> Corlys
            (12, 10, "Mother"),  # Baela -> Laena
            (12, 11, "Father"),  # Baela -> Daemon
            (12, 11, "BiologicalFather"),  # Baela -> Daemon
            (1, 11, "Spouse"),  # Rhaenyra -> Daemon
            (11, 1, "Spouse"),  # Daemon -> Rhaenyra
            (10, 11, "FormerSpouse"),  # Laena -> Daemon
            (11, 10, "FormerSpouse"),  # Daemon -> Laena
            (11, 10, "Widower"),  # Daemon -> Laena
            (1, 13, "Father"),  # Rhaenyra -> Viserys
            (1, 13, "BiologicalFather"),  # Rhaenyra -> Viserys
            (16, 14, "Mother"),  # Aegon -> Alicent
            (14, 15, "Father"),  # Alicent => Otto
            (14, 15, "BiologicalFather"),  # Alicent => Otto
        ],
    )

    db.commit()


def test_define_predicate_alias() -> None:
    """Ensure table aliases are registered and properly used."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    engine.execute_script(
        """
        ALIAS characters AS Character;
        """
    )

    rows = engine.query(
        """
        FIND ?x
        WHERE
            Character(id=?x)
        """,
        db,
    ).fetch_all()

    assert len(rows) == 17

    db.close()


def test_define_rule_alias() -> None:
    """Ensure rule aliases and registered and properly used."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    engine.execute_script(
        """
        ALIAS FromNobleHouse AS IsNobility;

        DEFINE
            FromNobleHouse(?x)
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, is_noble=TRUE);
        """
    )

    rows = engine.query(
        """
        FIND ?x
        WHERE
            IsNobility(x=?x);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 12

    db.close()


def test_define_rule() -> None:
    """Ensure rules can be defined and used within a query."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    engine.execute_script(
        """
        DEFINE
            FromNobleHouse(?x)
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, is_noble=TRUE);
        """
    )

    rows = engine.query(
        """
        FIND ?x
        WHERE
            FromNobleHouse(x=?x);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 12

    db.close()


def test_composite_rules() -> None:
    """Test composing a rule using other rules."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    engine.execute_script(
        """
        DEFINE
            IsAdult(?x)
        WHERE
            characters(id=?x, life_stage="Adult");

        DEFINE
            FromNobleHouse(?x)
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, is_noble=TRUE);

        DEFINE
            AdultNoble(?x)
        WHERE
            IsAdult(x=?x)
            FromNobleHouse(x=?x);
        """
    )

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            AdultNoble(x=?x);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 7

    db.close()


def test_single_predicate_query() -> None:
    """Test queries composed of a single predicate."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND ?x
        WHERE
            characters(id=?x);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 17

    rows = engine.query(
        """
        FIND ?x, ?house_id
        WHERE
            characters(id=?x, house_id=?house_id);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 17

    db.close()


def test_query_output_aliases() -> None:
    """Test that queries output columns with the proper alias names."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?x AS character_id
        WHERE
            characters(id=?x);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 17

    db.close()


def test_rule_param_aliases() -> None:
    """Test that rule parameters can be referred to using provided aliases."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    engine.execute_script(
        """
        DEFINE
            FromNobleHouse(?x AS character_id)
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, is_noble=TRUE);
        """
    )

    rows = engine.query(
        """
        FIND ?x
        WHERE
            FromNobleHouse(character_id=?x);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 12

    db.close()


def test_multi_predicate_query() -> None:
    """Test a query that joins across multiple predicate statements."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, is_noble=TRUE);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 12

    db.close()


def test_eq_filter() -> None:
    """Test the equals comparison filter."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, life_stage=?life_stage, house_id=?house_id)
            houses(id=?house_id, name="Targaryen")
            (?life_stage = "Adult");
        """,
        db,
    ).fetch_all()

    assert len(rows) == 3

    db.close()


def test_neq_filter() -> None:
    """Test the not equals filter."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, life_stage=?life_stage, house_id=?house_id)
            houses(id=?house_id, name="Targaryen")
            (?life_stage != "Adult");
        """,
        db,
    ).fetch_all()

    assert len(rows) == 3

    engine.execute_script(
        """
        ALIAS characters AS Character;
        ALIAS relations AS Relation;
        ALIAS houses AS House;

        DEFINE
            PaternalHalfSiblings(?x, ?y)
        WHERE
            Relation(from_id=?x, to_id=?bf, type="BiologicalFather")
            Relation(from_id=?y, to_id=?bf, type="BiologicalFather")
            Relation(from_id=?x, to_id=?x_m, type="Mother")
            Relation(from_id=?y, to_id=?y_m, type="Mother")
            ((?x_m != ?y_m) AND (?x != ?y));
        """
    )

    rows = engine.query(
        """
        FIND
        ?siblingId, ?siblingName
        WHERE
            Character(id=?adam_id, name="Addam")
            PaternalHalfSiblings(x=?adam_id, y=?siblingId)
            Character(id=?siblingId, name=?siblingName)
        ORDER BY ?siblingId;
        """,
        db,
    ).fetch_all()

    assert len(rows) == 2

    db.close()


def test_lt_filter() -> None:
    """Test the less than filter."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?house_id
        WHERE
            houses(id=?house_id, reputation=?rep)
            (?rep < 50);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 2

    db.close()


def test_gt_filter() -> None:
    """Test the greater than filter."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?house_id
        WHERE
            houses(id=?house_id, reputation=?rep)
            (?rep > 50);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 2

    db.close()


def test_lte_filter() -> None:
    """Test the less-than or equal to filter."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?house_id
        WHERE
            houses(id=?house_id, reputation=?rep)
            (?rep <= 50);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 3

    db.close()


def test_gte_filter() -> None:
    """Test the greater-than or equal to filter."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?house_id
        WHERE
            houses(id=?house_id, reputation=?rep)
            (?rep >= 50);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 3

    db.close()


def test_membership_filter() -> None:
    """Test the list membership filter."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, name=?family_name)
            (?family_name IN ["Velaryon", "Targaryen"]);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 10

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, name=?family_name)
            (?family_name NOT IN ["Velaryon", "Targaryen"]);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 4

    db.close()


def test_null_check() -> None:
    """Test checking for NULL values."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, house_id=NULL);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 3

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, house_id=?house_id)
            (?house_id = NULL);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 3

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, house_id=?house_id)
            (?house_id != NULL);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 14

    db.close()


def test_and_statement() -> None:
    """Test using AND keyword to combine filter statements."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, house_id=?house_id, is_alive=?is_alive)
            houses(id=?house_id, name=?family_name)
            ((?family_name = "Velaryon") AND (?is_alive = FALSE));
        """,
        db,
    ).fetch_all()

    assert len(rows) == 1

    db.close()


def test_or_statement() -> None:
    """Test using OR keyword to combine filter statements."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, name=?family_name)
            ((?family_name = "Velaryon") OR (?family_name = "Targaryen"));
        """,
        db,
    ).fetch_all()

    assert len(rows) == 10

    db.close()


def test_not_filter_statement() -> None:
    """Test using NOT keyword on filter statements."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, name=?family_name)
            (NOT (?family_name IN ["Velaryon", "Targaryen"]));
        """,
        db,
    ).fetch_all()

    assert len(rows) == 4

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, name=?family_name)
            (NOT ((?family_name = "Velaryon") OR (?family_name = "Targaryen")));
        """,
        db,
    ).fetch_all()

    assert len(rows) == 4

    db.close()


def test_not_predicate_statement() -> None:
    """Test using NOT keyword on predicate statements."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?x
        WHERE
            characters(id=?x)
            NOT characters(id=?x, is_alive=FALSE);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 13


def test_not_rule_statement() -> None:
    """Test using NOT keyword on rule statements."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    engine.execute_script(
        """
        DEFINE
            FromNobleHouse(?x)
        WHERE
            characters(id=?x, house_id=?house_id)
            houses(id=?house_id, is_noble=TRUE);
        """
    )

    rows = engine.query(
        """
        FIND ?x
        WHERE
            characters(id=?x)
            NOT FromNobleHouse(x=?x);
        """,
        db,
    ).fetch_all()

    assert len(rows) == 5

    db.close()


def test_alias_cycle_detection() -> None:
    """Test that alias cycles are detected."""

    aliases = {"A": "D", "B": "C", "G": "D", "E": "A", "F": "B"}

    assert has_alias_cycle(aliases) == (False, "")

    aliases["C"] = "F"

    assert has_alias_cycle(aliases) == (True, "B")


def test_duplicate_queries() -> None:
    """Test that running the same query twice does not throw duplicate table error."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    engine.execute_script(
        """
        ALIAS characters AS Character;
        ALIAS relations AS Relation;
        ALIAS houses AS House;

        DEFINE
            PaternalHalfSiblings(?x, ?y)
        WHERE
            Relation(from_id=?x, to_id=?bf, type="BiologicalFather")
            Relation(from_id=?y, to_id=?bf, type="BiologicalFather")
            Relation(from_id=?x, to_id=?x_m, type="Mother")
            Relation(from_id=?y, to_id=?y_m, type="Mother")
            ((?x_m != ?y_m) AND (?x != ?y));
        """
    )

    engine.query(
        """
        FIND
        ?siblingId, ?siblingName
        WHERE
            Character(id=?adam_id, name="Addam")
            PaternalHalfSiblings(x=?adam_id, y=?siblingId)
            Character(id=?siblingId, name=?siblingName)
        ORDER BY ?siblingId;
        """,
        db,
    )

    engine.query(
        """
        FIND
        ?siblingId, ?siblingName
        WHERE
            Character(id=?adam_id, name="Addam")
            PaternalHalfSiblings(x=?adam_id, y=?siblingId)
            Character(id=?siblingId, name=?siblingName)
        ORDER BY ?siblingId;
        """,
        db,
    )

    db.close()


def test_double_fetch_throws_error() -> None:
    """Ensure that double fetching data throws an exception."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    engine.execute_script(
        """
        ALIAS characters AS Character;
        ALIAS relations AS Relation;
        ALIAS houses AS House;

        DEFINE
            PaternalHalfSiblings(?x, ?y)
        WHERE
            Relation(from_id=?x, to_id=?bf, type="BiologicalFather")
            Relation(from_id=?y, to_id=?bf, type="BiologicalFather")
            Relation(from_id=?x, to_id=?x_m, type="Mother")
            Relation(from_id=?y, to_id=?y_m, type="Mother")
            ((?x_m != ?y_m) AND (?x != ?y));
        """
    )

    result = engine.query(
        """
        FIND
        ?siblingId, ?siblingName
        WHERE
            Character(id=?adam_id, name="Addam")
            PaternalHalfSiblings(x=?adam_id, y=?siblingId)
            Character(id=?siblingId, name=?siblingName)
        ORDER BY ?siblingId;
        """,
        db,
    )

    result.fetch_all()

    with pytest.raises(RuntimeError):
        result.fetch_all()

    result = engine.query(
        """
        FIND
        ?siblingId, ?siblingName
        WHERE
            Character(id=?adam_id, name="Addam")
            PaternalHalfSiblings(x=?adam_id, y=?siblingId)
            Character(id=?siblingId, name=?siblingName)
        ORDER BY ?siblingId;
        """,
        db,
    )

    # Have to call next() on the generator. Otherwise, the user
    # technically never read the data and it is still valid
    # to call fetch_all().
    next(result.fetch_chunks(20))

    with pytest.raises(RuntimeError):
        result.fetch_all()

    db.close()


def test_count_aggregate() -> None:
    """Test the COUNT aggregate function."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    engine.execute_script(
        """
        ALIAS characters AS Character;
        ALIAS relations AS Relation;
        ALIAS houses AS House;

        DEFINE
            HouseSize(?house_id AS id, COUNT(?character_id) AS size)
        WHERE
            Character(id=?character_id, house_id=?house_id)
            House(id=?house_id)
        GROUP BY ?house_id
        ORDER BY ?house_id ASC;
        """
    )

    rows = engine.query(
        """
        FIND
            ?house_id, ?size
        WHERE
            HouseSize(id=?house_id, size=?size)
        ORDER BY ?size DESC;
        """,
        db,
    ).fetch_all()

    assert len(rows) == 5
    assert rows[0] == (1, 6)
    assert rows[1] == (2, 4)
    assert rows[2] == (5, 2)

    db.close()


def test_order_by_asc() -> None:
    """Test ORDER BY ACS clause support."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?character_id, ?house_id
        WHERE
            characters(id=?character_id, house_id=?house_id)
        ORDER BY ?house_id;
        """,
        db,
    ).fetch_all()

    assert rows[0][1] is None
    assert rows[3][1] == 1
    assert rows[-1][1] == 5

    rows = engine.query(
        """
        FIND
            ?character_id, ?house_id
        WHERE
            characters(id=?character_id, house_id=?house_id)
        ORDER BY ?house_id ASC;
        """,
        db,
    ).fetch_all()

    assert rows[0][1] is None
    assert rows[3][1] == 1
    assert rows[-1][1] == 5

    rows = engine.query(
        """
        FIND
            ?character_id, ?house_id
        WHERE
            characters(id=?character_id, house_id=?house_id)
        ORDER BY ?house_id ASC NULLS FIRST;
        """,
        db,
    ).fetch_all()

    assert rows[0][1] is None
    assert rows[3][1] == 1
    assert rows[-1][1] == 5

    rows = engine.query(
        """
        FIND
            ?character_id, ?house_id
        WHERE
            characters(id=?character_id, house_id=?house_id)
        ORDER BY ?house_id ASC NULLS LAST;
        """,
        db,
    ).fetch_all()

    assert rows[0][1] == 1
    assert rows[6][1] == 2
    assert rows[-1][1] is None


def test_order_by_desc() -> None:
    """Test ORDER BY DESC clause support."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?character_id, ?house_id
        WHERE
            characters(id=?character_id, house_id=?house_id)
        ORDER BY ?house_id DESC;
        """,
        db,
    ).fetch_all()

    assert rows[0][1] == 5
    assert rows[2][1] == 4
    assert rows[-1][1] is None

    rows = engine.query(
        """
        FIND
            ?character_id, ?house_id
        WHERE
            characters(id=?character_id, house_id=?house_id)
        ORDER BY ?house_id DESC NULLS FIRST;
        """,
        db,
    ).fetch_all()

    assert rows[0][1] is None
    assert rows[3][1] == 5
    assert rows[-1][1] == 1

    rows = engine.query(
        """
        FIND
            ?character_id, ?house_id
        WHERE
            characters(id=?character_id, house_id=?house_id)
        ORDER BY ?house_id DESC NULLS LAST;
        """,
        db,
    ).fetch_all()

    assert rows[0][1] == 5
    assert rows[2][1] == 4
    assert rows[-1][1] is None


def test_order_by_multiple_columns() -> None:
    """Test ORDER BY support for multiple columns."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?character_id, ?name, ?house_id
        WHERE
            characters(id=?character_id, name=?name, house_id=?house_id)
        ORDER BY ?house_id ASC, ?name DESC;
        """,
        db,
    ).fetch_all()

    assert rows[0][1] == "Marilda"
    assert rows[1][1] == "Alyn"
    assert rows[2][1] == "Addam"
    assert rows[3][1] == "Viserys"


def test_limit() -> None:
    """Test LIMIT clause support."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?character_id, ?name
        WHERE
            characters(id=?character_id, name=?name)
        ORDER BY ?character_id
        LIMIT 5;
        """,
        db,
    ).fetch_all()

    assert len(rows) == 5
    assert rows[0][1] == "Rhaenyra"
    assert rows[1][1] == "Laenor"
    assert rows[2][1] == "Harwin"
    assert rows[3][1] == "Jacaerys"
    assert rows[4][1] == "Addam"


def test_limit_offset() -> None:
    """Test LIMIT with OFFSET support."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?character_id, ?name
        WHERE
            characters(id=?character_id, name=?name)
        ORDER BY ?character_id
        LIMIT 5 OFFSET 5;
        """,
        db,
    ).fetch_all()

    assert len(rows) == 5
    assert rows[0][1] == "Corlys"
    assert rows[1][1] == "Marilda"
    assert rows[2][1] == "Alyn"
    assert rows[3][1] == "Rhaenys"
    assert rows[4][1] == "Laena"


def test_group_by() -> None:
    """Test GROUP BY support."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?house_id, COUNT(?character_id) AS size
        WHERE
            characters(id=?character_id, house_id=?house_id)
        GROUP BY ?house_id
        ORDER BY ?size DESC;
        """,
        db,
    ).fetch_all()

    assert len(rows) == 6


def test_group_by_multiple_columns() -> None:
    """Test GROUP BY multiple columns support."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            ?house_id, ?sex, COUNT(?character_id) AS size
        WHERE
            characters(id=?character_id, sex=?sex, house_id=?house_id)
        GROUP BY ?house_id, ?sex
        ORDER BY ?size DESC;
        """,
        db,
    ).fetch_all()

    assert len(rows) == 10


def test_avg_aggregate() -> None:
    """Test support for the AVG aggregate function."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            AVG(?rep) AS avg_rep
        WHERE
            houses(reputation=?rep);
        """,
        db,
    ).fetch_all()

    assert rows[0][0] == 43


def test_max_aggregate() -> None:
    """Test support for the MAX aggregate function."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            MAX(?rep)
        WHERE
            houses(reputation=?rep);
        """,
        db,
    ).fetch_all()

    assert rows[0][0] == 85


def test_min_aggregate() -> None:
    """Test support for the MIN aggregate function."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            MIN(?rep)
        WHERE
            houses(reputation=?rep);
        """,
        db,
    ).fetch_all()

    assert rows[0][0] == -20


def test_sum_aggregate() -> None:
    """Test support for the SUM aggregate function."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = drolta.engine.QueryEngine()

    rows = engine.query(
        """
        FIND
            SUM(?rep)
        WHERE
            houses(reputation=?rep);
        """,
        db,
    ).fetch_all()

    assert rows[0][0] == 215
