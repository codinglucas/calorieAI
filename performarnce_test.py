import os
from google import genai
from pydantic import BaseModel, Field
import base64
from data_handler import update_daily_records, update_test_data
from dotenv import load_dotenv

load_dotenv()

with open('uploads/images.jpeg', 'rb') as file:
    image_bytes = file.read()

class ExtractedData(BaseModel):
    all_food: str = Field(description="A table-like format, where a row means a different food seen in the image, and the columns are: quantity, calorie (based on the food * quantity), and macro nutrients (carbs, fat, protein)")
    sum: int = Field(description="The sum of all food calories")
    sum_carbs: str = Field(description="A sum of all carbs in the picture")
    sum_fat: str = Field(description="A sum of all fat (macronutrient) in the picture")
    sum_protein: str = Field(description="A sum of all protein in the picture")


client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

# The image_bytes variable is already available from the previously uploaded file.

generation_config = {
    'temperature': 1,
    'max_output_tokens': 65536,
    'top_p': 0.95,
    'thinking_level': 'medium',
}   

for x in range(10):
    print(f"Running test {x}")
    interaction = client.interactions.create(
        model='models/gemini-3-flash-preview',
        input=[
            {"type": "text", "text": "Caption this image."},
            {
                "type": "image",
                "data": base64.b64encode(image_bytes).decode('utf-8'),
                "mime_type": "image/jpeg"
            }
        ],
        system_instruction = """
    You are a food recognition and portion estimation AI.

    Your task is to analyze an image of a plate or meal and identify all food that are visibly present. For each item, provide a realistic estimate of its quantity based only on what can reasonably be inferred from the image.

    Your goals:

    1. Identify every distinct food item visible in the image.
    2. Describe the food specifically when possible (for example, "grilled chicken breast" rather than simply "chicken").
    3. Estimate the quantity of each food item using practical units such as:
    - grams (g)
    - milliliters (ml)
    - number of pieces
    - slices
    - tablespoons/teaspoons
    - cups
    - other appropriate units
    4. Use visual cues such as portion size, plate size, thickness, number of pieces, and typical food dimensions to make the most realistic estimate possible.
    5. Do not assume that an item is present if it cannot reasonably be seen.
    6. If the exact food or quantity cannot be determined with confidence, provide the most reasonable estimate and clearly indicate uncertainty rather than inventing unnecessary details.
    7. Distinguish between separate foods whenever they can reasonably be distinguished. For example, rice, beans, chicken, salad, and fries should be reported as separate items.
    8. If multiple pieces of the same food are present, estimate the total quantity when appropriate, while also mentioning the number of pieces if useful.
    9. Focus only on foods and beverages visible in the image. Do not provide nutritional information, calories, macros, recipes, or health advice unless explicitly requested.
    10. Return concise information that can be directly used by another program. Return only numbers (eg: 15.5, 70, 150).

    The quantity estimate should represent the amount of food actually visible in the image, not the amount that would typically be served in a restaurant or recommended serving size.

    When the image quality, angle, lighting, occlusion, or lack of scale makes precise estimation difficult, give a reasonable range or approximate quantity rather than pretending to know an exact value.
    """,
        generation_config=generation_config,
        response_format = {
            "type": "text",
            "mime_type": "application/json",
            "schema": ExtractedData.model_json_schema()
        },
    )

    result = ExtractedData.model_validate_json(interaction.output_text)
    result_dict = result.model_dump()

    update_test_data(float(result_dict['sum']), float(result_dict['sum_carbs']), float(result_dict['sum_fat']), float(result_dict['sum_protein']))
    print(f"Finished test {x} sucessfully")