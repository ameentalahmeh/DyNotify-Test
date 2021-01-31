# Description
  DyNotify-Test is a Fast API that measures and return the similarity percentage between two given images.

# How to run project
 - Open your terminal.
 - Clone the project repo via `git clone https://github.com/ameentalahmeh/DyNotify-Test.git` command, then `cd DyNotify-Test`.
 - Install all used libraries via `pip install fastapi uvicorn[standard] Pillow scikit-image numpy requests` command.
 -  Run the project using `uvicorn api:app --reload` command.
 - Fast API is running, Enjoy :)
 
# API Request and Response
 - **Standard API Endpoint**: 
   - `http://127.0.0.1:8000/compare-images?apiKey=[Your-APIKey]&firstImgUrl=[First image (URL or Local path)]&secondImgUrl=[Second image (URL or Local path)]`
 - **Example**:
   - Request
   
   ![Request](https://i.imgur.com/PWXIGxF.png)
   
   - Response
   
   ![Request](https://i.imgur.com/cZUmdXH.png)
