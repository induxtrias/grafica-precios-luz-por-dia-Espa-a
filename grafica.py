import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Realiza una solicitud a la API y obtén datos JSON
url = 'https://api.preciodelaluz.org/v1/prices/all?zone=PCB'  # Reemplaza con la URL de tu API

response = requests.get(url)

try:
    response.raise_for_status()  # Verifica si hay errores en la respuesta
    data = response.json()
except requests.exceptions.RequestException as e:
    print("Error al obtener los datos de la API:", e)

# Procesa los datos JSON para obtener los precios por hora en €/kWh
prices = [data[key]['price'] / 1000 for key in data]  # Divide por 1000 para convertir de €/MWh a €/kWh

# Encuentra el valor máximo y mínimo
max_price = max(prices)
min_price = min(prices)

# Calcula la media del costo
average_price = sum(prices) / len(prices)

# Obtiene la fecha del día actual
current_date = datetime.now().strftime('%d-%m-%Y')

# Encuentra las cinco columnas más cercanas al costo mínimo
sorted_prices = sorted(enumerate(prices), key=lambda x: abs(x[1] - min_price))
closest_to_min_indices = [index for index, _ in sorted_prices[:5]]

# Define los colores para las barras
colors = ['red' if price == max_price else 'green' if price == min_price else 'orange' if index in closest_to_min_indices else 'blue' for index, price in enumerate(prices)]

# Crea una gráfica de barras utilizando matplotlib
hours = list(data.keys())  # Obtén las horas del diccionario
plt.bar(hours, prices, color=colors)
plt.xlabel('Hora')
plt.ylabel('Precio (€/kWh)')  # Etiqueta del eje Y en €/kWh
plt.title(f'PRECIO ELECTRICIDAD ESPAÑA - {current_date}')  # Cambia el título

# Agrega etiquetas para el valor máximo y mínimo
plt.text(hours[prices.index(max_price)], max_price, f'Max: {max_price:.4f} €/kWh', ha='center', va='bottom', color='red')
plt.text(hours[prices.index(min_price)], min_price, f'Min: {min_price:.4f} €/kWh', ha='center', va='bottom', color='green')

# Agrega la media del costo en la esquina superior izquierda
plt.text(0, max_price, f'Media: {average_price:.4f} €/kWh', ha='left', va='top', color='black')

plt.xticks(rotation=90)  # Rota las etiquetas del eje X para mayor legibilidad
plt.tight_layout()
plt.show()
