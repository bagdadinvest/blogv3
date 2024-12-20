from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import io
import sys
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ShellEndpointView(APIView):
    # Disable authentication for testing
    permission_classes = []  # Remove IsAuthenticated temporarily

    def post(self, request):
        # Extract the code snippet from the request
        code_snippet = request.data.get("code")
        if not code_snippet:
            return Response({"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Capture standard output and errors
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output

        try:
            # Execute the provided code
            exec(code_snippet, globals())
            output = captured_output.getvalue() or "Execution completed successfully."
            logger.info(f"Executed Code: {code_snippet}")
        except Exception as e:
            output = f"Error: {str(e)}"
            logger.error(f"Code Execution Error: {str(e)}")

        # Restore standard output and error streams
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        return Response({"output": output}, status=status.HTTP_200_OK)
