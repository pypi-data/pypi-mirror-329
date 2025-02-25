import zipfile
import io

def save_xml_from_response(response, file_path):
   """
   Extract and save XML file from ZIP response
   Args:
       response: API response object
       file_path: Path to save XML file
   Returns:
       bool: Success status
   """
   try:
       # Process response as memory stream
       with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
           # Find XML filename
           xml_filename = zf.namelist()[0]
           
           # Extract and save XML content
           with zf.open(xml_filename) as xml_file:
               with open(file_path, 'wb') as f:
                   f.write(xml_file.read())
       return True
   except Exception as e:
       print(f"Error saving XML: {e}")
       return False

def get_xml_text_from_response(response):
   """
   Extract XML content directly as text from ZIP response
   Args:
       response: API response object
   Returns:
       str: XML string content
       None: If error occurs
   """
   try:
       # Process response as memory stream
       with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
           # Find XML filename
           xml_filename = zf.namelist()[0]
           
           # Convert XML content directly to string
           with zf.open(xml_filename) as xml_file:
               return xml_file.read().decode('utf-8')
               
   except Exception as e:
       print(f"Error extracting XML text: {e}")
       return None
