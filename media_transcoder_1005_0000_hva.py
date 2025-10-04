# 代码生成时间: 2025-10-05 00:00:27
import asyncio
import logging
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.views import CompositionView
from sanic_openapi import doc
from sanic_openapi import swagger_blueprint
from sanic_openapi.contrib.tus import tus_blueprint
from sanic_openapi.operations import Operation
import ffmpeg

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Sanic app
app = Sanic("MediaTranscoder")

# Define routes
@app.route("/transcode", methods=["POST"])
@doc.summary("Transcode a media file")
@doc.consumes(doc.JsonBody(request_model="TranscodeRequest"), content_type="application/json")
@doc.produces(doc.JsonBody(response_model="TranscodeResponse"), content_type="application/json")
async def transcode(request: Request):
    # Retrieve the video file from the request
    video_file = request.files.get("video")
    if not video_file:
        return response.json({"error": "No video file provided"}, status=400)
    
    # Extract the file path
    file_path = video_file[0].body
    
    try:
        # Transcode the video file
        output_path = await transcode_video(file_path)
        return response.json({"path": output_path})
    except Exception as e:
        logger.error(f"Transcoding error: {e}")
        return response.json({"error": "Transcoding failed"}, status=500)

# Define the transcode_video function
async def transcode_video(file_path: str) -> str:
    # Use ffmpeg-python to transcode the video file
    output_path = file_path + "_transcoded.mp4"
    try:
        await ffmpeg.input(file_path).output(output_path).run_async()
    except ffmpeg.Error as e:
        logger.error(f"FFmpeg error: {e}")
        raise
    return output_path

# Define models for OpenAPI documentation
@doc.model("TranscodeRequest", description="Request model for transcoding")
class TranscodeRequest:
    video: UploadFile = doc.required("The video file to transcode")

@doc.model("TranscodeResponse", description="Response model for transcoding")
class TranscodeResponse:
    path: str = doc.required("The path to the transcoded video file")

# Add Swagger documentation
swagger_blueprint = swagger_blueprint("MediaTranscoder", "/media_transcoder", "/swagger", "/swagger-ui")
app.blueprint(swagger_blueprint)

# Add Tus support
app.blueprint(tus_blueprint)

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, auto_reload=True)
