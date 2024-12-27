import pandas as pd

from agents.agent import Agent, llm

class CampaignAgent(Agent):
    """Kampanya oluşturma ajanı."""
    def create_campaigns(self, recommendations_df, season):
        campaigns = []

        for _, row in recommendations_df.iterrows():
            try:
                prompt = f"""
                İçecek: {row['İçecek']}
                Mevcut Fiyat: {row['Mevcut Fiyat']} TL
                Trend: {row['Satış Trendi']}
                Mevsim: {season}

                Kampanya önerisi oluştur.
                """
                campaign = llm.invoke(prompt)
            except Exception as e:
                self.log(f"Kampanya oluşturulamadı: {e}")
                campaign = "Kampanya oluşturulamadı"

            campaigns.append({"İçecek": row["İçecek"], "Kampanya": campaign})

        self.log("Kampanyalar oluşturuldu.")
        return pd.DataFrame(campaigns)


