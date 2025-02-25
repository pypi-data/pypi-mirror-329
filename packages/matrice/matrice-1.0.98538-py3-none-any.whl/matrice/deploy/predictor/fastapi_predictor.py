import requests
import uvicorn
from fastapi import Body, FastAPI, File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import logging
import threading


class MatriceFastAPIPredictor:
    def __init__(self, load_model, predict, actionTracker):
        """Initialize the predictor with model loading and prediction functions"""
        try:
            logging.info("Initializing MatriceFastAPIPredictor")
            self.actionTracker = actionTracker
            logging.info("Loading model...")
            self.model = load_model(actionTracker)
            logging.info("Model loaded successfully")
            self.predict = lambda model, image: predict(model, image)
            self.app = FastAPI()
            logging.info("Registering FastAPI endpoints")
            self._register_endpoints()
            logging.info("FastAPI endpoints registered successfully")
        except Exception as e:
            logging.error(f"Failed to initialize predictor: {str(e)}", exc_info=True)
            raise

    def _register_endpoints(self):
        """Register the FastAPI endpoints"""
        @self.app.post("/inference/")
        async def serve_inference(image: UploadFile = File(...)):
            logging.info(f"Received inference request for file: {image.filename}")
            try:
                image_data = await image.read()
                results, ok = self.inference(image_data)

                if ok:
                    logging.info("Inference completed successfully")
                    return JSONResponse(content=jsonable_encoder({
                        "status": 1,
                        "message": "Request success",
                        "result": results
                    }))
                else:
                    logging.error("Inference failed")
                    raise HTTPException(status_code=500, detail="Inference failed")
            except Exception as e:
                logging.error(f"Error in inference endpoint: {str(e)}", exc_info=True)
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/inference_from_url/")
        async def serve_inference_from_url(imageUrl: str = Body(embed=True)):
            logging.info(f"Received inference request for URL: {imageUrl}")
            if not imageUrl:
                logging.error("No imageUrl provided")
                raise HTTPException(status_code=400, detail="Please provide imageUrl")

            try:
                logging.info(f"Fetching image from URL: {imageUrl}")
                response = requests.get(imageUrl, timeout=10)
                response.raise_for_status()
                image_data = response.content
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to fetch image from URL: {str(e)}", exc_info=True)
                raise HTTPException(status_code=400, detail=f"Failed to fetch image: {str(e)}")

            results, ok = self.inference(image_data)

            if ok:
                logging.info("Inference from URL completed successfully")
                return JSONResponse(content=jsonable_encoder({
                    "status": 1,
                    "message": "Request success", 
                    "result": results
                }))
            else:
                logging.error("Inference from URL failed")
                raise HTTPException(status_code=500, detail="Inference failed")
            
    def inference(self, image):
        """Run inference on the provided image data"""
        try:
            logging.info("Starting inference")
            results = self.predict(self.model, image)
            logging.info("Inference completed successfully")
            return results, True
        except Exception as e:
            logging.error(f"Inference error: {str(e)}", exc_info=True)
            return None, False

    def setup(self, instance_port):
        """Start the FastAPI server"""
        try:
            logging.info(f"Starting FastAPI server on port {instance_port}")
            server = uvicorn.Server(uvicorn.Config(
                app=self.app,
                host="0.0.0.0",
                port=80, # it must be 80 as it is the port mapped the the external instance port
                log_level="info"
            ))
            thread = threading.Thread(target=server.run, daemon=True)
            thread.start()
            logging.info(f"FastAPI server started successfully on port {instance_port}")
            return server
        except Exception as e:
            logging.error(f"Failed to start server: {str(e)}", exc_info=True)
            raise
