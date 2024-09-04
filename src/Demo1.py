from locust import HttpUser, TaskSet, task, between
import time
import os


class FileUploadTasks(TaskSet):

    @task
    def upload_file(self):
        # Specify the file to upload
        file_path = "C:\\Users\\anon\\Downloads\\customer-aws-output\\input.csv"
        files = {'file': open(file_path, 'rb')}
        file_size = os.path.getsize(file_path)

        # Record the start time
        start_time = time.time()

        # Perform the POST request with multipart/form-data
        with self.client.post("/new-post", files=files, stream=True) as response:
            # Measure the time taken until the request is sent
            upload_end_time = time.time()

        # Calculate the time taken to upload the file
        upload_time = upload_end_time - start_time
        upload_speed = file_size / upload_time if upload_time > 0 else 0

        print("---------------------------------------------------------------")

        # Log the estimated time taken to upload the file
        print(f"Estimated upload time: {upload_time:.2f} seconds, Upload speed: {upload_speed / 1024:.2f} KB/s")

        # Optionally log response time separately
        response_time = time.time() - upload_end_time
        print(f"Response time after upload: {response_time:.2f} seconds")

        # Check the response status
        if response.status_code == 200:
            print("File uploaded successfully")
            end = float(response.headers.get("file-end", 0))
            finish = float(response.headers.get("finish", 0))
            process_time = response.headers.get("Process-Time", "")

            BEGIN = (response.headers.get("BEGIN", ""))
            END = (response.headers.get("ENDED", ""))

            print("---------")
            print(f"BEGIN DT ============ : {BEGIN} ")
            print(f"END DT   ========= : {END} ")
            print("---------")
            print(f"End Sec============ : {end} seconds.")
            print(f"Finish Sec========= : {finish} seconds.")
            print(f"Process Sec========= : {process_time} seconds.")
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")

        print("---------------------------------------------------------------")

class WebsiteUser(HttpUser):
    tasks = [FileUploadTasks]
    wait_time = between(1, 5)  # Simulates waiting time between tasks
