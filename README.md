# NEURON-Simulator
Graphical Interface for Computational Neuroscience

## Core Application Features
This application has a set of features to explore computational neuronal dynamics. The current implementation status of each feature is detailed below.

### 1. Model Configuration and Simulation
*   **Neuron Network Configuration:** The application now provides controls to define a network of neurons, including setting the total number of neurons and their connectivity pattern ('All-to-All' or 'Random' with adjustable probability).
*   **Neuron Model Selection:** A dropdown menu instantiates a population of identical pre-built neuron models for the entire network: a active single-compartment **soma**, a passive **dendrite** connected to a soma, and a multi-compartment neuron with active Hodgkin-Huxley channels.
*   **Parameter Control:** Users can define key biophysical parameters (membrane resistance R<sub>m</sub> and capacitance C<sub>m</sub>) applied uniformly to all neurons in the network using interactive sliders and numerical input fields.
*   **Advanced Stimulation Options:** The interface allows for the selection of stimulation protocols (NetStim, IClamp, VClamp) via a dropdown menu and to target a specific neuron within the network for applying the stimulus.
*   **Simulation Control:** The application provides dedicated buttons to initiate (`Start Simulation`) and reset (`Reset Simulation`) the simulation state. Simulation duration and timestep (`dt`) can be adjusted numerically.

### 2. Data Visualization and Analysis
*   **Interactive 3D Network Morphology Visualization:** The application generates an interactive 3D plot of the entire network's morphology using Plotly, color-coding individual neurons for clarity and allowing for dynamic inspection.
*   **Population Membrane Potential Plots:** After a simulation is run, a single plot displays the membrane potential over time for all neurons in the network, enabling direct comparison of activity across the population.
*   **Network Spike Raster Plot:** The application automatically detects and plots the timing of action potentials for every neuron, providing a clear visual representation of population firing patterns and network-wide activity.
*   **Comparison of Runs:** The results from batch simulations can be overlaid on a single graph, facilitating the comparative analysis of network responses under different parameter sets.

### 3. Data and Configuration Management
*   **Data Export:** Simulation results, including voltage traces for all neurons, can be exported as a CSV file using a download button.
*   **Configuration Management:** The application supports saving the current network and simulation parameters to a JSON file and loading a previously saved configuration.
*   **Batch Simulation:** This feature enables the execution of multiple network simulations using a predefined list of parameter presets.

## Application Manual

### Installation and Setup
To get started with `NEURON-Simulator`, ensure that Python 3.8 or a later version is installed and follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kssrikar4/NEURON-Simulator.git
    cd NEURON-Simulator
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
*   **Configure Network:** Set the `Number of Neurons` and select a `Connectivity Pattern` to define the network architecture.
*   **Select Neuron Model:** Choose a model from the dropdown menu to define the neuronal geometry for all neurons in the network.
*   **Model Parameters:** Use the sliders to adjust the passive membrane properties, which will be applied globally to all neurons.
*   **Select Stimulus Type and Target:** Select the desired input method and specify the `Target Neuron Index` which will receive the stimulus.

#### 2. Simulation Control
*   **Set Duration and Timestep:** Define the simulation length and temporal resolution in the designated input fields.
*   **Start Simulation:** Click this button to run the network simulation. The application will display the population results upon completion.
*   **Reset Simulation:** This button clears all simulation data and resets the network state, preparing the application for a new run.

#### 3. Data Management
*   **Export Data:** Use the "Export Data to CSV" button to download a file containing the time series data for all neurons in the simulation.
*   **Save/Load Configuration:** Save the current network configuration to a JSON file or load an existing one using the file uploader.
