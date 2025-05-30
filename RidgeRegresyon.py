# 1 - Gerekli kütüphaneler içe aktarılıyor
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge

# 2 - Veri dosyası okunur
df = pd.read_excel(r"C:\Users\mert_\OneDrive\Masaüstü\Veri Madenciliği Final\oznitelikler.xlsx")

# 3 - Kullanılacak bağımsız değişkenler
X_vars = [
    'Yıl',
    'Nüfus Yoğunluğu',
    'Population',
    'Emisyon(MtCO₂)',
    'Emisyon(Gg N/Year)',
    'Emisyon(TgC/year)',
    'Kıta'
]

# 4 - Sonuçlar burada toplanacak
results = []

# 5 - Eksik veriler temizleniyor
df_all = df.dropna(subset=X_vars + ['Ortalama_Sıcaklık'])

# 6 - Ülke bazlı modelleme ve tahmin süreci
for country in df_all['Ülke'].unique():
    cdf = df_all[df_all['Ülke'] == country]
    if len(cdf) < 5 or 2013 not in cdf['Yıl'].values:
        continue

    X = pd.get_dummies(cdf[X_vars])
    y = cdf['Ortalama_Sıcaklık']

    model = Pipeline([
        ('scale', StandardScaler()),
        ('poly', PolynomialFeatures(degree=1, include_bias=False)),
        ('ridge', Ridge(alpha=1.0))
    ])
    model.fit(X, y)

    row_2013 = cdf[cdf['Yıl'] == 2013].copy()
    row_2013['Yıl'] = 2100

    X_pred = pd.get_dummies(row_2013[X_vars])
    for col in X.columns:
        if col not in X_pred.columns:
            X_pred[col] = 0
    X_pred = X_pred[X.columns]

    tahmin_2100 = model.predict(X_pred)[0]
    gercek_2013 = row_2013['Ortalama_Sıcaklık'].values[0]
    fark = tahmin_2100 - gercek_2013

    if fark < 1:
        risk = 'Düşük Risk'
    elif fark < 1.5:
        risk = 'Orta Risk'
    elif fark < 2:
        risk = 'Yüksek Risk'
    else:
        risk = 'Çok Yüksek Risk'

    results.append({
        'Ülke': country,
        'Sıcaklık_2013': round(gercek_2013, 2),
        'Tahmini_Sıcaklık_2100': round(tahmin_2100, 2),
        'Fark (°C)': round(fark, 2),
        'Risk Seviyesi': risk
    })

# 7 - Tahmin sonuçları veri çerçevesine dönüştürülür
df_results = pd.DataFrame(results).sort_values(by="Fark (°C)", ascending=False)

# 8 - Kıta bilgisi eklenir
country_continent = df[['Ülke', 'Kıta']].drop_duplicates()
results_with_continent = df_results.merge(country_continent, on='Ülke', how='left')

# 9 - Risk özeti hazırlanır
risk_counts = results_with_continent['Risk Seviyesi'].value_counts().reset_index()
risk_counts.columns = ['Risk Seviyesi', 'Ülke Sayısı']

# 10 - Tüm çıktılar tek dosyada kaydedilir
summary_output_path = r"C:\Users\mert_\OneDrive\Masaüstü\Veri Madenciliği Final\Kita_Ve_Risk_Esigi_Ozetli_Tablo.xlsx"
with pd.ExcelWriter(summary_output_path) as writer:
    results_with_continent.to_excel(writer, sheet_name='Tahmin Sonuçları', index=False)
    risk_counts.to_excel(writer, sheet_name='Risk Özeti', index=False)

# 11 - Bilgilendirme
print(f"📁 Tek çıktı başarıyla oluşturuldu: {summary_output_path}")
