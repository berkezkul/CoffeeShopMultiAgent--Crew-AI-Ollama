from agents.agent import Agent

class CustomerSegmentationAgent(Agent):
    """Müşteri segmentasyonu yapan ajan."""
    def segment_customers(self, sales_data, prices_data):
        try:
            # İçecek fiyatlarını satış verileriyle çarparak günlük gelir hesapla
            for drink in prices_data['İçecek']:
                if drink in sales_data.columns:
                    sales_data[drink] = sales_data[drink] * prices_data.loc[prices_data['İçecek'] == drink, 'Fiyat'].values[0]

            # Günlük toplam gelir hesapla
            sales_data['Günlük Gelir'] = sales_data.iloc[:, 1:].sum(axis=1)

            # Ortalama gelir eşiklerini belirle
            threshold = sales_data['Günlük Gelir'].mean()

            # Gelir eşiğine göre müşteri segmentasyonu yap
            sales_data['Müşteri Segmenti'] = [
                "Premium" if income > threshold * 1.2 else
                "Fiyat Duyarlı" if income < threshold * 0.8 else
                "Orta Segment"
                for income in sales_data['Günlük Gelir']
            ]

            self.log(f"Segmentasyon tamamlandı: {sales_data['Müşteri Segmenti'].value_counts().to_dict()}")
            return sales_data
        except Exception as e:
            self.log(f"Segmentasyon hatası: {e}")
            raise

