from physics.thermophysical import density_thermo, density_mendeleev
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Define temperature range and step
temperatures = np.arange(-50, 501, 50)

# Calculate density using density_thermo and density_mendeleev
density_thermo = [density_thermo(t) for t in temperatures]
density_mendeleev = [density_mendeleev(t) for t in temperatures]

# Create a DataFrame with temperature, density_thermo, and density_mendeleev
data = {
    "Temperature (°C)": temperatures,
    "Density (thermo) (kg/m^3)": density_thermo,
    "Density (Mendeleev) (kg/m^3)": density_mendeleev,
}
df = pd.DataFrame(data)

# Create a scatter plot using Seaborn
sns.scatterplot(
    x="Temperature (°C)",
    y="Density (thermo) (kg/m^3)",
    data=df,
    label="Density (thermo)",
    marker="o",
)
sns.scatterplot(
    x="Temperature (°C)",
    y="Density (Mendeleev) (kg/m^3)",
    data=df,
    label="Density (Mendeleev)",
    marker="x",
)
# Add legend, axis labels, and gridlines
plt.legend()
plt.xlabel("Temperature (°C)")
plt.ylabel("Density (kg/m^3)")
plt.grid()

# Save the plot as a file
plt.savefig("analytics/plots/density_plot.png")

# Close the plot
plt.close()
