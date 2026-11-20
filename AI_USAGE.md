# Responsible AI and External-Code Use

## AI assistance disclosure

AI tools, including ChatGPT, were used during the development of PuneSahayak. This assistance included:
- Generating and substantially modifying portions of Python code.
- Explaining programming concepts and helping with implementation decisions.
- Debugging errors and improving existing code.
- Suggesting and preparing automated tests.
- Assisting with documentation and presentation preparation.

The project team is responsible for reviewing, testing and understanding the submitted work. Passing automated tests does not mean every component was independently authored by the team.

## External code and data

The PMPML GTFS snapshot is attributed in `data/gtfs/SOURCE_NOTES.txt` and `DATA_SOURCES.md`.

The project also includes adapted modules from the supplied Pune CommuteWise project archive. Applicable source attribution and licence notices must be preserved. Adapted upstream logic should not be presented as wholly original work.

## Project limitations

PuneSahayak does not claim to provide:
- Live GPS tracking.
- Live traffic API integration.
- An AI chatbot.
- Generative AI route recommendations.
- A predictive machine-learning model.

The traffic view uses Pandas to aggregate the included historical traffic CSV data.