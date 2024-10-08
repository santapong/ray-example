import s3fs
import zipfile
import io


def to_S3URI(Bucket: str, Prefix: str) -> str:
    """
    Generate S3 Path to use save model

    Args:
        Bucket (str): _description_
        Prefix (str): _description_

    Returns:
        str: _description_
    """
    s3_path = ''
    
    return s3_path
    

def update_file_in_zip_on_s3(bucket_name, zip_key, target_file_name, code_to_append):
    # Initialize S3 filesystem
    s3 = s3fs.S3FileSystem(anon=False)

    # Read the .zip file content from S3
    with s3.open(f'{bucket_name}/{zip_key}', 'rb') as s3_file:
        zip_data = s3_file.read()

    # Open the zip file in memory
    updated_zip_buffer = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as existing_zip:
        with zipfile.ZipFile(updated_zip_buffer, 'w', zipfile.ZIP_DEFLATED) as new_zip:
            # Copy all files from the existing zip to the new zip, updating the target file
            for item in existing_zip.infolist():
                file_name = item.filename
                file_data = existing_zip.read(file_name)

                if file_name == target_file_name:
                    # Append the code to the target file's content
                    file_data = file_data.decode('utf-8') + f"\n\n# Added code\n{code_to_append}"
                    file_data = file_data.encode('utf-8')

                # Write the (updated or original) file to the new zip
                new_zip.writestr(file_name, file_data)

    # Seek to the beginning of the buffer
    updated_zip_buffer.seek(0)

    # Upload the updated zip file back to S3
    with s3.open(f'{bucket_name}/{zip_key}', 'wb') as s3_file:
        s3_file.write(updated_zip_buffer.read())

if __name__ == '__main__':

    # Example usage
    bucket_name = 'santapong'
    zip_key = 'test_zip/model_1.zip'
    target_file_name = 'model_1.py'  # The file you want to update inside the zip archive
    code_to_append = 'app = Deploy.bind()'  # The code to add to the file

    # Update the file in the zip archive on S3
    update_file_in_zip_on_s3(bucket_name, zip_key, target_file_name, code_to_append)
    print("File updated and replaced in the zip archive on S3.")
