from world.models import Room

def get_initial_rooms() -> dict[str, Room]:
    return {
        "hallway": Room(
            name="Hallway",
            description="A narrow, dimly lit hallway. It connects the kitchen and the bedroom.",
            contents=["a small rug", "a coat rack"]
        ),
        "kitchen": Room(
            name="Kitchen",
            description="A cozy kitchen smelling of fresh coffee. There's a wooden table in the center.",
            contents=["a wooden table", "a coffee maker", "some plates"]
        ),
        "bedroom": Room(
            name="Bedroom",
            description="A quiet, comfortable bedroom with a large bed.",
            contents=["a large bed", "a nightstand", "a lamp"]
        )
    }
