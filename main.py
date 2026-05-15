import os

print("1. Veri çekme başlıyor...")
os.system("python src/data_collection.py")

print("2. Preprocessing başlıyor...")
os.system("python src/preprocessing.py")

print("3. Korelasyon analizi başlıyor...")
os.system("python src/correlation_analysis.py")

print("4. Network analizi başlıyor...")
os.system("python src/network_analysis.py")

print("5. Network metricleri hesaplanıyor...")
os.system("python src/network_metrics.py")

print("6. Community detection başlıyor...")
os.system("python src/community_detection.py")

print("Tüm pipeline tamamlandı.")