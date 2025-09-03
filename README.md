# Cisco Product UI Application

This project is a user interface application designed to query data about Cisco products using SPARQL queries. It leverages the functionality provided in the `graph_connection.py` file to interact with a SPARQL endpoint.

## Project Structure

```
cisco-product-ui
├── src
│   ├── graph_connection.py       # Contains functions for querying the SPARQL endpoint.
│   ├── ui
│   │   ├── main_window.py         # Defines the main window of the UI application.
│   │   └── components.py          # Contains reusable UI components.
│   ├── services
│   │   └── product_query_service.py # Handles logic for querying Cisco product data.
│   └── utils
│       └── __init__.py           # Initializer for the utils package.
├── requirements.txt               # Lists project dependencies.
├── README.md                      # Documentation for the project.
└── setup.py                       # Configuration file for packaging the project.
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd cisco-product-ui
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Execute the main window script to start the application:
   ```
   python src/ui/main_window.py
   ```

## Usage Guidelines

- The application provides an interface to input queries related to Cisco products.
- Users can view results displayed in the UI, which are fetched from the SPARQL endpoint.
- Ensure that the environment variables for the SPARQL endpoint and token (if required) are set before running the application.

## Functionality

- **Query Cisco Products:** Users can input SPARQL queries to retrieve information about Cisco products.
- **User Interface:** The application features a user-friendly interface for easy interaction with the data.
- **Modular Design:** The project is structured to separate concerns, making it easier to maintain and extend.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.