import time
from locust import HttpUser, task, between, events
from requests_toolbelt.multipart.encoder import MultipartEncoder


class FileUploadUser(HttpUser):
    wait_time = between(1, 5)  # Simulate user think time

    @task
    def upload_file(self):
        # Prepare the file data for multipart/form-data
        file_path = "C:\\Users\\anon\\Downloads\\customer-aws-output\\input.csv"
        file_data = {
            "file": ("input.csv", open(file_path, "rb"), "text/csv")
        }
        multipart_data = MultipartEncoder(fields=file_data)

        # Start timing the upload
        upload_start_time = time.time()

        # Perform the POST request to upload the file
        response = self.client.post("/new-post", data=multipart_data,
                                    headers={"Content-Type": multipart_data.content_type})

        # Time taken to upload the file
        upload_end_time = time.time()
        upload_time = upload_end_time - upload_start_time
        print(f"Time taken to upload the file: {upload_time:.2f} seconds")

        # Total time from the start of the request until receiving the response
        total_time = upload_end_time - upload_start_time

        # Time taken to receive the response
        response_time = time.time() - upload_start_time

        # Estimated server processing time (total time minus upload time)
        server_processing_time = response_time - upload_time
        print(f"Estimated server processing time: {server_processing_time:.2f} seconds")
        print(f"Total time for the request: {response_time:.2f} seconds")

        # Handle the response (optional)
        if response.status_code == 200:
            print("File uploaded successfully.")
            response.headers.get("Process-Time" , 0);
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
