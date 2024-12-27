import pandas as pd
from agents.agent import Agent

class DataCollectorAgent(Agent):
    """Veri toplama ve doğrulama ajanı."""
    def collect_data(self, sales_path, prices_path, costs_path):
        try:
            sales_data = pd.read_csv(sales_path)
            prices_data = pd.read_csv(prices_path)
            costs_data = pd.read_csv(costs_path)
            self.validate_data(sales_data, prices_data, costs_data)
            self.log("Veriler başarıyla toplandı.")
            return sales_data, prices_data, costs_data
        except Exception as e:
            self.log(f"Veri toplama hatası: {e}")
            raise

    @staticmethod
    def validate_data(sales, prices, costs):
        if not set(prices['İçecek']).issubset(sales.columns):
            raise ValueError("Fiyatlardaki içecekler satış verilerinde yok!")
        if not set(costs['İçecek']).issubset(prices['İçecek']):
            raise ValueError("Maliyetlerdeki içecekler fiyat verilerinde yok!")

