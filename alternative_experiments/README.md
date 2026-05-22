# Alternatif Denemeler

Bu klasor ana teslim projesinden ayridir. Buradaki amac, mevcut rapor/notebook/sunum dosyalarina dokunmadan "baska nasil yapabilirdik?" sorusunu denemektir.

## Klasor Mantigi

- `alternative_ag_deneyleri.ipynb`: Alternatif analizlerin notebook dosyasi.
- `data/raw/`: Deney notebook'unun kendi indirecegi genisletilmis ham veri dosyasi.
- `data/processed/`: Notebook calistirilinca ara veri dosyalari buraya yazilir.
- `outputs/metrics/`: Ozet metrik tablolarinin yeri.
- `outputs/edges/`: Her deneme icin olusan edge list dosyalarinin yeri.
- `outputs/figures/`: Deney gorsellerinin yeri.

## Onemli Not

Bu klasor kendi icinde calisir. Ana proje klasorundeki `data`, `outputs`, `report` veya ana notebook dosyasina cikti yazmaz.

Notebook'ta su denemeler hazirdir:

- Farkli varlik evrenleri
- Farkli korelasyon yontemleri
- Farkli esik degerleri
- Farkli tarih araliklari

Calistirma icin `alternative_ag_deneyleri.ipynb` dosyasini acip hucreleri sirayla calistirman yeterli.
