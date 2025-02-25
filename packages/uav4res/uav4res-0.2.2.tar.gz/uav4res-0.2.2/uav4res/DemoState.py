import pygame
from .engine.GameState import GameState
from .engine.GameStateManager import GameStateManager
from .engine.InputManager import InputManager
from .Uav import Uav
from .SwarmManager import SwarmManager
from .Map import Map


class DemoState(GameState):
    def __init__(self):
        self.swarm_manager = SwarmManager()
        # Create UAVs (example values)
        uav1 = Uav(
            remain_energy=100,
            min_speed=1,
            max_speed=10,
            buffer_data=50,
            x=150,
            y=300,
            size=30,
            connection_range=100,
        )
        uav2 = Uav(
            remain_energy=100,
            min_speed=1,
            max_speed=10,
            buffer_data=50,
            x=800,
            y=210,
            size=30,
            connection_range=50,
        )
        uav3 = Uav(
            remain_energy=100,
            min_speed=1,
            max_speed=10,
            buffer_data=50,
            x=300,
            y=300,
            size=30,
            connection_range=70,
        )
        uav4 = Uav(
            remain_energy=100,
            min_speed=1,
            max_speed=10,
            buffer_data=50,
            x=700,
            y=200,
            size=30,
            connection_range=100,
        )
        uav5 = Uav(
            remain_energy=100,
            min_speed=1,
            max_speed=10,
            buffer_data=50,
            x=500,
            y=900,
            size=30,
            connection_range=100,
        )

        # Add UAVs to the SwarmManager
        self.swarm_manager.add_uav(uav1)
        self.swarm_manager.add_uav(uav2)
        self.swarm_manager.add_uav(uav3)

        self.ground_map = Map(
            AoI=[
                (19, 13),
                (15, 13),
                (16, 14),
                (17, 14),
                (18, 14),
                (19, 14),
                (15, 15),
                (16, 15),
                (17, 15),
                (18, 15),
                (19, 15),
                (5, 13),
                (6, 13),
                (7, 13),
                (8, 13),
                (9, 13),
                (5, 13),
                (6, 14),
                (8, 14),
                (6, 15),
                (7, 15),
                (8, 15),
                (9, 15),
                (5, 4),
                (6, 4),
                (8, 4),
                (8, 5),
                (6, 6),
                (7, 6),
                (8, 6),
                (9, 6),
                (6, 7),
                (8, 6),
                (10, 7),
                (10, 9),
                (8, 11),
                (9, 12),
                (10, 13),
                (10, 14),
            ],
            width=30,
            height=20,
            wind_direction=(0.5, 0.5),
            wind_strength=10,
        )

    def update(self):
        self.ground_map.update()
        self.swarm_manager.update()

    def handle_events(self):
        self._handle_game_state()
        self.ground_map.handle_events()
        self.swarm_manager.handle_events(self.ground_map)

    def render(self):
        self.ground_map.draw()
        self.swarm_manager.draw()

    def clean(self):
        pass

    def _handle_game_state(self):
        if InputManager().is_key_down(pygame.K_ESCAPE):
            GameStateManager().pop_state()
