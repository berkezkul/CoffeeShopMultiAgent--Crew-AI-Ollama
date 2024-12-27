import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from langchain_ollama import OllamaLLM
import torch

# GPU kullanımı kontrolü
device = "cuda" if torch.cuda.is_available() else "cpu"

# LLM Modeli
llm = OllamaLLM(model="llama3.2")

# Sabitler
INFLATION_RATE = 0.47        #enflasyon
MIN_PROFIT_MARGIN = 0.20


class Agent:
    """Tüm ajanların temel sınıfı."""
    def __init__(self, name, role, goal):
        self.name = name
        self.role = role
        self.goal = goal

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.name} ({self.role}): {message}")