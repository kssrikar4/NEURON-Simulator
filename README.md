# NEURON-Simulator
Graphical Interface for Computational Neuroscience

## Core Application Features
This application has a set of features to explore computational neuronal dynamics. The current implementation status of each feature is detailed below.

### 1. Model Configuration and Simulation
* **Neuron Model Selection:** The application provides a dropdown menu to instantiate three distinct pre-built neuron models: a passive single-compartment **soma**, a passive **dendrite** connected to a soma, and a multi-compartment neuron with active Hodgkin-Huxley channels.
* **Parameter Control:** Users can precisely define key biophysical parameters, including membrane resistance ($R_m$) and capacitance ($C_m$), using interactive sliders and numerical input fields.
* **Advanced Stimulation Options:** The interface allows for the selection of three primary stimulation protocols via a dropdown menu:
    * **NetStim:** Simulates synaptic input to the neuron.
    * **IClamp:** Injects a fixed current waveform into the neuron.
    * **VClamp:** Clamps the membrane potential at a specific voltage level.
* **Simulation Control:** The application provides dedicated buttons to initiate (`Start Simulation`) and reset (`Reset Simulation`) the simulation state. Simulation duration and timestep ($dt$) can be adjusted numerically.

### 2. Data Visualization and Analysis
* **Interactive 3D Morphology Visualization:** The application generates an interactive 3D plot of the neuron's morphology using Plotly, which allows for dynamic inspection of the geometry of the soma, dendrites, and axon.
* **Membrane Potential Plots:** After a simulation is run, a plot displays the membrane potential over time. For multi-compartment models, this plot includes a trace for both the soma and a dendrite to enable direct comparison of electrical activity across different neuronal regions.
* **Spike Raster Plot:** The application automatically detects and plots the timing of action potentials, providing a clear visual representation of neuronal firing patterns.
* **Comparison of Runs:** The results from batch simulations can be overlaid on a single graph, facilitating the comparative analysis of neuronal responses under different parameter sets.

### 3. Data and Configuration Management
* **Data Export:** Simulation results can be exported as a CSV file using a download button.
* **Configuration Management:** The application supports saving the current simulation parameters to a JSON file and loading a previously saved configuration.
* **Batch Simulation:** This feature enables the execution of multiple simulations using a predefined list of parameter presets.

## Application Manual

### Installation and Setup
To get started with `NEURON-Simulator`, ensure that Python 3.8 or a later version is installed and follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kssrikar4/NEURON-Simulator.git
    cd COBRApy-GUI
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv py
    source py/bin/activate  # On Windows: `py\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
Launch the application from the terminal using the following command:
    ```bash
    streamlit run app.py
    ```
This will open the application in your web browser.

### User Guide
#### 1. Model and Parameters
* **Select Neuron Model:** Choose a model from the dropdown menu to define the neuronal geometry.
* **Model Parameters:** Use the sliders to adjust the passive membrane properties.
* **Select Stimulus Type:** Select the desired input method. The parameter section will dynamically update to reflect the selected stimulus type.

#### 2. Simulation Control
* **Set Duration and Timestep:** Define the simulation length and temporal resolution in the designated input fields.
* **Start Simulation:** Click this button to run the simulation. The application will display the results upon completion.
* **Reset Simulation:** This button clears all simulation data and resets the state, preparing the application for a new run.

#### 3. Data Management
* **Export Data:** Use the "Export Data to CSV" button to download a file containing the time series data of the simulation.
* **Save/Load Configuration:** Save the current configuration to a JSON file or load an existing one using the file uploader.
