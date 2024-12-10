from physics.thermophysical import kinematic_viscosity_idelchik, kinematic_viscosity_thermo
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Define temperature range and step
temperatures = np.arange(-60, 60, 5)

# Calculate viscosity using kinematic_viscosity_idelchik and kinematic_viscosity_thermo
kinematic_viscosity_thermo = [kinematic_viscosity_thermo(t) for t in temperatures]
kinematic_viscosity_idelchik = [kinematic_viscosity_idelchik(t) for t in temperatures]

# Create a DataFrame
data = {
    "Temperature (°C)": temperatures,
    "Kinematic viscosity (thermo) (м^2/с)": kinematic_viscosity_thermo,
    "Kinematic viscosity (Idelchik) (м^2/с)": kinematic_viscosity_idelchik,
}
df = pd.DataFrame(data)

# Create a scatter plot using Seaborn
sns.scatterplot(
    x="Temperature (°C)",
    y="Kinematic viscosity (thermo) (м^2/с)",
    data=df,
    label="Kinematic viscosity (thermo)",
    marker="s",
)
sns.scatterplot(
    x="Temperature (°C)",
    y="Kinematic viscosity (Idelchik) (м^2/с)",
    data=df,
    label="Kinematic viscosity (Idelchik)",
    marker="o",
)
# Add legend, axis labels, and gridlines
plt.legend()
plt.xlabel("Temperature (°C)")
plt.ylabel("Kinematic viscosity (м^2/с)")
plt.grid()

# Save the plot as a file
plt.savefig("analytics/plots/kinematic_viscosity_plot.png")

# Close the plot
plt.close()
