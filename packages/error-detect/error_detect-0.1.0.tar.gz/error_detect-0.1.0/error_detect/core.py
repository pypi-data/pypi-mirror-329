import sys
import requests
import traceback

class ErrorDetect:
    def __init__(self, ollama_url=None, model_name=None):
        """
        Initialize the client.
        If ollama_url and model_name are provided, they are used to connect to the LLM API.
        If omitted, LLM integration is disabled.
        """
        if ollama_url is not None:
            if not (ollama_url.startswith("http://") or ollama_url.startswith("https://")):
                raise ValueError("Invalid URL: URL must start with 'http://' or 'https://'.")
            self.ollama_url = ollama_url.rstrip("/")
        else:
            self.ollama_url = None
        self.model_name = model_name

    def error_detect(self):
        """
        Returns error details captured from the current exception context.
        """
        exc_type, exc_obj, exc_tb = sys.exc_info()
        return f"Type: {exc_type.__name__}\nLine: {exc_tb.tb_lineno}\nError: {exc_obj}"

    def _capture_error_line(self):
        """
        Captures the line of code that triggered the exception from the traceback.
        Returns the code line as a string, or an empty string if unavailable.
        """
        exc_type, exc_obj, exc_tb = sys.exc_info()
        tb_list = traceback.extract_tb(exc_tb)
        if tb_list:
            # Get the last frame from the traceback
            last_frame = tb_list[-1]
            return last_frame.line.strip() if last_frame.line else ""
        return ""

    def connect_to_model(self):
        """
        Connects to the Ollama API at '/api/tags' and checks if the configured model is available.
        Returns:
            True if available,
            False if not,
            or an error description if an exception occurs.
        If LLM integration is not configured, returns an informative message.
        """
        if self.ollama_url is None or self.model_name is None:
            return "LLM integration is not configured."
        try:
            url = f"{self.ollama_url}/api/tags"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            models = data.get("models", [])
            for model in models:
                if model.get("name") == self.model_name or model.get("model") == self.model_name:
                    return True
            return False
        except Exception:
            return self.error_detect()

    def get_error_solution(self, error_message=None, error_line=None):
        """
        Uses the Ollama LLM API to generate a corrected line of code for the provided error.
        If no error_message is passed, it automatically uses the output from error_detect().
        If no error_line is provided, it automatically captures the line of code that caused the error.
        
        The prompt instructs the LLM to return only the corrected line of code that fixes the error.
        The final output is formatted as:
        
        Type: <ExceptionType>
        Line: <line number>
        Error: <error message>
        Solution : "<corrected line of code>"
        
        Returns:
            The combined formatted error details and solution,
            or error details if an exception occurs.
            
        API usage reference: See the "Generate a completion" section in the Ollama API readme.
        """
        # Automatically capture error details if none provided.
        if error_message is None:
            error_message = self.error_detect()
        
        # Automatically capture the error line if not provided.
        if error_line is None:
            error_line = self._capture_error_line()
        
        # Construct the prompt.
        prompt = (
            "I encountered the following error:\n"
            f"{error_message}\n"
        )
        if error_line:
            prompt += (
                "\nThe error is caused by this line of code:\n"
                f"{error_line}\n"
            )
        prompt += (
            "\nPlease provide only the corrected line of code that fixes this error."
        )
        
        # If no LLM integration is configured, return the error details.
        if self.ollama_url is None or self.model_name is None:
            return f"{error_message}\nSolution : \"LLM integration not configured.\""
        
        try:
            url = f"{self.ollama_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(url, json=payload)
            data = response.json()
            solution = data.get("response", "No solution provided by the model Or the model is not available.").strip()
            returing_message = f"{error_message}\nError line : \"{error_line}\"\nSolution : \"{solution}\""
            return returing_message
        except Exception:
            return self.error_detect()