import os
from agents.agent import Agent
from datetime import datetime


class ReportingAgent(Agent):
    """Sonuçları raporlayan ve kaydeden ajan."""

    def __init__(self, name, role, goal):
        super().__init__(name, role, goal)
        # Output directories
        self.output_dir = "reports/"
        self.csv_dir = os.path.join(self.output_dir, "csv/")
        self.report_dir = os.path.join(self.output_dir, "summary/")
        os.makedirs(self.csv_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)

    def save_results_to_csv(self, dataframes, timestamp):
        """Sonuçları CSV dosyalarına kaydet."""
        filenames = ["segmented_sales", "price_recommendations", "campaigns"]
        try:
            for df, name in zip(dataframes, filenames):
                csv_path = os.path.join(self.csv_dir, f"{name}.csv")
                df.to_csv(csv_path, index=False)
            self.log(f"Sonuçlar CSV dosyalarına kaydedildi: {', '.join([f'{name}.csv' for name in filenames])}")
        except Exception as e:
            self.log(f"CSV kaydetme hatası: {e}")
            raise

    def create_summary_report(self, timestamp, sales_data, segmented_sales, recommendations, campaigns, prices_data):
        """Özet raporu oluştur ve dosyaya kaydet."""
        try:
            # Sadece sayısal sütunları seç
            numeric_sales_data = sales_data.select_dtypes(include='number')

            # Ortalama fiyat artışı hesaplama
            avg_price_increase = (
                (recommendations['Mevcut Fiyat'].mean() / prices_data['Fiyat'].mean()) - 1
            ) * 100

            # En yüksek fiyat artışı
            max_price_increase_drink = recommendations.loc[
                recommendations['Mevcut Fiyat'].idxmax(), 'İçecek'
            ]

            # Rapor formatı
            report = f"""
            KAHVE ZİNCİRİ ANALİZ RAPORU
            Tarih: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

            1. GENEL BAKIŞ
            - Toplam İçecek Sayısı: {len(numeric_sales_data.columns)}
            - Analiz Edilen Dönem: {sales_data['Tarih'].iloc[-1]}  # Son tarih
            - Ortalama Günlük Satış Geliri: {sales_data['Günlük Gelir'].mean():.2f} TL

            2. MÜŞTERİ SEGMENTLERİ
            {segmented_sales['Müşteri Segmenti'].value_counts().to_string()}

            3. FİYAT ÖNERİLERİ ÖZETİ
            - Ortalama Fiyat Artışı: {avg_price_increase:.2f}%
            - En Yüksek Fiyat Artışı: {max_price_increase_drink}

            4. KAMPANYA ÖNERİLERİ
            {campaigns.to_string(index=False)}

            5. ÖNERİLER
            - Fiyat değişiklikleri aşamalı olarak uygulanmalıdır.
            - Kampanyalar mevsimsel faktörler göz önüne alınarak planlanmalıdır.
            - Müşteri segmentlerine özel promosyonlar düzenlenmelidir.
            """

            # Raporu kaydet
            report_file = os.path.join(self.report_dir, f"summary_report.txt")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)

            self.log(f"Özet rapor başarıyla oluşturuldu: {report_file}")
        except Exception as e:
            self.log(f"Rapor oluşturulamadı: {e}")
            raise
