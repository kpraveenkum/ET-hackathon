import base64

from openai import OpenAI


client = OpenAI()



def analyze_drawing(image_path):


    with open(
        image_path,
        "rb"
    ) as f:

        image_data = base64.b64encode(
            f.read()
        ).decode()



    response = client.chat.completions.create(

        model="gpt-4o",

        messages=[

            {
            "role":"system",
            "content":
            "You are an EPC drawing review engineer"
            },


            {
            "role":"user",
            "content":[

                {
                "type":"text",
                "text":
                """
Review this electrical drawing.
Find missing information.
"""
                },


                {
                "type":"image_url",
                "image_url":{
                    "url":
                    f"data:image/png;base64,{image_data}"
                }
                }

            ]

            }

        ]

    )


    return response.choices[0].message.content