from infinianalytics import InfiniAnalytics

execution = InfiniAnalytics(
            token="randomtoken1",
            automation_id="44444444-4444-4444-4444-444444444444"
        )


execution.start("Starting the process")

execution.event("An event occurred")

execution.error("An error occurred", error_id="1234", error_detailed="Detailed error message")

execution.end("Ending the process")
