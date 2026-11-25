from mcp.server import MCPServer

from app.database.connection import SessionLocal
from app.models.apartment import Apartment

from sqlalchemy import func

mcp = MCPServer("StayOps AI")


@mcp.tool()
def say_hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"


@mcp.tool()
def search_apartments(city: str | None = None) -> list[dict]:
    """Search for available apartments, optionally filtering by provided parameters."""
    db = SessionLocal()

    try:
        query = db.query(Apartment).filter(Apartment.status == "available")

        if city:
            query = query.filter(func.lower(Apartment.city) == city.lower())

        apartments = query.all()

        return [
            {
                "id": apartment.id,
                "name": apartment.name,
                "city": apartment.city,
                "bedrooms": apartment.bedrooms,
                "max_guests": apartment.max_guests,
                "nightly_rate": float(apartment.nightly_rate),
            }
            for apartment in apartments
        ]

    finally:
        db.close()



if __name__ == "__main__":
    mcp.run()