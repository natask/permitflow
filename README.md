# PermitFlow - Solar Installation Permit Application

A web application for submitting solar installation permit applications in the Greater Boston area.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/natask/PermitFlow.git
cd PermitFlow
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following:
```
AI21_API_KEY=your_api_key
```

4. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Features

- Clean, modern interface using Bootstrap
- Simple form submission for permit applications
- Collects installation details:
  - Zip code
  - Address
  - Roof area
- JSON response format for easy integration
- Error handling and responsive design

## API Endpoints

### Submit Permit Application
- **URL**: `/submit`
- **Method**: `POST`
- **Data Format**:
```json
{
    "zipcode": "string",
    "address": "string",
    "roofArea": "number"
}
```
- **Response**: Returns the submitted data in JSON format
