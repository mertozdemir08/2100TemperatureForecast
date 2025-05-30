import os
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge

current_dir = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(current_dir, "Data.xlsx")
df = pd.read_excel(input_path)

X_vars = [
    'Year',
    'Population_Density',
    'Population',
    'Emission(MtCO₂)',
    'Emission(Gg N/Year)',
    'Emission(TgC/year)',
    'Continent'
]

# 4 - Sonuçlar burada toplanacak
results = []

# 5 - Eksik veriler temizleniyor
df_all = df.dropna(subset=X_vars + ['Average_Temperature'])

# 6 - Ülke bazlı modelleme ve tahmin süreci
for country in df_all['Country'].unique():
    cdf = df_all[df_all['Country'] == country]
    if len(cdf) < 5 or 2013 not in cdf['Year'].values:
        continue

    X = pd.get_dummies(cdf[X_vars])
    y = cdf['Average_Temperature']

    model = Pipeline([
        ('scale', StandardScaler()),
        ('poly', PolynomialFeatures(degree=1, include_bias=False)),
        ('ridge', Ridge(alpha=1.0))
    ])
    model.fit(X, y)

    row_2013 = cdf[cdf['Year'] == 2013].copy()
    row_2013['Year'] = 2100

    X_pred = pd.get_dummies(row_2013[X_vars])
    for col in X.columns:
        if col not in X_pred.columns:
            X_pred[col] = 0
    X_pred = X_pred[X.columns]

    tahmin_2100 = model.predict(X_pred)[0]
    gercek_2013 = row_2013['Average_Temperature'].values[0]
    fark = tahmin_2100 - gercek_2013

    if fark < 1:
        risk = 'Low Risk'
    elif fark < 1.5:
        risk = 'Average Risk'
    elif fark < 2:
        risk = 'High Risk'
    else:
        risk = 'Very High Risk'

    results.append({
        'Country': country,
        'Temperature_2013': round(gercek_2013, 2),
        'Predicted_2100': round(tahmin_2100, 2),
        'Difference (°C)': round(fark, 2),
        'Risk Level': risk
    })

# 7 - Tahmin sonuçları veri çerçevesine dönüştürülür
df_results = pd.DataFrame(results).sort_values(by="Difference (°C)", ascending=False)

# 8 - Kıta bilgisi eklenir
country_continent = df[['Country', 'Continent']].drop_duplicates()
results_with_continent = df_results.merge(country_continent, on='Country', how='left')

# 9 - Risk özeti hazırlanır
risk_counts = results_with_continent['Risk Level'].value_counts().reset_index()
risk_counts.columns = ['Risk Level', 'Number of Countries']

output_path = os.path.join(current_dir, "Output.xlsx")
with pd.ExcelWriter(output_path) as writer:
    results_with_continent.to_excel(writer, sheet_name='Forecast Results', index=False)
    risk_counts.to_excel(writer, sheet_name='Risk Summary', index=False)
