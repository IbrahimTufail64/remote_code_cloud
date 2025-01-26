from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)
current_exe = "script.exe"
current_hex = "script.hex"

# --- API Endpoints ---
@app.route("/get-exe/<string:file_name>", methods=["GET"])
def get_exe_file(file_name):
    # Get the file name from the request (either as query param or JSON body)
    if file_name != current_exe:
        return jsonify({"error": f"No current file available"}), 404
    # Check if the file exists
    if not os.path.exists(f"./formdata_exe_files/{file_name}"):
        return jsonify({"error": f"File not available to request."}), 404

    try:
        # Send the file as a response
        return send_file(f"./formdata_exe_files/{file_name}", as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    
@app.route("/get-hex/<string:file_name>", methods=["GET"])
def get_hex_file(file_name):
    # Get the file name from the request (either as query param or JSON body)
    if file_name != current_hex:
        return jsonify({"error": f"No current file available"}), 404
    # Check if the file exists
    if not os.path.exists(f"./formdata_hex_files/{file_name}"):
        return jsonify({"error": f"File not available to request."}), 404

    try:
        # Send the file as a response
        return send_file(f"./formdata_hex_files/{file_name}", as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/pool-for-exe", methods=["GET"]) 
def pool_exe():
    # Get the file name from the request (either as query param or JSON body)

        return jsonify({"file_name": current_exe}), 200
    
@app.route("/pool-for-hex", methods=["GET"]) 
def pool_hex():
    # Get the file name from the request (either as query param or JSON body)

        return jsonify({"file_name": current_hex}), 200
    

#------------Admin Routes-----------#
@app.route("/submit_exe",methods=['POST']) 
def recieve_file():
    file = request.files.get('exe_file')
    print("what the fuck")

    print(file)
    
    if file:
        file.save(f"./formdata_exe_files/{file.filename}");
        file_info = {"filename": file.filename, "content_type": file.content_type}
        current_exe = f"{file.filename}"

        # os.startfile(file_path)
        return jsonify(file_info),200
    return jsonify({"Error": "Can't create file"}),400


@app.route('/submit_hex', methods=['POST'])
def recieve_hex():
    hex_file = request.files.get('hex_file')

    if not hex_file:
        return jsonify({"error": "No hex file provided"}), 400

    try:
        # Save the uploaded hex file to a specific directory
        UPLOAD_FOLDER = os.path.abspath("./formdata_hex_files")
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

        file_path = os.path.join(UPLOAD_FOLDER, hex_file.filename)
        hex_file.save(file_path)
        current_hex = f"{hex_file.filename}"

        return jsonify({"message": "Saved successful"})

    except Exception as e:
        # Handle exceptions
        return jsonify({"error": "An error occurred while submitting", "details": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
