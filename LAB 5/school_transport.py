"""Manage the school bus rider register, rosters, alerts, and fees."""

import sqlite3


conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE riders (
        id INTEGER PRIMARY KEY,
        student TEXT,
        route TEXT,
        stop TEXT,
        fee INTEGER
    )
    """
)


def enroll_rider(student, route, stop, fee):
    """Enroll a rider using parameterized SQL."""
    conn.execute(
        """
        INSERT INTO riders (student, route, stop, fee)
        VALUES (?, ?, ?, ?)
        """,
        (student, route, stop, fee),
    )
    conn.commit()


def route_roster(route):
    """Return student names assigned to a bus route."""
    result = conn.execute(
        "SELECT student FROM riders WHERE route = ?",
        (route,),
    )
    return [row[0] for row in result]


def export_roster(path, route):
    """Export a route's student roster to a UTF-8 text file."""
    with open(path, "w", encoding="utf-8") as output_file:
        for name in route_roster(route):
            output_file.write(f"{name}\n")


def dispatch_alert(route):
    """Print a dispatch alert without invoking a system shell."""
    print(f"Dispatching bus {route}")


def fee_collected(route):
    """Return the total fees collected for a route."""
    result = conn.execute(
        "SELECT SUM(fee) FROM riders WHERE route = ?",
        (route,),
    ).fetchone()
    return result[0] if result[0] is not None else 0


def main():
    """Run a demonstration of the school transport register."""
    enroll_rider("Tara", "R1", "Lake Road", 1800)
    enroll_rider("Kabir", "R1", "Mill Street", 1800)
    enroll_rider("Zoya", "R2", "Fort Gate", 2100)

    total_fees = fee_collected("R1")
    if total_fees != 3600:
        raise ValueError(f"Unexpected fee total: {total_fees}")

    export_roster("route_r1.txt", "R1")
    dispatch_alert("R1")
    print(route_roster("R2"))


if __name__ == "__main__":
    main()
