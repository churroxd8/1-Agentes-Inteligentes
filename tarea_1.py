#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Luis Mario Sainz'

import entornos_f
import entornos_o
import random
from tabulate import tabulate

class NineRooms:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.rooms = [
            [random.choice(["clean", "dirty"]) for _ in range(3)] for _ in range(3)
        ]
        self.agent_position = [0, 0]
        self.energy_cost = 0

    def all_rooms_clean(self):
        return all(room == "clean" for floor in self.rooms for room in floor)
    
    def perform_action(self, action):
        floor, room = self.agent_position

        if action == "clean":
            self.rooms[floor][room] = "clean"
            self.energy_cost += 1 # 
        elif action == "go_Right" and room < 2:
            self.agent_position[1] += 1
            self.energy_cost += 2
        elif action == "go_Left" and room > 0:
            self.agent_position[1] -= 1
            self.energy_cost += 2
        elif action == "go_Upstairs" and floor < 2 and room == 2:
            self.agent_position[0] += 1
            self.energy_cost += 5 
        elif action == "go_Downstairs" and floor >2 and room == 0:
            self.agent_position[0] -= 1
            self.energy_cost += 5 
        elif action == "do_Nothing":
            self.energy_cost += 0 

    def all_rooms_clean(self):
        return all(all(room == "clean" for room in floor) for floor in self.rooms)

    def print_environment(self):
        for floor in reversed(range(3)):
            print(f"Floor {floor + 1}: {self.rooms[floor]}")
            print(f"Agent Position: Floor {self.agent_position[0] + 1}, Room {self.agent_position[1] + 1}")
            print("-" * 30)

class SimpleReflexAgent:
    def __init__(self):
        pass

    def choose_action(self, percept):
        """Choose action based on the current percept"""
        if percept == "dirty":
            return "clean"
        else:
            return random.choice(["go_Right", "go_Left", "go_Upstairs", "go_Downstairs", "do_Nothing"])

class ModelBasedReflexAgent:
    def __init__(self):
        self.internal_state = [[None for _ in range(3)] for _ in range(3)] 
        self.visited_rooms = set() 

    def update_state(self, position, percept):
        """Update the internal state based on the percept"""
        floor, room = position
        self.internal_state[floor][room] = percept
        self.visited_rooms.add(tuple(position))
    
    def choose_action(self, position):
        """Choose the next action based on the internal state"""
        floor, room = position

        if self.internal_state[floor][room] == "dirty":
            return "clean"
        
        for f in range(3):
            for r in range(3):
                if self.internal_state[f][r] != "clean":
                    if f > floor and room == 2:
                        return "go_Upstairs"
                    elif f < floor and room == 1:
                        return "go_Downstairs"
                    elif r > room:
                        return "go_Right"
                    elif r < room:
                        return "go_Left"

        return "do_Nothing"


def simulate(agent, environment, steps=200):
    log = []
    for step in range(steps):
        if environment.all_rooms_clean():
            log.append([step + 1, "All rooms clean", f"Floor {environment.agent_position[0] + 1}, Room {environment.agent_position[1] + 1}", environment.energy_cost])
            break
        
        percept = environment.rooms[environment.agent_position[0]][environment.agent_position[1]]

        if hasattr(agent, 'update_state'):
            agent.update_state(environment.agent_position, percept)
        
        action = agent.choose_action(
            percept if not hasattr(agent, 'update_state') else environment.agent_position
        )

        environment.perform_action(action)

        log.append([
            step + 1,
            action,
            f"Floor {environment.agent_position[0] + 1}, Room {environment.agent_position[1] + 1}",
            environment.energy_cost
        ])

        # Si alguno de los agentes se queda atorado, intentemos romper el ciclo
        if action == "do_Nothing" and environment.energy_cost > 0:
            log.append([step + 1, "Agent stuck", f"Floor {environment.agent_position[0] + 1}. Room {environment.agent_position[1] + 1}", environment.energy_cost])
            break
    
    return log, environment.energy_cost

SEED = 42

simple_agent = SimpleReflexAgent()
simple_env = NineRooms(seed=SEED)
simple_log, simple_cost = simulate(simple_agent, simple_env)

model_agent = ModelBasedReflexAgent()
model_env = NineRooms(seed=SEED)
model_log, model_cost = simulate(model_agent, model_env)

# La tabla del agente reactivo
print("\nSimple Reflex Agent Results:")
print(tabulate(simple_log, headers=["Step", "Action", "Agent Position", "Energy Cost"]))

# La tabla del agente basado en modelo
print("\nModel-based Reflex Agent Results:")
print(tabulate(model_log, headers=["Step", "Action", "Agent Position", "Energy Cost"]))

# Resumen comparando los resultados de ambos modelos
print("\nEnergy Cost Comparison:")
print(f"- Simple Reflex Agent: {simple_cost} energy units")
print(f"- Model-based Reflex Agent: {model_cost} energy units")

if model_cost < simple_cost:
    print(f"✅ Model-based agent saved {simple_cost - model_cost} energy units!")
elif model_cost > simple_cost:
    print(f"⚠️ Simple agent was more efficient by {model_cost - simple_cost} energy units!")
else:
    print("Both agents used the same amount of energy")