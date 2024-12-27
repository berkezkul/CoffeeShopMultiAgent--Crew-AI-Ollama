import pandas as pd

from agents.agent import Agent, INFLATION_RATE, MIN_PROFIT_MARGIN, llm


class PricingAgent(Agent):
    """Fiyat önerisi ve analiz ajanı."""
    def recommend_prices(self, sales_data, prices_data, costs_data):
        recommendations = []

        numeric_sales_data = sales_data.select_dtypes(include="number")
        total_daily_sales = numeric_sales_data.sum(axis=1)  # Günlük toplam satışları hesapla

        for drink in prices_data["İçecek"]:
            try:
                current_price = prices_data.loc[prices_data["İçecek"] == drink, "Fiyat"].values[0]
                cost = costs_data.loc[costs_data["İçecek"] == drink, "Fiyat"].values[0]

                # Maliyet analizi
                adjusted_cost = cost * (1 + INFLATION_RATE)
                min_price = adjusted_cost * (1 + MIN_PROFIT_MARGIN)

                # Satış yüzdesi analizi
                if drink in numeric_sales_data.columns:
                    daily_sales = numeric_sales_data[drink].sum()
                    sales_percentage = (daily_sales / total_daily_sales.sum()) * 100
                else:
                    sales_percentage = 0

                # Satış trendi analizi
                sales_trend = self.analyze_sales_trend(numeric_sales_data, drink)

                # Fiyat önerisini oluşturma
                recommendation = self.generate_price_recommendation(
                    drink, current_price, min_price, sales_trend, sales_percentage
                )

            except Exception as e:
                self.log(f"Fiyat önerisi oluşturulamadı: {e}")
                recommendation = "Fiyat önerisi oluşturulamadı"

            recommendations.append({
                "İçecek": drink,
                "Mevcut Fiyat": current_price,
                "Minimum Fiyat": min_price,
                "Satış Trendi": sales_trend,
                "Satış Yüzdesi": f"{sales_percentage:.2f}%",
                "Fiyat Önerisi": recommendation
            })

        self.log("Fiyat önerileri oluşturuldu.")
        return pd.DataFrame(recommendations)

    def generate_price_recommendation(self, drink, current_price, min_price, sales_trend, sales_percentage):
        """Fiyat önerisi oluştur."""
        try:
            # Prompt oluştur
            prompt = f"""
            İçecek: {drink}
            Mevcut fiyat: {current_price:.2f} TL
            Minimum fiyat: {min_price:.2f} TL
            Satış trendi: {sales_trend}
            Satış yüzdesi: {sales_percentage:.2f}%

            Bu verilere dayanarak, içecek için uygun bir fiyat önerisi oluştur.
            """
            return llm.invoke(input=prompt)
        except Exception as e:
            self.log(f"Fiyat önerisi oluşturulamadı: {e}")
            return "Fiyat önerisi oluşturulamadı"

    @staticmethod
    def analyze_sales_trend(sales_data, drink):
        """Satış trendini analiz et."""
        try:
            if drink not in sales_data.columns:
                return "Yeterli veri yok"
            sales = sales_data[drink].dropna().values
            if len(sales) < 2 or sales[0] == 0:
                return "Yeterli veri yok"
            trend = (sales[-1] - sales[0]) / sales[0] * 100
            return "Yükseliş" if trend > 10 else "Düşüş" if trend < -10 else "Stabil"
        except Exception:
            return "Yeterli veri yok"


