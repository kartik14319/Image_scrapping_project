# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import os
# import logging
# import time
# import json
# from urllib.parse import quote

# logging.basicConfig(filename="scrapper.log", level=logging.INFO)

# st.title("Image Scraper")

# query = st.text_input("Enter the search term for images:")

# # 🔹 NEW FEATURE: Number of images
# num_images = st.number_input(
#     "Number of images to download",
#     min_value=1,
#     max_value=30,
#     value=10,
#     step=1
# )

# if st.button("Search and Download Images"):
#     if not query:
#         st.warning("Please enter a search term!")
#     else:
#         try:
#             save_directory = "images"
#             os.makedirs(save_directory, exist_ok=True)

#             headers = {
#                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#                 "Accept-Language": "en-US,en;q=0.9",
#             }

#             search_url = f"https://www.bing.com/images/search?q={quote(query)}&form=HDRSC2"
#             response = requests.get(search_url, headers=headers, timeout=10)

#             soup = BeautifulSoup(response.text, "html.parser")
#             image_tags = soup.find_all("a", class_="iusc")

#             st.write(f"Found {len(image_tags)} images. Downloading...")

#             count = 0

#             for img_tag in image_tags:
#                 if count >= num_images:
#                     break

#                 try:
#                     meta_data = img_tag.get("m")
#                     if not meta_data:
#                         continue

#                     meta_json = json.loads(meta_data)
#                     image_url = meta_json.get("murl")

#                     if not image_url:
#                         continue

#                     image_data = requests.get(
#                         image_url, headers=headers, timeout=10
#                     ).content

#                     image_path = os.path.join(
#                         save_directory, f"{query.replace(' ', '_')}_{count}.jpg"
#                     )

#                     with open(image_path, "wb") as f:
#                         f.write(image_data)

#                     st.image(image_data, caption=f"{query}_{count}", width=500)

#                     count += 1
#                     time.sleep(1)  # prevents blocking

#                 except Exception as e:
#                     logging.info(e)
#                     continue

#             st.success(
#                 f"Downloaded {count} high-quality images to '{save_directory}' folder!"
#             )

#         except Exception as e:
#             logging.info(e)
#             st.error("Something went wrong. Check scrapper.log for details.")




import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import logging
import time
import json
from urllib.parse import quote

# Logging (optional on Render)
logging.basicConfig(level=logging.INFO)

st.title("Image Scraper")

query = st.text_input("Enter the search term for images:")

num_images = st.number_input(
    "Number of images to download",
    min_value=1,
    max_value=30,
    value=10,
    step=1
)

if st.button("Search and Download Images"):
    if not query:
        st.warning("Please enter a search term!")
    else:
        try:
            save_directory = "images"
            os.makedirs(save_directory, exist_ok=True)

            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept-Language": "en-US,en;q=0.9",
            }

            search_url = f"https://www.bing.com/images/search?q={quote(query)}"
            response = requests.get(search_url, headers=headers, timeout=10)

            soup = BeautifulSoup(response.text, "html.parser")
            image_tags = soup.find_all("a", class_="iusc")

            st.write(f"Found {len(image_tags)} images. Downloading...")

            count = 0

            for img_tag in image_tags:
                if count >= num_images:
                    break

                try:
                    meta_data = img_tag.get("m")
                    if not meta_data:
                        continue

                    meta_json = json.loads(meta_data)
                    image_url = meta_json.get("murl")

                    if not image_url:
                        continue

                    img_response = requests.get(
                        image_url, headers=headers, timeout=10
                    )

                    if img_response.status_code != 200:
                        continue

                    image_bytes = img_response.content

                    # Save locally (temporary on Render)
                    image_path = os.path.join(
                        save_directory, f"{query.replace(' ', '_')}_{count}.jpg"
                    )

                    with open(image_path, "wb") as f:
                        f.write(image_bytes)

                    st.image(image_bytes, caption=f"{query}_{count}", width=400)

                    count += 1
                    time.sleep(1)

                except Exception as e:
                    logging.info(e)
                    continue

            st.success(f"Downloaded {count} images!")

        except Exception as e:
            logging.exception(e)
            st.error("Something went wrong. Try again.")
