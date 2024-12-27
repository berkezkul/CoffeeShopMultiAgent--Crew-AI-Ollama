from datetime import datetime

from agents.campaign_agent import CampaignAgent
from agents.data_collector_agent import DataCollectorAgent
from agents.pricing_agent import PricingAgent
from agents.reporting_agent import ReportingAgent
from agents.segmentation_agent import CustomerSegmentationAgent


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Ajanları oluştur
    data_collector = DataCollectorAgent("DataCollector", "Veri Analisti", "Veri toplama ve doğrulama")
    segmenter = CustomerSegmentationAgent("Segmenter", "Segmentasyon Uzmanı", "Müşteri segmentasyonu")
    pricing_agent = PricingAgent("PricingAgent", "Fiyat Uzmanı", "Fiyat analizi ve önerisi")
    campaign_agent = CampaignAgent("CampaignAgent", "Pazarlama Uzmanı", "Kampanya oluşturma")
    reporting_agent = ReportingAgent("ReportingAgent", "Raporlama Uzmanı", "Sonuçları raporlama ve kaydetme")

    # Verileri yükleme
    sales_data, prices_data, costs_data = data_collector.collect_data(
        sales_path="datas/drink_sales.csv",
        prices_path="datas/drink_prices.csv",
        costs_path="datas/drink_costs.csv"
    )

    # Müşteri segmentasyonu
    segmented_sales = segmenter.segment_customers(sales_data, prices_data)

    # Fiyat önerileri
    recommendations = pricing_agent.recommend_prices(segmented_sales, prices_data, costs_data)

    # Kampanya önerileri
    campaigns = campaign_agent.create_campaigns(recommendations, "Yaz")

    # Sonuçları kaydetme ve raporlama
    reporting_agent.save_results_to_csv([segmented_sales, recommendations, campaigns], timestamp)
    reporting_agent.create_summary_report(timestamp, sales_data, segmented_sales, recommendations, campaigns, prices_data)


if __name__ == "__main__":
    main()
