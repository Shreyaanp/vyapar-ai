# vyaparAI-backend

## Setup Instructions

### 1. Clone the Repository

First, clone this repository to your local machine using Git:

```bash
git clone https://github.com/Pradyogik/vyaparAI-backend.git
cd vyaparAI-backend
```
### 2. Create a Virtual Environment

Create a virtual environment to manage your project's dependencies:

```bash

# For Unix/macOS
python3 -m venv venv

# For Windows
python -m venv venv
```
Activate the virtual environment:

```bash

# For Unix/macOS
source venv/bin/activate

# For Windows
.\venv\Scripts\activate
```
### 3. Install Requirements

Install the project dependencies using pip:

```bash

pip install -r requirements.txt
```
### 4. Create a .env File

Create a .env file in the root directory of your project and add the necessary environment variables in the following format:

.env
```bash
OPENAI_APIKEY=your_openai_api_key_here
SERPERAPI_APIKEY=your_serpapi_api_key_here
```
Make sure to replace your_openai_api_key_here and your_serpapi_api_key_here with your actual API keys.
### 5. Run the Application

Start the FastAPI application with the following command:

```bash

uvicorn main:app --reload
```
The application will be available at http://127.0.0.1:8000.
## Testing the Application
Using curl

Test the application using curl with the following command:

## Output response :

{
    "result": {
        "Product Regional Names": [
            "बनारसी साड़ी (Banarasi Saree)",
            "बनारसी पटोला (Banarasi Patola)",
            "बनारसी सिल्क साड़ी (Banarasi Silk Saree)",
            "बनारसी कतान साड़ी (Banarasi Katan Saree)",
            "बनारसी खद्दी साड़ी (Banarasi Khaddi Saree)"
        ],
        "Product Name": "Pure Banarasi Saree",
        "Product Description": "Pure Banarasi Sarees are exquisite handloom creations from the ancient city of Varanasi. These sarees are woven using fine silk threads and adorned with intricate designs and motifs crafted from gold or silver zari. Known for their luxurious texture and timeless elegance, Banarasi sarees are a must-have for every woman's wardrobe, especially for bridal and festive occasions.",
        "About Product": [
            "Handwoven in Varanasi using fine silk threads.",
            "Features intricate designs and motifs with gold or silver zari.",
            "Available in various types such as Katan Silk, Khaddi Georgette, and Organza.",
            "Ideal for bridal trousseau and festive wear.",
            "Offers a range of colors and styles including antique zari, meenakari work, and bandhani.",
            "Known for their luxurious texture and timeless elegance.",
            "Available with blouse stitching services.",
            "International shipping, COD, and EMI options available."
        ],
        "Product Tagline": "Embrace Timeless Elegance with Pure Banarasi Sarees.",
        "Product Prompt": "Capture the timeless elegance of Pure Banarasi Sarees in your photos. Highlight the intricate zari work, rich textures, and vibrant colors. Use natural light to enhance the silk's sheen and ensure the saree's luxurious details are clearly visible. Ideal for ecommerce platforms.",
        "Seo Friendly Tags": [
            "Banarasi Saree",
            "Pure Banarasi Silk",
            "Handloom Banarasi Saree",
            "Banarasi Bridal Saree",
            "Banarasi Silk Saree Online",
            "Varanasi Saree",
            "Designer Banarasi Saree",
            "Banarasi Sari",
            "Banarasi Katan Silk",
            "Banarasi Khaddi Georgette",
            "Traditional Indian Saree",
            "Luxury Banarasi Saree",
            "Banarasi Saree for Wedding",
            "Buy Banarasi Saree Online",
            "Banarasi Saree with Zari"
        ]
    }
}