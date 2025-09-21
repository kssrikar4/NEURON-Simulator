# NEURON-Simulator

NEURON-Simulator is a graphical interface designed for computational neuroscience. The application allows you to build, simulate, and analyze neuronal networks using the powerful NEURON simulation environment.

## Core Application Features

The simulator is built around three main areas: Model Configuration, Simulation, and Data Visualization.

  * **Model Configuration and Simulation**:

      * **Neuron Model Selection**: The application provides a dropdown menu to instantiate three distinct pre-built neuron models: a passive single-compartment **soma**, a passive **dendrite** connected to a soma, and a **multi-compartment** neuron with active Hodgkin-Huxley channels.
      * **Parameter Control**: You can precisely define key biophysical parameters, including membrane resistance (R<sub>m</sub>) and capacitance (C<sub>m</sub>), using interactive sliders and numerical input fields.
      * **Stimulation Options**: The interface allows for the selection of three primary stimulation protocols via a dropdown menu:
          * **NetStim**: Simulates synaptic input to the neuron.
          * **IClamp**: Injects a fixed current waveform into the neuron.
          * **VClamp**: Holds the membrane potential at a specific voltage level.
      * **Simulation Control**: The application provides dedicated buttons to initiate (**Start Simulation**) and reset (**Reset Simulation**) the simulation state. Simulation duration and timestep (`dt`) can be adjusted numerically.

  * **Data Visualization and Analysis**:

      * **Interactive 3D Morphology Visualization**: The application generates an interactive 3D plot of the neuron's morphology using Plotly, allowing for dynamic inspection of the geometry of the soma, dendrites, and axon.
      * **Membrane Potential Plots**: After a simulation is run, a plot displays the membrane potential over time.
      * **Spike Raster Plot**: The application automatically detects and plots the timing of action potentials using an improved spike detection algorithm with a refractory period.
      * **Interactive "About" Section**: A new expandable dropdown menu at the top of the page provides a short manual explaining the different components of the simulator.

## Installation and Setup

To run the simulator, you need Python 3.10 or later. **Note**: The simulator currently only works on Linux and macOS; Windows is not supported.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/kssrikar4/NEURON-Simulator.git
    cd NEURON-Simulator
    ```
2.  **Create a Virtual Environment**: It is highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv py
    source py/bin/activate
    ```
3.  **Install Dependencies**: Use the provided `requirements.txt` file to install all necessary Python libraries.
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Launch the application from your terminal. This will automatically open a new tab in your web browser.

```bash
streamlit run app.py
```

## Step-by-Step User Guide

1.  **Define Your Network**: On the left panel, use the **Number of Neurons** input to set the size of your network. Choose a **Connectivity Pattern** (All-to-All or Random) and, for Random, set the **Connection Probability**.
2.  **Configure Neuron Model**: Select a **Neuron Model Type** from the dropdown and use the sliders to set the **Membrane Resistance** and **Membrane Capacitance**.
3.  **Set Up Stimulation**: Choose a **Stimulus Type** and adjust its parameters in the dynamically generated section below. You must also select a **Target Neuron Index** to receive the stimulus.
4.  **Run the Simulation**: Set the **Simulation Duration** and **Timestep (dt)**. Click the **Start Simulation** button to run the simulation.
5.  **View Results**: Once the simulation is complete, the right panel will populate with the results. You can view the 3D morphology plot and the membrane potential traces. For the **Spike Raster Plot**, adjust the **Spike Detection Threshold** to visualize the neuron firing times.

## Acknowledgements

Thank you to the following open-source libraries for making this project possible:

  * **NEURON**: The core simulation engine for modeling neuronal networks.
  * **Streamlit**: The framework for building the interactive web application.
  * **Plotly** and **Matplotlib**: Used for all data visualization and plotting.
  * **NumPy** and **Pandas**: Used for data handling and numerical operations.
  * **Git**: For version control.

The code for this application was developed with the assistance of Gemini for code suggestions and refinement.

## Licensing

This project is released under the **BSD 3-Clause License**.
