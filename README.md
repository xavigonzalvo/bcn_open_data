# Open data Barcelona

Data extracted from the [OpenData website](https://opendata-ajuntament.barcelona.cat/data/en/dataset/incidents-gestionats-gub).

A simple analysis of incidents managed by the local police in Barcelona.

    # Parse data.
    python delitos_bcn.py --create_data

Plot data for a particilar police code:

    python delitos_bcn.py --create_data=false --codi 620


Examples:

- Local police collaborates with other services (e.g., State Police)

<center><img src="codi_305.png" width="70%"></center>

- Drugs

<center><img src="codi_620.png" width="70%"></center>

- Domestic violence

<center><img src="codi_660.png" width="70%"></center>

- Aggressions

<center><img src="codi_670.png" width="70%"></center>
